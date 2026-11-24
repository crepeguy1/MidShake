# Self-Compilation Bootstrap

This folder contains all the tools, examples, and code needed to make MidShake self-compiling — a MidShake compiler written in MidShake.

## Goal

Build a tokenizer, parser, and eventually a compiler entirely in MidShake (`.mish` files), so the language can compile itself without relying on the Python implementation.

## Current Progress: ~95% (All 5 Phases Complete)

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
- **Recursive AST-building parser**: `parser.mish` (941 lines) reads source code and builds a full AST with nested maps. Recursively parses body lines into child AST nodes for all block statements (IF, WHILST, DEFINE, FOR). Includes pretty-printer with indentation for visualizing the AST.
- **AST interpreter**: `interpreter.mish` walks the AST produced by `parser.mish` and executes it. Supports LET, SET, PROCLAIM, IF, WHILST, DEFINE, CALL, RETURN, FileWrite, FOR, BREAK, CONTINUE, TERMINATE, and IMPORT.
- **C++ code generator**: `codegen.mish` (823 lines) converts the AST produced by `parser.mish` into C++ source code. Handles LET, SET, PROCLAIM, IF/ELSE, WHILST, DEFINE, CALL, RETURN, FOR, BREAK, CONTINUE, TERMINATE, FileWrite, and Import.
- **Semantic analyzer**: `semantic.mish` (277 lines) — self-hosted semantic analysis with symbol table, type inference, and error detection. Python version (`python/midshake_semantic.py`, 721 lines) provides full two-pass analysis with scope resolution.
- **Formal grammar**: BNF/EBNF grammar specification in `docs/grammar.md`
- **Test suite**: 171 passing tests (146 unit + 15 integration + 10 skipped)

### What's Still Needed

1. **✓ Self-hosted compiler binary** — `codegen.mish` compiled to `cpp/output/codegen.exe` via the Python compiler
2. **✓ Bootstrap chain** — codegen.exe compiles simple programs (functions.mish, conditionals.mish) → valid C++ → compiles and runs
3. **✓ Binary expression compilation** — `X plus Y` and `X minus Y` handling in compileExpr
4. **✓ Recursive condition compilation** — compileCondition compiles sub-expressions to C++
5. **✓ IF/ELSE handling** — Parser collects ELSE bodies, codegen generates C++ else branches
6. **✓ TERMINATE fix** — Generates `return 0;` instead of `return Value::from_double(0);`
7. **✓ Semantic analyzer import resolution** — Self-host globals and stdlib functions recognized
8. **✓ Self-compiling demo** — `minicodegen.mish` (~300 lines) compiles itself end-to-end, generating 51 lines of C++
9. **~ Full self-compilation** — codegen.exe compiling itself hangs (self-hosted parser limitation with 800+ line files)
10. **Replace C++ runtime** — Implement runtime functions in MidShake so compiled programs don't need external C++

### Known Limitations

- **Self-hosted parser**: Hangs on files with 800+ lines due to the deep-copy scope model making it difficult to share mutable state (g_pos, g_lines) across CALL boundaries in the WHILST parse loop
- **Array index formatting**: C++ code generation prints array indices as floats (`args[0.000000]` instead of `args[0]`)
- **Full self-compilation**: Requires rewriting the self-hosted parser to avoid CALL boundaries for shared state

## Folder Structure

```
selfhost/
├── README.md              ← This file
├── ROADMAP.md             ← Detailed roadmap to self-compilation
├── tokenizer.mish         ← Line-based tokenizer written in MidShake
├── lexer.mish             ← Character-level lexer written in MidShake
├── parser.mish            ← AST-building parser written in MidShake (941 lines)
├── interpreter.mish       ← AST interpreter written in MidShake
├── semantic.mish          ← Semantic analyzer written in MidShake (277 lines)
├── codegen.mish           ← C++ code generator written in MidShake (823 lines)
├── minicodegen.mish       ← Minimal self-compiling demo (~300 lines, compiles itself)
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
- **Parser g_pos fix** — parseStatement now always advances g_pos for non-block statements, preventing infinite loops on unrecognized lines
- **GLOBAL SET for g_myAst** — The AST accumulation in the parse loop uses GLOBAL SET so nodes persist across CALL boundaries

The next milestones are:

1. **✓ Compile the self-hosted codegen** — `codegen.mish` compiled to `cpp/output/codegen.exe` via the Python compiler (2700+ lines of C++)
2. **✓ Bootstrap chain** — codegen.exe compiles functions.mish and conditionals.mish → valid C++ → compiles and runs
3. **✓ IF/ELSE handling** — Parser collects ELSE bodies, codegen generates C++ else branches
4. **✓ TERMINATE fix** — Generates `return 0;` instead of `return Value::from_double(0);`
5. **~ Full self-compilation** — Fix the self-hosted parser to handle 800+ line files so codegen.exe can compile itself
6. **Replace C++ runtime** — Implement runtime functions in MidShake so compiled programs don't need external C++

### Key fixes in this phase:
- **Binary expression compilation** — compileExpr now handles `X plus Y` and `X minus Y` patterns recursively
- **Recursive condition compilation** — compileCondition compiles left/right sub-expressions to C++ instead of passing raw strings
- **Condition THEN stripping** — Fixed condition parsing to strip trailing `THEN` keywords
- **CLI compile pipeline** — Fixed include paths so `midshake compile` links against the correct runtime (`selfhost/runtime/`)
- **IF/ELSE body collection** — Parser now collects ELSE bodies into separate AST field
- **C++ else branch generation** — Codegen generates `} else {` when ELSE body exists
- **Function deduplication** — Later function definitions override imported ones
- **Map literal keys** — Bare identifiers treated as string literals in map literals
