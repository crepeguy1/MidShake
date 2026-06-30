# MidShake Examples

These examples reflect the syntax currently used by the interpreter and are intended to be easy to read and adapt.

## Hello world

```midshake
PROCLAIM the string "Hello, World!";
```

## Variables and output

```midshake
LET the variable name BE the string "MidShake";
PROCLAIM the string "Language: ";
PROCLAIM the value of name;
```

## Conditionals

```midshake
LET the variable age BE the number 18;
IF the value of age IS greater than the number 21 THEN
    PROCLAIM the string "Adult";
ELSE
    PROCLAIM the string "Minor";
END IF;
```

## Loops

```midshake
LET the variable count BE the number 3;
LET the variable i BE the number 0;

WHILST the value of i IS less than the value of count DO
    PROCLAIM the value of i;
    SET the variable i TO the value of i plus the number 1;
END WHILST;
```

## Functions

```midshake
DEFINE function greet WITH the variable name;
    PROCLAIM the string "Hello, ";
    PROCLAIM the value of name;
END FUNCTION;

CALL greet WITH the string "Ada";
```

## User input

```midshake
INQUIRE user for number "Enter a number:";
LET the variable input BE the RESPONSE;
PROCLAIM the string "You entered: ";
PROCLAIM the value of input;
```

## Standard library helpers

```midshake
CALL println WITH the string "MidShake is running";
CALL greet WITH the string "Ava";
```

