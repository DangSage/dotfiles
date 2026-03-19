#!/usr/bin/env bash

# Audio setup (only if pactl is available)
if command -v pactl >/dev/null; then
    pactl set-sink-mute @DEFAULT_SINK@ 0
    pactl set-sink-volume @DEFAULT_SINK@ 60%
fi

# Touchpad configuration (find device ID dynamically)
if command -v xinput >/dev/null; then
    TOUCHPAD_ID=$(xinput list | grep -i "touchpad" | grep -oP 'id=\K\d+' | head -1)
    [ -n "$TOUCHPAD_ID" ] && xinput set-prop "$TOUCHPAD_ID" "libinput Click Method Enabled" 0 1
fi

# Auto-detect and apply display configuration (fixes cursor DPI)
# Sleep briefly to ensure display server is fully initialized
sleep 0.5
command -v autorandr >/dev/null && autorandr --change --default stacked &

# System tray and utilities
command -v udiskie >/dev/null && udiskie --tray &
command -v dunst >/dev/null && dunst &
command -v picom >/dev/null && picom -b &

# System applets
command -v pasystray >/dev/null && pasystray --notify=sink --volume-max=150 --volume-inc=5 &
command -v blueman-applet >/dev/null && blueman-applet &
command -v nm-applet >/dev/null && nm-applet &

# Audio services
command -v mpd >/dev/null && mpd &
command -v mpDris2 >/dev/null && mpDris2 &
command -v playerctl >/dev/null && playerctl daemon &

# Terminal
command -v wezterm >/dev/null && wezterm &
