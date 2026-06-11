#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return


alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias vim='nvim'
PS1='[\u@\h \W]\$ '

export GDK_SCALE=1
export GDK_DPI_SCALE=1.0
export TERMINAL=wezterm


eval "$(fzf --bash)"

export FZF_DEFAULT_OPTS="
  --height 40%
  --layout=reverse
  --border
  --inline-info
  --color=fg:#dcdcdc,bg:#303030,hl:#9ab8d7
  --color=fg+:#ffffff,bg+:#6a6a6a,hl+:#94BFF3
  --color=info:#dfaf8f,prompt:#dc8cc3,pointer:#60b48a
  --color=marker:#72D5A3,spinner:#8cd0d3,header:#9ab8d7
"

# FZF commands using fd for better performance
if command -v fd &> /dev/null; then
  export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
  export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
  export FZF_ALT_C_COMMAND='fd --type directory --hidden --follow --exclude .git .'
fi

export FZF_CTRL_T_OPTS="
  --preview 'if file -b --mime-type {} | grep -q \"^image/\"; then chafa -f sixel -s \${FZF_PREVIEW_COLUMNS}x\${FZF_PREVIEW_LINES} --work=9 --preprocess=off {}; else bat --color=always --style=numbers --line-range=:500 {} 2> /dev/null || cat {} 2> /dev/null || tree -C {} 2> /dev/null; fi'
  --preview-window right:50%:wrap
"

export FZF_CTRL_R_OPTS="
  --preview 'echo {}'
  --preview-window down:3:hidden:wrap
  --bind '?:toggle-preview'
"

export FZF_ALT_C_OPTS="
  --preview 'tree -C {} | head -200'
  --preview-window right:50%
"

# Image browser function using fzf
img() {
  local dir="${1:-.}"
  fd -e jpg -e jpeg -e png -e gif -e bmp -e webp -e svg . "$dir" | \
  fzf --preview 'chafa -f sixel -s ${FZF_PREVIEW_COLUMNS}x${FZF_PREVIEW_LINES} --work=9 --preprocess=off {}' \
      --preview-window=right:70% \
      --bind 'enter:execute(xdg-open {} &)'
}

export PATH="$HOME/.local/apps/usr/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"
export XDG_DATA_DIRS="$HOME/.local/apps/usr/share:/home/khai/.local/share:$XDG_DATA_DIRS"

