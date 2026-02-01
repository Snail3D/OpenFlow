#!/bin/bash
# Start speech-to-text with hotkey trigger
# Run with: sudo ./start-stt.sh
cd /home/snailpi/speech-to-text
SUDO_USER=snailpi SUDO_UID=1000 /home/snailpi/speech-to-text-venv/bin/python3 stt.py
