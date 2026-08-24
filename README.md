# MidShake

MidShake is a small interpreted programming language implemented in Python and C++ that was made entirely because I was bored. It is designed to be readable, beginner-friendly, and easy to extend.

## Overview

MidShake programs are plain text files with the `.ms` extension. The language currently supports variables, input, conditionals, loops, functions, and a small standard library.

## Example

```midshake
PROCLAIM the string "Hello, World!";
```
## Instalation
### Step 1: 
* Download midshake.exe.
### Step 2: 
* Open Environment Variables
* Press the Windows key on your keyboard.
* Type environment variables and click on Edit the system environment variables.
* Click the Environment Variables... button at the bottom right of the window.
### Step 3: 
* Edit the Path Variable
* Look at the bottom section labeled System variables (or the top section for your user account).
* Find the row named Path and click on it.
* Click the Edit... button.
* Click the New button on the right side.
* Type the exact folder path where your .exe is saved (for example: C:\Midshake).
* Click OK on all open windows to save your changes.
### Step 4: 
* Test Your Installation
* Open a brand new Command Prompt or PowerShell window.
* Type midshake --version or just midshake and press Enter.

## CLI:

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
PROCLAIM "Hello, World!";
```

Another example using input:

```
INQUIRE the user for the string "What is your name?";
LET name BE the RESPONSE;
PROCLAIM "Hello, " + name;
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

## Project structure

```text
MidShake/
    python/        # Interpreter, tokenizer, parser, runtime
    cpp/           # C++ runtime implementation
    stdlib/        # Standard library files
    examples/      # Example MidShake programs
    docs/          # Documentation
    bindings/      # pybind11 bindings
    tools/         # Developer utilities
```

## Roadmap

The project is moving toward a more complete language experience with better tooling, stronger standard-library support, and a more polished runtime. See [docs/roadmap.md](docs/roadmap.md) for the current plan.

## License

MidShake is released under the MIT License. See the `LICENSE` file for details.
