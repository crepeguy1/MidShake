# MidShake v0.1.0 — Self-Compilation Prototype

**Release Date:** November 23, 2026

---

## Overview

MidShake is a self-hosting programming language with a complete compilation pipeline: lexer, parser, semantic analyzer, and C++ code generator — all implemented in both Python and MidShake itself. This release marks the first stable version with formal grammar, type checking, a comprehensive test suite, and a working self-hosted compiler.

**Key Achievement:** The self-hosted compiler (`codegen.mish`) can compile MidShake programs to native C++ without Python, and a minimal compiler (`minicodegen.mish`) can compile itself end-to-end, proving the self-compilation concept.

---

## What's New

### Language Formalization (Phase 1)
- **Formal BNF/EBNF grammar** — `docs/grammar.md` defines the complete lexical and syntax grammar
- **Type system documentation** — `docs/types.md` describes 6 built-in types (Number, String, Boolean, List, Map, Response), dynamic type inference, and coercion rules
- **Language reference manual** — `docs/language-reference.md` covers all 16 statement types, 30+ expression types, and standard library functions

### Semantic Analysis (Phase 2)
- **Symbol table** — Tracks variable declarations, function definitions, and scope resolution across nested scopes
- **Type inference** — Automatically infers types for all expression types
- **Error detection** — Catches undeclared variables, duplicate declarations, SET without LET, undefined functions, RETURN outside function, BREAK/CONTINUE outside loop
- **CLI integration** — `midshake check <file>` for standalone type checking
- **Self-hosted version** — `selfhost/semantic.mish` (277 lines) with symbol table and type inference

### Self-Compilation (Phase 3)
- **Bootstrap chain works** — Python compiler → compiles `codegen.mish` → `codegen.exe` → compiles MidShake programs → valid C++
- **Self-compiling demo** — `minicodegen.mish` (~300 lines) compiles itself, generating 51 lines of C++
- **IF/ELSE support** — Parser collects ELSE bodies, codegen generates C++ else branches
- **Binary expression compilation** — `X plus Y` and `X minus Y` compile to C++ operators
- **Function deduplication** — Later function definitions override imported ones
- **Map literal keys** — Bare identifiers treated as string literals in map literals

### Test Suite (Phase 4)
- **161 passing tests** — 146 unit tests + 15 integration tests, 0 failures
- **Lexer tests** — 52 tests covering all token types
- **Parser tests** — 63 tests covering all AST node types
- **Codegen tests** — 31 tests verifying C++ output correctness
- **Integration tests** — 15 `.mish` files covering all language constructs
- **Semantic error tests** — 5 intentional errors correctly detected

### Documentation (Phase 5)
- **Design document** — `docs/design.md` explains architecture, deep-copy scope model, and self-compilation strategy
- **Demo walkthrough** — `docs/demo.md` shows the self-compilation process with command output evidence
- **Project roadmap** — `docs/roadmap.md` tracks all 5 completed phases
- **IDE support** — Syntax highlighting for VS Code, IntelliJ, Vim, and Sublime Text

---

## Language Features

| Feature | Status |
|---------|--------|
| Variables (LET/SET/GLOBAL SET) | ✓ |
| Arithmetic (+, -, *, /) | ✓ |
| Comparisons (equal to, greater than, etc.) | ✓ |
| Conditionals (IF/THEN/ELSE) | ✓ |
| While loops (WHILST/DO) | ✓ |
| For-in loops (FOR/IN/DO) | ✓ |
| Loop control (BREAK, CONTINUE) | ✓ |
| Functions (DEFINE/CALL/RETURN) | ✓ |
| String operations (length, substring, split, join, replace, trim, indexOf) | ✓ |
| String checks (startsWith, endsWith, isDigit, isLetter) | ✓ |
| Math functions (min, max, abs, round) | ✓ |
| Lists (literals, get, append, size) | ✓ |
| Maps (literals, get, set) | ✓ |
| File I/O (read, write) | ✓ |
| Imports (IMPORT) | ✓ |
| User input (INQUIRE) | ✓ |
| Type checking | ✓ |
| Formal grammar | ✓ |
| Self-hosted compiler | ✓ (partial) |

---

## Compiler Status

| Component | Python | Self-Hosted (.mish) |
|-----------|--------|---------------------|
| Lexer/Tokenizer | ✓ | ✓ |
| Parser (AST) | ✓ | ✓ (941 lines) |
| Semantic Analysis | ✓ | ✓ (277 lines) |
| Interpreter | ✓ | ~ (partial) |
| C++ Code Generator | ✓ | ~ (823 lines) |
| Test Suite | ✓ (161 tests) | — |

---

## Quick Start

### Prerequisites
- **Python 3.8+** — for the reference compiler
- **g++ (GCC 8+ or MinGW)** — to compile generated C++

### Build and Run

```bash
# Clone and enter the repository
git clone https://github.com/crepeguy1/MidShake.git
cd MidShake

# Run a program directly
python python/midshake_cli.py run examples/hello.mish

# Compile to native binary
python python/midshake_cli.py compile examples/functions.mish
./cpp/output/functions.exe

# Check for type errors
python python/midshake_cli.py check examples/functions.mish

# Run all tests
python tests/run_tests.py
```

### Self-Hosted Compiler

```bash
# Compile the self-hosted compiler
python python/midshake_cli.py compile selfhost/codegen.mish

# Use it to compile a MidShake program
./cpp/output/codegen.exe examples/functions.mish
```

---

## Example Program

```midshake
^ A simple MidShake program
LET the variable greeting BE the string "Hello, World!";
PROCLAIM the value of greeting;
```

**Output:**
```
Hello, World!
```

---

## Known Limitations

1. **Full self-compilation** — The self-hosted parser hangs on files with 800+ lines due to the deep-copy scope model. The self-compiling demo (`minicodegen.mish`) works for files up to ~200 lines.
2. **Array index formatting** — C++ code generation prints array indices as floats (`args[0.000000]` instead of `args[0]`).
3. **Import resolution** — The semantic analyzer does not follow IMPORT statements to analyze imported files, which may cause false "undefined function" errors for imported functions.
4. **Self-hosted interpreter** — The interpreter works for simple programs but has limitations with complex nested function calls.

---

## Project Structure

```
MidShake/
├── python/              # Reference compiler (Python)
│   ├── midshake_tokenizer.py
│   ├── midshake_parser.py
│   ├── midshake_semantic.py
│   ├── midshake_compiler.py
│   ├── midshake_runtime.py
│   └── midshake_cli.py
├── selfhost/            # Self-hosted compiler (MidShake)
│   ├── parser.mish
│   ├── codegen.mish
│   ├── minicodegen.mish
│   ├── semantic.mish
│   ├── interpreter.mish
│   └── runtime/         # C++ runtime for self-hosted output
├── stdlib/
│   └── stdlib.mish      # Standard library
├── examples/            # Example programs
├── tests/               # Test suite (161 tests)
├── docs/                # Documentation
├── ide/                 # IDE syntax highlighting
└── cpp/                 # C++ output directory
```

---

## Documentation

- [Syntax Guide](docs/syntax.md) — Language syntax with examples
- [Formal Grammar](docs/grammar.md) — BNF/EBNF specification
- [Type System](docs/types.md) — Dynamic typing and coercion
- [Language Reference](docs/language-reference.md) — Complete construct reference
- [Semantic Analysis](docs/semantic-analysis.md) — Symbol table and type inference
- [Design Document](docs/design.md) — Architecture and decisions
- [Project Roadmap](docs/roadmap.md) — Development phases
- [Demo Walkthrough](docs/demo.md) — Self-compilation demonstration

---

## Test Results

```
Unit Tests:
  ✓ Lexer: 52/52 passed
  ✓ Parser: 63/63 passed
  ✓ Codegen: 31/31 passed

Integration Tests:
  ✓ 15/15 passed (collections, GLOBAL SET, IF/ELSE, CONTINUE,
    function calls, imports, maps, recursion, etc.)

Semantic Analysis:
  ✓ 5/5 errors correctly detected

Total: 161 passed, 0 failed, 10 skipped
```

---

## License

MidShake is released under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

This project was developed as a demonstration of compiler construction principles, including lexer/parser design, semantic analysis, code generation, and the self-compilation (bootstrapping) process.
