# MidShake

MidShake is a self-hosting programming language with a compiler written in MidShake itself. It features a complete compilation pipeline: lexer, parser, semantic analyzer, and C++ code generator — all implemented in both Python and MidShake. The language is designed to be readable, beginner-friendly, and academically rigorous.

## Overview

MidShake programs are plain text files with the `.mish` extension. The language supports variables, conditionals, loops, functions, classes, module visibility, collections (lists and maps), file I/O, and a standard library. The compiler performs five phases: tokenization, parsing, semantic analysis, code generation, and native compilation.

## Example

```MidShake
PROCLAIM the string "Hello, World!";
```

## Quick Start

### Option 1: Standalone Executable (No Installation)

Download `midshake.exe` from the [latest release](https://github.com/crepeguy1/MidShake/releases) and place it in the MidShake directory. No Python or g++ required:

```bash
# Run a program (interpreter — no C++ needed)
midshake.exe run examples/hello.mish

# Check for type errors (no C++ needed)
midshake.exe check examples/functions.mish

# View tokens, AST, or syntax-highlighted code
midshake.exe tokens examples/hello.mish
midshake.exe ast examples/functions.mish
midshake.exe highlight examples/hello.mish
```

### Option 2: Build from Source

**Prerequisites:**
- **Python 3.8+** — for the reference compiler and CLI
- **g++ (GCC 8+ or MinGW)** — only needed for `midshake compile` to build native binaries

```bash
# Clone the repository
git clone https://github.com/crepeguy1/MidShake.git
cd MidShake

# The Python compiler requires no installation — just run it directly
python python/midshake_cli.py --help

# Verify g++ is available (only needed for compilation)
g++ --version
```

### Run a Program

```bash
# Interpret and run directly (no C++ needed)
python python/midshake_cli.py run examples/hello.mish

# Or compile to native binary first (requires g++)
python python/midshake_cli.py compile examples/hello.mish
./build/output/hello.exe
```

### No C++? No Problem

Most MidShake commands work **without g++ or C++**:

| Command | Needs g++? | Description |
|---------|-----------|-------------|
| `run` | ❌ No | Runs programs via built-in interpreter |
| `check` | ❌ No | Semantic analysis and type checking |
| `tokens` | ❌ No | Show tokenized output |
| `ast` | ❌ No | Show parsed AST |
| `highlight` | ❌ No | Syntax-highlighted code |
| `compile` | ✅ Yes | Generates C++ and compiles to native binary |

### Compile the Self-Hosted Compiler

The self-hosted compiler (`selfhost/codegen.mish`) is written in MidShake and can be compiled using the Python reference compiler:

```bash
# Compile the self-hosted code generator to a standalone binary
python python/midshake_cli.py compile selfhost/codegen.mish

# The compiled binary can compile MidShake programs without Python
./build/output/codegen.exe examples/functions.mish
```

### Self-Compilation Chain

```
Python compiler → compiles codegen.mish → codegen.exe → compiles MidShake programs → C++ → g++ → native binary
```

See [docs/demo.md](docs/demo.md) for a detailed walkthrough of the self-compilation process.

## CLI Commands

Use either the standalone `midshake.exe` or the Python CLI:

```bash
# Standalone executable (no Python needed)
midshake.exe <command> [args]

# Or Python CLI
python python/midshake_cli.py <command> [args]
```

| Command | Needs g++? | Description | Example |
|---------|-----------|-------------|---------|
| `run` | ❌ No | Interpret and run a `.mish` file | `midshake.exe run examples/hello.mish` |
| `compile` | ✅ Yes | Compile to C++ and build native binary | `midshake.exe compile examples/functions.mish` |
| `check` | ❌ No | Run semantic analysis (type checking) | `midshake.exe check examples/functions.mish` |
| `tokens` | ❌ No | Show tokenized output | `midshake.exe tokens examples/full.mish` |
| `ast` | ❌ No | Show parsed AST | `midshake.exe ast examples/functions.mish` |
| `highlight` | ❌ No | Show syntax-highlighted code | `midshake.exe highlight examples/hello.mish` |
| `version` | ❌ No | Show version | `midshake.exe version` |
| `help` | ❌ No | Show help | `midshake.exe help` |

### Self-Hosted Compiler

The self-hosted compiler is written in MidShake and lives in `selfhost/`. It includes:

- `parser.mish` — AST-building parser
- `codegen.mish` — C++ code generator
- `interpreter.mish` — AST interpreter
- `lexer.mish` / `tokenizer.mish` — Character-level lexer

To compile the self-hosted compiler:

```bash
python python/midshake_cli.py compile selfhost/codegen.mish
./build/output/codegen.exe examples/functions.mish

# Verify the complete native bootstrap chain
python tools/bootstrap.py
```

The bootstrap builds a Python-seeded compiler, recompiles it twice natively,
compares both generated compiler sources, compiles `selfhost/parser.mish` with
both native generations and checks their output matches, then runs the scope,
class, module-visibility, and exception-handling regressions.
All generated artifacts are isolated under the ignored `build/` directory.

### Running Tests

```bash
# Run all unit and integration tests (196 active, 10 skipped)
python tests/run_tests.py

# Run specific test categories
python tests/test_lexer.py      # 52 lexer unit tests
python tests/test_parser.py     # 63 parser unit tests
python tests/test_codegen.py    # 36 codegen unit tests
```

## Language Features

- **Variables** — LET, SET, GLOBAL SET with dynamic typing
- **Control flow** — IF/THEN/ELSE, WHILST loops, FOR IN loops, BREAK, CONTINUE
- **Exceptions** — `TRY`/`CATCH` and `THROW`, with propagation through function calls
- **Functions** — DEFINE with parameters, CALL with arguments, RETURN
- **Classes** — Single inheritance, constructors, and Public/Private/Protected members
- **Modules** — Public/Private declarations with enforced imported-symbol access
- **Collections** — Lists and maps with literals and operations
- **String operations** — length, substring, split, join, replace, trim, startsWith, and more
- **Math functions** — min, max, abs, round
- **File I/O** — Read and write files
- **User input** — INQUIRE for interactive prompts
- **Imports** — Modular code with IMPORT
- **Semantic analysis** — Symbol table, type inference, scope resolution, error detection
- **Self-hosted compiler** — Parser and code generator written in MidShake
- **Standard library** — `stdlib.mish` with utility functions

## Documentation

- [Syntax Guide](docs/syntax.md) — Language syntax with examples
- [Formal Grammar](docs/grammar.md) — BNF/EBNF grammar specification
- [Type System](docs/types.md) — Dynamic type system and coercion rules
- [Language Reference](docs/language-reference.md) — Complete construct reference
- [Semantic Analysis](docs/semantic-analysis.md) — Symbol table and type inference
- [Design Document](docs/design.md) — Architecture and design decisions
- [Project Roadmap](docs/roadmap.md) — Development phases and milestones
- [Demo Walkthrough](docs/demo.md) — Self-compilation process demonstration
- [Examples](examples/) — Example programs
- [Standard Library](stdlib/stdlib.mish) — Built-in utility functions
- [Tests](tests/) — Unit/integration suite plus skipped cases

## Project Structure

```text
MidShake/
    python/            # Reference compiler (Python)
        midshake_tokenizer.py    # Lexer/tokenizer
        midshake_parser.py       # AST parser
        midshake_semantic.py     # Semantic analyzer
        midshake_compiler.py     # C++ code generator
        midshake_runtime.py      # Runtime execution
        midshake_cli.py          # CLI entry point
    selfhost/          # Self-hosted compiler (MidShake)
        parser.mish            # AST parser in MidShake
        codegen.mish           # C++ code generator in MidShake
        interpreter.mish       # AST interpreter in MidShake
        lexer.mish / tokenizer.mish
    cpp/               # Legacy C++ runtime sources
    selfhost/runtime/  # C++ runtime for self-hosted compiler
    stdlib/            # Standard library
        stdlib.mish            # Built-in utility functions
    examples/          # Example MidShake programs
    docs/              # Documentation
    tests/             # Test suite (196 active + 10 skipped)
        run_tests.py           # Test runner
        test_lexer.py          # Lexer unit tests (52)
        test_parser.py         # Parser unit tests (63)
        test_codegen.py        # Codegen unit tests (36)
        *.mish                 # Integration test files (22)
    ide/               # IDE syntax highlighting (VS Code, IntelliJ, Vim, Sublime)
    bindings/          # pybind11 bindings
    tools/             # Developer utilities
```

## Compiler Pipeline

```
Source (.mish)
    ↓
[1] Tokenization → Tokens
    ↓
[2] Parsing → AST
    ↓
[3] Semantic Analysis → Type-checked AST
    ↓
[4] Code Generation → C++ source
    ↓
[5] Native Compilation (g++) → Executable
```

## Self-Compilation Status

The self-hosted compiler (`selfhost/codegen.mish`) can compile MidShake programs to C++ without Python. `python tools/bootstrap.py` verifies that the native compiler reproduces itself:

```
Python compiler → compiles codegen.mish → codegen.exe → compiles MidShake programs → C++ → g++ → native binary
```

See [docs/demo.md](docs/demo.md) for the full self-compilation walkthrough.

## Other info
I have had AI help me in the creation of this language due to some skill limitations

## License

MidShake is released under the MIT License. See the `LICENSE` file for details.
