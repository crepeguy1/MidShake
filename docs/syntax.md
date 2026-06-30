# MidShake Syntax Guide

MidShake is a statement-based language with English-like keywords.

## Program structure
- Programs are made of statements.
- Statements usually end with a semicolon `;`.
- Comments begin with `^` or `#`.

## Supported statements

### Output
```midshake
PROCLAIM the value of name;
PROCLAIM the string "Hello";
```

### Variables
```midshake
LET the variable name BE the number 10;
SET the variable name TO the value of name plus the number 1;
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

### Input
```midshake
INQUIRE user for number "Enter a number:";
LET the variable input BE the RESPONSE;
```

### Termination
```midshake
TERMINATE the program;
```

## Values
- Numbers: `the number 10`
- Strings: `the string "Hello"`
- Variables: `the value of name`

## Operators
- Arithmetic: `plus`, `minus`, `times`, `divided`
- Comparisons: `IS greater than`, `IS less than`, `IS equal to`, `IS not equal to`

## Example
```midshake
LET the variable name BE the string "MidShake";
PROCLAIM the value of name;
```
