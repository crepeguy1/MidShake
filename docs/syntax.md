# MidShake Syntax Guide

MidShake is a small, statement-based language with English-like keywords. Its goal is to remain readable while still supporting basic programming concepts such as variables, input, branching, loops, and functions.

## Program structure

- MidShake programs are written as plain text files with the `.ms` extension.
- Statements usually end with a semicolon `;`.
- Comments begin with `^` or `#`.
- Indentation is optional, but it improves readability.

## Core statements

### Output

Use `PROCLAIM` to print information to the console.

```midshake
PROCLAIM the value of name;
PROCLAIM the string "Hello";
```

### Variables

Variables are created with `LET` and updated with `SET`.

```midshake
LET the variable name BE the number 10;
SET the variable name TO the value of name plus the number 1;
```

### Input

Use `INQUIRE` to prompt the user for input.

```midshake
INQUIRE user for number "Enter a number:";
LET the variable answer BE the RESPONSE;
PROCLAIM the value of answer;
```

### Conditionals

```midshake
IF the value of age IS greater than the number 21 THEN
    PROCLAIM the string "Adult";
ELSE
    PROCLAIM the string "Minor";
END IF;
```

### Loops

```midshake
WHILST the value of i IS less than the value of count DO
    PROCLAIM the value of i;
    SET the variable i TO the value of i plus the number 1;
END WHILST;
```

### Functions

```midshake
DEFINE function greet WITH the variable name;
    PROCLAIM the string "Hello, ";
    PROCLAIM the value of name;
END FUNCTION;

CALL greet WITH the string "Ada";
```

### Termination

```midshake
TERMINATE the program;
```

## Values

MidShake currently supports a small set of value forms:

- Numbers: `the number 10`
- Strings: `the string "Hello"`
- Variables: `the value of name`
- Response values from input: `the RESPONSE`

## Expressions

### Arithmetic

- `plus`
- `minus`
- `times`
- `divided`

### Comparisons

- `IS greater than`
- `IS less than`
- `IS equal to`
- `IS not equal to`

## Standard library

The standard library is currently small and intentionally focused on basic helper functions. It is defined in `stdlib/stdlib.ms` and loaded automatically for programs that use it.

Common helpers include:

- `println`: print a value to the console
- `greet`: print a greeting for a name
- `add_and_print`: print the result of a simple expression
- `repeat`: repeat a message a given number of times

## Example programs

### Arithmetic and output

```midshake
LET the variable a BE the number 4;
LET the variable b BE the number 5;
LET the variable sum BE the value of a plus the value of b;
LET the variable product BE the value of a times the value of b;
PROCLAIM the string "Sum: ";
PROCLAIM the value of sum;
PROCLAIM the string "Product: ";
PROCLAIM the value of product;
```

### Input and output

```midshake
INQUIRE user for string "What is your name?";
LET the variable name BE the RESPONSE;
PROCLAIM the string "Hello, ";
PROCLAIM the value of name;
```
