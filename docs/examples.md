# MidShake Example Programs

These examples use the syntax supported by the current interpreter.

## Hello World
```midshake
PROCLAIM the string "Hello, World!";
```

## Variables
```midshake
LET the variable name BE the string "MidShake";
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

## User Input
```midshake
INQUIRE user for number "Enter a number:";
LET the variable input BE the RESPONSE;
PROCLAIM the value of input;
```

