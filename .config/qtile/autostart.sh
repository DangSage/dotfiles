#!/usr/bin/env bash

pactl set-sink-mute @DEFAULT_SINK@ 0
pactl set-sink-volume @DEFAULT_SINK@ 60%

dunst &
picom &
mpd &
mpDris2 &
playerctl daemon &

blueman-applet &
volumeicon &
nm-applet &
