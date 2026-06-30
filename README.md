# MidShake

MidShake is a small interpreted programming language implemented in Python and C++ that was made entirely because I was bored. It is designed to be readable, beginner-friendly, and easy to extend.

## Overview

MidShake programs are plain text files with the `.ms` extension. The language currently supports variables, input, conditionals, loops, functions, and a small standard library.

## Example

```midshake
PROCLAIM the string "Hello, World!";
```

A slightly richer example:

```midshake
LET the variable name BE the string "MidShake";
PROCLAIM the string "Hello, ";
PROCLAIM the value of name;
```

## Documentation

- [Syntax Guide](docs/syntax.md)
- [Examples](docs/examples.md)
- [Standard Library Reference](docs/stdlib_reference.md)
- [Roadmap](docs/roadmap.md)

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
