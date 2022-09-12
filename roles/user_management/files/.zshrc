export SHELL=$(which zsh)

autoload -Uz compinit
compinit

autoload -U select-word-style
select-word-style bash

bindkey -e

zstyle ':completion:*' menu select

setopt AUTO_CD
setopt COMPLETE_ALIASES

HISTFILE=$HOME/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt append_history
setopt extended_history
setopt hist_expire_dups_first
setopt hist_ignore_dups
setopt hist_ignore_space
setopt hist_verify
setopt inc_append_history
setopt share_history

if [ $commands[kubectl] ]; then
    source <(kubectl completion zsh)
fi

PROMPT='%(!.%S%B%F{red}%n%f%b%s.%F{cyan}%n%f)@%F{green}%m%f %F{yellow}%1~%f%b '
