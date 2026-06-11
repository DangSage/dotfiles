local wezterm = require 'wezterm'


return {
  -- Color scheme matching your Alacritty config
  colors = {
    foreground = "#dcdcdc",
    background = "#303030",
    cursor_bg = "#ffdd00",
    cursor_fg = "#303030",
    cursor_border = "#ffdd00",

    selection_fg = "#dcdcdc",
    selection_bg = "#6a6a6a",

    ansi = {
      "#3f3f3f",        -- black
      "#D67979",          -- red
      "#60b48a",        -- green
      "#dfaf8f",       -- yellow
      "#9ab8d7",         -- blue
      "#dc8cc3",       -- magenta
      "#8cd0d3",         -- cyan
      "#ffffff",        -- white
    },

    brights = {
      "#555555",    -- black
      "#DCA3A3",   -- red
      "#72D5A3", -- green
      "#F0DFAF",-- yellow
      "#94BFF3",  -- blue
      "#EC93D3",-- magenta
      "#93E0E3",  -- cyan
      "#ffffff",        -- white
    },
  },
  
  -- Environment variables
  set_environment_variables = {
    TERM = "xterm-256color",
  },
  
  font = wezterm.font("Hack Nerd Font Mono"),
  font_size = 11.0,

  disable_default_key_bindings = true,
  keys = {
    -- Copy/Paste
    { key = "v", mods = "CTRL|SHIFT", action = wezterm.action({ PasteFrom = "Clipboard" }) },
    { key = "c", mods = "CTRL|SHIFT", action = wezterm.action({ CopyTo = "Clipboard" }) },
    { key = "Insert", mods = "SHIFT", action = wezterm.action({ PasteFrom = "PrimarySelection" }) },
    
    -- Font size
    { key = "0", mods = "CTRL", action = wezterm.action.ResetFontSize },
    { key = "=", mods = "CTRL", action = wezterm.action.IncreaseFontSize },
    { key = "+", mods = "CTRL|SHIFT", action = wezterm.action.IncreaseFontSize },
    { key = "-", mods = "CTRL", action = wezterm.action.DecreaseFontSize }, 

    -- Scrolling (matching your Alacritty bindings)
    { key = "PageUp", mods = "SHIFT", action = wezterm.action.ScrollByPage(-1) },
    { key = "PageDown", mods = "SHIFT", action = wezterm.action.ScrollByPage(1) },
    { key = "Home", mods = "SHIFT", action = wezterm.action.ScrollToTop },
    { key = "End", mods = "SHIFT", action = wezterm.action.ScrollToBottom },
    { key = "UpArrow", mods = "SHIFT", action = wezterm.action.ScrollByLine(-1) },
    { key = "DownArrow", mods = "SHIFT", action = wezterm.action.ScrollByLine(1) },
    { key = "LeftArrow", mods = "SHIFT", action = wezterm.action.ScrollToTop },
    { key = "RightArrow", mods = "SHIFT", action = wezterm.action.ScrollToBottom },

    -- Split Pane Management
    { key = "t", mods = "ALT", action = wezterm.action.SplitHorizontal { domain = "CurrentPaneDomain" } },
    { key = "t", mods = "ALT|SHIFT", action = wezterm.action.SplitVertical { domain = "CurrentPaneDomain" } },
    { key = "w", mods = "ALT", action = wezterm.action.CloseCurrentPane { confirm = true } },
    { key = "h", mods = "ALT", action = wezterm.action.ActivatePaneDirection "Left" },
    { key = "l", mods = "ALT", action = wezterm.action.ActivatePaneDirection "Right" },
    { key = "k", mods = "ALT", action = wezterm.action.ActivatePaneDirection "Up" },
    { key = "j", mods = "ALT", action = wezterm.action.ActivatePaneDirection "Down" },
    -- grow/shrink
    { key = "H", mods = "CTRL|SHIFT", action = wezterm.action.AdjustPaneSize { "Left", 5 } },
    { key = "L", mods = "CTRL|SHIFT", action = wezterm.action.AdjustPaneSize { "Right", 5 } },
    { key = "K", mods = "CTRL|SHIFT", action = wezterm.action.AdjustPaneSize { "Up", 5 } },
    { key = "J", mods = "CTRL|SHIFT", action = wezterm.action.AdjustPaneSize { "Down", 5 } },
  },
  
  -- Mouse bindings - FIXED
  mouse_bindings = {
    {
      event = { Up = { streak = 1, button = "Middle" } },
      action = wezterm.action({ PasteFrom = "PrimarySelection" }),
    },
  },
  
  -- Window configuration
  enable_tab_bar = true,
  hide_tab_bar_if_only_one_tab = true,
  use_fancy_tab_bar = false,
  window_decorations = "RESIZE",
  
  window_padding = {
    left = 12,
    right = 12,
    top = 12,
    bottom = 12,
  },
  
  initial_cols = 95,
  initial_rows = 28,
  
  scrollback_lines = 100000,
  window_background_opacity = 1.0,
  
  -- Disable some WezTerm-specific features to match Alacritty behavior
  adjust_window_size_when_changing_font_size = false,
  warn_about_missing_glyphs = false,

  -- Enable Kitty graphics protocol for better image support with fzf
  -- enable_kitty_graphics = true,
}
