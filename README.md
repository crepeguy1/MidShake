# MidShake — Experimental Programming Language

MidShake is a small interpreted programming language implemented in Python and C++.  
It includes a tokenizer, parser, AST, runtime, and command‑line interface.  
The project is designed as a learning‑oriented language with a simple syntax and a growing standard library.

---

## Overview

MidShake programs are plain text files with the `.ms` extension.  
The language supports basic statements, expressions, printing, user input, and standard library functions.

MidShake is distributed as a standalone executable (`midshake.exe`) built using PyInstaller.  
The executable bundles the interpreter, runtime, and standard library.

---

## Installation

Download the latest `midshake.exe` from the GitHub Releases page.

Place the executable anywhere on your system.  
You may optionally add it to your system PATH for convenience.

---

## Usage

Run a MidShake program:

```
midshake run examples/hello.ms
```

Show tokens:

```
midshake tokens examples/full.ms
```

Show AST:

```
midshake ast examples/functions.ms
```

Show version:

```
midshake version
```

Show help:

```
midshake help
```

---

## Example Program

```
PROCLAIM "Hello, World!"
```

Another example using input:

```
ASK "What is your name?" INTO name
PROCLAIM "Hello, " + name
```

---

## Language Features

- Custom tokenizer  
- AST‑based parser  
- C++ runtime  
- Standard library (`stdlib.ms`)  
- CLI commands: run, tokens, ast, version  
- Simple, readable syntax  
- Cross‑platform source code (Windows executable provided)

More details:  
- [Syntax Guide](ca://s?q=Show_MidShake_Syntax_Guide)  
- [Examples](ca://s?q=Show_MidShake_Examples)  
- [Standard Library Reference](ca://s?q=Show_MidShake_Stdlib_Reference)

---

## Project Structure

```
MidShake/
    python/        # Interpreter, tokenizer, parser, runtime
    cpp/           # C++ runtime implementation
    stdlib/        # Standard library files
    examples/      # Example MidShake programs
    docs/          # Documentation
    bindings/      # pybind11 bindings
    tools/         # Developer utilities
```

---

## Building From Source

MidShake consists of:

- Python interpreter code  
- C++ runtime compiled with CMake  
- PyInstaller packaging for the final executable  

Build instructions will be added in future versions.

---

## Roadmap

- Variables and assignment  
- Functions  
- Loops  
- Modules  
- REPL  
- Improved error messages  
- Compiler mode (MidShake → C++ → native binary)

More details:  
- [Roadmap](ca://s?q=Show_MidShake_Roadmap)

---

## License

MidShake is released under the MIT License.  
See the `LICENSE` file for details.
