# MidShake Self-Compilation Demo

This document demonstrates the MidShake self-compilation process — showing how a compiler written in MidShake can compile MidShake programs to native C++ code.

## Overview

MidShake features a complete compilation pipeline implemented in two ways:

1. **Python Reference Compiler** — The primary compiler written in Python
2. **Self-Hosted Compiler** — The same compiler written in MidShake itself

The self-compilation chain:

```
Python compiler → compiles codegen.mish → codegen.exe → compiles MidShake programs → C++ → g++ → native binary
```

## Prerequisites

- Python 3.8+
- g++ (GCC 8+ or MinGW on Windows)

## Step 1: Python Compiler — Hello World

The simplest MidShake program:

```MidShake
^ examples/hello.mish
PROCLAIM the string "Hello from MidShake!";
```

**Compile and run:**

```bash
python python/midshake_cli.py compile examples/hello.mish
./build/output/hello.exe
```

**Expected output:**
```
Hello from MidShake!
```

**What happens:**
1. Tokenizer converts source to tokens
2. Parser builds an AST (Abstract Syntax Tree)
3. Semantic analyzer checks types and variable declarations
4. Code generator produces C++ source
5. g++ compiles the C++ to a native executable

## Step 2: Python Compiler — Functions

A program with function definitions and calls:

```MidShake
^ examples/functions.mish
DEFINE function greet WITH the parameter name
    PROCLAIM the string "Hello, " + name;
END FUNCTION;

CALL greet WITH the string "adam";
```

**Compile and run:**

```bash
python python/midshake_cli.py compile examples/functions.mish
./build/output/functions.exe
```

**Expected output:**
```
Hello, adam
```

**What happens:**
- The parser recognizes `DEFINE function` and builds a `FunctionDef` AST node
- The code generator creates a C++ function with parameter binding
- `CALL` is compiled to a C++ function invocation
- String concatenation uses `Value::operator+`

## Step 3: Semantic Analysis

The semantic analyzer catches errors before compilation:

```MidShake
^ tests/test_semantic_errors.mish
^ (Intentional errors for demonstration)
PROCLAIM the value of undeclaredVar;      ^ Error: undeclared variable
SET the variable x TO the number 1;       ^ Error: SET without LET
LET the variable y BE the number 1;
LET the variable y BE the number 2;       ^ Error: duplicate declaration
```

**Run semantic analysis:**

```bash
python python/midshake_cli.py check tests/test_semantic_errors.mish
```

**Expected output:**
```
Semantic analysis found 5 errors:
  - Undeclared variable: undeclaredVar
  - SET without prior LET: x
  - Duplicate declaration: y
  - RETURN outside function
  - BREAK outside loop
```

**What happens:**
- Symbol table tracks all variable declarations and function definitions
- Type inference determines the type of every expression
- Scope resolution ensures variables are declared before use
- Context validation checks RETURN/BREAK/CONTINUE are in valid scope

## Step 4: Self-Hosted Compiler — Compilation

The self-hosted compiler (`selfhost/codegen.mish`) is written entirely in MidShake. It imports the self-hosted parser and generates C++ code.

**Compile the self-hosted compiler using the Python compiler:**

```bash
python python/midshake_cli.py compile selfhost/codegen.mish
```

**This produces:** `build/output/codegen.exe` — a standalone MidShake compiler binary.

**Compile a program using the self-hosted compiler:**

```bash
./build/output/codegen.exe examples/functions.mish
```

**Expected output:**
```
Compiling:
examples/functions.mish
Generated C++ code written to build/output/generated.cpp
Compilation complete!
```

**What happens:**
1. `codegen.exe` reads the source file
2. The self-hosted parser (`parser.mish`) builds an AST
3. The self-hosted code generator (`codegen.mish`) converts AST nodes to C++
4. The C++ is written to `build/output/generated.cpp`

## Step 5: Native Bootstrap Verification

Run the bootstrap verifier to build the Python seed, compile two native generations, compare their generated C++ source, compile `selfhost/parser.mish` with both native generations and compare the results, then test scope, classes, base-constructor forwarding, imported-module privacy, and exceptions:

```bash
python tools/bootstrap.py
```

The verifier stores binaries and intermediate generated source under `build/bootstrap/`.

## Step 6: Test Suite

MidShake currently has 206 test cases: 174 unit checks, 22 integration programs, and 10 skipped cases.

```bash
python tests/run_tests.py
```

**Expected output:**
```
=== Running Unit Tests ===
  Unit tests: 174 passed, 0 failed

=== MidShake Test Suite ===
Found 22 test files

=== Results ===
Unit tests: 174 passed, 0 failed
Integration tests: 22 passed, 0 failed
Skipped: 10
Total: 206 (196 ok, 0 failed, 10 skipped)
```

**Test breakdown:**
| Category | Tests | Coverage |
|----------|-------|----------|
| Lexer unit tests | 52 | All token types |
| Parser unit tests | 63 | All AST node types |
| Codegen unit tests | 36 | C++ output correctness |
| Visibility and exception unit tests | 23 | Encapsulation and exception semantics |
| Integration tests | 22 | End-to-end compilation |

## Architecture

The MidShake compiler follows a classic 5-phase pipeline:

```
Source (.mish)
    ↓
[1] Tokenization → Tokens (lexer)
    ↓
[2] Parsing → AST (recursive descent)
    ↓
[3] Semantic Analysis → Type-checked AST (symbol table)
    ↓
[4] Code Generation → C++ source (AST walker)
    ↓
[5] Native Compilation (g++) → Executable
```

### Lexical Environment Frames

The compiled native backend gives each function a local environment frame whose parent is the caller's environment. Local assignments stay in the current frame, lookups fall back through parent frames, and `GLOBAL SET` writes to the root frame. The Python interpreter snapshots and restores its call environment instead; both implementations preserve the same observable local, recursive, and global behavior.

## Compiler Components

| Component | Python | Self-Hosted |
|-----------|--------|-------------|
| Lexer/Tokenizer | `midshake_tokenizer.py` | `lexer.mish`, `tokenizer.mish` |
| Parser (AST) | `midshake_parser.py` | `parser.mish` |
| Semantic Analysis | `midshake_semantic.py` | `semantic.mish` (partial) |
| Interpreter | `midshake_runtime.py` | `interpreter.mish` (partial) |
| C++ Code Generator | `midshake_compiler.py` | `codegen.mish` |
| CLI | `midshake_cli.py` | — |

## Language Features

The compiler supports all of the following language constructs:

- **Variables**: `LET`, `SET`, `GLOBAL SET`
- **Literals**: Numbers, strings, lists, maps
- **Expressions**: Binary ops (`plus`, `minus`), string functions, math functions
- **Control flow**: `IF/THEN/ELSE`, `WHILST/DO`, `FOR/IN/DO`, `BREAK`, `CONTINUE`
- **Exceptions**: `TRY`/`CATCH` and `THROW`, with propagation through function calls
- **Functions**: `DEFINE function`, `CALL`, `RETURN`
- **I/O**: `PROCLAIM`, `INQUIRE`, file read/write
- **Modules**: `IMPORT`
- **Collections**: List and map literals with get/set/append/size operations

## Step 7: Self-Compilation Status

`python tools/bootstrap.py` verifies the complete native bootstrap: the Python compiler builds stage 0, stage 0 builds stage 1, stage 1 rebuilds stage 2, and both native generations produce identical C++ source. The verifier then runs scope, class/base-constructor, imported-module privacy, and exception regressions against the native compiler and Python interpreter.

The generated native compiler still links against `selfhost/runtime/` and requires a C++17 compiler to turn generated C++ into an executable. The Python interpreter and semantic analyzer also remain more complete than their self-hosted counterparts.

## Conclusion

MidShake demonstrates a working self-hosting compiler pipeline:

1. ✅ Formal grammar specification (BNF/EBNF)
2. ✅ Lexer/tokenizer (Python + self-hosted)
3. ✅ Parser with AST construction (Python + self-hosted)
4. ✅ Semantic analysis with type inference (Python)
5. ✅ C++ code generation (Python + self-hosted)
6. ✅ Native compiler bootstrap: two generations match byte-for-byte
7. ✅ Test suite: 206 total (196 passing, 10 skipped)
8. ✅ Standard library with utility functions
9. ✅ Documentation: grammar, types, language reference, design

The self-hosted compiler can regenerate itself and compile MidShake programs to C++ without Python. A shared C++ runtime and C++17 toolchain are still required for native executables.
