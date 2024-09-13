#!/usr/bin/env bash

pactl set-sink-mute @DEFAULT_SINK@ 0
pactl set-sink-volume @DEFAULT_SINK@ 60%

xinput set-prop "device" "libinput Click Method Enabled" 0 1

udiskie --tray &
dunst &
picom &
mpd &
mpDris2 &
playerctl daemon &

blueman-applet &
volumeicon &
nm-applet &
