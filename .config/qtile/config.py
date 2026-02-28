import gi
import os
import subprocess
import datetime

gi.require_version("Notify", "0.7")

from libqtile import qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import bar, layout
from qtile_extras import widget
from mycolors import colors

mod = "mod4"
terminal = "wezterm"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    subprocess.Popen([home + "/.config/qtile/autostart.sh"])


@hook.subscribe.client_focus
def bring_floating_to_front(window):
    """Ensure floating windows always stay on top when focused"""
    if window.floating:
        window.bring_to_front()


@hook.subscribe.client_new
def float_to_front(window):
    """Bring new floating windows to front immediately"""
    if window.floating:
        window.bring_to_front()


@hook.subscribe.float_change
def on_float_change():
    """Bring newly floated windows to front"""
    window = qtile.current_window
    if window and window.floating:
        window.bring_to_front()


@hook.subscribe.resume
def restart_on_resume():
    """Restart compositor and refresh display after waking from sleep"""
    import time

    time.sleep(1)  # Give the system a moment to stabilize
    subprocess.Popen(["killall", "picom"])
    time.sleep(0.5)
    subprocess.Popen(["picom", "-b"])
    qtile.reload_config()  # Reload to refresh wallpaper


def toggle_focus_floating():
    """Toggle focus between floating window and other windows in group"""

    @lazy.function
    def _toggle_focus_floating(qtile):
        group = qtile.current_group
        switch = "non-float" if qtile.current_window.floating else "float"
        logger.debug(
            f"toggle_focus_floating: switch = {switch}\t current_window: {qtile.current_window}"
        )
        logger.debug(f"focus_history: {group.focus_history}")

        for win in reversed(group.focus_history):
            logger.debug(f"{win}: {win.floating}")
            if switch == "float" and win.floating:
                group.focus(win)
                return
            if switch == "non-float" and not win.floating:
                group.focus(win)
                return

    return _toggle_focus_floating


def open_google_calendar():
    """Open Google Calendar in browser"""
    today = datetime.date.today()
    url = f"https://calendar.google.com/calendar/r/week/{today.year}/{today.month:02d}/{today.day:02d}"
    qtile.cmd_spawn(f"xdg-open {url}")


def change_brightness(direction):
    """Change brightness and show notification in one call"""

    @lazy.function
    def _change(qtile):
        try:
            # Change brightness
            subprocess.run(["brightnessctl", "set", f"5%{direction}"])

            # Get current values for notification
            get = subprocess.run(
                ["brightnessctl", "get"], capture_output=True, text=True
            )
            max_b = subprocess.run(
                ["brightnessctl", "max"], capture_output=True, text=True
            )
            current = int(get.stdout.strip())
            maximum = int(max_b.stdout.strip())
            pct = (current * 100) // maximum

            # Send notification
            subprocess.Popen(
                [
                    "notify-send",
                    "-a",
                    "Brightness",
                    "-r",
                    "999",
                    f"Brightness: {pct}%",
                    "-h",
                    f"int:value:{pct}",
                    "-t",
                    "1000",
                ]
            )
        except:
            pass

    return _change


def toggle_redshift():
    """Toggle color shift between 6500K (daylight) and 3500K (warm)"""

    @lazy.function
    def _toggle(qtile):
        try:
            state_file = "/tmp/redshift_state"

            # Read current state from file, default to daylight (6500K)
            try:
                with open(state_file, "r") as f:
                    current_temp = int(f.read().strip())
            except:
                current_temp = 6500

            # Toggle between 3500K and 6500K
            if current_temp == 6500:
                # Currently daylight, switch to warm
                new_temp = 3500
                state = "3500K (Warm)"
            else:
                # Currently warm, switch to daylight
                new_temp = 6500
                state = "6500K (Daylight)"

            # Apply the temperature
            subprocess.run(["redshift", "-P", "-O", str(new_temp)])

            # Save the new state
            with open(state_file, "w") as f:
                f.write(str(new_temp))

            # Send notification
            subprocess.Popen(
                [
                    "notify-send",
                    "-a",
                    "Redshift",
                    "-r",
                    "998",
                    f"Color Temperature: {state}",
                    "-t",
                    "2000",
                ]
            )
        except:
            pass

    return _toggle


# ============================================================================
# SCRATCHPAD FUNCTIONALITY
# ============================================================================


@hook.subscribe.client_managed
def auto_float_scratchpad(window):
    """Automatically float and center windows sent to scratchpad"""
    if window.group and window.group.name == "scratchpad":
        window.floating = True
        screen = window.group.screen or qtile.current_screen
        window.place(
            screen.x + screen.width // 10,
            screen.y + screen.height // 10,
            screen.width * 8 // 10,
            screen.height * 8 // 10,
            0,
            None,
        )


@lazy.function
def toggle_scratchpad(qtile):
    """Toggle visibility of all scratchpad windows"""
    scratchpad = qtile.groups_map["scratchpad"]

    if not scratchpad.windows:
        return

    current_group = qtile.current_group

    visible = False
    for window in scratchpad.windows:
        if window.group == current_group or not window.minimized:
            visible = True
            break

    if visible:
        for window in scratchpad.windows:
            window.togroup("scratchpad")
            window.minimized = True
            window.hide()
    else:
        for window in scratchpad.windows:
            window.minimized = False
            window.unhide()
            window.floating = True
            window.bring_to_front()

            screen = qtile.current_screen
            window.place(
                screen.x + screen.width // 10,
                screen.y + screen.height // 10,
                screen.width * 8 // 10,
                screen.height * 8 // 10,
                0,
                None,
            )

        if scratchpad.windows:
            scratchpad.windows[0].focus(False)


@lazy.function
def send_to_scratchpad(qtile):
    """Send current window to scratchpad"""
    if qtile.current_window:
        qtile.current_window.togroup("scratchpad")


@lazy.function
def pull_from_scratchpad(qtile):
    """Pull the first window from scratchpad to current group"""
    scratchpad = qtile.groups_map["scratchpad"]

    if scratchpad.windows:
        window = scratchpad.windows[0]
        current_group = qtile.current_group
        window.togroup(current_group.name)
        window.floating = False
        window.focus(False)


############################################################################
# KEYBINDINGS
############################################################################

from libqtile.config import EzKey

keymap = {
    # Window management
    "M-h": (lazy.layout.left(), "Move focus to left"),
    "M-j": (lazy.layout.down(), "Move focus down"),
    "M-k": (lazy.layout.up(), "Move focus up"),
    "M-l": (lazy.layout.right(), "Move focus to right"),
    "M-S-h": (lazy.layout.swap_left(), "Move window to the left"),
    "M-S-j": (lazy.layout.shuffle_down(), "Move window down"),
    "M-S-k": (lazy.layout.shuffle_up(), "Move window up"),
    "M-S-l": (lazy.layout.swap_right(), "Move window to the right"),
    "M-S-C-j": (lazy.layout.section_down(), "Move window to the next section"),
    "M-S-C-k": (lazy.layout.section_up(), "Move window to the previous section"),
    "M-a": (lazy.layout.grow(), "Grow monad"),
    "M-x": (lazy.layout.shrink(), "Shrink monad"),
    "M-n": (lazy.layout.normalize(), "Reset size"),
    "M-S-n": (lazy.layout.reset(), "Reset layout"),
    "A-<Tab>": (lazy.layout.next(), "Move to next window"),
    "A-S-<Tab>": (lazy.layout.previous(), "Move to previous window"),
    "M-<grave>": (lazy.spawn(terminal), "Launch terminal"),
    "M-q": (lazy.window.kill(), "Kill focused window"),
    "M-f": (lazy.next_layout(), "Toggle between layouts"),
    "M-S-f": (lazy.layout.flip(), "Flip Monad"),
    "M-t": (lazy.window.toggle_floating(), "Toggle floating mode"),
    #"M-f": (lazy.window.toggle_fullscreen(), "Toggle fullscreen mode"),
    # Application launchers - Rofi based
    "A-<Space>": (
        lazy.spawn("/home/khai/.config/qtile/rofi_app_launcher.sh"),
        "App launcher",
    ),
    "M-w": (lazy.spawn("thorium-browser"), "Launch thorium-browser"),
    # System controls - Rofi based power menu
    "M-<Escape>": (
        lazy.spawn("/home/khai/.config/qtile/rofi_power_menu.sh"),
        "Power menu",
    ),
    "M-r": (lazy.spawncmd(), "Spawn command"),
    "M-S-<Escape>": (lazy.spawn("systemctl suspend"), "Suspend system"),
    "M-C-r": (lazy.restart(), "Restart Qtile"),
    # Scratchpad controls (manual scratchpad for general use)
    "M-p": (toggle_scratchpad, "Toggle scratchpad visibility"),
    "M-S-p": (send_to_scratchpad, "Send window to scratchpad"),
    "M-C-p": (pull_from_scratchpad, "Pull window from scratchpad"),
    "<F9>": (toggle_redshift(), "Toggle night light (redshift)"),
    # Rofi Keybindings viewer (large window with green borders)
    "<F12>": (
        lazy.spawn("/home/khai/.config/qtile/rofi_keybinds.sh"),
        "Show keybindings",
    ),
}

keys = [*[EzKey(k, v[0], desc=v[1]) for k, v in keymap.items()]]

keys.extend(
    [
        Key(
            [],
            "XF86MonBrightnessDown",
            change_brightness("-"),
            desc="Lower Brightness by 5%",
        ),
        Key(
            [],
            "XF86MonBrightnessUp",
            change_brightness("+"),
            desc="Raise Brightness by 5%",
        ),
        Key(
            [],
            "XF86AudioRaiseVolume",
            lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
            desc="Raise volume by 5%",
        ),
        Key(
            [],
            "XF86AudioLowerVolume",
            lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
            desc="Lower volume by 5%",
        ),
        Key(
            [],
            "XF86AudioMute",
            lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
            desc="Toggle audio mute",
        ),
        Key(
            [],
            "Print",
            lazy.spawn("/home/khai/.config/qtile/screenshot.sh"),
            desc="Take screenshot",
        ),
    ]
)

# Add key bindings to switch VTs in Wayland
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

############################################################################
# GROUPS AND SCRATCHPAD
############################################################################

groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4"),
]

# MANUAL SCRATCHPAD - For general window management
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term", terminal, opacity=1.0, height=0.6, width=0.6, x=0.2, y=0.2
            ),
            DropDown(
                "music", "spotify", opacity=1.0, height=0.7, width=0.7, x=0.15, y=0.15
            ),
            DropDown(
                "files", "thunar", opacity=1.0, height=0.6, width=0.6, x=0.2, y=0.2
            ),
        ],
    )
)

# ROFI MENUS - Simple, fast, purpose-built menu system
# All menus (power, apps, keybindings) now use rofi with green borders (#72D5A3)

for i in groups:
    if isinstance(i, ScratchPad):
        continue

    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

############################################################################
# LAYOUTS
############################################################################

layouts = [
    layout.MonadTall(
        border_focus=colors[5],
        border_normal="#000000",
        border_width=1,
        margin=12,
    ),
    layout.Max()
]

############################################################################
# WIDGETS AND BAR
############################################################################

widget_defaults = dict(
    font="Hack Nerd Font",
    fontsize=12,
    padding=6,
    foreground=colors[1],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="text",
                    highlight_color=colors[5],
                    padding=3,
                    borderwidth=1,
                    active=colors[1],
                    inactive=colors[3],
                    this_current_screen_border=colors[5],
                    this_screen_border=colors[5],
                    other_screen_border=colors[5],
                    # Make the line appear as dots by reducing visibility
                    line_width=2,
                    border_width=0,
                    highlight_margin=2,
                    disable_drag=True,
                ),
                widget.Spacer(),
                widget.Prompt(),
                widget.Spacer(),
                widget.Systray(),
                widget.Clock(
                    format="%I:%M:%S %P %a %Y-%m-%d",
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn("gsimplecal"),
                        "Button3": lambda: open_google_calendar(),
                    },
                ),
                widget.WindowCount(show_zero=True,),
            ],
            20,
            border_width=[0, 0, 0, 0],
            background=colors[0],
        ),
        wallpaper="~/.config/qtile/_bg.png",
        wallpaper_mode="stretch",
    ),
]

############################################################################
# MOUSE
############################################################################

mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

############################################################################
# FLOATING LAYOUT
############################################################################

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(wm_class="blueman-manager"),
        Match(title="pinentry"),
        Match(wm_class="floatterm"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="Pavucontrol"),
    ],
    border_focus=colors[8],
    bring_front_click=True,
)
auto_fullscreen = True
focus_on_window_activation = "focus"
reconfigure_screens = False
auto_minimize = True

wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 12

wmname = "qtile"
