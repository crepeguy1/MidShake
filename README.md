# MidShake Language

A small, experimental programming language with a C++ backend and Python bindings. MidShake demonstrates a full language pipeline (tokenization → parsing → interpretation) and provides a C++ core for performance with optional Python bindings.

---

## Overview

MidShake implements the main stages of a language implementation:

- Tokenization — lexical analysis of source code
- Parsing — building an Abstract Syntax Tree (AST)
- Interpretation — executing the AST in a runtime
- Bindings — calling the C++ engine from Python

The project is intentionally compact and designed to be easy to read and extend.

---

## Features

- Clean, readable syntax inspired by natural language
- Full-stack implementation (tokenizer → parser → interpreter)
- C++ core for performance
- Python bindings for integration and scripting

---

## Requirements

### Windows (MSYS2 MinGW64)
- MSYS2 MinGW64 environment: https://www.msys2.org/
- GCC 11+ (MinGW-w64)
- CMake 3.15+
- Python 3.7+ (for building/running bindings inside MinGW64)

### macOS / Linux
- GCC or Clang
- CMake 3.15+
- Python 3.7+

---

## Installation / Build

Notes:
- On Windows, use the MSYS2 MinGW64 terminal for building the native bindings.
- On macOS/Linux, use your normal shell (bash/zsh).

1. Clone the repository:
   ```bash
   git clone https://github.com/crepeguy1/MidShake.git
   cd MidShake
   ```

2. Build the C++ engine and Python bindings:
   ```bash
   cd bindings/build
   cmake ..
   cmake --build .
   ```
   On Windows with MSYS2 MinGW64, you can generate MinGW Makefiles:
   ```bash
   cmake -G "MinGW Makefiles" ..
   cmake --build .
   ```

The build produces a Python extension module (e.g., midshake_cpp.pyd on Windows or midshake_cpp.so on macOS/Linux) in bindings/build or the configured output directory.

---

## Verify Installation

From the repository root or a Python environment that can import the built extension:
```bash
python -c "import midshake_cpp; print(midshake_cpp.tokenize('LET x BE 5'))"
```
If tokens are printed, the C++ engine and its Python binding are available.

---

## Project Structure

```
MidShake/
├── cpp/                       # C++ language engine
│   ├── midshake_engine.hpp
│   └── midshake_engine.cpp
│
├── bindings/                  # Python C++ bindings (CMake project)
│   ├── CMakeLists.txt
│   ├── midshake_bindings.cpp
│   └── build/                 # Build artifacts
│
├── python/                    # Pure Python components and experiments
│   ├── midshake_tokenizer.py
│   ├── midshake_parser.py
│   ├── midshake_ast.py
│   ├── midshake_interpreter.py
│   └── midshake_runtime_stub.py
│
├── examples/                  # Example programs
│   ├── hello.ms
│   └── error.ms
│
└── README.md
```

---

## Quick Start

Write a short MidShake program (example.ms):
```
LET x BE 5
LET y BE 10
PROCLAIM x + y
```

Run with the Python interpreter (uses the Python-side interpreter):
```bash
python -c "from python.midshake_interpreter import run; run(open('example.ms').read())"
```

Or use the C++ tokenizer via Python bindings:
```bash
python -c "import midshake_cpp; print(midshake_cpp.tokenize('LET x BE 5'))"
```

---

## Examples & Reference

- examples/hello.ms — Basic syntax examples
- examples/error.ms — Error handling examples
- python/midshake_tokenizer.py — Lexical analysis implementation
- python/midshake_parser.py — Parsing logic
- python/midshake_ast.py — AST node definitions
- python/midshake_interpreter.py — Interpreter implementation

Refer to these files for implementation details and as starting points for changes.

---

## Development

Rebuild after code changes:
```bash
cd bindings/build
cmake --build . --target clean
cmake --build .
```

Run the verification command to confirm the bindings:
```bash
python -c "import midshake_cpp; print(midshake_cpp.tokenize('LET x BE 5'))"
```

---

## Contributing

To extend the language:
1. Add or modify tokens in python/midshake_tokenizer.py
2. Update grammar/parsing in python/midshake_parser.py
3. Extend AST nodes in python/midshake_ast.py
4. Add evaluation logic in python/midshake_interpreter.py
5. If adding features to the C++ core, mirror or expose them via bindings in bindings/

Please open issues or pull requests with a description of the change and any tests or examples.

---

## License

MidShake is open source. Check individual files for specific licensing details.
