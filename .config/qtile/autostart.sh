#!/usr/bin/env bash

pactl set-sink-mute @DEFAULT_SINK@ 0
pactl set-sink-volume @DEFAULT_SINK@ 60%

# xrandr --output HDMI-0 --mode 1920x1080 --rate 140
xinput set-prop 10 "libinput Click Method Enabled" 0 1

conky -c ~/.config/conky/.conkyrc &
udiskie --tray &
dunst &
picom -b &
mpd &
mpDris2 &
playerctl daemon &

blueman-applet &
volumeicon &
nm-applet &

# Run vim in a floating window
alacritty --class floatingVim -e vim &
