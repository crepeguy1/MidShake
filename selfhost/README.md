# Self-Compilation Bootstrap

This folder contains all the tools, examples, and code needed to make MidShake self-compiling — a MidShake compiler written in MidShake.

## Goal

Build a tokenizer, parser, and eventually a compiler entirely in MidShake (`.mish` files), so the language can compile itself without relying on the Python implementation.

## Current Progress: ~95% (Compiler Binary Working)

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
- **AST interpreter**: `interpreter.mish` walks the AST produced by `parser.mish` and executes it. Supports LET, SET, PROCLAIM, IF, WHILST, DEFINE, CALL, RETURN, FileWrite, FOR, BREAK, CONTINUE, TERMINATE, and IMPORT.
- **C++ code generator**: `codegen.mish` converts the AST produced by `parser.mish` into C++ source code. Handles LET, SET, PROCLAIM, IF, WHILST, DEFINE, CALL, RETURN, FOR, BREAK, CONTINUE, TERMINATE, FileWrite, and Import. Generates `#include`, function definitions, and a `main()` function that links against the C++ runtime.

### What's Still Needed

1. **~ Self-hosted compiler binary** ✓ — `codegen.mish` has been compiled to a standalone C++ binary (`cpp/output/codegen.exe`) that compiles MidShake → C++ without Python
2. **End-to-end self-compilation** — Run the self-hosted compiler on itself to produce a self-compiled MidShake
3. **Replace C++ runtime** — Implement runtime functions in MidShake so compiled programs don't need external C++

## Folder Structure

```
selfhost/
├── README.md              ← This file
├── ROADMAP.md             ← Detailed roadmap to self-compilation
├── tokenizer.mish         ← Line-based tokenizer written in MidShake
├── lexer.mish             ← Character-level lexer written in MidShake
├── parser.mish            ← AST-building parser written in MidShake
├── interpreter.mish       ← AST interpreter written in MidShake
├── codegen.mish           ← C++ code generator written in MidShake
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

The C++ code generator (`codegen.mish`) is now fully functional and verified end-to-end. It parses MidShake source code using the self-hosted parser, walks the AST, and generates C++ code that compiles and runs correctly. It correctly handles LET, SET, PROCLAIM, IF, WHILST, DEFINE, CALL, RETURN, FOR, BREAK, CONTINUE, TERMINATE, FileWrite, and Import. The generated C++ has been compiled with `g++` and executed successfully, producing correct output.

Key fixes that enabled this:
- **Tokenizer line joining fix** — `IF ... THEN` lines are now treated as standalone statements so the body on the next line isn't joined with the header, preventing CALL statements inside IF bodies from being swallowed
- **Scope propagation** — GLOBAL SET properly shares state (g_lines, g_pos, g_ast, g_params) across CALL boundaries between codegen.mish and parser.mish
- **Parameter name cleaning** — Trailing semicolons are stripped from function parameter names during parsing
- **String/int concatenation** — The `+` operator now auto-converts integers to strings when concatenating with strings
- **Compiler fixes** — Python compiler now handles string concatenation (`Value::operator+`), proper comparisons (`value_equals`), CALL RESPONSE storage, and map key literals

The next milestones are:

1. **~ Compile the self-hosted codegen** ✓ — `codegen.mish` has been compiled to `cpp/output/codegen.exe` via the Python compiler
2. **End-to-end self-compilation** — Run the self-hosted compiler on itself to produce a self-compiled MidShake
3. **Replace C++ runtime** — Implement runtime functions in MidShake so compiled programs don't need external C++
