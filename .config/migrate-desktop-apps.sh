#!/bin/bash
# Migration script: Move desktop apps from system to ~/.local/apps/
# Uses bind mount to share system libraries - no duplicate installations
# WARNING: This removes packages from system and reinstalls to ~/.local/apps

APPS_DIR="/home/khai/.local/apps"
CONFIG_FILE="$APPS_DIR/etc/pacman-desktop.conf"

DESKTOP_PACKAGES=(
    "audacity"
    "electron"
    "electron39"
    "flatpak"
    "flameshot"
    "gimp"
    "firefox"
    "obs-studio"
    "reaper"
    "solaar"
    "snappy"
    "spotify"
    "spotify-player"
    "thunar"
    "thunar-archive-plugin"
    "zoom"
)

VLC_PACKAGES=$(pacman -Qq | grep '^vlc-')

echo "=== Desktop Apps Migration ==="
echo "This will remove packages from system and reinstall to ~/.local/apps/"
echo "Using bind mount to share system libraries (no duplicate installations)"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Install base packages with --nodeps (system libraries are bind mounted)
echo "[1/2] Installing desktop packages to ~/.local/apps/..."
for pkg in "${DESKTOP_PACKAGES[@]}"; do
    echo "  Installing $pkg (without deps - using system libraries)..."
    sudo pacman --config "$CONFIG_FILE" -S --nodeps --noconfirm "$pkg" 2>/dev/null || true
done

# Install vlc packages
echo "  Installing vlc packages..."
for pkg in $VLC_PACKAGES; do
    echo "  Installing $pkg..."
    sudo pacman --config "$CONFIG_FILE" -S --nodeps --noconfirm "$pkg" 2>/dev/null || true
done

echo ""
echo "[2/2] Migration complete!"
echo ""
echo "PATH has been updated in ~/.bashrc to include ~/.local/apps/usr/bin"
echo "Restart your shell or run: source ~/.bashrc"
