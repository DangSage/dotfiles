# filepath: /home/khai/.config/qtile/mycolors.py
# Single source of truth for all color definitions across the system

# Original indexed list for backward compatibility with qtile config
colors = [
    "#303030",  # grey, 0
    "#ffffff",  # white, 1
    "#202020",  # dark grey, 2
    "#808080",  # light grey, 3
    "#93E0E3",  # blue, 4
    "#D67979",  # red, 5
    "#EC93D3",  # pink, 6
    "#72D5A3",  # green, 7
    "#94BFF3",  # light blue, 8
    "#1cfc03",  # deep green, 9
    "#ff0000",  # deep red, 10
    "#dfaf8f",  # gold, 11
    "#dc8cc3",  # purple, 12
]

# Semantic color mappings
class DalacrittiyColors:
    """Dalacritty color scheme - single source for all applications"""

    # Base colors
    background = "#303030"      # Main background
    background_dark = "#202020"  # Darker variant
    background_light = "#6a6a6a" # Lighter variant (for selections)

    foreground = "#dcdcdc"      # Main text
    foreground_dim = "#828997"  # Dimmed text

    # Greys
    grey_dark = "#555555"
    grey = "#606060"
    grey_light = "#808080"
    grey_lighter = "#909090"

    # Accent colors (matching dalacritty vim theme)
    red = "#D67979"
    red_bright = "#DCA3A3"
    red_deep = "#ff0000"
    red_critical = "#900000"

    green = "#60b48a"
    green_bright = "#72D5A3"
    green_deep = "#1cfc03"

    blue = "#9ab8d7"
    blue_bright = "#94BFF3"
    blue_cyan = "#93E0E3"
    blue_highlight = "#00a2ff"

    cyan = "#8cd0d3"
    cyan_bright = "#93E0E3"

    purple = "#dc8cc3"
    purple_bright = "#EC93D3"

    yellow = "#dfaf8f"
    yellow_bright = "#F0DFAF"
    yellow_cursor = "#ffdd00"

    orange = "#d19a66"
    orange_bright = "#e5c07b"

    # Monochrome
    white = "#ffffff"
    black = "#3f3f3f"

    # Additional semantic names
    cursor_bg = yellow_cursor
    cursor_fg = background

    @classmethod
    def to_wezterm_lua(cls):
        """Generate WezTerm color configuration in Lua format"""
        return f'''  colors = {{
    foreground = "{cls.foreground}",
    background = "{cls.background}",
    cursor_bg = "{cls.cursor_bg}",
    cursor_fg = "{cls.cursor_fg}",
    cursor_border = "{cls.cursor_bg}",

    selection_fg = "{cls.foreground}",
    selection_bg = "{cls.background_light}",

    ansi = {{
      "{cls.black}",        -- black
      "{cls.red}",          -- red
      "{cls.green}",        -- green
      "{cls.yellow}",       -- yellow
      "{cls.blue}",         -- blue
      "{cls.purple}",       -- magenta
      "{cls.cyan}",         -- cyan
      "{cls.white}",        -- white
    }},

    brights = {{
      "{cls.grey_dark}",    -- black
      "{cls.red_bright}",   -- red
      "{cls.green_bright}", -- green
      "{cls.yellow_bright}",-- yellow
      "{cls.blue_bright}",  -- blue
      "{cls.purple_bright}",-- magenta
      "{cls.cyan_bright}",  -- cyan
      "{cls.white}",        -- white
    }},
  }}'''

    @classmethod
    def to_fzf_opts(cls):
        """Generate FZF color options"""
        return f'''export FZF_DEFAULT_OPTS="
  --height 40%
  --layout=reverse
  --border
  --inline-info
  --color=fg:{cls.foreground},bg:{cls.background},hl:{cls.blue}
  --color=fg+:{cls.white},bg+:{cls.background_light},hl+:{cls.blue_bright}
  --color=info:{cls.yellow},prompt:{cls.purple},pointer:{cls.green}
  --color=marker:{cls.green_bright},spinner:{cls.cyan},header:{cls.blue}
"'''

    @classmethod
    def to_dunst_ini(cls):
        """Generate Dunst color configuration"""
        return f'''[global]
    highlight = "{cls.blue_highlight}"
    frame_color = "{cls.grey_lighter}"

[urgency_low]
    background = "{cls.background_dark}"
    foreground = "{cls.foreground}"
    frame_color = "{cls.grey_light}"

[urgency_normal]
    background = "{cls.background_dark}"
    foreground = "{cls.foreground}"
    frame_color = "{cls.blue}"

[urgency_critical]
    background = "{cls.red_critical}"
    foreground = "{cls.white}"
    frame_color = "{cls.red_deep}"'''

    @classmethod
    def to_gtk_css(cls):
        """Generate GTK CSS for custom theming"""
        return f'''/* GTK Custom Colors - Generated from dalacritty theme */
@define-color theme_bg_color {cls.background};
@define-color theme_fg_color {cls.foreground};
@define-color theme_base_color {cls.background_dark};
@define-color theme_text_color {cls.foreground};
@define-color theme_selected_bg_color {cls.blue};
@define-color theme_selected_fg_color {cls.white};
@define-color insensitive_bg_color {cls.grey_dark};
@define-color insensitive_fg_color {cls.grey_light};
@define-color borders {cls.grey_light};
@define-color warning_color {cls.yellow};
@define-color error_color {cls.red};
@define-color success_color {cls.green_bright};

* {{
    background-color: {cls.background};
    color: {cls.foreground};
}}

window {{
    background-color: {cls.background};
}}

.titlebar {{
    background-color: {cls.background_dark};
    color: {cls.foreground};
}}

button {{
    background-color: {cls.background_light};
    color: {cls.foreground};
    border: 1px solid {cls.grey_light};
}}

button:hover {{
    background-color: {cls.blue};
    color: {cls.white};
}}

entry {{
    background-color: {cls.background_dark};
    color: {cls.foreground};
    border: 1px solid {cls.grey_light};
}}

entry:focus {{
    border-color: {cls.blue};
}}

.view {{
    background-color: {cls.background};
    color: {cls.foreground};
}}

.view:selected {{
    background-color: {cls.blue};
    color: {cls.white};
}}'''

# Create instance for easy access
dalacritty = DalacrittiyColors()
