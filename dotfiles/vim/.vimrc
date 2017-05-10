if &compatible
  set nocompatible
endif
set runtimepath+={.vim}

call dein#begin({path to plugin base path directory})

call dein#add({path to dein.vim directory})
call dein#add('Shougo/neocomplete.vim')
...

call dein#end()

filetype plugin indent on
syntax enable
