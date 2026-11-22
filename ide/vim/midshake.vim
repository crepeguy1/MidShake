"MidShake syntax file for Vim/Neovim
" Place this file in: ~/.vim/syntax/midshake.vim or ~/.config/nvim/syntax/midshake.vim
" Then add to your vimrc/nvim init.vim:
"   au BufRead,BufNewFile *.mish,*.ms setfiletype midshake
"   filetype plugin indent on

if exists("b:current_syntax")
  finish
endif

" Comments
syn region midshakeComment start="\^" end="$" containedin=ALL contained transparent
syn match midshakeComment /\^.*$/
syn match midshakeHashComment /#.*$/

" Strings
syn region midshakeString start='"' end='"' contains=midshakeEscape

" Escape sequences inside strings
syn match midshakeEscape /\\./ contained

" Booleans
syn keyword midshakeBoolean true false

" Block keywords
syn keyword midshakeBlockKeyword IF THEN WHILST DO DEFINE FUNCTION WITH IMPORT RETURN TERMINATE BREAK CONTINUE
syn match midshakeBlockKeyword /END\s\+IF/
syn match midshakeBlockKeyword /END\s\+WHILST/
syn match midshakeBlockKeyword /END\s\+FUNCTION/
syn match midshakeBlockKeyword /END\s\+FOR/

" Statement keywords
syn keyword midshakeStatementKeyword LET BE SET TO PROCLAIM CALL INQUIRE FOR IN

" Expression prefixes
syn match midshakeExpression /the\s\+value\s\+of/
syn match midshakeExpression /the\s\+variable/
syn match midshakeExpression /the\s\+number/
syn match midshakeExpression /the\s\+string/
syn match midshakeExpression /the\s\+length\s\+of/
syn match midshakeExpression /the\s\+trimmed/
syn match midshakeExpression /the\s\+size\s\+of/
syn match midshakeExpression /the\s\+item\s\+at/
syn match midshakeExpression /the\s\+character\s\+at/
syn match midshakeExpression /the\s\+substring\s\+of/
syn match midshakeExpression /the\s\+append\s\+of/
syn match midshakeExpression /the\s\+join\s\+of/
syn match midshakeExpression /the\s\+split\s\+of/
syn match midshakeExpression /the\s\+minimum\s\+of/
syn match midshakeExpression /the\s\+maximum\s\+of/
syn match midshakeExpression /the\s\+absolute\s\+of/
syn match midshakeExpression /the\s\+round\s\+of/
syn match midshakeExpression /the\s\+upper\s\+case\s\+of/
syn match midshakeExpression /the\s\+lower\s\+case\s\+of/
syn match midshakeExpression /the\s\+content\s\+of\s\+the\s\+file/
syn match midshakeExpression /the\s\+RESPONSE/
syn match midshakeExpression /the\s\+check\s\+if/

" Built-in functions
syn keyword midshakeBuiltin startsWith endsWith isDigit isLetter isWhitespace min max abs round toupper tolower length charAt substring split join trim size append getItem mapSet mapGet readFile

" Arithmetic operators
syn keyword midshakeArithmeticOperator plus minus times modulo
syn match midshakeArithmeticOperator /divided\s\+by/

" Comparison operators
syn match midshakeComparisonOperator /IS\s\+greater\s\+than/
syn match midshakeComparisonOperator /IS\s\+less\s\+than/
syn match midshakeComparisonOperator /IS\s\+equal\s\+to/
syn match midshakeComparisonOperator /IS\s\+not\s\+equal\s\+to/
syn match midshakeComparisonOperator /IS\s\+greater\s\+than\s\+or\s\+equal\s\+to/
syn match midshakeComparisonOperator /IS\s\+less\s\+than\s\+or\s\+equal\s\+to/

" Logical operators
syn keyword midshakeLogicalOperator AND OR NOT

" Symbolic operators
syn match midshakeSymbolicOperator /[+\-*/=<>!]/

" Numbers
syn match midshakeFloat /\b\d\+\.\d\+\b/
syn match midshakeNumber /\b\d\+\b/

" Variable type keywords
syn keyword midshakeVariableType variable value number string key map list

" Punctuation
syn match midshakeTerminator /;/
syn match midshakeSeparator /[,\[\]{}()]/

" Highlighting groups
hi def link midshakeComment Comment
hi def link midshakeHashComment Comment
hi def link midshakeString String
hi def link midshakeEscape SpecialChar
hi def link midshakeBoolean Boolean
hi def link midshakeBlockKeyword Keyword
hi def link midshakeStatementKeyword Statement
hi def link midshakeExpression Type
hi def link midshakeBuiltin Function
hi def link midshakeArithmeticOperator Operator
hi def link midshakeComparisonOperator Operator
hi def link midshakeLogicalOperator Operator
hi def link midshakeSymbolicOperator Operator
hi def link midshakeFloat Float
hi def link midshakeNumber Number
hi def link midshakeVariableType Type
hi def link midshakeTerminator Delimiter
hi def link midshakeSeparator Delimiter

b:current_syntax = "midshake"
