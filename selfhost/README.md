# Self-Compilation Bootstrap

This folder contains all the tools, examples, and code needed to make MidShake self-compiling — a MidShake compiler written in MidShake.

## Goal

Build a tokenizer, parser, and eventually a compiler entirely in MidShake (`.mish` files), so the language can compile itself without relying on the Python implementation.

## Current Progress: ~85%

### What's Done ✓

- **Data structures**: Lists, maps, string operations (length, trim, substring, charAt, split, join, replace)
- **Math helpers**: min, max, abs, round
- **Character utilities**: isDigit, isLetter, isWhitespace, toupper, tolower, startsWith, endsWith
- **File I/O**: Read and write files from MidShake programs
- **Control flow**: `FOR...IN...DO` loops, `BREAK`, `CONTINUE`
- **Booleans**: `true`/`false` literals
- **Map mutation**: `SET the key K IN the map M TO the value V`
- **Global state**: `GLOBAL SET` enables functions to modify shared state across recursive calls
- **Recursion support**: Functions can call themselves (deep copy of variable environment)
- **Line-based tokenizer**: `tokenizer.mish` reads source code and classifies each line by keyword type
- **Character-level lexer**: `lexer.mish` walks source code character by character and produces tokens
- **Recursive AST-building parser**: `parser.mish` reads source code and builds a full AST with nested maps. Recursively parses body lines into child AST nodes for all block statements (IF, WHILST, DEFINE, FOR). Includes pretty-printer with indentation for visualizing the AST.
- **AST interpreter**: `interpreter.mish` walks the AST produced by `parser.mish` and executes it. Supports LET, SET, PROCLAIM, IF, WHILST, DEFINE, CALL, RETURN, FileWrite, FOR, BREAK, CONTINUE, TERMINATE, and IMPORT. Includes expression normalization to handle concatenated keywords (e.g., "thestring" → "the string").

### What's Still Needed

1. **Interpreter CALL argument handling** — The parser needs to store CALL arguments in the AST so the interpreter can properly bind them to function parameters
2. **Code generator in MidShake** — Write a MidShake program (`generator.mish`) that converts the AST to C++ source code

## Folder Structure

```
selfhost/
├── README.md              ← This file
├── ROADMAP.md             ← Detailed roadmap to self-compilation
├── tokenizer.mish         ← Line-based tokenizer written in MidShake
├── lexer.mish             ← Character-level lexer written in MidShake
├── parser.mish            ← AST-building parser written in MidShake
├── interpreter.mish       ← AST interpreter written in MidShake
├── examples/
│   ├── fileio.mish        ← File read/write example
│   ├── lists.mish         ← List operations example
│   ├── maps.mish          ← Map operations example
│   ├── strings.mish       ← String manipulation example
│   ├── stringutils.mish   ← Character-level string utils example
│   └── math.mish          ← Math helper functions example
├── compiler/
│   └── midshake_compiler.py  ← Python C++ code generator (reference implementation)
├── runtime/
│   ├── midshake_runtime.hpp       ← C++ runtime header
│   ├── midshake_runtime.cpp       ← C++ runtime implementation
│   ├── midshake_runtime_types.hpp ← C++ type definitions
│   └── stdlib.hpp                 ← C++ standard library bindings
└── tools/
    └── midshake_highlight.py  ← Syntax highlighter for MidShake code
```

## How to Run

Run the tokenizer on a MidShake file:
```bash
python python/midshake_cli.py run selfhost/tokenizer.mish
```

Run any of the examples:
```bash
python python/midshake_cli.py run selfhost/examples/fileio.mish
python python/midshake_cli.py run selfhost/examples/math.mish
python python/midshake_cli.py run selfhost/examples/stringutils.mish
```

## Next Steps

The recursive AST-building parser and interpreter are complete. The parser correctly builds ASTs with proper node types, names, and values. The interpreter successfully executes simple MidShake programs (like hello.mish) by walking the AST and evaluating expressions. Key improvements include global state variables (GLOBAL SET) for surviving deep-copy scope restoration, inline map access for reading AST node fields, and expression normalization. The next milestones are:

1. **Fix interpreter CALL argument handling** — The parser now stores CALL arguments in the AST, but the interpreter needs to properly parse and bind them to function parameters so function calls work correctly.
2. **Code generator in MidShake** — Write a MidShake program (`generator.mish`) that converts the AST to C++ source code, enabling MidShake to compile itself to native code.
