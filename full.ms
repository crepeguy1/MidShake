^declare a variable named hero;
LET the variable hero BE the number 1;
LET the variable villain BE the number 2;

PROCLAIM the value of hero;

IF the value of hero IS the number 1 THEN
    PROCLAIM the value of villain;
END IF;

WHILST the value of villain IS the number 2 DO
    SET the variable villain TO the number 3;
    IF the value of villain IS the number 3 THEN
        PROCLAIM the value of villain;
    END IF;
END WHILST;

TERMINATE the program;

DECLARE a function named greet that TAKES a parameter named name;
    PROCLAIM "Hello, " + name + "!";
END FUNCTION;