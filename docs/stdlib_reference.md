# MidShake Standard Library Reference

The current MidShake implementation does not provide a full built-in standard library yet. The examples and parser focus on core language features such as variables, conditionals, loops, functions, and input.

## Built-in language features
- `PROCLAIM` for output
- `LET` and `SET` for variables
- `IF ... ELSE ... END IF` for conditionals
- `WHILST ... END WHILST` for loops
- `DEFINE function ... END FUNCTION` for functions
- `INQUIRE user for ...` for input

## Example
```midshake
DEFINE function add_and_print WITH the variables a, b;
    PROCLAIM the value of a plus the value of b;
END FUNCTION;

CALL add_and_print WITH the number 2, the number 3;
```
