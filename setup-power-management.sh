#!/bin/bash
# Framework 13 Power Management Setup Script
# Run this script with: bash setup-power-management.sh

set -e

echo "========================================="
echo "Framework 13 Power Optimization Setup"
echo "========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as your normal user (it will ask for sudo when needed)"
    exit 1
fi

# Step 1: Install required packages
echo "[1/8] Installing power management packages..."
sudo pacman -S --needed tlp tlp-rdw thermald intel-ucode brightnessctl --noconfirm

# Step 2: Stop and mask conflicting services
echo "[2/8] Masking conflicting services..."
sudo systemctl stop power-profiles-daemon 2>/dev/null || true
sudo systemctl mask power-profiles-daemon 2>/dev/null || true
sudo systemctl mask systemd-rfkill.service
sudo systemctl mask systemd-rfkill.socket

# Step 3: Enable TLP
echo "[3/8] Enabling TLP service..."
sudo systemctl enable tlp.service
sudo systemctl start tlp.service

# Step 4: Enable thermald
echo "[4/8] Enabling thermald service..."
sudo systemctl enable thermald.service
sudo systemctl start thermald.service

# Step 5: Create udev rules for power management
echo "[5/8] Creating udev rules..."

# USB power management
sudo tee /etc/udev/rules.d/50-usb-power-save.rules > /dev/null <<'EOF'
# Enable USB autosuspend for power saving
ACTION=="add", SUBSYSTEM=="usb", TEST=="power/control", ATTR{power/control}="auto"
EOF

# PCI power management
sudo tee /etc/udev/rules.d/50-pci-power-save.rules > /dev/null <<'EOF'
# Enable PCI runtime PM
ACTION=="add", SUBSYSTEM=="pci", ATTR{power/control}="auto"
EOF

# SATA power management
sudo tee /etc/udev/rules.d/50-sata-power-save.rules > /dev/null <<'EOF'
# Enable SATA link power management
ACTION=="add", SUBSYSTEM=="scsi_host", KERNEL=="host*", ATTR{link_power_management_policy}="med_power_with_dipm"
EOF

# Step 6: Configure systemd sleep
echo "[6/8] Configuring systemd sleep settings..."
sudo tee /etc/systemd/sleep.conf > /dev/null <<'EOF'
[Sleep]
AllowSuspend=yes
AllowHibernation=yes
AllowSuspendThenHibernate=yes
AllowHybridSleep=yes
SuspendMode=suspend
SuspendState=mem
HibernateDelaySec=3600
EOF

# Step 7: Create PowerTOP systemd service for auto-tuning at boot
echo "[7/8] Setting up PowerTOP auto-tuning service..."
sudo tee /etc/systemd/system/powertop-autotune.service > /dev/null <<'EOF'
[Unit]
Description=PowerTOP auto tune
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/bin/powertop --auto-tune
RemainAfterExit=true

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable powertop-autotune.service

# Step 8: Update kernel parameters for systemd-boot
echo "[8/8] Updating kernel parameters..."

# Backup current boot entry
sudo cp /boot/loader/entries/2024-08-12_15-48-53_linux.conf /boot/loader/entries/2024-08-12_15-48-53_linux.conf.backup

# Read current options
CURRENT_OPTIONS=$(grep "^options" /boot/loader/entries/2024-08-12_15-48-53_linux.conf | sed 's/^options //')

# Add new parameters if they don't exist
NEW_PARAMS="intel_pstate=active nvme.noacpi=1 mem_sleep_default=deep"

for param in $NEW_PARAMS; do
    if ! echo "$CURRENT_OPTIONS" | grep -q "$param"; then
        CURRENT_OPTIONS="$CURRENT_OPTIONS $param"
    fi
done

# Update the boot entry
sudo tee /boot/loader/entries/2024-08-12_15-48-53_linux.conf > /dev/null <<EOF
# Created by: archinstall
# Created on: 2024-08-12_15-48-53
# Modified for power optimization: $(date +%Y-%m-%d)
title   Arch Linux (linux)
linux   /vmlinuz-linux
initrd  /initramfs-linux.img
options $CURRENT_OPTIONS
EOF

# Reload udev rules
echo ""
echo "Reloading udev rules..."
sudo udevadm control --reload-rules
sudo udevadm trigger

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Services enabled:"
echo "  - TLP (power management)"
echo "  - thermald (thermal management)"
echo "  - powertop-autotune (runtime tuning)"
echo ""
echo "Configuration created:"
echo "  - /etc/udev/rules.d/50-usb-power-save.rules"
echo "  - /etc/udev/rules.d/50-pci-power-save.rules"
echo "  - /etc/udev/rules.d/50-sata-power-save.rules"
echo "  - /etc/systemd/sleep.conf"
echo "  - Kernel parameters updated in systemd-boot"
echo ""
echo "IMPORTANT: Reboot your system for all changes to take effect!"
echo ""
echo "After reboot, you can check status with:"
echo "  sudo tlp-stat -s    # TLP status"
echo "  sudo powertop       # Power consumption analysis"
echo ""
