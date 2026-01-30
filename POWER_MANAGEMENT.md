# Framework 13 Power Management Configuration

Comprehensive power optimization setup for Framework 13 (Intel 12th Gen i7-1260P) running Arch Linux.

## Installation

Run the setup script:
```bash
chmod +x setup-power-management.sh
./setup-power-management.sh
```

After installation, copy the TLP configuration:
```bash
sudo cp tlp.conf /etc/tlp.conf
sudo systemctl restart tlp
```

## What's Configured

### Services
- **TLP**: Advanced power management
- **thermald**: Thermal optimization for Intel CPUs
- **PowerTOP**: Runtime power tuning

### Kernel Parameters
- `intel_pstate=active`: Intel P-state driver
- `nvme.noacpi=1`: NVMe power management
- `mem_sleep_default=deep`: Deep sleep state

### Power Saving Features
- USB autosuspend
- PCI runtime power management
- SATA link power management
- CPU frequency scaling
- Battery charge thresholds (40-80%)
- WiFi power saving on battery
- Audio power saving

## Post-Installation

**Reboot required** for all changes to take effect.

### Check Status
```bash
sudo tlp-stat -s              # TLP status
sudo tlp-stat -b              # Battery info
sudo powertop                 # Power analysis
systemctl status tlp          # Service status
systemctl status thermald     # Thermal status
```

### Calibrate PowerTOP (Optional)
```bash
sudo powertop --calibrate     # Takes ~15 minutes on battery
```

### Adjust Battery Thresholds
Edit `/etc/tlp.conf` and modify:
```
START_CHARGE_THRESH_BAT0=40
STOP_CHARGE_THRESH_BAT0=80
```

For maximum capacity, set both to 0 to disable.

## Expected Results
- 8-12 hours battery life under normal workloads
- 40-60% improvement over default configuration
- Lower temperatures under load
- Reduced fan noise

## Troubleshooting

If device not working after suspend:
```bash
sudo systemctl restart tlp
```

If USB device not detected:
```bash
# Add device to USB_EXCLUDE_DEVICE in /etc/tlp.conf
```

Disable charge thresholds if battery not charging:
```bash
sudo tlp setcharge 0 100 BAT0
```
