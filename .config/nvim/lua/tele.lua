-- Safely require telescope
local status_ok, builtin = pcall(require, 'telescope.builtin')
if not status_ok then
  return
end

vim.keymap.set('n', '<leader>fg', function()
  builtin.live_grep({
    find_command = {'rg', '--ignore', '--hidden', '--files'},
    prompt_prefix = ' search:  '
  })
end, {})

vim.keymap.set('n', '<leader>ff', function()
  builtin.find_files({
    find_command = {'rg', '--ignore', '--hidden', '--files'},
    prompt_prefix = ' search:  '
  })
end, {})

vim.keymap.set('n', '<leader>fb', function()
  builtin.buffers({
    find_command = {'rg', '--ignore', '--hidden', '--files'},
    prompt_prefix = ' search:  '
  })
end, {})

vim.keymap.set('n', '<leader>fh', function()
  builtin.help_tags({
    find_command = {'rg', '--ignore', '--hidden', '--files'},
    prompt_prefix = ' search:  '
  })
end, {})
