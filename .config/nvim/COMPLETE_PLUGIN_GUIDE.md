# Complete Neovim Plugin Guide

This guide covers all installed plugins and their configurations in your Neovim setup.

---

## Table of Contents

1. [File Explorer - NERDTree](#1-file-explorer---nerdtree)
2. [Auto-Pairs - Pear Tree](#2-auto-pairs---pear-tree)
3. [Enhanced Matching - vim-matchit](#3-enhanced-matching---vim-matchit)
4. [Intellisense - CoC.nvim](#4-intellisense---cocnvim)
5. [Text Manipulation - vim-surround](#5-text-manipulation---vim-surround)
6. [Code Formatting - Neoformat](#6-code-formatting---neoformat)
7. [Vim Practice - vim-be-good](#7-vim-practice---vim-be-good)
8. [Fuzzy Finder - Telescope](#8-fuzzy-finder---telescope)
9. [Syntax Highlighting - Treesitter](#9-syntax-highlighting---treesitter)
10. [Focus Mode - True Zen](#10-focus-mode---true-zen)
11. [Git Integration - Neogit, Gitsigns, Diffview](#11-git-integration---neogit-gitsigns-diffview)
12. [General Keybindings](#12-general-keybindings)
13. [Editor Options](#13-editor-options)

---

## 1. File Explorer - NERDTree

**What it does:** A tree-based file system explorer for navigating your project files.

### Keybindings

| Key | Action |
|-----|--------|
| `<leader>n` | Focus NERDTree window |
| `<C-n>` | Open NERDTree |
| `<A-n>` | Toggle NERDTree on/off |
| `<leader>/` | Find current file in NERDTree |

### Inside NERDTree

| Key | Action |
|-----|--------|
| `Enter` | Open file or expand/collapse directory |
| `o` | Open file in split |
| `i` | Open file in horizontal split |
| `s` | Open file in vertical split |
| `t` | Open file in new tab |
| `m` | Show menu (create, delete, move files) |
| `r` | Refresh current directory |
| `R` | Refresh root directory |
| `?` | Toggle help |
| `q` | Close NERDTree |

### Usage Example
```
1. Press <A-n> to toggle NERDTree
2. Navigate with j/k
3. Press Enter to open files
4. Press m to create/delete/move files
```

---

## 2. Auto-Pairs - Pear Tree

**What it does:** Automatically inserts matching pairs of brackets, quotes, and parentheses.

### Features
- Automatically closes `()`, `[]`, `{}`, `""`, `''`
- Smart closing - doesn't duplicate if closing char already exists
- Press the closing character to skip over it

### Examples
```
Type: function(
Result: function(|)
        (| represents cursor)

Type: "hello
Result: "hello|"

Type: {
Result: {|}
```

---

## 3. Enhanced Matching - vim-matchit

**What it does:** Extends the `%` command to match language-specific pairs.

### Keybinding
| Key | Action |
|-----|--------|
| `%` | Jump between matching pairs |

### What it matches
- HTML/XML tags: `<div>` ↔ `</div>`
- Programming constructs: `if` ↔ `endif`, `function` ↔ `endfunction`
- Ruby: `def` ↔ `end`
- Python: tries to match block structures
- And many more language-specific pairs

### Usage Example
```html
<div>
  <p>Hello</p>  <!-- Press % on <p> to jump to </p> -->
</div>           <!-- Press % on <div> to jump to </div> -->
```

---

## 4. Intellisense - CoC.nvim

**What it does:** Provides VSCode-like intellisense, autocompletion, diagnostics, and language server support.

### Main Features
- Auto-completion
- Go to definition
- Find references
- Hover documentation
- Diagnostics (errors/warnings)
- Code actions (quick fixes)
- Refactoring
- Snippet support

### Completion Keybindings

| Key | Action |
|-----|--------|
| `<Tab>` | Navigate to next completion item |
| `<S-Tab>` | Navigate to previous completion item |
| `<CR>` (Enter) | Accept completion |
| `<C-c>` | Trigger completion manually |
| `<C-j>` | Expand snippet and jump to next placeholder |

### Navigation Keybindings

| Key | Action |
|-----|--------|
| `gd` | Go to definition |
| `gy` | Go to type definition |
| `gi` | Go to implementation |
| `gr` | Find references |
| `K` | Show documentation/hover info |
| `[g` | Previous diagnostic (error/warning) |
| `]g` | Next diagnostic (error/warning) |

### Code Actions

| Key | Action |
|-----|--------|
| `<leader>rn` | Rename symbol |
| `<leader>F` | Format selected code (visual mode) |
| `<leader>a` | Apply code action to selection |
| `<leader>ac` | Code action at cursor |
| `<leader>as` | Source code action (e.g., organize imports) |
| `<leader>qf` | Quick fix current line |
| `<leader>re` | Refactor |
| `<leader>r` | Refactor selected (visual mode) |
| `<leader>cl` | Code lens action |

### Text Objects

| Key | Action |
|-----|--------|
| `if` | Inner function (select inside function) |
| `af` | Around function (select whole function) |
| `ic` | Inner class |
| `ac` | Around class |

### Float Window Scrolling

| Key | Action |
|-----|--------|
| `<C-f>` | Scroll down in popup/documentation |
| `<C-b>` | Scroll up in popup/documentation |

### CoC Lists (Space Commands)

| Key | Action |
|-----|--------|
| `<space>a` | Show all diagnostics |
| `<space>e` | Manage CoC extensions |
| `<space>c` | Show available commands |
| `<space>o` | Document outline/symbols |
| `<space>s` | Search workspace symbols |
| `<space>j` | Next item in CoC list |
| `<space>k` | Previous item in CoC list |
| `<space>p` | Resume latest CoC list |

### Commands

| Command | Action |
|---------|--------|
| `:Format` | Format current buffer |
| `:Fold` | Fold current buffer |
| `:OR` | Organize imports |
| `:CocList diagnostics` | Show all diagnostics |

### Usage Example
```typescript
// 1. Start typing, autocomplete appears
function myFunc|  // Press Tab to complete

// 2. Hover over function to see docs
myFunction()  // Press K on myFunction

// 3. Go to definition
myFunction()  // Press gd on myFunction

// 4. Rename variable
let oldName = 5;  // Press <leader>rn on oldName

// 5. Fix errors
const x = "hello"  // If underlined, press <leader>qf
```

---

## 5. Text Manipulation - vim-surround

**What it does:** Easily add, change, and delete surrounding pairs (quotes, brackets, tags).

### Main Commands

| Command | Action |
|---------|--------|
| `cs"'` | Change surrounding " to ' |
| `cs'<q>` | Change surrounding ' to `<q></q>` tag |
| `ds"` | Delete surrounding " |
| `dst` | Delete surrounding HTML/XML tag |
| `ysiw"` | Add " around current word |
| `yss"` | Add " around entire line |
| `vS"` | In visual mode, surround selection with " |

### Examples

```
"Hello world!"
cs"'        → 'Hello world!'
cs'<em>     → <em>Hello world!</em>
dst         → Hello world!

Hello
ysiw"       → "Hello"

Hello world
yss(        → ( Hello world )

(visual select "world")
S"          → "world"
```

### Common Surrounds
- `"` - Double quotes
- `'` - Single quotes
- `` ` `` - Backticks
- `(` or `)` - Parentheses (with or without spaces)
- `[` or `]` - Square brackets
- `{` or `}` - Curly braces
- `<` or `>` - Angle brackets/HTML tags
- `t` - HTML/XML tags (e.g., `cst<div>`)

---

## 6. Code Formatting - Neoformat

**What it does:** Formats code using external formatters (prettier, black, etc.).

### Commands

| Command | Action |
|---------|--------|
| `:Neoformat` | Format current buffer |
| `:Neoformat prettier` | Format with specific formatter |

### Supported Formatters (examples)
- JavaScript/TypeScript: prettier, eslint
- Python: black, autopep8, yapf
- Go: gofmt
- Rust: rustfmt
- C/C++: clang-format
- HTML/CSS: prettier
- And many more...

### Usage
```
:Neoformat          " Auto-detect and format
:Neoformat prettier " Use prettier specifically
```

**Note:** You need to install formatters separately (e.g., `npm install -g prettier`)

---

## 7. Vim Practice - vim-be-good

**What it does:** A game/tutorial to practice Vim motions and improve speed.

### Commands

| Command | Action |
|---------|--------|
| `:VimBeGood` | Start the game menu |

### Available Games
- `relative` - Practice relative line jumping
- `ci{` - Practice change-inside motions
- `hjkl` - Basic movement practice
- `w/b/e` - Word navigation practice

### Usage
```
:VimBeGood
" Select a game from the menu
" Complete challenges to improve muscle memory
```

---

## 8. Fuzzy Finder - Telescope

**What it does:** Fast fuzzy finder for files, text, buffers, and more using ripgrep.

### Keybindings

| Key | Action |
|-----|--------|
| `<leader>ff` | Find files (including hidden, respecting .gitignore) |
| `<leader>fg` | Live grep (search text in files) |
| `<leader>fb` | Browse open buffers |
| `<leader>fh` | Search help tags |

### Inside Telescope

| Key | Action |
|-----|--------|
| `<C-n>` or `↓` | Next item |
| `<C-p>` or `↑` | Previous item |
| `<CR>` | Open selected file |
| `<C-x>` | Open in horizontal split |
| `<C-v>` | Open in vertical split |
| `<C-t>` | Open in new tab |
| `<Esc>` | Close Telescope |
| `<C-u>` | Scroll preview up |
| `<C-d>` | Scroll preview down |

### Usage Example
```
1. Press <leader>ff to find files
2. Start typing filename: "conf"
3. Results filter in real-time
4. Press Enter to open, or Ctrl-v for vertical split

Or:

1. Press <leader>fg to search text
2. Type: "function myFunc"
3. See all occurrences across all files
4. Press Enter to jump to match
```

### Configuration
- Uses ripgrep for fast searching
- Searches hidden files
- Respects .gitignore
- Custom prompt: " search:  "

---

## 9. Syntax Highlighting - Treesitter

**What it does:** Advanced syntax highlighting and code understanding using tree-sitter parsers.

### Features
- Better syntax highlighting than regex-based highlighting
- Code-aware selections and movements
- Better indentation
- Incremental parsing (fast)

### Installed Languages
Your config auto-installs parsers, with these guaranteed:
- Bash
- Lua
- Vim
- Vimdoc

### Disabled For
- PHP highlighting (using regex instead)
- Markdown highlighting (using regex instead)
- YAML indentation (disabled)

### Usage
Treesitter works automatically. You'll notice:
- More accurate syntax colors
- Better handling of complex code structures
- Faster highlighting updates

### Commands
```
:TSInstall <language>        " Install parser for language
:TSUpdate                    " Update all parsers
:TSUninstall <language>      " Remove parser
:TSInstallInfo              " Show installed parsers
```

### Example
```python
# Without Treesitter: basic colors
def function():
    return "hello"

# With Treesitter: accurate semantic colors
# - 'def' is keyword
# - 'function' is function name
# - 'return' is keyword
# - "hello" is string
# Each gets precise highlighting
```

---

## 10. Focus Mode - True Zen

**What it does:** Distraction-free writing/coding mode with various focus options.

### Commands

| Command | Action |
|---------|--------|
| `:TZAtaraxis` | Centered focus mode (Ataraxis) |
| `:TZMinimalist` | Minimal UI mode |
| `:TZNarrow` | Focus on selected text only |
| `:TZFocus` | Focus on current window |

### Modes Explained

**Ataraxis Mode** - Centered buffer with comfortable width
- Good for writing documentation
- Centers your code/text
- Dims background

**Minimalist Mode** - Hides UI elements
- No line numbers
- No status line
- Clean interface

**Narrow Mode** - Focus on selection
- Hides everything except selected text
- Good for reviewing specific sections

**Focus Mode** - Dims inactive splits
- Highlights current window
- Good for multi-window setups

### Usage
```
:TZAtaraxis    " Enter focus mode
" Work on your code
:TZAtaraxis    " Exit focus mode (toggle)
```

**Note:** Currently commented out in your config (`--require('zen')`). Uncomment line 9 in `init.lua` to enable.

---

## 11. Git Integration - Neogit, Gitsigns, Diffview

**What it does:** Complete git workflow integration similar to VSCode's Source Control.

See [GIT_INTEGRATION_GUIDE.md](GIT_INTEGRATION_GUIDE.md) for the complete guide.

### Quick Reference

#### Main Commands
| Key | Action |
|-----|--------|
| `<leader>gg` | Open Neogit (git status) |
| `<leader>gc` | Git commit |
| `<leader>gp` | Git push |
| `<leader>gl` | Git pull |
| `<leader>gd` | Open Diffview |
| `<leader>gh` | File history (current file) |
| `<leader>gb` | Toggle git blame |

#### Hunk Operations
| Key | Action |
|-----|--------|
| `]c` | Next git hunk (change) |
| `[c` | Previous git hunk |
| `<leader>hs` | Stage hunk |
| `<leader>hr` | Reset hunk |
| `<leader>hp` | Preview hunk |

#### In Neogit Window
| Key | Action |
|-----|--------|
| `s` | Stage file/hunk |
| `u` | Unstage file/hunk |
| `c` then `c` | Commit |
| `p` then `p` | Push |
| `?` | Show help |

---

## 12. General Keybindings

### Clipboard (X11)

| Key | Action | Mode |
|-----|--------|------|
| `<C-c>` | Copy to system clipboard | Visual |
| `<C-x>` | Cut to system clipboard | Visual |
| `<C-p>` | Paste from clipboard | Normal |
| `<leader>p` | Paste before cursor | Normal |

### Vertical Motion (Centered)

| Key | Action |
|-----|--------|
| `<C-d>` | Half page down (centered) |
| `<C-u>` | Half page up (centered) |
| `n` | Next search result (centered) |
| `N` | Previous search result (centered) |

### Spell Check

| Key | Action |
|-----|--------|
| `<leader>sc` | Toggle spell check on/off |

### Splits

| Key | Action |
|-----|--------|
| `<A-s>` | Create vertical split |
| `<A-d>` | Create horizontal split |
| `<A-q>` | Quit split (no save) |
| `<A-z>` | Save and quit split |

#### Split Navigation
| Key | Action |
|-----|--------|
| `<A-h>` | Move to left split |
| `<A-j>` | Move to down split |
| `<A-k>` | Move to up split |
| `<A-l>` | Move to right split |
| `<A-e>` | Cycle to next split |
| `<A-w>` | Cycle to previous split |

#### Split Resizing
| Key | Action |
|-----|--------|
| `<A-,>` | Decrease width |
| `<A-.>` | Increase width |
| `<A-->` | Decrease height |
| `<A-=>` | Increase height |

### Tabs

| Key | Action |
|-----|--------|
| `<A-t>` | New tab |
| `<A-[>` | Previous tab |
| `<A-]>` | Next tab |
| `<A-;>` | Move tab left |
| `<A-'>` | Move tab right |

### Other

| Key | Action |
|-----|--------|
| `<leader>ft` | Set file type (`:set filetype=`) |

---

## 13. Editor Options

### Display Options
- **Line numbers:** Absolute + relative
- **Cursor line:** Highlighted with bold
- **Mouse:** Enabled
- **Cursor style:** Block in normal, line in insert
- **Color scheme:** `dalacritty` (terminal), `tender` (GUI)

### Indentation
- **Tab width:** 4 spaces
- **Expand tabs:** Yes (converts tabs to spaces)
- **Auto indent:** Yes
- **Smart indent:** Based on file type

### Search
- **Highlight search:** Yes
- **Ignore case:** Yes (unless search has uppercase)
- **Smart case:** Yes

### Splits
- **Split below:** Yes (horizontal splits open below)
- **Split right:** Yes (vertical splits open right)

### Other Features
- **Undo file:** Persistent undo across sessions
- **Auto change directory:** Changes to file's directory
- **Line breaking:** On word boundaries
- **Show matching brackets:** Yes

### Whitespace Characters
When visible (`:set list`):
- Tab: `>-`
- Trailing space: `~`
- Extends: `>`
- Precedes: `<`
- Space: `.`

### Custom Statusline
Shows (from left to right):
- Buffer number
- File type
- File name
- Modified flag
- Current line / Total lines
- Column number
- Character code (hex)
- File format

---

## Quick Reference Card

### Most Used Commands

```
File Navigation:
  <leader>ff      - Find files
  <leader>fg      - Search in files
  <A-n>           - Toggle file tree

Code Navigation:
  gd              - Go to definition
  gr              - Find references
  K               - Show documentation
  [g / ]g         - Prev/Next error

Editing:
  <leader>rn      - Rename
  cs"'            - Change surround " to '
  <leader>F       - Format code

Git:
  <leader>gg      - Git status
  <leader>gc      - Commit
  <leader>gp      - Push

Windows:
  <A-s>           - Vertical split
  <A-hjkl>        - Navigate splits
  <A-t>           - New tab
```

---

## Plugin Installation/Updates

### Install Plugins
```vim
:PlugInstall
```

### Update Plugins
```vim
:PlugUpdate
```

### Clean Removed Plugins
```vim
:PlugClean
```

### Update CoC Extensions
```vim
:CocUpdate
```

### Install CoC Language Servers
```vim
:CocInstall coc-tsserver coc-json coc-python coc-rust-analyzer
```

---

## Troubleshooting

### Plugin not working?
1. Run `:PlugInstall`
2. Restart Neovim
3. Check `:checkhealth`

### CoC not providing completions?
1. Check if language server is installed: `:CocList extensions`
2. Install language server: `:CocInstall coc-<language>`
3. Check `:CocInfo` for errors

### Telescope not finding files?
- Requires `ripgrep` installed: `pacman -S ripgrep`

### Git integration not working?
1. Run `:PlugInstall`
2. Restart Neovim
3. Check if in a git repository

### Treesitter highlighting issues?
```vim
:TSUpdate        " Update parsers
:TSInstall <lang> " Install specific language
```

---

## Tips and Tricks

1. **Learn one plugin at a time** - Don't try to memorize everything at once
2. **Use `?` for help** - Many plugins show help with `?`
3. **Check `:checkhealth`** - Diagnoses common issues
4. **Use `:Telescope keymaps`** - Shows all keybindings (requires setup)
5. **Practice with `:VimBeGood`** - Improve muscle memory
6. **Use `<leader>sc`** - Turn on spell check when writing docs
7. **Press `K` liberally** - Hover documentation is your friend
8. **Use git hunks** - `<leader>hs` for partial commits is powerful

---

## What is `<leader>`?

Check your leader key:
```vim
:echo mapleader
```

If it returns nothing or `\`, your leader is backslash `\`.

To change leader key, add to your config:
```lua
vim.g.mapleader = " "  -- Space as leader
```

Common choices:
- Space (most popular)
- Comma `,`
- Backslash `\` (default)

---

## Resources

- NERDTree: https://github.com/preservim/nerdtree
- CoC.nvim: https://github.com/neoclide/coc.nvim
- Telescope: https://github.com/nvim-telescope/telescope.nvim
- Treesitter: https://github.com/nvim-treesitter/nvim-treesitter
- vim-surround: https://github.com/tpope/vim-surround
- Neogit: https://github.com/TimUntersberger/neogit

---

**Config Location:** `~/.config/nvim/`
**Last Updated:** 2025-10-29
