# midshake_highlight.py
#
# Syntax highlighter for MidShake code.
# Colorizes source code using ANSI escape codes for terminal output.
# Also provides the keyword/phrase lists used by the VS Code grammar.

# ------------------------------------------------------------
# ANSI Color Codes
# ------------------------------------------------------------
class Colors:
    RESET     = "\033[0m"
    BOLD      = "\033[1m"
    DIM       = "\033[2m"
    
    # Foreground colors
    RED       = "\033[31m"
    GREEN     = "\033[32m"
    YELLOW    = "\033[33m"
    BLUE      = "\033[34m"
    MAGENTA   = "\033[35m"
    CYAN      = "\033[36m"
    WHITE     = "\033[37m"
    BRIGHT_RED    = "\033[91m"
    BRIGHT_GREEN  = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE   = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN   = "\033[96m"

# ------------------------------------------------------------
# Keyword and phrase definitions
# ------------------------------------------------------------

# Top-level statement keywords (exact match at start of statement)
STATEMENT_KEYWORDS = {
    "PROCLAIM",
    "LET",
    "SET",
    "INQUIRE",
    "IF",
    "WHILST",
    "DEFINE",
    "CALL",
    "RETURN",
    "ELSE",
    "END IF",
    "END WHILST",
    "END FUNCTION",
    "TERMINATE",
    "IN",
}

# Block-level structural keywords
BLOCK_KEYWORDS = {
    "THEN",
    "DO",
    "BE",
    "TO",
    "WITH",
    "FOR",
    "function",
    "the program",
    "WRITE",
    "the file",
}

# Expression prefixes
EXPR_PREFIXES = [
    "the value of",
    "the number",
    "the string",
    "the RESPONSE",
    "the length of",
    "the size of",
    "the index of",
    "the element at index",
    "the item at position",
    "the character at",
    "the substring of",
    "the split of",
    "the join of",
    "the trim of",
    "the minimum of",
    "the maximum of",
    "the absolute value of",
    "the round of",
    "the rounded value of",
    "the upper case of",
    "the lower case of",
    "the starts with",
    "the ends with",
    "the is digit",
    "the is letter",
    "the is whitespace",
    "the content of the file",
    "the write to file",
    "the list",
    "the map",
    "the key",
    "the variables",
    "the append of",
]

# Arithmetic and comparison operators
OPERATORS = {
    "plus",
    "minus",
    "times",
    "divided",
    "modulo",
    "multiplied by",
    "IS greater than",
    "IS less than",
    "IS equal to",
    "IS not equal to",
    "IS greater than or equal to",
    "IS less than or equal to",
    "or equal to",
    "and",
    "or",
    "not",
}

# Built-in function names from stdlib
BUILTIN_FUNCTIONS = {
    "println",
    "greet",
    "add_and_print",
    "repeat",
    "factorial",
    "fibonacci",
    "readFile",
    "min",
    "max",
    "abs",
    "round",
    "toupper",
    "tolower",
    "startsWith",
    "endsWith",
    "isDigit",
    "isLetter",
    "isWhitespace",
}

# ------------------------------------------------------------
# Tokenizer for syntax highlighting
# ------------------------------------------------------------

def tokenize_line(line):
    """
    Tokenize a single line of MidShake code into (text, kind) pairs.
    Kinds: keyword, block, expr, operator, function, string, number,
           comment, variable, punctuation, text
    """
    tokens = []
    i = 0
    length = len(line)
    
    while i < length:
        # Skip whitespace
        if line[i] in (' ', '\t'):
            start = i
            while i < length and line[i] in (' ', '\t'):
                i += 1
            tokens.append((line[start:i], 'whitespace'))
            continue
        
        # String literals
        if line[i] == '"':
            start = i
            i += 1
            while i < length and line[i] != '"':
                if line[i] == '\\':
                    i += 2  # skip escaped character
                else:
                    i += 1
            if i < length:
                i += 1  # include closing quote
            tokens.append((line[start:i], 'string'))
            continue
        
        # Numbers (integers and floats)
        if line[i].isdigit() or (line[i] == '.' and i + 1 < length and line[i+1].isdigit()):
            start = i
            while i < length and (line[i].isdigit() or line[i] == '.'):
                i += 1
            tokens.append((line[start:i], 'number'))
            continue
        
        # Semicolon
        if line[i] == ';':
            tokens.append((';', 'punctuation'))
            i += 1
            continue
        
        # Caret comment (whole remaining line)
        if line[i] == '^':
            tokens.append((line[i:], 'comment'))
            break
        
        # Hash comment (whole remaining line)
        if line[i] == '#':
            tokens.append((line[i:], 'comment'))
            break
        
        # Double-slash comment (whole remaining line)
        if line[i] == '/' and i + 1 < length and line[i+1] == '/':
            tokens.append((line[i:], 'comment'))
            break
        
        # Try to match multi-word phrases first (longest match wins)
        matched = False
        remaining = line[i:]
        
        # Check statement keywords (multi-word first)
        for kw in sorted(STATEMENT_KEYWORDS, key=len, reverse=True):
            if remaining.upper().startswith(kw.upper()):
                tokens.append((remaining[:len(kw)], 'keyword'))
                i += len(kw)
                matched = True
                break
        
        if matched:
            continue
        
        # Check block keywords
        for kw in sorted(BLOCK_KEYWORDS, key=len, reverse=True):
            if remaining.upper().startswith(kw.upper()):
                tokens.append((remaining[:len(kw)], 'block'))
                i += len(kw)
                matched = True
                break
        
        if matched:
            continue
        
        # Check expression prefixes (multi-word, longest first)
        for prefix in sorted(EXPR_PREFIXES, key=len, reverse=True):
            if remaining.lower().startswith(prefix.lower()):
                tokens.append((remaining[:len(prefix)], 'expr'))
                i += len(prefix)
                matched = True
                break
        
        if matched:
            continue
        
        # Check operators (multi-word, longest first)
        for op in sorted(OPERATORS, key=len, reverse=True):
            if remaining.lower().startswith(op.lower()):
                tokens.append((remaining[:len(op)], 'operator'))
                i += len(op)
                matched = True
                break
        
        if matched:
            continue
        
        # Check for function calls (word followed by '(')
        if line[i].isalpha():
            start = i
            while i < length and (line[i].isalnum() or line[i] == '_'):
                i += 1
            word = line[start:i]
            
            # Skip whitespace to check for '('
            j = i
            while j < length and line[j] == ' ':
                j += 1
            
            if j < length and line[j] == '(':
                # Check if it's a built-in function
                if word.lower() in {f.lower() for f in BUILTIN_FUNCTIONS}:
                    tokens.append((word, 'function'))
                else:
                    tokens.append((word, 'variable'))
            else:
                # Check if it looks like a variable name
                tokens.append((word, 'variable'))
            continue
        
        # Parentheses and brackets
        if line[i] in '()[]{}':
            tokens.append((line[i], 'punctuation'))
            i += 1
            continue
        
        # Commas
        if line[i] == ',':
            tokens.append((line[i], 'punctuation'))
            i += 1
            continue
        
        # Default: single character
        tokens.append((line[i], 'text'))
        i += 1
    
    return tokens


# ------------------------------------------------------------
# Color mapping
# ------------------------------------------------------------

def get_color(kind, use_color=True):
    """Return the ANSI color code for a token kind."""
    if not use_color:
        return Colors.RESET
    
    color_map = {
        'keyword':   Colors.BOLD + Colors.BRIGHT_MAGENTA,
        'block':     Colors.BOLD + Colors.BRIGHT_YELLOW,
        'expr':      Colors.BOLD + Colors.CYAN,
        'operator':  Colors.BOLD + Colors.BRIGHT_GREEN,
        'function':  Colors.BOLD + Colors.BRIGHT_BLUE,
        'string':    Colors.GREEN,
        'number':    Colors.BRIGHT_YELLOW,
        'comment':   Colors.DIM + Colors.WHITE,
        'variable':  Colors.BRIGHT_CYAN,
        'punctuation': Colors.DIM,
        'whitespace': Colors.RESET,
        'text':      Colors.RESET,
    }
    return color_map.get(kind, Colors.RESET)


# ------------------------------------------------------------
# Main highlight function
# ------------------------------------------------------------

def highlight(source, use_color=True):
    """
    Apply syntax highlighting to MidShake source code.
    
    Args:
        source: The MidShake source code string
        use_color: Whether to apply ANSI colors (default True)
    
    Returns:
        A string with ANSI color codes inserted
    """
    lines = source.split('\n')
    colored_lines = []
    
    for line in lines:
        tokens = tokenize_line(line)
        colored_parts = []
        
        for text, kind in tokens:
            if text.strip() == '' and kind == 'whitespace':
                colored_parts.append(text)
                continue
            
            color = get_color(kind, use_color)
            colored_parts.append(f"{color}{text}{Colors.RESET}")
        
        colored_lines.append(''.join(colored_parts))
    
    return '\n'.join(colored_lines)


# ------------------------------------------------------------
# CLI entry point
# ------------------------------------------------------------

def main():
    import sys
    import os
    
    if len(sys.argv) < 2:
        print("Usage: midshake_highlight.py <file.mish>")
        sys.exit(1)
    
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        sys.exit(1)
    
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    colored = highlight(source)
    print(colored)


if __name__ == "__main__":
    main()
