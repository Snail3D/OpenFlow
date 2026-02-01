#!/home/snailpi/speech-to-text-venv/bin/python3
"""
Speech-to-Text with hotkey trigger.
Hold Right Ctrl to record, release to transcribe and type.
"""

import subprocess
import sys
import os
import json
import struct
import select
import threading
import time

import pyaudio
from vosk import Model, KaldiRecognizer

# Configuration
HOTKEY_CODE = 97  # KEY_RIGHTCTRL
MODEL_PATH = "/home/snailpi/speech-to-text/model"
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 1024
DEVICE_NAME = "Blue Snowball"

# Input event format: time_sec, time_usec, type, code, value
EVENT_FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)


def find_keyboard_devices():
    """Find all Gaming KB keyboard device paths."""
    # Gaming KB uses multiple event devices - need to listen to all of them
    devices = []
    import glob
    for path in sorted(glob.glob('/dev/input/event*')):
        try:
            event_name = os.path.basename(path)
            name_path = f'/sys/class/input/{event_name}/device/name'
            if os.path.exists(name_path):
                with open(name_path) as f:
                    name = f.read().strip().lower()
                if 'gaming kb' in name:
                    devices.append(path)
        except (PermissionError, IOError):
            continue
    return devices if devices else ['/dev/input/event4']


def find_audio_device(p):
    """Find the Blue Snowball microphone."""
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if DEVICE_NAME.lower() in info['name'].lower() and info['maxInputChannels'] > 0:
            return i
    return None


def type_text(text):
    """Type text using wtype (Wayland)."""
    if not text.strip():
        return
    try:
        user = os.environ.get('SUDO_USER', 'snailpi')
        uid = os.environ.get('SUDO_UID', '1000')
        env = os.environ.copy()
        env['XDG_RUNTIME_DIR'] = f'/run/user/{uid}'
        # Find wayland display
        import glob
        wayland_sockets = glob.glob(f'/run/user/{uid}/wayland-*')
        if wayland_sockets:
            env['WAYLAND_DISPLAY'] = os.path.basename(wayland_sockets[0])
        subprocess.run(['sudo', '-u', user, '-E', 'wtype', '--', text],
                      check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error typing text: {e}", file=sys.stderr)
    except FileNotFoundError:
        print("wtype not found", file=sys.stderr)


def main():
    print("Loading speech recognition model...")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    print("Finding keyboard devices...")
    kbd_paths = find_keyboard_devices()
    if not kbd_paths:
        print("No keyboard found!", file=sys.stderr)
        sys.exit(1)
    print(f"Using keyboards: {kbd_paths}")

    print("Setting up audio...")
    p = pyaudio.PyAudio()
    device_index = find_audio_device(p)
    if device_index is not None:
        print(f"Using audio device: {p.get_device_info_by_index(device_index)['name']}")
    else:
        print("Using default audio device")

    print(f"\nReady! Hold Right Ctrl to speak, release to transcribe.\n")

    recording = False
    audio_data = []
    stream = None
    record_thread = None
    kbd_files = []
    last_hotkey_time = 0
    RELEASE_TIMEOUT = 0.15  # If no key event for 150ms, assume released

    try:
        # Open all keyboard devices
        kbd_files = [open(path, 'rb') for path in kbd_paths]

        def stop_recording():
            nonlocal recording, stream, record_thread, recognizer
            recording = False
            print("Processing...")

            if record_thread:
                record_thread.join(timeout=1)

            if stream:
                stream.stop_stream()
                stream.close()
                stream = None

            if audio_data:
                full_audio = b''.join(audio_data)
                recognizer.AcceptWaveform(full_audio)
                result = json.loads(recognizer.FinalResult())
                text = result.get('text', '')

                if text:
                    print(f"Recognized: {text}")
                    type_text(text)
                else:
                    print("(no speech detected)")
            else:
                print("(no audio recorded)")

            recognizer = KaldiRecognizer(model, SAMPLE_RATE)
            print("\nReady!")

        while True:
            # Wait for keyboard event from any device
            r, _, _ = select.select(kbd_files, [], [], 0.05)

            # Check for timeout-based release detection
            if recording and last_hotkey_time > 0 and (time.time() - last_hotkey_time) > RELEASE_TIMEOUT:
                stop_recording()
                last_hotkey_time = 0
                continue

            if not r:
                continue

            for kbd in r:
                event_data = kbd.read(EVENT_SIZE)
                if len(event_data) < EVENT_SIZE:
                    continue

                _, _, ev_type, ev_code, ev_value = struct.unpack(EVENT_FORMAT, event_data)

                # EV_KEY = 1
                if ev_type == 1 and ev_code == HOTKEY_CODE:
                    last_hotkey_time = time.time()

                    if ev_value == 1 and not recording:  # Key pressed
                        recording = True
                        audio_data = []
                        print("Recording... (release Right Ctrl to stop)")

                        stream = p.open(
                            format=pyaudio.paInt16,
                            channels=CHANNELS,
                            rate=SAMPLE_RATE,
                            input=True,
                            input_device_index=device_index,
                            frames_per_buffer=CHUNK
                        )

                        def record():
                            while recording and stream and stream.is_active():
                                try:
                                    data = stream.read(CHUNK, exception_on_overflow=False)
                                    audio_data.append(data)
                                except:
                                    break

                        record_thread = threading.Thread(target=record, daemon=True)
                        record_thread.start()

                    elif ev_value == 0 and recording:  # Key released
                        stop_recording()
                        last_hotkey_time = 0

    except KeyboardInterrupt:
        print("\nExiting...")
    except PermissionError:
        print(f"Permission denied reading keyboard. Try: sudo {sys.argv[0]}", file=sys.stderr)
        sys.exit(1)
    finally:
        for f in kbd_files:
            f.close()
        if stream:
            stream.close()
        p.terminate()


if __name__ == "__main__":
    main()
