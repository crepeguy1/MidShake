# MidShake Design Document

## Overview

MidShake is a self-hosting programming language with a natural-language syntax inspired by spoken English. It is a compiled language that translates source code to C++, which is then compiled to native machine code via g++. The project aims for full self-compilation: a MidShake compiler written entirely in MidShake.

## Architecture

MidShake follows a traditional compiler pipeline with five phases:

```
Source Code → Tokenizer → Parser → Semantic Analysis → C++ Code Generator → C++ Compiler → Native Binary
```

### 1. Tokenizer (`midshake_tokenizer.py`, 1290 lines)

The tokenizer converts raw source text into typed tokens representing MidShake statements. It operates in two stages:

1. **Statement splitting**: Raw text is split into individual statements by recognizing semicolons, newlines, and standalone keywords (ELSE, END IF, BREAK, etc.). Lines are joined when they form part of a single statement (e.g., `LET` declarations that span multiple lines).

2. **Statement tokenization**: Each statement string is parsed into a `Token` with a type (LET, SET, PROCLAIM, IF, etc.) and a value (the parsed expression or sub-structure).

Key design decisions:
- **Statement-level tokens**: Rather than producing a flat stream of lexical tokens (identifiers, operators, literals), the tokenizer produces one token per statement. This simplifies the parser significantly since each token already contains the parsed structure of the statement.
- **Line joining**: The tokenizer handles multi-line statements by joining lines until a semicolon or standalone keyword is found. This means `IF ... THEN` on one line and the body on the next are properly connected.
- **Expression parsing**: Within each statement, a recursive descent parser handles expressions with operator precedence (multiplication before addition, comparisons, etc.).

### 2. Parser (`midshake_parser.py`, 245 lines)

The parser takes the statement-level tokens and builds an Abstract Syntax Tree (AST). Since the tokenizer already parsed most of the statement structure, the parser's main job is:

- Creating AST node objects (`Let`, `Set`, `If`, `While`, `FunctionDef`, etc.)
- Handling block structures (IF/ELSE bodies, WHILE bodies, function bodies)
- Recursively parsing nested statements

Key design decisions:
- **Section-based AST**: The AST is organized into `Section` objects (currently only "MAIN"), each containing a list of statements. This design预留s room for future module/package support.
- **Recursive block parsing**: Functions like `parse_if` and `parse_while` recursively call `parse_statement` to build nested structures, stopping when they encounter the corresponding end keyword.

### 3. Semantic Analysis (`midshake_semantic.py`, 697 lines)

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

### 4. C++ Code Generator (`midshake_compiler.py`, 551 lines)

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
- **Built-in functions**: String operations (length, substring, split, join, trim, etc.), math functions (min, max, abs, round), list operations (get, append, size), map operations (get, set)

## The Deep-Copy Scope Model

One of MidShake's most distinctive design features is its **deep-copy scope model** for function calls:

### How it works

When a `CALL` statement executes:
1. The current variable scope is deep-copied
2. Function parameters are bound in the new scope
3. The function body executes in this isolated scope
4. When the function returns, the scope is restored to the pre-call state
5. The return value is stored in the `RESPONSE` variable

### Why this design

This model was chosen because:
- **Simplicity**: No need for complex stack frame management or register allocation
- **Safety**: Functions cannot accidentally modify caller variables
- **Natural language semantics**: Each function call is an independent "action" that doesn't leak state

### Challenges

The deep-copy model creates significant challenges for the self-hosted compiler:
- **Shared state**: Lists, maps, and accumulators cannot be easily shared across CALL boundaries
- **Workaround**: `GLOBAL SET` bypasses the deep-copy by writing directly to the global scope
- **Self-hosted parser**: Uses `GLOBAL SET` for all shared state (g_lines, g_pos, g_result, etc.)

This is the primary blocker for full self-compilation: the self-hosted parser and codegen must use `GLOBAL SET` extensively, which is less elegant than local variable sharing.

## Self-Compilation Strategy

The self-compilation path follows a bootstrap approach:

1. **Python compiler**: The initial compiler is written in Python, handling all phases from tokenization to C++ generation
2. **Self-hosted parser**: `selfhost/parser.mish` implements the parser in MidShake
3. **Self-hosted codegen**: `selfhost/codegen.mish` implements C++ code generation in MidShake
4. **Bootstrap**: The Python compiler compiles `codegen.mish` to produce `codegen.exe`
5. **Self-compilation**: `codegen.exe` can compile MidShake programs to C++ without Python

### Current status

The bootstrap chain works for simple programs (functions, conditionals, loops). Full self-compilation (codegen.exe compiling itself) is blocked by the self-hosted parser's inability to handle 800+ line files efficiently.

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

- **Unit tests** (146 tests): Verify each phase independently — tokenizer produces correct tokens, parser builds correct AST, codegen produces correct C++
- **Integration tests** (15 tests): End-to-end compilation and execution of MidShake programs covering all language constructs
- **Semantic error tests** (5 errors): Verify the semantic analyzer catches common mistakes

## Known Limitations

1. **Full self-compilation**: The self-hosted parser hangs on files over 800 lines due to the deep-copy scope model's performance characteristics
2. **Array index formatting**: Integer indices print as floats (`args[0.000000]` instead of `args[0]`)
3. **Self-hosted semantic analysis**: Not yet implemented in MidShake
4. **Import resolution**: The semantic analyzer doesn't follow imports, causing false "undefined function" errors for imported functions
5. **C++ runtime dependency**: Compiled programs still require the C++ runtime library; full survival without C++ is not yet achieved

## Future Work

1. **Fix self-hosted parser performance**: Enable codegen.exe to compile itself
2. **Self-hosted semantic analysis**: Port `midshake_semantic.py` to MidShake
3. **Replace C++ runtime**: Implement runtime functions in MidShake
4. **Minimal bootstrap**: Create a tiny C bootstrap program (~500 lines) as the only external dependency
5. **Full self-compilation**: Achieve `midshake-compiler selfhost/codegen.mish → new-midshake-compiler`
