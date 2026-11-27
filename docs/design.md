# MidShake Design Document

## Overview

MidShake is a self-hosting programming language with a natural-language syntax inspired by spoken English. It is a compiled language that translates source code to C++, which is then compiled to native machine code via g++. The project aims for full self-compilation: a MidShake compiler written entirely in MidShake.

## Architecture

MidShake follows a traditional compiler pipeline with five phases:

```
Source Code → Tokenizer → Parser → Semantic Analysis → C++ Code Generator → C++ Compiler → Native Binary
```

### 1. Tokenizer (`midshake_tokenizer.py`)

The tokenizer converts raw source text into typed tokens representing MidShake statements. It operates in two stages:

1. **Statement splitting**: Raw text is split into individual statements by recognizing semicolons, newlines, and standalone keywords (ELSE, END IF, BREAK, etc.). Lines are joined when they form part of a single statement (e.g., `LET` declarations that span multiple lines).

2. **Statement tokenization**: Each statement string is parsed into a `Token` with a type (LET, SET, PROCLAIM, IF, etc.) and a value (the parsed expression or sub-structure).

Key design decisions:
- **Statement-level tokens**: Rather than producing a flat stream of lexical tokens (identifiers, operators, literals), the tokenizer produces one token per statement. This simplifies the parser significantly since each token already contains the parsed structure of the statement.
- **Line joining**: The tokenizer handles multi-line statements by joining lines until a semicolon or standalone keyword is found. This means `IF ... THEN` on one line and the body on the next are properly connected.
- **Expression parsing**: Within each statement, a recursive descent parser handles expressions with operator precedence (multiplication before addition, comparisons, etc.).

### 2. Parser (`midshake_parser.py`)

The parser takes the statement-level tokens and builds an Abstract Syntax Tree (AST). Since the tokenizer already parsed most of the statement structure, the parser's main job is:

- Creating AST node objects (`Let`, `Set`, `If`, `While`, `FunctionDef`, etc.)
- Handling block structures (IF/ELSE bodies, WHILE bodies, function bodies)
- Recursively parsing nested statements

Key design decisions:
- **Section-based AST**: The AST is organized into `Section` objects (currently only "MAIN"), each containing a list of statements. This design leaves room for future module/package support.
- **Recursive block parsing**: Functions like `parse_if` and `parse_while` recursively call `parse_statement` to build nested structures, stopping when they encounter the corresponding end keyword.

### 3. Semantic Analysis (`midshake_semantic.py`)

The semantic analyzer performs two-pass analysis:

**Pass 1**: Collect all function definitions to build the symbol table.
**Pass 2**: Analyze all statements for type correctness and scope validity.

Key capabilities:
- **Symbol table**: Tracks variable declarations, function definitions, and their types across nested scopes (global, function, block, loop).
- **Type inference**: Infers types for all expression types — literals are explicit, variables are looked up, binary operations follow type rules, and built-in expression functions return known types.
- **Error detection**: Catches undeclared variables, duplicate declarations, SET without LET, undefined function calls, RETURN outside functions, and BREAK/CONTINUE outside loops.

Key design decisions:
- **Dynamic typing with inference**: MidShake is dynamically typed at runtime, but the semantic analyzer performs static type inference to catch obvious errors early.
- **Scope chain**: Nested scopes delegate to parent scopes for variable lookup, implementing lexical scoping.
- **Map key handling**: Bare identifiers used as map keys are not flagged as undeclared variables, since they are string keys, not variable references.

### 4. C++ Code Generator (`midshake_compiler.py`)

The code generator walks the AST and produces C++ code that links against the MidShake C++ runtime library.

Key design decisions:
- **Environment-based execution**: Generated C++ uses an `Environment` object that manages variables, functions, and I/O. This mirrors the MidShake runtime model where all variables are stored in a central environment.
- **Value type**: All MidShake values are represented as C++ `Value` objects that can hold strings, numbers, booleans, lists, or maps. This unified type system simplifies code generation.
- **Function deduplication**: When importing files, function definitions may be duplicated. The compiler deduplicates by name, with later definitions overriding earlier ones.
- **Print-based I/O**: PROCLAIM compiles to `print()` calls that format the Value object for output.

### 5. C++ Runtime (`selfhost/runtime/midshake_runtime.cpp`)

The C++ runtime provides:
- **Value type**: Unified type for strings, numbers, booleans, lists, and maps
- **Environment**: Variable storage, function dispatch, and I/O
- **Primitive operations**: String, math, collection, class, and file operations that depend on native value storage or platform APIs

The self-hosted compiler currently emits `println`, `greet`, `add_and_print`, and `repeat` from `stdlib/native_core.mish` as ordinary MidShake functions. Other standard-library calls still use C++ adapters while their expression forms are brought into the self-hosted code generator; the Python compiler compiles the full `stdlib/stdlib.mish` source.

## Lexical Environment Frames

Each compiled function receives its caller's environment as a parent and creates a fresh local frame. Parameters and local assignments are stored in that frame; reads search the current frame and then its parents. `GLOBAL SET` explicitly writes to the root environment, while `RESPONSE` remains local to each call so recursion preserves return values. The Python interpreter currently implements the same observable behavior by snapshotting and restoring its environment around calls.

This linked-frame model isolates local variables without copying the complete environment and provides a direct parent-chain lookup for lexical scope.

## Self-Compilation Strategy

The self-compilation path follows a bootstrap approach:

1. **Python compiler**: The initial compiler is written in Python, handling all phases from tokenization to C++ generation
2. **Self-hosted parser**: `selfhost/parser.mish` implements the parser in MidShake
3. **Self-hosted codegen**: `selfhost/codegen.mish` implements C++ code generation in MidShake
4. **Bootstrap**: The Python compiler compiles `codegen.mish` to produce `codegen.exe`
5. **Self-compilation**: `codegen.exe` can compile MidShake programs to C++ without Python

### Current status

`python tools/bootstrap.py` builds the Python seed, compiles two native generations, verifies byte-for-byte identical compiler source, and runs a recursion/scope smoke test. The generated compiler still relies on the shared C++ runtime.

## Language Design Philosophy

MidShake's syntax prioritizes readability over brevity:

| Concept | MidShake | Traditional |
|---------|----------|-------------|
| Variable declaration | `LET the variable x BE the number 42;` | `int x = 42;` |
| Assignment | `SET the variable x TO the number 10;` | `x = 10;` |
| Output | `PROCLAIM the value of x;` | `print(x);` |
| Condition | `IF the value of x IS greater than the number 5 THEN` | `if (x > 5)` |
| Loop | `WHILST the value of i IS less than the number 10 DO` | `while (i < 10)` |
| Function | `DEFINE function greet WITH the parameter name` | `void greet(string name)` |
| Call | `CALL greet WITH the string "Alice";` | `greet("Alice");` |

This design makes MidShake accessible to beginners while maintaining the expressiveness needed for self-hosting.

## Test Strategy

The test suite covers all compiler phases:

- **Unit tests** (177 checks): Verify each phase independently — tokenizer produces correct tokens, parser builds correct AST, semantic analysis reports issues, and codegen produces correct C++
- **Integration tests** (23 tests): End-to-end compilation and execution of MidShake programs covering language constructs and the standard-library boundary
- **Semantic error tests** (5 errors): Verify the semantic analyzer catches common mistakes

## Known Limitations

1. **Semantic import analysis**: The analyzer may not resolve all declarations from imported modules.
2. **Self-hosted implementation parity**: The interpreter and semantic analyzer do not yet cover every Python implementation feature.
3. **C++ runtime dependency**: Native output still requires the shared runtime and a C++17 compiler.

## Future Work

1. **Runtime independence**: Implement runtime functionality in MidShake and reduce the native C++ dependency.
2. **Semantic import analysis**: Resolve imported declarations during static analysis.
3. **Interpreter parity**: Match Python interpreter coverage and test behavior across both implementations.
