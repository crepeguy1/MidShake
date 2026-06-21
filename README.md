# 🎨 MidShake Language
### Warning: README may not be up to date with actual project
A small, experimental programming language with a C++ backend and Python bindings.

MidShake is designed to be **simple**, **readable**, and **fun to extend**—a perfect playground for learning how programming languages work under the hood.

---

## 🌟 Overview

MidShake demonstrates the complete lifecycle of a programming language:

- **Tokenization** – Breaking source code into meaningful tokens
- **Parsing** – Building an Abstract Syntax Tree (AST)
- **Interpretation** – Executing the AST with a runtime
- **Bindings** – Seamlessly calling C++ from Python

The architecture is intentionally small but clean enough to grow into a real language.

---

## ✨ Features

- ✅ Clean, readable syntax inspired by natural language
- ✅ Full-stack implementation (tokenizer → parser → interpreter)
- ✅ C++ core for performance
- ✅ Python bindings for ease of use
- ✅ Well-documented codebase for learning

---

## 📋 Requirements

### On Windows

- **MSYS2 MinGW64** (not PowerShell or CMD)
  - Download: https://www.msys2.org/
- **GCC 11+** or compatible C++ compiler
- **CMake 3.15+**
- **Python 3.7+** for the MinGW64 environment

### On macOS/Linux

- **GCC** or **Clang**
- **CMake 3.15+**
- **Python 3.7+**

---

## 🔧 Installation

### 1. Set Up MSYS2 (Windows Only)

Open **MSYS2 MinGW64** terminal and install dependencies:

```bash
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-cmake python
```

### 2. Build the C++ Engine

Navigate to the bindings directory:

```bash
cd bindings/build
cmake -G "MinGW Makefiles" ..
cmake --build .
```

This generates `midshake_cpp.pyd` (or `.so` on Linux/macOS).

### 3. Verify Installation

Test the C++ bindings from Python:

```bash
python -c "import midshake_cpp; print(midshake_cpp.tokenize('LET x BE 5'))"
```

If you see tokens printed, the C++ engine is working! ✅

---

## 📁 Project Structure

```
MidShake/
├── cpp/                       # C++ language engine
│   ├── midshake_engine.hpp    # Core engine definitions
│   └── midshake_engine.cpp    # Engine implementation
│
├── bindings/                  # Python C++ bindings
│   ├── CMakeLists.txt         # Build configuration
│   ├── midshake_bindings.cpp  # Binding interface
│   └── build/                 # Build artifacts
│
├── python/                    # Pure Python components
│   ├── midshake_tokenizer.py  # Lexical analysis
│   ├── midshake_parser.py     # Syntax analysis
│   ├── midshake_ast.py        # AST definitions
│   ├── midshake_interpreter.py # AST interpreter
│   └── midshake_runtime_stub.py# Runtime utilities
│
├── examples/                  # Example programs
│   ├── hello.ms              # Hello world
│   └── error.ms              # Error handling demo
│
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Write a MidShake Program

Create `example.ms`:

```
LET x BE 5
LET y BE 10
PRINT x + y
```

### Run It

```bash
python -c "from midshake_interpreter import run; run(open('example.ms').read())"
```

---

## 📚 Learning Resources

- **[examples/hello.ms](examples/hello.ms)** – Basic syntax
- **[examples/error.ms](examples/error.ms)** – Error handling
- **[python/midshake_tokenizer.py](python/midshake_tokenizer.py)** – Lexical analysis
- **[python/midshake_parser.py](python/midshake_parser.py)** – Parsing logic
- **[python/midshake_ast.py](python/midshake_ast.py)** – AST structure

---

## 🛠️ Development

### Rebuilding After Changes

```bash
cd bindings/build
cmake --build . --target clean
cmake --build .
```

### Testing

Run the verification command:

```bash
python -c "import midshake_cpp; print(midshake_cpp.tokenize('LET x BE 5'))"
```

---

## 📝 License

MidShake is open source. Check individual files for licensing details.

---

## 💡 Contributing

Want to extend MidShake? Start with:

1. **Add tokens** in [python/midshake_tokenizer.py](python/midshake_tokenizer.py)
2. **Update the parser** in [python/midshake_parser.py](python/midshake_parser.py)
3. **Extend the interpreter** in [python/midshake_interpreter.py](python/midshake_interpreter.py)

The architecture is designed for easy extension!

---

Made with ❤️ for language nerds and curious developers.
