-- Git integration configuration

-- Gitsigns setup (inline git decorations, staging, blame)
require('gitsigns').setup {
  signs = {
    add          = { text = '│' },
    change       = { text = '│' },
    delete       = { text = '_' },
    topdelete    = { text = '‾' },
    changedelete = { text = '~' },
    untracked    = { text = '┆' },
  },
  signcolumn = true,  -- Toggle with `:Gitsigns toggle_signs`
  numhl      = false, -- Toggle with `:Gitsigns toggle_numhl`
  linehl     = false, -- Toggle with `:Gitsigns toggle_linehl`
  word_diff  = false, -- Toggle with `:Gitsigns toggle_word_diff`
  watch_gitdir = {
    follow_files = true
  },
  attach_to_untracked = true,
  current_line_blame = false, -- Toggle with `:Gitsigns toggle_current_line_blame`
  current_line_blame_opts = {
    virt_text = true,
    virt_text_pos = 'eol', -- 'eol' | 'overlay' | 'right_align'
    delay = 1000,
    ignore_whitespace = false,
  },
  current_line_blame_formatter = '<author>, <author_time:%Y-%m-%d> - <summary>',
  sign_priority = 6,
  update_debounce = 100,
  status_formatter = nil, -- Use default
  max_file_length = 40000,
  preview_config = {
    -- Options passed to nvim_open_win
    border = 'single',
    style = 'minimal',
    relative = 'cursor',
    row = 0,
    col = 1
  },
  on_attach = function(bufnr)
    local gs = package.loaded.gitsigns

    local function map(mode, l, r, opts)
      opts = opts or {}
      opts.buffer = bufnr
      vim.keymap.set(mode, l, r, opts)
    end

    -- Navigation between hunks
    map('n', ']c', function()
      if vim.wo.diff then return ']c' end
      vim.schedule(function() gs.next_hunk() end)
      return '<Ignore>'
    end, {expr=true, desc = 'Next git hunk'})

    map('n', '[c', function()
      if vim.wo.diff then return '[c' end
      vim.schedule(function() gs.prev_hunk() end)
      return '<Ignore>'
    end, {expr=true, desc = 'Previous git hunk'})

    -- Actions
    map('n', '<leader>hs', gs.stage_hunk, {desc = 'Stage hunk'})
    map('n', '<leader>hr', gs.reset_hunk, {desc = 'Reset hunk'})
    map('v', '<leader>hs', function() gs.stage_hunk {vim.fn.line('.'), vim.fn.line('v')} end, {desc = 'Stage hunk'})
    map('v', '<leader>hr', function() gs.reset_hunk {vim.fn.line('.'), vim.fn.line('v')} end, {desc = 'Reset hunk'})
    map('n', '<leader>hS', gs.stage_buffer, {desc = 'Stage buffer'})
    map('n', '<leader>hu', gs.undo_stage_hunk, {desc = 'Undo stage hunk'})
    map('n', '<leader>hR', gs.reset_buffer, {desc = 'Reset buffer'})
    map('n', '<leader>hp', gs.preview_hunk, {desc = 'Preview hunk'})
    map('n', '<leader>hb', function() gs.blame_line{full=true} end, {desc = 'Blame line'})
    map('n', '<leader>tb', gs.toggle_current_line_blame, {desc = 'Toggle line blame'})
    map('n', '<leader>hd', gs.diffthis, {desc = 'Diff this'})
    map('n', '<leader>hD', function() gs.diffthis('~') end, {desc = 'Diff this ~'})
    map('n', '<leader>td', gs.toggle_deleted, {desc = 'Toggle deleted'})

    -- Text object
    map({'o', 'x'}, 'ih', ':<C-U>Gitsigns select_hunk<CR>', {desc = 'Select hunk'})
  end
}

-- Neogit setup (main git interface)
local neogit = require('neogit')
neogit.setup {
  disable_signs = false,
  disable_hint = false,
  disable_context_highlighting = false,
  disable_commit_confirmation = false,
  -- Neogit refreshes its internal state after specific events, which can be expensive depending on the repository size.
  -- Disabling `auto_refresh` will make it so you have to manually refresh the status after you open it.
  auto_refresh = true,
  disable_builtin_notifications = false,
  use_magit_keybindings = false,
  -- Change the default way of opening neogit
  kind = "tab",
  -- The time after which an output console is shown for slow running commands
  console_timeout = 2000,
  -- Automatically show console if a command takes more than console_timeout milliseconds
  auto_show_console = true,
  -- Persist the values of switches/options within and across sessions
  remember_settings = true,
  -- Scope persisted settings on a per-project basis
  use_per_project_settings = true,
  -- Array-like table of settings to never persist. Uses format "Filetype--cli-value"
  --   ie: `{ "NeogitCommitPopup--author", "NeogitCommitPopup--no-verify" }`
  ignored_settings = {},
  -- Change the default way of opening the commit popup
  commit_popup = {
    kind = "split",
  },
  -- Change the default way of opening popups
  popup = {
    kind = "split",
  },
  -- customize displayed signs
  signs = {
    -- { CLOSED, OPENED }
    section = { ">", "v" },
    item = { ">", "v" },
    hunk = { "", "" },
  },
  integrations = {
    diffview = true  -- Enable diffview integration
  },
  -- Setting any section to `false` will make the section not render at all
  sections = {
    untracked = {
      folded = false
    },
    unstaged = {
      folded = false
    },
    staged = {
      folded = false
    },
    stashes = {
      folded = true
    },
    unpulled = {
      folded = true
    },
    unmerged = {
      folded = false
    },
    recent = {
      folded = true
    },
  },
}

-- Diffview setup
require('diffview').setup {
  diff_binaries = false,    -- Show diffs for binaries
  enhanced_diff_hl = false, -- See ':h diffview-config-enhanced_diff_hl'
  git_cmd = { "git" },      -- The git executable followed by default args.
  use_icons = true,         -- Requires nvim-web-devicons
  icons = {                 -- Only applies when use_icons is true.
    folder_closed = "",
    folder_open = "",
  },
  signs = {
    fold_closed = "",
    fold_open = "",
  },
  file_panel = {
    listing_style = "tree",             -- One of 'list' or 'tree'
    tree_options = {                    -- Only applies when listing_style is 'tree'
      flatten_dirs = true,              -- Flatten dirs that only contain one single dir
      folder_statuses = "only_folded",  -- One of 'never', 'only_folded' or 'always'.
    },
    win_config = {                      -- See ':h diffview-config-win_config'
      position = "left",
      width = 35,
    },
  },
  file_history_panel = {
    log_options = {   -- See ':h diffview-config-log_options'
      git = {
        single_file = {
          diff_merges = "combined",
        },
        multi_file = {
          diff_merges = "first-parent",
        },
      },
    },
    win_config = {    -- See ':h diffview-config-win_config'
      position = "bottom",
      height = 16,
    },
  },
  commit_log_panel = {
    win_config = {},  -- See ':h diffview-config-win_config'
  },
  default_args = {    -- Default args prepended to the arg-list for the listed commands
    DiffviewOpen = {},
    DiffviewFileHistory = {},
  },
  hooks = {},         -- See ':h diffview-config-hooks'
  keymaps = {
    disable_defaults = false, -- Disable the default keymaps
    view = {
      -- The `view` bindings are active in the diff buffers, only when the current
      -- tabpage is a Diffview.
      ["<tab>"]      = require('diffview.actions').select_next_entry,         -- Open the diff for the next file
      ["<s-tab>"]    = require('diffview.actions').select_prev_entry,         -- Open the diff for the previous file
      ["gf"]         = require('diffview.actions').goto_file,                 -- Open the file in a new split in the previous tabpage
      ["<C-w><C-f>"] = require('diffview.actions').goto_file_split,           -- Open the file in a new split
      ["<C-w>gf"]    = require('diffview.actions').goto_file_tab,             -- Open the file in a new tabpage
      ["<leader>e"]  = require('diffview.actions').focus_files,               -- Bring focus to the file panel
      ["<leader>b"]  = require('diffview.actions').toggle_files,              -- Toggle the file panel.
    },
    file_panel = {
      ["j"]             = require('diffview.actions').next_entry,         -- Bring the cursor to the next file entry
      ["<down>"]        = require('diffview.actions').next_entry,
      ["k"]             = require('diffview.actions').prev_entry,         -- Bring the cursor to the previous file entry.
      ["<up>"]          = require('diffview.actions').prev_entry,
      ["<cr>"]          = require('diffview.actions').select_entry,       -- Open the diff for the selected entry.
      ["o"]             = require('diffview.actions').select_entry,
      ["<2-LeftMouse>"] = require('diffview.actions').select_entry,
      ["-"]             = require('diffview.actions').toggle_stage_entry, -- Stage / unstage the selected entry.
      ["S"]             = require('diffview.actions').stage_all,          -- Stage all entries.
      ["U"]             = require('diffview.actions').unstage_all,        -- Unstage all entries.
      ["X"]             = require('diffview.actions').restore_entry,      -- Restore entry to the state on the left side.
      ["R"]             = require('diffview.actions').refresh_files,      -- Update stats and entries in the file list.
      ["L"]             = require('diffview.actions').open_commit_log,    -- Open the commit log panel.
      ["<c-b>"]         = require('diffview.actions').scroll_view(-0.25), -- Scroll the view up
      ["<c-f>"]         = require('diffview.actions').scroll_view(0.25),  -- Scroll the view down
      ["<tab>"]         = require('diffview.actions').select_next_entry,
      ["<s-tab>"]       = require('diffview.actions').select_prev_entry,
      ["gf"]            = require('diffview.actions').goto_file,
      ["<C-w><C-f>"]    = require('diffview.actions').goto_file_split,
      ["<C-w>gf"]       = require('diffview.actions').goto_file_tab,
      ["i"]             = require('diffview.actions').listing_style,        -- Toggle between 'list' and 'tree' views
      ["f"]             = require('diffview.actions').toggle_flatten_dirs,  -- Flatten empty subdirectories in tree listing style.
      ["<leader>e"]     = require('diffview.actions').focus_files,
      ["<leader>b"]     = require('diffview.actions').toggle_files,
    },
    file_history_panel = {
      ["g!"]            = require('diffview.actions').options,          -- Open the option panel
      ["<C-A-d>"]       = require('diffview.actions').open_in_diffview, -- Open the entry under the cursor in a diffview
      ["y"]             = require('diffview.actions').copy_hash,        -- Copy the commit hash of the entry under the cursor
      ["L"]             = require('diffview.actions').open_commit_log,
      ["zR"]            = require('diffview.actions').open_all_folds,
      ["zM"]            = require('diffview.actions').close_all_folds,
      ["j"]             = require('diffview.actions').next_entry,
      ["<down>"]        = require('diffview.actions').next_entry,
      ["k"]             = require('diffview.actions').prev_entry,
      ["<up>"]          = require('diffview.actions').prev_entry,
      ["<cr>"]          = require('diffview.actions').select_entry,
      ["o"]             = require('diffview.actions').select_entry,
      ["<2-LeftMouse>"] = require('diffview.actions').select_entry,
      ["<c-b>"]         = require('diffview.actions').scroll_view(-0.25),
      ["<c-f>"]         = require('diffview.actions').scroll_view(0.25),
      ["<tab>"]         = require('diffview.actions').select_next_entry,
      ["<s-tab>"]       = require('diffview.actions').select_prev_entry,
      ["gf"]            = require('diffview.actions').goto_file,
      ["<C-w><C-f>"]    = require('diffview.actions').goto_file_split,
      ["<C-w>gf"]       = require('diffview.actions').goto_file_tab,
      ["<leader>e"]     = require('diffview.actions').focus_files,
      ["<leader>b"]     = require('diffview.actions').toggle_files,
    },
    option_panel = {
      ["<tab>"] = require('diffview.actions').select_entry,
      ["q"]     = require('diffview.actions').close,
    },
  },
}

-- Key mappings for git operations
local map = vim.keymap.set

-- Neogit mappings
map('n', '<leader>gg', '<cmd>Neogit<CR>', { desc = 'Open Neogit (Git Status)' })
map('n', '<leader>gc', '<cmd>Neogit commit<CR>', { desc = 'Git Commit' })
map('n', '<leader>gp', '<cmd>Neogit push<CR>', { desc = 'Git Push' })
map('n', '<leader>gl', '<cmd>Neogit pull<CR>', { desc = 'Git Pull' })

-- Diffview mappings
map('n', '<leader>gd', '<cmd>DiffviewOpen<CR>', { desc = 'Open Diffview' })
map('n', '<leader>gD', '<cmd>DiffviewClose<CR>', { desc = 'Close Diffview' })
map('n', '<leader>gh', '<cmd>DiffviewFileHistory %<CR>', { desc = 'File History (current file)' })
map('n', '<leader>gH', '<cmd>DiffviewFileHistory<CR>', { desc = 'File History (all)' })

-- Gitsigns mappings (git blame toggle)
map('n', '<leader>gb', '<cmd>Gitsigns toggle_current_line_blame<CR>', { desc = 'Toggle Git Blame' })
