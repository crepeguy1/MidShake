# Self-Compilation Bootstrap

This folder contains all the tools, examples, and code needed to make MidShake self-compiling — a MidShake compiler written in MidShake.

## Goal

Maintain a tokenizer, parser, and compiler in MidShake (`.mish` files), so native compiler generations can be rebuilt without relying on Python after the seed.

## Current Progress: Native Bootstrap Verified

### What's Done ✓

- **Data structures**: Lists, maps, string operations (length, trim, substring, charAt, split, join, replace)
- **Math helpers**: min, max, abs, round
- **Character utilities**: isDigit, isLetter, isWhitespace, toupper, tolower, startsWith, endsWith
- **File I/O**: Read and write files from MidShake programs
- **Control flow**: `FOR...IN...DO` loops, `BREAK`, `CONTINUE`
- **Booleans**: `true`/`false` literals
- **Map mutation**: `SET the key K IN the map M TO the value V`
- **Global state**: `GLOBAL SET` enables functions to modify shared state across recursive calls
- **Recursion support**: Functions use parent-linked local environment frames and can call themselves
- **Line-based tokenizer**: `tokenizer.mish` reads source code and classifies each line by keyword type
- **Character-level lexer**: `lexer.mish` walks source code character by character and produces tokens
- **Recursive AST-building parser**: `parser.mish` reads source code and builds a full AST with nested maps. Recursively parses body lines into child AST nodes for block statements, including IF, WHILST, DEFINE, FOR, and TRY/CATCH.
- **AST interpreter**: `interpreter.mish` walks the AST produced by `parser.mish` and executes it. Supports LET, SET, PROCLAIM, IF, WHILST, DEFINE, CALL, RETURN, FileWrite, FOR, BREAK, CONTINUE, TERMINATE, and IMPORT.
- **C++ code generator**: `codegen.mish` converts the AST produced by `parser.mish` into C++ source code, including recursive imports, module-level visibility, class access control, base-constructor forwarding, local function frames, global updates, and exception handling.
- **Semantic analyzer**: `semantic.mish` (277 lines) — self-hosted semantic analysis with symbol table, type inference, and error detection. Python version (`python/midshake_semantic.py`, 721 lines) provides full two-pass analysis with scope resolution.
- **Formal grammar**: BNF/EBNF grammar specification in `docs/grammar.md`
- **Exceptions**: Python and native backends support `TRY`/`CATCH`, `THROW`, and propagation through function calls.
- **Test suite**: 206 total (174 unit + 22 integration + 10 skipped)

### Bootstrap Verification

`python tools/bootstrap.py` builds the Python seed, compiles the self-hosted compiler, rebuilds it natively, and compares both native generations. It also compiles `parser.mish` with each native generation, checks that their generated C++ matches, builds and runs the result, and verifies scope, classes, base-constructor forwarding, imported-module privacy, and exception propagation. Build artifacts are written under the ignored `build/` directory.

### Runtime Requirement

Native output currently links against `selfhost/runtime/` and requires a C++17 compiler. The bootstrap verifies the compiler generations, parser compilation, and exception behavior, but does not yet replace the shared runtime with MidShake code.

## Folder Structure

```
selfhost/
├── README.md              ← This file
├── ROADMAP.md             ← Detailed roadmap to self-compilation
├── tokenizer.mish         ← Line-based tokenizer written in MidShake
├── lexer.mish             ← Character-level lexer written in MidShake
├── parser.mish            ← AST-building parser written in MidShake
├── interpreter.mish       ← AST interpreter written in MidShake
├── semantic.mish          ← Semantic analyzer written in MidShake (277 lines)
├── codegen.mish           ← C++ code generator written in MidShake
├── fixtures/              ← Imported-module visibility regression programs
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

## Remaining Work

- Reduce dependence on the shared C++ runtime and provide a standalone native runtime distribution.
- Bring the self-hosted interpreter and semantic analyzer to parity with their Python implementations.
- Extend expression and module-analysis coverage with regression tests as the language evolves.
