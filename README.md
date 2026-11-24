# MidShake

MidShake is a self-hosting programming language with a compiler written in MidShake itself. It features a complete compilation pipeline: lexer, parser, semantic analyzer, and C++ code generator — all implemented in both Python and MidShake. The language is designed to be readable, beginner-friendly, and academically rigorous.

## Overview

MidShake programs are plain text files with the `.mish` extension. The language supports variables, conditionals, loops, functions, collections (lists and maps), file I/O, and a standard library. The compiler performs five phases: tokenization, parsing, semantic analysis, code generation, and native compilation.

## Example

```MidShake
PROCLAIM the string "Hello, World!";
```

## Quick Start

### Prerequisites

- **Python 3.8+** — for the reference compiler and CLI
- **g++ (GCC 8+ or MinGW)** — to compile generated C++ into native binaries
- No other dependencies are required

### Build from Source

```bash
# Clone the repository
git clone https://github.com/crepeguy1/MidShake.git
cd MidShake

# The Python compiler requires no installation — just run it directly
python python/midshake_cli.py --help

# Verify g++ is available
g++ --version
```

### Run a Program

```bash
# Interpret and run directly
python python/midshake_cli.py run examples/hello.mish

# Or compile to native binary first
python python/midshake_cli.py compile examples/hello.mish
./cpp/output/hello.exe
```

### Compile the Self-Hosted Compiler

The self-hosted compiler (`selfhost/codegen.mish`) is written in MidShake and can be compiled using the Python reference compiler:

```bash
# Compile the self-hosted code generator to a standalone binary
python python/midshake_cli.py compile selfhost/codegen.mish

# The compiled binary can compile MidShake programs without Python
./cpp/output/codegen.exe examples/functions.mish
```

### Self-Compilation Chain

```
Python compiler → compiles codegen.mish → codegen.exe → compiles MidShake programs → C++ → g++ → native binary
```

See [docs/demo.md](docs/demo.md) for a detailed walkthrough of the self-compilation process.

## CLI Commands

All commands are run through the Python CLI:

```bash
python python/midshake_cli.py <command> [args]
```

| Command | Description | Example |
|---------|-------------|---------|
| `run` | Interpret and run a `.mish` file | `python python/midshake_cli.py run examples/hello.mish` |
| `compile` | Compile to C++ and build native binary | `python python/midshake_cli.py compile examples/functions.mish` |
| `check` | Run semantic analysis (type checking) | `python python/midshake_cli.py check examples/functions.mish` |
| `tokens` | Show tokenized output | `python python/midshake_cli.py tokens examples/full.mish` |
| `ast` | Show parsed AST | `python python/midshake_cli.py ast examples/functions.mish` |
| `version` | Show version | `python python/midshake_cli.py version` |
| `help` | Show help | `python python/midshake_cli.py help` |

### Self-Hosted Compiler

The self-hosted compiler is written in MidShake and lives in `selfhost/`. It includes:

- `parser.mish` — AST-building parser (941 lines)
- `codegen.mish` — C++ code generator (819 lines)
- `interpreter.mish` — AST interpreter
- `lexer.mish` / `tokenizer.mish` — Character-level lexer

To compile the self-hosted compiler:

```bash
python python/midshake_cli.py compile selfhost/codegen.mish
./cpp/output/codegen.exe examples/functions.mish
```

### Running Tests

```bash
# Run all unit and integration tests (161 tests)
python tests/run_tests.py

# Run specific test categories
python tests/test_lexer.py      # 52 lexer unit tests
python tests/test_parser.py     # 63 parser unit tests
python tests/test_codegen.py    # 31 codegen unit tests
```

## Language Features

- **Variables** — LET, SET, GLOBAL SET with dynamic typing
- **Control flow** — IF/THEN/ELSE, WHILST loops, FOR IN loops, BREAK, CONTINUE
- **Functions** — DEFINE with parameters, CALL with arguments, RETURN
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
- [Tests](tests/) — 161 unit and integration tests

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
    cpp/               # C++ runtime and compiled output
    selfhost/runtime/  # C++ runtime for self-hosted compiler
    stdlib/            # Standard library
        stdlib.mish            # Built-in utility functions
    examples/          # Example MidShake programs
    docs/              # Documentation
    tests/             # Test suite (161 tests)
        run_tests.py           # Test runner
        test_lexer.py          # Lexer unit tests (52)
        test_parser.py         # Parser unit tests (63)
        test_codegen.py        # Codegen unit tests (31)
        *.mish                 # Integration test files (15)
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

The self-hosted compiler (`selfhost/codegen.mish`) can compile MidShake programs to C++ without Python:

```
Python compiler → compiles codegen.mish → codegen.exe → compiles MidShake programs → C++ → g++ → native binary
```

See [docs/demo.md](docs/demo.md) for the full self-compilation walkthrough.

## License

MidShake is released under the MIT License. See the `LICENSE` file for details.
