fish_vi_key_bindings
set -gx VISUAL "vim"

set -x LESS_TERMCAP_md (printf "\e[01;31m")
set -x LESS_TERMCAP_md (printf "\e[01;31m")
set -x LESS_TERMCAP_me (printf "\e[0m")
set -x LESS_TERMCAP_se (printf "\e[0m")
set -x LESS_TERMCAP_so (printf "\e[01;44;33m")
set -x LESS_TERMCAP_ue (printf "\e[0m")
set -x LESS_TERMCAP_us (printf "\e[01;32m")

set -gx PATH $PATH "~/.local/bin"
set -gx PATH $PATH "~/.mos/bin"
set -gx GOPATH $GOPATH $HOME"/Code/go"
# source ~/.autoenv/activate.fish
# status --is-login; and status --is-interactive; and exec byobu-launcher
