^ stdlib.ms

^ Print a value (simple wrapper, but nice for semantics)
DEFINE function println WITH the variable x;
    PROCLAIM the value of x;
END FUNCTION;

^ Greet a person by name
DEFINE function greet WITH the variable name;
    PROCLAIM the string "Hello, ";
    PROCLAIM the value of name;
END FUNCTION;

^ Add two numbers and print the result
DEFINE function add_and_print WITH the variables a, b;
    PROCLAIM the value of a plus the value of b;
END FUNCTION;

^ Repeat a message N times
DEFINE function repeat WITH the variables count, message;
    LET the variable i BE the number 0;
    WHILST the value of i IS less than the value of count DO
        PROCLAIM the value of message;
        SET the variable i TO the value of i plus the number 1;
    END WHILST;
END FUNCTION;
