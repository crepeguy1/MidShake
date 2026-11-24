#!/usr/bin/env python3
"""
MidShake Syntax Highlighter
Tokenizes MidShake source code and applies ANSI color codes for terminal display.
"""

import re

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


# MidShake keywords and phrases
STATEMENT_KEYWORDS = [
    "LET", "SET", "PROCLAIM", "IF", "WHILST", "DEFINE", "CALL",
    "RETURN", "IMPORT", "TERMINATE", "INQUIRE", "BREAK", "CONTINUE",
    "FOR", "END", "THEN", "DO"
]

BLOCK_KEYWORDS = [
    "END FUNCTION", "END WHILST", "END IF", "ELSE", "END FOR"
]

EXPRESSION_PREFIXES = [
    "the value of", "the string", "the number", "the variable",
    "the content of the file", "the length of", "the trimmed",
    "the substring of", "the character at", "the split of",
    "the join of", "the size of", "the item at position",
    "the append of", "the minimum of", "the maximum of",
    "the absolute value of", "the rounded value of",
    "the uppercase of", "the lowercase of",
    "the check if", "the response", "RESPONSE",
    "plus", "minus", "times", "divided by",
    "IS", "equal to", "not equal to", "less than", "greater than",
    "and", "or", "not",
    "WITH", "BE", "IN", "TO", "STARTING AT", "ENDING AT",
    "STARTS WITH", "ENDS WITH", "IS DIGIT", "IS LETTER", "IS WHITESPACE"
]

BUILT_IN_FUNCTIONS = [
    "min", "max", "abs", "round", "toupper", "tolower",
    "startsWith", "endsWith", "isDigit", "isLetter", "isWhitespace",
    "length", "charAt", "substring", "split", "join", "trim",
    "size", "append", "getItem", "mapSet", "readFile"
]

OPERATORS = ["+", "-", "*", "/", "=", "<", ">", "!", ";", ",", ":", ".", "#"]


def highlight(source):
    """
    Apply syntax highlighting to MidShake source code.
    Returns a string with ANSI color codes.
    """
    lines = source.split("\n")
    result_lines = []
    
    for line in lines:
        result_lines.append(highlight_line(line))
    
    return "\n".join(result_lines)


def highlight_line(line):
    """
    Highlight a single line of MidShake code.
    """
    # Handle empty lines
    if not line.strip():
        return line
    
    # Handle comment lines
    stripped = line.lstrip()
    if stripped.startswith("^") or stripped.startswith("#"):
        return f"{Colors.DIM}{Colors.WHITE}{line}{Colors.RESET}"
    
    # Tokenize the line
    tokens = tokenize_line(line)
    
    # Build colored output
    result = ""
    for token_type, token_text in tokens:
        color = get_color_for_token(token_type, token_text)
        result += f"{color}{token_text}{Colors.RESET}"
    
    return result


def tokenize_line(line):
    """
    Simple tokenizer that breaks a line into (type, text) pairs.
    """
    tokens = []
    i = 0
    length = len(line)
    
    while i < length:
        # Skip whitespace (preserve it)
        if line[i].isspace():
            start = i
            while i < length and line[i].isspace():
                i += 1
            tokens.append(("WHITESPACE", line[start:i]))
            continue
        
        # String literals
        if line[i] == '"':
            start = i
            i += 1
            while i < length and line[i] != '"':
                if line[i] == '\\':
                    i += 1  # Skip escaped character
                i += 1
            if i < length:
                i += 1  # Include closing quote
            tokens.append(("STRING", line[start:i]))
            continue
        
        # Numbers
        if line[i].isdigit() or (line[i] == '.' and i + 1 < length and line[i + 1].isdigit()):
            start = i
            while i < length and (line[i].isdigit() or line[i] == '.'):
                i += 1
            tokens.append(("NUMBER", line[start:i]))
            continue
        
        # Operators and punctuation
        if line[i] in "+-*/=<>!;,:.":
            tokens.append(("OPERATOR", line[i]))
            i += 1
            continue
        
        # Words (keywords, identifiers, etc.)
        if line[i].isalpha() or line[i] == '_':
            start = i
            while i < length and (line[i].isalnum() or line[i] == '_'):
                i += 1
            word = line[start:i]
            tokens.append(("WORD", word))
            continue
        
        # Hash/comment character
        if line[i] == '#':
            tokens.append(("COMMENT", line[i]))
            i += 1
            continue
        
        # Caret comment
        if line[i] == '^':
            # Rest of line is comment
            tokens.append(("COMMENT", line[i:]))
            i = length
            continue
        
        # Unknown character
        tokens.append(("UNKNOWN", line[i]))
        i += 1
    
    return tokens


def get_color_for_token(token_type, token_text):
    """
    Determine the ANSI color for a token.
    """
    if token_type == "WHITESPACE":
        return ""  # No color change
    
    if token_type == "COMMENT":
        return f"{Colors.DIM}{Colors.WHITE}"
    
    if token_type == "STRING":
        return Colors.GREEN
    
    if token_type == "NUMBER":
        return Colors.BRIGHT_YELLOW
    
    if token_type == "OPERATOR":
        if token_text == ";":
            return f"{Colors.DIM}{Colors.WHITE}"
        return Colors.BRIGHT_GREEN
    
    if token_type == "WORD":
        upper = token_text.upper()
        
        # Statement keywords
        if upper in STATEMENT_KEYWORDS:
            return f"{Colors.BOLD}{Colors.MAGENTA}"
        
        # Block keywords (check multi-word separately)
        if upper in ["END", "ELSE"]:
            return f"{Colors.BOLD}{Colors.YELLOW}"
        
        # Boolean literals
        if upper in ["TRUE", "FALSE"]:
            return f"{Colors.BOLD}{Colors.BRIGHT_BLUE}"
        
        # Expression prefixes (common ones)
        if token_text.lower() in ["the", "of", "is", "be", "in", "to", "with", "then", "do"]:
            return f"{Colors.BOLD}{Colors.CYAN}"
        
        # Built-in function names
        if token_text.lower() in [f.lower() for f in BUILT_IN_FUNCTIONS]:
            return f"{Colors.BOLD}{Colors.BRIGHT_CYAN}"
        
        # Variables (capitalized words that aren't keywords)
        if token_text[0].isupper():
            return Colors.BRIGHT_CYAN
        
        # Regular identifiers
        return Colors.WHITE
    
    if token_type == "UNKNOWN":
        return Colors.DIM
    
    return Colors.WHITE


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python midshake_highlight.py <file.mish>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        colored = highlight(source)
        sys.stdout.write(colored)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
