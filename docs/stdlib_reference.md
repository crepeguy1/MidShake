# MidShake Standard Library Reference

MidShake currently ships with a small, growing standard library. The library is intentionally lightweight while the core language is still being shaped.

## What is available now

The standard library is defined in `stdlib/stdlib.ms` and provides a few helper functions that are easy to reuse in programs.

### `println`

Prints a value to the console.

```midshake
CALL println WITH the string "Hello from MidShake";
```

### `greet`

Prints a simple greeting for a provided name.

```midshake
CALL greet WITH the string "Ada";
```

### `add_and_print`

Prints the result of a simple arithmetic expression.

```midshake
CALL add_and_print WITH the number 2, the number 3;
```

### `repeat`

Prints a message a given number of times.

```midshake
CALL repeat WITH the number 3, the string "Hi";
```

## Current library philosophy

The standard library emphasizes:

- small, readable helper functions
- simple syntax over advanced abstractions
- a foundation for future growth

## Planned additions

The roadmap for the library includes:

- string utilities such as trimming, joining, and splitting
- math helpers such as rounding, minimum, and maximum
- collection helpers for lists and mappings
- file and console input helpers
- additional convenience functions for common scripting tasks

## Notes

The language itself provides the core features needed to build programs, while the library fills in common everyday helpers. As the language matures, the library is expected to expand significantly.
