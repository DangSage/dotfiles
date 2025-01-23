import gi
import os
import subprocess
import datetime

gi.require_version('Notify', '0.7')

from libqtile import qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import bar, layout  # Core Qtile components
from qtile_extras import widget  # Custom widgets
from mycolors import colors

from backlight_notify import notify_brightness

mod = "mod4"
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


from libqtile.config import EzKey
from libqtile.lazy import lazy
keymap = {
    # M = mod, S = shift, A = alt, C = control
    # Window management
    'M-h': (lazy.layout.left(), "Move focus to left"),
    'M-j': (lazy.layout.down(), "Move focus down"),
    'M-k': (lazy.layout.up(), "Move focus up"),
    'M-l': (lazy.layout.right(), "Move focus to right"),
    'M-S-h': (lazy.layout.move_left(), "Move window to the left"),
    'M-S-j': (lazy.layout.move_down(), "Move window down"),
    'M-S-k': (lazy.layout.move_up(), "Move window up"),
    'M-S-l': (lazy.layout.move_right(), "Move window to the right"),
    'M-S-C-j': (lazy.layout.section_down(), "Move window to the next section"),
    'M-S-C-k': (lazy.layout.section_up(), "Move window to the previous section"),
    'M-S-C-<Return>': (lazy.layout.add_section(), "Add a new section"),
    'M-S-C-q': (lazy.layout.remove_section(), "Remove current section"),
    'M-A-h': (lazy.layout.integrate_left(), "Integrate window to the left"),
    'M-A-j': (lazy.layout.integrate_down(), "Integrate window down"),
    'M-A-k': (lazy.layout.integrate_up(), "Integrate window up"),
    'M-A-l': (lazy.layout.integrate_right(), "Integrate window to the right"),
    'M-d': (lazy.layout.mode_horizontal(), "Switch to horizontal mode"),
    'M-v': (lazy.layout.mode_vertical(), "Switch to vertical mode"),
    'M-S-d': (lazy.layout.mode_horizontal_split(), "Split layout horizontally"),
    'M-S-v': (lazy.layout.mode_vertical_split(), "Split layout vertically"),
    'M-a': (lazy.layout.grow_width(20), "Grow width by 20"),
    'M-x': (lazy.layout.grow_width(-20), "Shrink width by 20"),
    'M-S-a': (lazy.layout.grow_height(20), "Grow height by 20"),
    'M-S-x': (lazy.layout.grow_height(-20), "Shrink height by 20"),
    'M-C-5': (lazy.layout.size(500), "Set size to 500"),
    'M-C-8': (lazy.layout.size(800), "Set size to 800"),
    'M-n': (lazy.layout.reset_size(), "Reset size"),
    'A-<Tab>': (lazy.layout.next(), "Move to next window"),
    'M-<return>': (lazy.spawn(terminal), "Launch terminal"),
    'M-q': (lazy.window.kill(), "Kill focused window"),
    'M-<Tab>': (lazy.next_layout(), "Toggle between layouts"),
    'M-f': (lazy.window.toggle_floating(), "Toggle floating mode"),

    # Application launchers
    'A-<Space>': (lazy.spawn("rofi -show drun"), "Launch rofi"),
    'M-w': (lazy.spawn("firefox"), "Launch firefox"),

    # System controls
    'M-<Escape>': (lazy.spawn("/home/khai/.config/rofi/rofi-power-menu.sh"), "Shutdown Qtile"),
    'M-r' : (lazy.spawncmd(), "Spawn command"),
    'M-S-<Escape>': (lazy.spawn("systemctl suspend"), "Suspend system"),
    'M-C-r': (lazy.restart(), "Restart Qtile"),

    # display keybindings
    # 'M-<slash>': (lazy.spawn("keyb -p | rofi -dmenu"), "Display keybindings"),
}

keys = [
    *[EzKey(k, v[0], desc=v[1]) for k, v in keymap.items()],
    # Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    #Key([mod, "shift"], "/", lazy.function(display_keybindings), desc="Print keyboard bindings"),
    Key([], "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 5%-"),
        lazy.function(lambda qtile: notify_brightness()),
        desc="Lower Brightness by 5%"
    ),
    Key([], "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set +5%"),
        lazy.function(lambda qtile: notify_brightness()),
        desc="Raise Brightness by 5%"
    ),

    # Media keys
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle"), desc="Mute volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-"), desc="Lower volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+"), desc="Raise volume"),
    Key([], "XF86AudioMicMute", lazy.spawn("amixer -q set Capture toggle"), desc="Mute microphone"),

    # screenshot on f11
    Key([], "Print", lazy.spawn("/home/khai/.config/qtile/screenshot.sh"), desc="Take screenshot"),
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
    layout.Plasma(
        border_focus=colors[5],
        border_normal="#000000",
        border_width=1,
        border_width_single=0,
        margin=15,
    ),
    layout.TreeTab(
        active_bg=colors[7],
        active_fg=colors[0],
        bg_color=colors[2],
        border_width=1,
        font='Hack Nerd Font',
        fontshadow=None,
        fontsize=10,
        inactive_bg=colors[2],
        inactive_fg=colors[1],
        level_shift=8,
        margin_left=6,
        margin_y=6,
        padding_left=2,
        padding_x=6,
        padding_y=2,
        panel_width=230,
        previous_on_rm=False,
        section_bottom=6,
        section_fg=colors[1],
        section_fontsize=11,
        section_left=2,
        section_padding=4,
        section_top=4,
        sections=['1', '2', '3', '4'],
        urgent_bg=colors[10],
        urgent_fg=colors[1],
        vspace=0,
        margin=0,  # Align text margins from the left
    ),
    # Try more layouts by unleashing below layouts.
]

widget_defaults = dict(
    font="Hack Nerd Font",
    fontsize=16,
    padding=6,
    type='line',
    foreground=colors[1],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # extra widgets tooltips for the clock
                # widget.Clock(format="%I:%M:%S %P %a %Y-%m-%d"),
                widget.GroupBox(
                    highlight_color=colors[5],
                    highlight_method='line',
                    padding=3,
                    borderwidth=3,
                    active=colors[1],
                    inactive=colors[3],
                    this_current_screen_border=colors[5],
                    this_screen_border=colors[5],
                    other_screen_border=colors[5],
                ),
                widget.Sep(foreground=colors[3]),
                widget.WindowName(
                    max_chars=0,
                    width=400,
                    scroll_fixed_width=True,
                    foreground=colors[8],
                ),
                widget.Spacer(),
                widget.Net(
                    format='󱚶 {down:6.2f} ',
                    foreground=colors[12],
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('alacritty -e btop -p 2')},
                ),
                widget.DF(
                    partition='/',
                    format=' {r:.0f}% ',
                    visible_on_warn=False,
                    measure='G',
                    update_interval=60,
                    foreground=colors[11],
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('alacritty -e gdu')}
                ),
                widget.CPU(
                    format=" {load_percent:.0f}% ",
                    markup=True,
                    foreground=colors[7],
                    padding=5,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('alacritty -e btop -p 1')}
                ),
                widget.Memory(
                    format=" {MemPercent:.0f}% ",
                    markup=True,
                    foreground=colors[4],
                    padding=5,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('alacritty -e btop -p 2')}
                ),

                widget.Spacer(),
                widget.Systray(
                    padding=5,
                    icon_size=20,
                ),

                widget.Sep(foreground=colors[3]),
                widget.Clock(format="%I:%M:%S %P %a %Y-%m-%d", mouse_callbacks={
                    'Button1': lambda: qtile.cmd_spawn('gsimplecal'),
                    'Button3': lambda: open_google_calendar(),
                }),
                widget.Sep(foreground=colors[3]),
                #widget.TextBox(
                #    text='󰍜 ',
                #    foreground=colors[5],
                #    padding=5,
                #    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('/home/khai/.config/rofi/rofi-power-menu.sh')}
                #),

                # Battery widget, comment out on desktop
                widget.Battery(
                    format="{char} {percent:2.0%} {hour:d}:{min:02d}  ",
                    foreground=colors[7]
                ),
            ],
            30,
            border_width=[0, 0, 0, 0],
            background=colors[0],
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,

        # Wallpaper
        wallpaper= "~/.config/qtile/_bg.png",
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
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(wm_class="blueman-manager"),
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class='floatingVim'),
    ],
    border_focus=colors[8],
    bring_front_click=True,  # Ensure floating windows are brought to front when clicked
)
auto_fullscreen = True
focus_on_window_activation = "true"
reconfigure_screens = False
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None
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
