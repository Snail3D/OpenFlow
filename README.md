<p align="center">
  <img src="https://img.shields.io/badge/Platform-Linux-blue?style=for-the-badge&logo=linux" alt="Linux">
  <img src="https://img.shields.io/badge/Python-3.x-green?style=for-the-badge&logo=python" alt="Python 3">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">🎙️ OpenFlow</h1>

<p align="center">
  <strong>Push-to-talk speech recognition for Linux</strong><br>
  Hold a key, speak, release — your words appear like magic ✨
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage">Usage</a> •
  <a href="#%EF%B8%8F-configuration">Configuration</a> •
  <a href="#-support">Support</a>
</p>

---

## 🚀 Features

- **🔒 Offline** — Uses Vosk for completely local speech recognition
- **⚡ Fast** — No cloud latency, instant transcription
- **🎮 Gaming KB Support** — Works with multi-device gaming keyboards
- **🖥️ Wayland Native** — Types text via wtype
- **🔄 Toggle On/Off** — Desktop launcher with system notifications

## 📦 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Snail3D/OpenFlow.git
cd OpenFlow
```

### 2. Set up Python environment
```bash
python3 -m venv --without-pip ~/speech-to-text-venv
curl -sS https://bootstrap.pypa.io/get-pip.py | ~/speech-to-text-venv/bin/python3
~/speech-to-text-venv/bin/pip install vosk pyaudio
```

### 3. Download Vosk model
```bash
mkdir -p model
cd model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15/* .
rm -rf vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15.zip
cd ..
```

### 4. Install desktop launcher
```bash
cp OpenFlow.desktop ~/Desktop/
chmod +x ~/Desktop/OpenFlow.desktop
```

## 🎯 Usage

### Desktop Launcher
Double-click the **OpenFlow** icon on your desktop to toggle on/off.

### Command Line
```bash
# Toggle on/off
./openflow-toggle.sh

# Run directly (foreground)
sudo ./start-stt.sh
```

### How to Dictate
1. **Start** OpenFlow (click desktop icon or run toggle script)
2. **Hold** Right Ctrl
3. **Speak** your text
4. **Release** Right Ctrl
5. ✨ Text appears at your cursor

## ⚙️ Configuration

Edit `stt.py` to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `HOTKEY_CODE` | `97` (Right Ctrl) | Key code to trigger recording |
| `DEVICE_NAME` | `"Blue Snowball"` | Microphone name to use |
| `SAMPLE_RATE` | `16000` | Audio sample rate |
| `RELEASE_TIMEOUT` | `0.15` | Seconds to wait before auto-release |

### Common Key Codes
| Key | Code |
|-----|------|
| Right Ctrl | 97 |
| Left Ctrl | 29 |
| Right Alt | 100 |
| Right Shift | 54 |
| Caps Lock | 58 |

## 🔧 Requirements

- **OS:** Linux with Wayland
- **Python:** 3.x
- **Audio:** Working microphone
- **Packages:** `wtype` (for typing output)

```bash
# Debian/Ubuntu
sudo apt install wtype

# Arch
sudo pacman -S wtype
```

## 🐛 Troubleshooting

<details>
<summary><strong>No keyboard detected</strong></summary>

Check your keyboard device:
```bash
cat /proc/bus/input/devices | grep -A 4 -i keyboard
```
Update the device path in `find_keyboard_devices()` in `stt.py`.
</details>

<details>
<summary><strong>Permission denied</strong></summary>

Run with sudo:
```bash
sudo ./start-stt.sh
```
</details>

<details>
<summary><strong>Key release not detected</strong></summary>

Gaming keyboards often split events across devices. OpenFlow uses timeout-based detection as a fallback — if key repeats stop for 150ms, it assumes you released.
</details>

---

## 📄 License

MIT License — do whatever you want with it!

---

<p align="center">
  <strong>If you find this useful, consider buying me a coffee! ☕</strong>
</p>

<p align="center">
  <a href="https://buymeacoffee.com/snail3d">
    <img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Buy Me A Coffee">
  </a>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/Snail3D">Snail3D</a>
</p>
