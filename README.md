# OpenFlow - Speech-to-Text

Push-to-talk speech recognition for Linux. Hold Right Ctrl to record, release to transcribe and type.

## Features

- Offline speech recognition using Vosk
- Hotkey-triggered recording (Right Ctrl)
- Auto-types transcribed text via wtype (Wayland)
- Works with Gaming KB and similar multi-device keyboards

## Requirements

- Python 3
- Vosk model
- Blue Snowball microphone (or modify `DEVICE_NAME` in stt.py)
- wtype (for Wayland text input)
- sudo access (for reading keyboard input device)

## Setup

```bash
# Create virtual environment
python3 -m venv --without-pip ~/speech-to-text-venv
curl -sS https://bootstrap.pypa.io/get-pip.py | ~/speech-to-text-venv/bin/python3

# Install dependencies
~/speech-to-text-venv/bin/pip install vosk pyaudio

# Download Vosk model
mkdir -p model
# Download from https://alphacephei.com/vosk/models and extract to model/
```

## Usage

```bash
sudo ./start-stt.sh
```

Hold Right Ctrl, speak, release to transcribe.
