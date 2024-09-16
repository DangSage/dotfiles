# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gi
import os
import subprocess
import datetime

gi.require_version('Notify', '0.7')
from gi.repository import Notify, GLib
from backlight_notify import notify_brightness

from libqtile import qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import bar, layout  # Core Qtile components
from qtile_extras import widget

mod = "mod4"
mod1 = "mod1"
terminal = guess_terminal()

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])

# gsimplecal integration with google calendar
def open_google_calendar():
    today = datetime.date.today()
    url = f"https://calendar.google.com/calendar/r/week/{today.year}/{today.month:02d}/{today.day:02d}"
    qtile.cmd_spawn(f'xdg-open {url}')

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),

    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod1], "space", lazy.spawn("rofi -show drun")),
    Key([mod], "w", lazy.spawn("firefox")),
    Key([mod], "f", lazy.window.toggle_floating()),
    Key([], "F11", lazy.spawn("/home/khai/.config/qtile/screenshot.sh")),
    Key([mod], "Escape", lazy.spawn("/home/khai/.config/rofi/rofi-power-menu.sh"), desc="Shutdown Qtile"),
    Key([], "F9", lazy.spawn("xrandr-invert-colors")),

    Key([], "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 1%-"),
        lazy.function(lambda qtile: notify_brightness()),
        desc="Lower Brightness by 5%"
    ),
    Key([], "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set +1%"),
        lazy.function(lambda qtile: notify_brightness()),
        desc="Raise Brightness by 5%"
    ),

    #Key([mod, "shift"], "/", lazy.function(display_keybindings), desc="Print keyboard bindings"),
]



# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus="#D67979",margin=15,border_width=1),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
    #layout.Bsp(),
    #layout.Matrix(),
    #layout.MonadTall(),
    #layout.MonadWide(),
    #layout.RatioTile(),
    #layout.Tile(),
    #layout.TreeTab(),
    #layout.Verticaltile(),
    #layout.Zoomy(),
]

widget_defaults = dict(
    font="Caskaydia Cove Nerd Font Mono",
    fontsize=14,
    padding=5,
    type='line',
    line_width=1,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.GroupBox(hide_unused=True,highlight_color="#93E0E3"),
                widget.Sep(foreground="#808080"),
                widget.Prompt(padding = 0),
                widget.WindowName(
                    format="{name}",
                    max_chars=0,
                    width=400,
                    scroll_fixed_width=True,
                ),
                widget.Spacer(),
                widget.CPUGraph(
                    graph_color="#EC93D3",
                    fill_color="#EC93D3",
                    border_width=0
                ),
                widget.MemoryGraph(
                    graph_color="#72D5A3",
                    fill_color="#72D5A3",
                    measure_mem=True,
                    border_width=0
                ),
                widget.NetGraph(
                    graph_color="#94BFF3",
                    fill_color="#94BFF3",
                    border_width=0
                ),
                widget.Sep(foreground="#808080"),
                widget.DF(
                    partition='/home/',
                    format='U: {uf}/{s} GB ({r:.3}%)',
                    visible_on_warn=False,
                    warn_space=80,
                    measure='G',
                    padding=5,
                    foreground='ffffff',
                    update_interval=60,
                ),
                widget.Sep(foreground="#808080"),
                widget.Spacer(),
                widget.Systray(),
                widget.Spacer(length=5),
                widget.Sep(foreground="#808080"),
                # extra widgets tooltips for the clock
                # widget.Clock(format="%I:%M:%S %P %a %Y-%m-%d"),
                # custom widget for the clock to bring up a calendar
                widget.Clock(format="%I:%M:%S %P %a %Y-%m-%d", mouse_callbacks={
                    'Button1': lambda: qtile.cmd_spawn('gsimplecal'),
                    'Button3': lambda: open_google_calendar(),
                }),
                widget.Sep(foreground="#808080"),
                
                # Battery widget, comment out on desktop
                widget.Battery(
                    format="{char} {percent:2.0%} {hour:d}:{min:02d}  ",
                    foreground="#1cfc03"
                ),
                #widget.QuickExit(background='C56868',foreground='F0DFAF'),
            ],
            24,
            border_width=[0, 0, 0, 0],
            background="#00000000",
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,

        # Wallpaper
        wallpaper='~/.config/qtile/_bg3.png',
        wallpaper_mode='stretch'
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(wm_class="blueman-manager"),
        Match(title="pinentry"),  # GPG key password entry
    ],
    border_focus="#94BFF3",
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = False

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 12

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
