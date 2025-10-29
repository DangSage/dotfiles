#!/bin/bash
# Install all essential packages from essential-packages.txt

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_FILE="$SCRIPT_DIR/essential-packages.txt"

if [ ! -f "$PACKAGE_FILE" ]; then
    echo "Error: essential-packages.txt not found!"
    exit 1
fi

echo "=========================================="
echo "Installing Essential Packages"
echo "for Qtile Desktop Environment"
echo "=========================================="
echo ""

# Read packages from file, skip comments and empty lines
PACKAGES=$(grep -v '^#' "$PACKAGE_FILE" | grep -v '^$' | tr '\n' ' ')

if [ -z "$PACKAGES" ]; then
    echo "Error: No packages found in $PACKAGE_FILE"
    exit 1
fi

echo "Packages to install:"
echo "$PACKAGES" | tr ' ' '\n' | sed 's/^/  - /'
echo ""

read -p "Continue with installation? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

echo ""
echo "Updating package database..."
sudo pacman -Sy

echo ""
echo "Installing packages..."
sudo pacman -S --needed $PACKAGES

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "Post-installation steps:"
echo ""
echo "1. Enable and start services:"
echo "   sudo systemctl enable NetworkManager bluetooth tlp"
echo "   sudo systemctl start NetworkManager bluetooth"
echo ""
echo "2. Install vim-plug for Neovim:"
echo "   sh -c 'curl -fLo \"\${XDG_DATA_HOME:-\$HOME/.local/share}\"/nvim/site/autoload/plug.vim --create-dirs \\"
echo "          https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'"
echo ""
echo "3. Clone your dotfiles and copy configs to ~/.config/"
echo ""
echo "4. Open Neovim and run: :PlugInstall"
echo ""
echo "5. Install CoC language servers in Neovim:"
echo "   :CocInstall coc-json coc-tsserver coc-pyright"
echo ""
echo "6. Reboot or restart X11"
echo ""
