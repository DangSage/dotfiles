# Framework 13 Arch Linux Configuration

My Arch Linux rice configured for the Framework 13 laptop (12th Gen Intel i7-1260P). Based on [kj_sh604's awesomeWM rice](https://github.com/kj-sh604/dotfiles) with extensive modifications for Qtile and Framework 13 optimizations.

## Hardware
- **Laptop**: Framework 13
- **CPU**: 12th Gen Intel Core i7-1260P (12 cores)
- **GPU**: Intel Iris Xe Graphics (Alder Lake-P GT2)
- **Kernel**: Linux 6.17.7-arch1-1

## Core Components

### Window Manager & Desktop
- **Qtile** - Tiling window manager with custom Python configuration
- **Rofi** - Application launcher, power menu, and keybind viewer
- **Picom** - Compositor with transparency effects
- **Dunst** - Notification daemon
- **Conky** - System monitor overlay
- **Ly** - TUI display manager

### Terminal & Shell
- **Wezterm** - Primary terminal emulator
- **Bash** - Shell with custom configuration
- **FZF** - Fuzzy finder with `fd` backend and image preview
  - Custom color scheme matching Qtile theme
  - Image preview using `chafa` with sixel support
  - Code preview using `bat`
  - Custom `img()` function for browsing images

### Editor
- **Neovim** - Primary text editor
  - LSP support with CoC
  - Telescope fuzzy finder
  - Git integration (Neogit, Fugitive, GitSigns)
  - Tree-sitter syntax highlighting
  - File explorer with nvim-tree

### File Management
- **Thunar** - GUI file manager
- **Ranger** - TUI file manager with image preview
- **Udiskie** - Automounting with tray icon

### Audio & Media
- **Pipewire** - Modern audio server (replaces PulseAudio)
  - ALSA, JACK, and PulseAudio compatibility layers
- **MPD** + **mpdris2** - Music player daemon with MPRIS2 support
- **Spotify Player** - TUI Spotify client
- **Pasystray** - Volume control tray applet
- **Playerctl** - Media player controller

### System Utilities
- **Brightnessctl** - Screen brightness control (integrated in Qtile)
- **Powertop** - Power management and monitoring
- **Btop** / **Bottom** - System resource monitors
- **Fastfetch** - System information display
- **NetworkManager** - Network management with nm-applet
- **Blueman** - Bluetooth management

## Configuration Highlights

### Shell Aliases (`~/.bashrc:10-11`)
```bash
alias vim='nvim'
alias vi='nvim'
```

### FZF Integration (`~/.bashrc:14-63`)
- Configured with custom color scheme matching Qtile
- Uses `fd` for fast file searching
- Image preview with `chafa` (sixel output)
- Code syntax highlighting with `bat`
- Directory tree preview
- Custom `img()` function for image browsing with xdg-open integration

### MIME Type Associations (`~/.config/mimeapps.list`)
- **Text files** → Neovim
- **Directories** → Wezterm (terminal file browser)
- **Archives** → Xarchiver
- **Web content** → Thorium Browser
- **Empty files** → Neovim

### Qtile Configuration

**Custom Scripts** (`.config/qtile/`):
- `rofi_app_launcher.sh` - Application launcher
- `rofi_power_menu.sh` - Power/session menu
- `rofi_keybinds.sh` - Interactive keybinding reference
- `generate_colors.py` - Dynamic color scheme generation
- `generate_keybinds_list.py` - Keybinding documentation
- `screenshot.sh` - Screenshot utility

**Autostart** (`~/.config/qtile/autostart.sh:1-22`):
- Sets default audio volume to 60%
- Configures touchpad click method
- Starts system tray applications (Blueman, Pasystray, nm-applet)
- Launches background services (Conky, MPD, Dunst, Picom)
- Opens Wezterm terminal on startup

**Statusbar Scripts** (`~/.local/bin/statusbar/`):
- `sb-battery` - Battery status (Framework 13 specific)
- `sb-clock` - Date/time display
- `sb-cpu` - CPU usage monitor
- `sb-memory` - RAM usage
- `sb-disk` - Disk usage
- `sb-network` - Network status

## Installation

### Required System Services
```bash
sudo systemctl enable bluetooth
sudo systemctl enable NetworkManager
sudo systemctl enable udiskie
```

### Key Dependencies
- `fzf` - Fuzzy finder
- `fd` - Fast file finder (used by FZF)
- `bat` - Syntax-highlighted file viewer
- `chafa` - Terminal image viewer with sixel support
- `rofi` - Application launcher
- `brightnessctl` - Brightness control
- `pipewire` - Audio server

## Branch Structure
- **framework13** - Current branch (Framework 13 specific config)
- **main** - Base configuration
- Other branches for different hardware setups

## Framework 13 Optimizations
- Intel-specific drivers and microcode
- Battery monitoring in statusbar
- Brightness control integrated in Qtile keybindings
- Power management with powertop
- Touchpad configuration in autostart

Happy ricing!
