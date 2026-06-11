# Desktop App Separation Plan

## Background

Desktop applications are being separated from system libraries to reduce root partition usage. Desktop apps are installed to `~/.local/apps/` while system libraries and dev tools remain in pacman/pikaur on root.

This allows for:
- Reduced root partition usage (~8-10GB saved)
- Per-user package management for desktop apps
- Clean separation between system and desktop applications

## Directory Structure

```
~/.local/apps/
├── etc/
│   └── pacman-desktop.conf    # Pacman config for desktop apps
├── var/lib/pacman/            # Package database
└── usr/                       # Bind mounted from system /usr
    ├── bin/                   # Desktop app binaries (installed here)
    └── lib/                   # System libraries (shared via bind mount)
```

## Implementation Steps

1. **Create directory structure**
   ```bash
   mkdir -p ~/.local/apps/{etc,var/lib/pacman,usr/bin,usr/lib,var/log}
   ```

2. **Bind mount system /usr** (critical for sharing libraries)
   ```bash
   sudo mount --bind /usr ~/.local/apps/usr
   # Add to /etc/fstab for persistence:
   echo "/usr ~/.local/apps/usr none defaults,bind 0 0" | sudo tee -a /etc/fstab
   ```

3. **Create pacman config** - Copy `/etc/pacman.conf` and modify:
   ```conf
   RootDir       = /home/khai/.local/apps/
   DBPath        = /home/khai/.local/apps/var/lib/pacman/
   CacheDir      = /var/cache/pacman/pkg/
   HookDir       = /usr/share/libalpm/hooks/
   LogFile       = /var/log/pacman.log
   ```

3. **Configure pikaur** - Create `~/.config/pikaur-desktop.conf`:
   ```ini
   [pikaur]
   database = /home/khai/.local/apps/var/lib/pacman/
   root = /home/khai/.local/apps/
   ```

4. **Migrate packages**:
   - Remove from system: `sudo pacman -Rns <package>`
   - Install to ~/.local: `pacman --config ... -S <package>`

5. **Update shell PATH** in ~/.bashrc, ~/.zshrc, etc.

6. **Update .desktop files** to point to new locations

## System Packages (Keep on Root)

These remain in system pacman/pikaur:

- **Core**: base, base-devel, linux, linux-firmware
- **Compilers**: gcc, clang, go, nodejs, jre-openjdk
- **Runtimes**: dotnet-runtime, dotnet-sdk
- **Dev tools**: git, cmake, boost, valgrind
- **Window manager**: qtile, qtile-extras
- **Audio**: pipewire, alsa-utils, mpd, mpv
- **Display**: xorg-server, picom, dunst
- **Networking**: networkmanager, iwd, bluez
- **Libraries**: gtk*, qt5*, qt6*, etc.

## Notes

- System pacman uses sudo (root) - desktop pacman runs as user
- Desktop packages use shared system libraries via bind mount of /usr
- Keep system and desktop package managers in sync for library versions
- The bind mount allows packages to install to ~/.local/apps/usr/bin/ while using system /usr/lib/ libraries - no duplicate library installations needed