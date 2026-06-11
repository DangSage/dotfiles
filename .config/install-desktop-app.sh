#!/bin/bash
# Helper script to install desktop apps to ~/.local/apps/
# Usage: ./install-desktop-app.sh <package>

APPS_DIR="/home/khai/.local/apps"
CONFIG_FILE="/home/khai/.local/apps/etc/pacman-desktop.conf"

if [ -z "$1" ]; then
    echo "Usage: $0 <package>"
    echo "Example: $0 flameshot"
    exit 1
fi

echo "Installing $1 to ~/.local/apps/..."
sudo pacman --config "$CONFIG_FILE" -S "$1"
