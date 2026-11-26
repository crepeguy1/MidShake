# MidShake Language Reference

This is the comprehensive reference for the MidShake programming language. It describes every language construct, statement, expression, and built-in function.

For the formal grammar, see [`docs/grammar.md`](grammar.md). For the type system, see [`docs/types.md`](types.md).

---

## Table of Contents

1. [Program Structure](#1-program-structure)
2. [Comments](#2-comments)
3. [Variables](#3-variables)
4. [Literals](#4-literals)
5. [Expressions](#5-expressions)
6. [Statements](#6-statements)
7. [Functions](#7-functions)
8. [Built-in Expression Functions](#8-built-in-expression-functions)
9. [Standard Library](#9-standard-library)
10. [Special Variables](#10-special-variables)
11. [Operator Precedence](#11-operator-precedence)

---

## 1. Program Structure

A MidShake program is a plain text file with the `.mish` extension containing a sequence of statements. Statements are typically terminated by semicolons (`;`), though block-delimited statements (IF, WHILST, FOR, DEFINE) use closing keywords instead.

```midshake
IMPORT the file "stdlib/stdlib.mish";

LET the variable greeting BE the string "Hello";
PROCLAIM the value of greeting;
```

### Execution Model

- Statements execute sequentially from top to bottom.
- Function definitions are processed when encountered; the function body does not execute until called.
- `IMPORT` statements load and execute the referenced file immediately.

---

## 2. Comments

Three comment styles are supported. Comments are ignored during execution.

| Style | Syntax | Example |
|-------|--------|---------|
| Caret | `^` to end of line | `^ This is a comment` |
| Hash | `#` to end of line | `# This is also a comment` |
| C-style | `//` to end of line | `// This is a C-style comment` |

---

## 3. Variables

### 3.1. Declaration (`LET`)

Declares a new variable and initializes it with a value.

```ebnf
LET the variable <name> BE <expression>;
```

**Example:**
```midshake
LET the variable name BE the string "Ada";
LET the variable age BE the number 30;
LET the variable items BE [1, 2, 3];
```

### 3.2. Assignment (`SET`)

Reassigns a value to an existing variable.

```ebnf
SET the variable <name> TO <expression>;
```

**Example:**
```midshake
SET the variable name TO the string "Bob";
SET the variable age TO the value of age plus the number 1;
```

### 3.3. Global Assignment (`GLOBAL SET`)

Modifies a variable in the global scope from within a function. This is the mechanism for functions to communicate results back to the caller beyond the `RESPONSE` variable.

```ebnf
GLOBAL SET the variable <name> TO <expression>;
```

**Example:**
```midshake
DEFINE function incrementCounter;
    GLOBAL SET the variable counter TO the value of counter plus the number 1;
END FUNCTION;

LET the variable counter BE the number 0;
CALL incrementCounter;
PROCLAIM the value of counter;  ^ Outputs: 1
```

### 3.4. Module Visibility (`PUBLIC` and `PRIVATE`)

Module-level variables and functions are public by default. Add `Public` or `Private` before a declaration to choose its visibility:

```midshake
Private LET the variable balance BE the number 0;

Private DEFINE function updateBalance;
    GLOBAL SET the variable balance TO the value of balance plus the number 1;
END FUNCTION;

Public DEFINE function getBalance;
    RETURN the value of balance;
END FUNCTION;
```

`Private` declarations are accessible only within the file that defines them. Importers must use public functions rather than reading or changing private variables or calling private functions directly. Public functions retain access to private declarations in their own file. `Protected` is reserved for class members.

### 3.5. Classes and Member Visibility

Classes are public by default. Class fields and methods are private by default; `Public`, `Private`, and `Protected` can be specified explicitly. `Private` members are accessible only from methods declared by that class. `Protected` members are accessible from that class and its subclasses. Inheritance is single-base.

```midshake
Public DEFINE class Counter;
    Private LET the variable value BE the number 0;

    Protected DEFINE function increase WITH the variable amount;
        SET the variable this.value TO the value of this.value plus the value of amount;
    END FUNCTION;

    Public DEFINE function read;
        RETURN the value of this.value;
    END FUNCTION;
END CLASS;

Public DEFINE class FastCounter EXTENDS Counter;
    Public DEFINE function increment;
        CALL this.increase WITH the number 1;
        RETURN the RESPONSE;
    END FUNCTION;
END CLASS;

LET the variable counter BE the new FastCounter;
CALL counter.increment;
CALL counter.read;
PROCLAIM the RESPONSE;
```

`this.member` accesses a field or method on the current instance; methods are called with `CALL instance.method`. A method named `constructor` runs automatically when an instance is created. Constructor arguments follow `WITH` and are evaluated left to right:

```midshake
LET the variable counter BE the new Counter WITH the number 10;
```

The Python interpreter, Python-to-C++ compiler, and self-hosted compiler support class fields, methods, single inheritance, parameterized constructors, and `Public`/`Private`/`Protected` member access. Base-class constructors run before derived-class constructors and currently must take no arguments; explicit base-constructor argument forwarding is not yet available. The self-hosted compiler does not yet enforce class-declaration visibility or module-level visibility across flattened imports.

---

## 4. Literals

### 4.1. Numbers

```midshake
the number 42
the number 3.14
-7
2.5
```

Numbers can be integers or floating-point. The `the number` prefix is optional in expressions.

### 4.2. Strings

```midshake
the string "Hello, World!"
"Hello"
```

Strings are enclosed in double quotes. Supported escape sequences:

| Escape | Character |
|--------|-----------|
| `\n` | Newline |
| `\t` | Tab |
| `\\` | Backslash |
| `\"` | Double quote |

### 4.3. Booleans

```midshake
true
false
```

### 4.4. Lists

```midshake
[1, 2, 3]
["a", "b", "c"]
[1, "mixed", true]
[]
```

### 4.5. Maps

```midshake
{name: "Ada", age: 30}
{"key1": "value1", "key2": 42}
{}
```

Map keys can be bare identifiers or quoted strings. Values can be any expression.

---

## 5. Expressions

### 5.1. Variable References

```midshake
the value of myVar
the string myStr
the number myNum
the list myList
the map myMap
myVar
```

The `the value of` prefix is the standard form. Bare identifiers are also accepted.

### 5.2. Arithmetic

| Syntax | Operation |
|--------|-----------|
| `A plus B` | Addition |
| `A minus B` | Subtraction |
| `A times B` | Multiplication |
| `A multiplied B` | Multiplication (alt) |
| `A divided B` | Division |
| `A + B` | Addition (symbol) |
| `A - B` | Subtraction (symbol) |
| `A * B` | Multiplication (symbol) |
| `A / B` | Division (symbol) |

When either operand of `+` or `plus` is a String, the operation performs string concatenation.

### 5.3. Comparisons

All comparisons use the `IS` keyword and return `Boolean`.

| Syntax | Operation |
|--------|-----------|
| `A IS equal to B` | Equality |
| `A IS not equal to B` | Inequality |
| `A IS greater than B` | Greater than |
| `A IS less than B` | Less than |
| `A IS greater than or equal to B` | Greater than or equal |
| `A IS less than or equal to B` | Less than or equal |

**Example:**
```midshake
IF the value of age IS greater than the number 21 THEN
    PROCLAIM the string "Adult";
END IF;
```

### 5.4. Parenthesized Expressions

```midshake
( the value of a plus the value of b ) times the value of c
```

Parentheses override the default operator precedence.

---

## 6. Statements

### 6.1. Output (`PROCLAIM`)

Prints the evaluated expression to standard output.

```midshake
PROCLAIM the string "Hello";
PROCLAIM the value of myVar;
PROCLAIM the value of a plus the value of b;
```

### 6.2. Input (`INQUIRE`)

Prompts the user for input and stores the result in `RESPONSE`.

```midshake
INQUIRE user for string "What is your name?";
LET the variable name BE the RESPONSE;

INQUIRE user for number "How old are you?";
LET the variable age BE the RESPONSE;
```

The type hint (`string` or `number`) indicates the expected input type.

### 6.3. Conditionals (`IF ... THEN ... END IF`)

```midshake
IF <condition> THEN
    <statements>
ELSE
    <statements>
END IF;
```

The `ELSE` clause is optional.

**Example:**
```midshake
IF the value of score IS greater than or equal to the number 90 THEN
    PROCLAIM the string "Grade: A";
ELSE
    IF the value of score IS greater than or equal to the number 80 THEN
        PROCLAIM the string "Grade: B";
    ELSE
        PROCLAIM the string "Grade: C";
    END IF;
END IF;
```

### 6.4. While Loop (`WHILST ... DO ... END WHILST`)

```midshake
WHILST <condition> DO
    <statements>
END WHILST;
```

**Example:**
```midshake
LET the variable i BE the number 0;
WHILST the value of i IS less than the number 10 DO
    PROCLAIM the value of i;
    SET the variable i TO the value of i plus the number 1;
END WHILST;
```

### 6.5. For-In Loop (`FOR ... IN ... DO ... END FOR`)

Iterates over each element of a list.

```midshake
FOR the variable <name> IN <list_expression> DO
    <statements>
END FOR;
```

**Example:**
```midshake
LET the variable fruits BE ["apple", "banana", "cherry"];
FOR the variable fruit IN the value of fruits DO
    PROCLAIM the value of fruit;
END FOR;
```

### 6.6. Loop Control

```midshake
BREAK;       ^ Exits the innermost loop
CONTINUE;    ^ Skips to the next iteration
```

### 6.7. Map Assignment

```midshake
SET the key <key_expr> IN the map <map_name> TO <value_expr>;
```

**Example:**
```midshake
LET the variable config BE {theme: "dark"};
SET the key "language" IN the map config TO the string "en";
```

### 6.8. File Write

```midshake
IN the file "<path>" WRITE <expression>;
```

**Example:**
```midshake
IN the file "output.txt" WRITE the string "Hello, file!";
```

### 6.9. File Read (Expression)

```midshake
the content of the file "path/to/file.txt"
the content of the file the value of filePath
```

Returns the file contents as a String.

### 6.10. Import

```midshake
IMPORT the file "path/to/file.mish";
```

Loads and executes the specified MidShake file.

### 6.11. Termination

```midshake
TERMINATE the program;
```

Immediately stops program execution.

---

## 7. Functions

### 7.1. Definition

```midshake
DEFINE function <name> WITH <parameters>;
    <body>
END FUNCTION;
```

**Single parameter:**
```midshake
DEFINE function greet WITH the variable name;
    PROCLAIM the string "Hello, ";
    PROCLAIM the value of name;
END FUNCTION;
```

**Multiple parameters:**
```midshake
DEFINE function add WITH the variables a, b;
    LET the variable result BE the value of a plus the value of b;
    RETURN the value of result;
END FUNCTION;
```

**No parameters:**
```midshake
DEFINE function hello;
    PROCLAIM the string "Hello!";
END FUNCTION;
```

### 7.2. Calling

```midshake
CALL <name> WITH <arguments>;
```

The return value is stored in `RESPONSE`.

**Example:**
```midshake
CALL add WITH the number 3, the number 4;
LET the variable sum BE the RESPONSE;
PROCLAIM the value of sum;  ^ Outputs: 7
```

### 7.3. Return

```midshake
RETURN <expression>;
```

Exits the function and yields a value. If no `RETURN` is present, the function returns an empty `RESPONSE`.

---

## 8. Built-in Expression Functions

### 8.1. String Operations

| Expression | Returns | Description |
|------------|---------|-------------|
| `the length of STR` | Number | Character count |
| `the substring of STR starting at S ending at E` | String | Substring from S to E |
| `the character at IDX in STR` | String | Single character at IDX |
| `the split of STR by DELIM` | List | Split into list by delimiter |
| `the trimmed STR` | String | Remove leading/trailing whitespace |
| `the join of LIST with DELIM` | String | Join list elements with delimiter |
| `the replace of STR with OLD to NEW` | String | Replace all occurrences |
| `the uppercase of STR` | String | Convert to uppercase |
| `the lowercase of STR` | String | Convert to lowercase |

### 8.2. String Checks (return Boolean)

| Expression | Returns | Description |
|------------|---------|-------------|
| `the check if STR starts with PREFIX` | Boolean | Prefix test |
| `the check if STR ends with SUFFIX` | Boolean | Suffix test |
| `the check if STR is a digit` | Boolean | All characters are digits |
| `the check if STR is a letter` | Boolean | All characters are letters |
| `the check if STR is whitespace` | Boolean | All characters are whitespace |

### 8.3. Math Operations

| Expression | Returns | Description |
|------------|---------|-------------|
| `the minimum of A and B` | Number | Smaller of two values |
| `the maximum of A and B` | Number | Larger of two values |
| `the absolute value of N` | Number | Absolute value |
| `the rounded value of N` | Number | Nearest integer |

### 8.4. List Operations

| Expression | Returns | Description |
|------------|---------|-------------|
| `the size of LIST` | Number | Element count |
| `the item at position IDX in LIST` | any | Element at index IDX |
| `the append of ITEM to LIST` | List | New list with ITEM added |

### 8.5. Map Operations

| Expression | Returns | Description |
|------------|---------|-------------|
| `the value of KEY in MAP` | any | Value for KEY in MAP |

---

## 9. Standard Library

The standard library (`stdlib/stdlib.mish`) provides wrapper functions for built-in expression functions. Import it with:

```midshake
IMPORT the file "stdlib/stdlib.mish";
```

### Available Functions

| Function | Parameters | Description |
|----------|-----------|-------------|
| `println` | `x` | Print a value |
| `greet` | `name` | Print a greeting |
| `add_and_print` | `a, b` | Add and print result |
| `repeat` | `count, message` | Repeat message N times |
| `min` | `a, b` | Minimum of two numbers |
| `max` | `a, b` | Maximum of two numbers |
| `abs` | `a` | Absolute value |
| `round` | `a` | Round to nearest integer |
| `toupper` | `s` | Convert to uppercase |
| `tolower` | `s` | Convert to lowercase |
| `startsWith` | `s, prefix` | Check prefix |
| `endsWith` | `s, suffix` | Check suffix |
| `isDigit` | `c` | Check if digit |
| `isLetter` | `c` | Check if letter |
| `isWhitespace` | `c` | Check if whitespace |
| `readFile` | `path` | Read file contents |
| `length` | `s` | String length |
| `charAt` | `s, index` | Character at position |
| `substring` | `s, start, end` | Extract substring |
| `split` | `s, delimiter` | Split string |
| `join` | `list, delimiter` | Join list |
| `trim` | `s` | Trim whitespace |
| `replace` | `s, old, new` | Replace substrings |
| `size` | `list` | List size |
| `append` | `element, list` | Append to list |
| `getItem` | `index, list` | Get list item |
| `mapSet` | `map, key, value` | Set map key |
| `mapGet` | `key, map` | Get map value |

---

## 10. Special Variables

| Variable | Description |
|----------|-------------|
| `RESPONSE` | Holds the result of the last `CALL` or `INQUIRE` |
| `the RESPONSE` | Alias for `RESPONSE` |
| `the answer` | Alias for `RESPONSE` |

These variables are automatically updated by the runtime and should not be directly assigned.

---

## 11. Operator Precedence

From lowest (evaluated last) to highest (evaluated first):

| Precedence | Operators | Associativity |
|------------|-----------|---------------|
| 1 (lowest) | `IS equal to`, `IS not equal to`, `IS greater than`, `IS less than`, `IS greater than or equal to`, `IS less than or equal to` | Left |
| 2 | `plus`, `minus`, `+`, `-` | Left |
| 3 (highest) | `times`, `multiplied`, `divided`, `*`, `/` | Left |

Parentheses `()` can be used to override precedence.

---

## Appendix A: Complete Keyword List

```
LET    SET    GLOBAL    THE    VARIABLE    BE    TO
PROCLAIM    IF    THEN    ELSE    END    WHILST    DO
FOR    IN    DEFINE    FUNCTION    WITH    AND
CALL    RETURN    BREAK    CONTINUE    TERMINATE    PROGRAM
INQUIRE    USER    RESPONSE    IMPORT    FILE    WRITE
CONTENT    OF    IS    PLUS    MINUS    TIMES    MULTIPLIED
DIVIDED    GREATER    LESS    EQUAL    NOT
STARTS    ENDS    DIGIT    LETTER    WHITESPACE
MINIMUM    MAXIMUM    ABSOLUTE    VALUE    ROUNDED
UPPERCASE    LOWERCASE    CHECK    LENGTH    SUBSTRING
CHARACTER    AT    POSITION    SPLIT    BY    JOIN
TRIMMED    REPLACE    APPEND    ITEM    SIZE    KEY    MAP
TRUE    FALSE
```

## Appendix B: File Extension

MidShake source files use the `.mish` extension.
