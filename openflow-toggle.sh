#!/bin/bash
# Toggle OpenFlow speech-to-text on/off

SCRIPT_DIR="/home/snailpi/speech-to-text"
VENV="/home/snailpi/speech-to-text-venv/bin/python3"

# Check if already running
if pgrep -f "stt.py" > /dev/null; then
    # Running - stop it
    sudo pkill -f "stt.py"
    notify-send "OpenFlow" "Speech-to-text stopped" -i microphone-sensitivity-muted 2>/dev/null
    echo "Stopped"
else
    # Not running - start it
    cd "$SCRIPT_DIR"
    sudo -E SUDO_USER=$USER SUDO_UID=$(id -u) "$VENV" stt.py &>/dev/null &
    disown
    sleep 1
    if pgrep -f "stt.py" > /dev/null; then
        notify-send "OpenFlow" "Speech-to-text started\nHold Right Ctrl to speak" -i microphone-sensitivity-high 2>/dev/null
        echo "Started"
    else
        notify-send "OpenFlow" "Failed to start" -i dialog-error 2>/dev/null
        echo "Failed"
    fi
fi
