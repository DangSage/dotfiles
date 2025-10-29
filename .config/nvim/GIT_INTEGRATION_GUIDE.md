# Git Integration Guide for Neovim

## Installation Steps

1. Open Neovim: `nvim`
2. Run: `:PlugInstall`
3. Wait for plugins to install
4. Restart Neovim

## Main Keybindings

### Git Status & Operations
- `<leader>gg` - Open Neogit (Git Status/Tree view) - **Main interface like VSCode**
- `<leader>gc` - Git Commit
- `<leader>gp` - Git Push
- `<leader>gl` - Git Pull

### Diff & History
- `<leader>gd` - Open Diffview (see all changes)
- `<leader>gD` - Close Diffview
- `<leader>gh` - File History (current file)
- `<leader>gH` - File History (all files)

### Git Blame & Hunks
- `<leader>gb` - Toggle Git Blame (shows who wrote each line)
- `]c` - Next git hunk (change)
- `[c` - Previous git hunk (change)

### Hunk Operations (in normal mode)
- `<leader>hs` - Stage hunk
- `<leader>hr` - Reset hunk
- `<leader>hS` - Stage entire buffer/file
- `<leader>hR` - Reset entire buffer/file
- `<leader>hp` - Preview hunk
- `<leader>hu` - Undo stage hunk
- `<leader>hb` - Show blame for current line

## VSCode-like Workflow

### 1. View Changes (like VSCode Source Control)
Press `<leader>gg` to open Neogit. You'll see:
- **Untracked files** - new files not in git
- **Unstaged changes** - modified files
- **Staged changes** - files ready to commit
- **Recent commits** - commit history

### 2. Stage Files
In the Neogit window:
- Move cursor to a file with `j`/`k`
- Press `s` to **stage** the file
- Press `u` to **unstage** the file
- Press `Tab` to expand/collapse sections
- Press `=` to see the diff

### 3. Stage Hunks (partial staging)
For staging parts of a file:
- Open the file in normal vim
- Navigate to the change you want
- Press `<leader>hs` to stage just that hunk
- Or visually select lines and press `<leader>hs`

### 4. Commit
**Option A: From Neogit**
- In Neogit window, press `c` then `c` again
- Write commit message in the buffer
- Press `Ctrl-c` twice (or `:wq`) to confirm commit

**Option B: Quick commit**
- Press `<leader>gc` from anywhere
- Write commit message
- Confirm

### 5. Push
**Option A: From Neogit**
- In Neogit window, press `p` then `p`

**Option B: Quick push**
- Press `<leader>gp` from anywhere

### 6. Pull
- In Neogit: press `F` then `p`
- Or press `<leader>gl` from anywhere

## Neogit Navigation & Commands

When in Neogit window (`<leader>gg`):

### Navigation
- `j`/`k` - Move up/down
- `Tab` - Expand/collapse section
- `Enter` - Open file
- `=` - Toggle diff view

### Staging
- `s` - Stage file/hunk
- `u` - Unstage file/hunk
- `S` - Stage all
- `U` - Unstage all

### Commits
- `c` then `c` - Commit
- `c` then `a` - Commit amend
- `c` then `e` - Commit extend

### Push/Pull
- `p` then `p` - Push
- `F` then `p` - Pull
- `f` then `f` - Fetch

### Other
- `r` - Refresh
- `q` - Close Neogit
- `?` - Show help (all keybindings)

## Diffview Commands

### In Diffview (`<leader>gd`)
- `Tab` - Next file
- `Shift-Tab` - Previous file
- `-` - Toggle stage/unstage file
- `S` - Stage all
- `U` - Unstage all
- `q` - Close diffview

### File History (`<leader>gh`)
- Shows all commits that modified current file
- `Enter` - View changes from that commit
- `j`/`k` - Navigate commits
- `Tab`/`Shift-Tab` - Switch between commits

## Gitsigns (Inline Git Decorations)

You'll see symbols in the gutter:
- `│` - Added lines
- `~` - Changed lines
- `_` - Deleted lines
- `┆` - Untracked lines

### Hunk Navigation
- `]c` - Jump to next change
- `[c` - Jump to previous change

### Quick Actions
- `<leader>hp` - Preview hunk (see diff in popup)
- `<leader>hs` - Stage this hunk
- `<leader>hr` - Reset this hunk (discard changes)
- `<leader>hb` - Show blame for line

## Tips

1. **Start with `<leader>gg`** - this is your main git interface
2. **Stage hunks for partial commits** - use `<leader>hs` to stage specific changes
3. **Use `=` in Neogit** to quickly see diffs
4. **Press `?` in Neogit** for help with all available commands
5. **Toggle blame with `<leader>gb`** to see who wrote what
6. **Use `<leader>gh`** to see history of current file

## Example Workflow

```
1. Edit some files
2. Press <leader>gg to open git status
3. Navigate with j/k to files
4. Press s to stage files
5. Press c then c to commit
6. Write message, save with :wq
7. Press p then p to push
8. Press q to close
```

Or the quick way:
```
1. Edit files
2. <leader>gc to commit
3. <leader>gp to push
```

## Troubleshooting

If you get errors about missing plugins:
1. Open Neovim
2. Run `:PlugInstall`
3. Restart Neovim

If keybindings don't work, check what `<leader>` is set to:
- Run `:echo mapleader` in Neovim
- It's probably `\` or space
