#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return


alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

export GDK_SCALE=1
export GDK_DPI_SCALE=1.0


eval "$(fzf --bash)"

export FZF_DEFAULT_OPTS="--bind 'enter:become(vim {}),ctrl-y:execute-silent(echo -n {} | xclip -selection clipboard)+abort'"
export FZF_CTRL_T_OPTS="
  --walker-skip .git,node_modules,target
  --preview 'bat -n --color=always {}'
  --bind 'ctrl-/:change-preview-window(down|hidden|)'"
export FZF_ALT_C_OPTS="
  --walker-skip .git,node_modules,target
  --preview 'tree -C {}'"
