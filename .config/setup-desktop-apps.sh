#!/bin/bash
# Desktop Apps Setup Script
# Run this to initialize ~/.local/apps/ for desktop applications

set -e

APPS_DIR="/home/khai/.local/apps"
CONFIG_FILE="$APPS_DIR/etc/pacman-desktop.conf"

echo "=== Desktop Apps Setup ==="
echo ""

# Create directories
echo "[1/3] Creating directory structure..."
mkdir -p "$APPS_DIR"/{etc,var/lib/pacman,var/log}
mkdir -p "$APPS_DIR"/usr/{bin,lib}

# Check if we need to undo any previous bind mount attempts
if mountpoint -q "$APPS_DIR/usr" 2>/dev/null; then
    echo "[2/3] Unmounting previous bind mount (if any)..."
    sudo umount "$APPS_DIR/usr" 2>/dev/null || true
fi

# Remove any fstab entry from previous attempts
if grep -q "$APPS_DIR/usr" /etc/fstab 2>/dev/null; then
    echo "[2/3] Removing old fstab entry..."
    sudo sed -i "\|$APPS_DIR/usr|d" /etc/fstab
fi

# Initialize pacman database
echo "[2/3] Initializing pacman database..."
sudo pacman --config "$CONFIG_FILE" -Sy --needed

echo "[3/3] Setup complete!"
echo ""
echo "To install desktop apps to ~/.local/apps/, use:"
echo "  sudo pacman --config $CONFIG_FILE -S <package> --nodeps"
echo ""
echo "Example: sudo pacman --config $CONFIG_FILE -S flameshot --nodeps"
echo ""
echo "The --nodeps flag is important - it prevents reinstalling system libraries"
echo ""
echo "Next steps:"
echo "  1. Migrate desktop apps: ~/.config/migrate-desktop-apps.sh"
echo "  2. Add to PATH: export PATH=\"\$HOME/.local/apps/usr/bin:\$PATH\""
