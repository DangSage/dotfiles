# "Dalacritty" - My Qtile Rice 🍚

This is my own Arch Linux rice based on [kj_sh604's awesomeWM rice](https://github.com/kj-sh604/dotfiles). I have made some modifications to the original rice to suit my own needs and different use cases for Qtile. This repository contains the configuration files for the following programs:

## Dotfiles
- `Qtile` (Window Manager)
- `dunst` (Notification Daemon)
- `picom` (Compositor)
- `rofi` (Application Launcher)
- `alacritty` (Terminal Emulator)
- `vim` (Text Editor)
- `gtk` (Theme)
- `volumeicon` (Volume Control)
- `ranger` (File Manager)
- `btop` (System Monitor)
- `thunar` (File Manager)
- `myxer` (Volume Control)

and some basic daemons and services.

## Installation

### Additional Packages

I have included a list of packages that I use on my system. I've kept the lists within the `.config/.PACKS/` directory. You can install all the packages w/ the simple bash script here:

```sh
while read -r line; do
    sudo pacman -S $line
done < .config/.PACKS/pacman.txt

while read -r line; do
    sudo pikaur -S $line   # or any other AUR helper
done < .config/.PACKS/aur.txt
```


### Required Daemons

The following daemons will need to be set up:

- `bluez` (Bluetooth)
- `networkmanager` (Networking)
- `solaar` (Logitech Unifying Receiver)
- `udiskie` (Automounting)

To enable these daemons, run the following commands:

```sh
sudo systemctl enable bluetooth
sudo systemctl enable NetworkManager
sudo systemctl enable solaar
sudo systemctl enable udiskie
```

### Vim Configuration for Arch Linux

By default, Vim on Arch Linux is not compiled with Python3 or clipboard support. To enable these features, you will need to recompile Vim with the following flags:

```sh
git clone git@github.com:vim/vim.git
cd vim
./configure \
    --prefix=/usr \
    --with-features=huge \
    --enable-multibyte \
    --enable-rubyinterp \
    --enable-python3interp \
    --enable-perlinterp \
    --enable-luainterp \
    --enable-gui=auto \
    --enable-gtk2-check \
    --enable-gnome-check \
    --with-x \
    --enable-cscope \
    --prefix=/usr
make
sudo make install
```

It's also worthy to note you WILL need uninstall the `vim` package from the official repositories before compiling Vim from source. This WILL cause conflicts in the package manager.

<!-- line here -->
**Note:** You may need to install the `python-pip` package to install the `neovim` package.

### Branches

There's different branches for this repository, where the `desktop` branch is the main most maintained one. All laptop-specific configurations are relatively the same with some performance tweaks and power management settings.

Happy ricing!
