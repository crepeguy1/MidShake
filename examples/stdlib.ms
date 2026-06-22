// stdlib.ms

DEFINE function println WITH the variable x;
    PROCLAIM the value of x;
END FUNCTION;

DEFINE function concat WITH the variables a, b;
    PROCLAIM the value of a;
    PROCLAIM the value of b;
END FUNCTION;

DEFINE function greet WITH the variable name;
    PROCLAIM the string "Hello, ";
    PROCLAIM the value of name;
END FUNCTION;

DEFINE function repeat WITH the variables count, message;
    LET the variable i BE the number 0;
    WHILST the value of i IS less than the value of count DO
        PROCLAIM the value of message;
        SET the variable i TO the value of i plus the number 1;
    END WHILST;
END FUNCTION;
