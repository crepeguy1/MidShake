# MidShake Formal Grammar

This document defines the formal grammar of the MidShake programming language using Extended Backus-Naur Form (EBNF).

## Notation Conventions

| Symbol | Meaning |
|--------|---------|
| `::=` | Definition |
| `[ ... ]` | Optional (0 or 1 occurrences) |
| `{ ... }` | Repeated (0 or more occurrences) |
| `( ... )` | Grouping |
| `a \| b` | Alternation (choice between a and b) |
| `'...'` | Terminal literal (keyword, operator, or punctuation) |
| `"..."` | String literal content |
| `/* ... */` | Comment (not part of grammar) |

---

## 1. Lexical Specification

### 1.1. Characters and Encoding

MidShake source files are plain text encoded in UTF-8. The source character set includes ASCII letters, digits, whitespace, and common punctuation.

### 1.2. Comments

Comments are ignored by the lexer and do not affect program semantics.

```ebnf
comment       ::= carets_comment | hash_comment | slash_slash_comment
carets_comment ::= '^' { character } newline
hash_comment   ::= '#' { character } newline
slash_slash_comment ::= '//' { character } newline
```

### 1.3. Whitespace

Whitespace characters (space, tab, newline) separate tokens but are otherwise ignored, except inside string literals.

```ebnf
whitespace    ::= ' ' | '\t' | '\n' | '\r'
```

### 1.4. Identifiers

Identifiers are case-sensitive sequences of alphanumeric characters and underscores, beginning with a letter or underscore.

```ebnf
identifier    ::= letter { letter | digit | '_' }
letter        ::= 'a' | 'b' | ... | 'z' | 'A' | 'B' | ... | 'Z'
digit         ::= '0' | '1' | ... | '9'
```

### 1.5. Literals

```ebnf
number_literal ::= ['-'] digit { digit } [ '.' digit { digit } ]
string_literal ::= '"' { string_char } '"'
string_char    ::= printable_char | escape_sequence
escape_sequence ::= '\\' 'n' | '\\' 't' | '\\' '\\' | '\\' '"'
```

### 1.6. Keywords

The following words are reserved keywords and cannot be used as identifiers:

```
LET, SET, GLOBAL, SET, THE, VARIABLE, BE, TO, PROCLAIM, IF, THEN, ELSE,
END, WHILST, DO, FOR, IN, DEFINE, FUNCTION, WITH, AND, CALL, RETURN,
BREAK, CONTINUE, TERMINATE, PROGRAM, INQUIRE, USER, THE, RESPONSE,
IMPORT, FILE, WRITE, CONTENT, OF, IS, PLUS, MINUS, TIMES, MULTIPLIED,
DIVIDED, GREATER, LESS, EQUAL, NOT, STARTS, ENDS, DIGIT, LETTER,
WHITESPACE, MINIMUM, MAXIMUM, ABSOLUTE, VALUE, ROUNDED, UPPERCASE,
LOWERCASE, CHECK, LENGTH, SUBSTRING, CHARACTER, AT, POSITION, SPLIT,
BY, JOIN, TRIMMED, REPLACE, OLD, NEW, APPEND, ITEM, SIZE, KEY, MAP,
TRUE, FALSE
```

### 1.7. Operators and Punctuation

```
;   ,   :   (   )   [   ]   {   }   +   -   *   /
```

---

## 2. Syntax Grammar

### 2.1. Program Structure

A MidShake program is a sequence of statements, optionally organized with imports and function definitions.

```ebnf
program       ::= { statement }
statement     ::= import_stmt | function_def | let_stmt | set_stmt | global_set_stmt
                | proclaim_stmt | inquire_stmt | if_stmt | whilst_stmt | for_in_stmt
                | call_stmt | return_stmt | map_set_stmt | file_write_stmt
                | break_stmt | continue_stmt | terminate_stmt | comment | empty_line
```

### 2.2. Variable Declarations and Assignments

```ebnf
let_stmt      ::= 'LET' 'the' 'variable' identifier 'BE' expression ';'
set_stmt      ::= 'SET' 'the' 'variable' identifier 'TO' expression ';'
global_set_stmt ::= 'GLOBAL' 'SET' 'the' 'variable' identifier 'TO' expression ';'
```

**Semantics:** `LET` declares a new variable. `SET` reassigns an existing variable. `GLOBAL SET` modifies a variable in the global scope from within a function.

### 2.3. Output

```ebnf
proclaim_stmt ::= 'PROCLAIM' expression ';'
```

**Semantics:** Evaluates the expression and prints the result to standard output.

### 2.4. Input

```ebnf
inquire_stmt  ::= 'INQUIRE' 'user' 'for' type_hint '"' question_string '"' ';'
type_hint     ::= 'string' | 'number'
```

**Semantics:** Prompts the user with `question_string` and stores the response in the special `RESPONSE` variable. The `type_hint` indicates the expected input type.

### 2.5. Conditionals

```ebnf
if_stmt       ::= 'IF' expression 'THEN'
                  { statement }
                  [ 'ELSE' { statement } ]
                  'END' 'IF'
```

**Semantics:** If the condition expression evaluates to a truthy value, the `THEN` body executes. Otherwise, if an `ELSE` clause is present, the `ELSE` body executes.

### 2.6. Loops

#### 2.6.1. While Loop

```ebnf
whilst_stmt   ::= 'WHILST' expression 'DO'
                  { statement }
                  'END' 'WHILST'
```

**Semantics:** Repeatedly executes the body while the condition expression evaluates to truthy.

#### 2.6.2. For-In Loop

```ebnf
for_in_stmt   ::= 'FOR' 'the' 'variable' identifier 'IN' expression 'DO'
                  { statement }
                  'END' 'FOR'
```

**Semantics:** Iterates over each element of a list, binding the loop variable to the current element.

### 2.7. Loop Control

```ebnf
break_stmt    ::= 'BREAK' ';'
continue_stmt ::= 'CONTINUE' ';'
```

**Semantics:** `BREAK` exits the innermost enclosing loop. `CONTINUE` skips to the next iteration of the innermost enclosing loop.

### 2.8. Functions

```ebnf
function_def  ::= 'DEFINE' 'function' identifier [ 'WITH' parameter_list ] ';'
                  { statement }
                  'END' 'FUNCTION'

parameter_list ::= 'the' 'variable' identifier
                 | 'the' 'variables' identifier { ',' identifier }

return_stmt   ::= 'RETURN' expression ';'
```

**Semantics:** `DEFINE function` creates a named function with optional parameters. `RETURN` exits the function and yields a value.

### 2.9. Function Calls

```ebnf
call_stmt     ::= 'CALL' identifier [ 'WITH' argument_list ] ';'
argument_list ::= expression { ',' expression }
```

**Semantics:** Invokes the named function with the given arguments. The return value is stored in the special `RESPONSE` variable.

### 2.10. Map Operations

```ebnf
map_set_stmt  ::= 'SET' 'the' 'key' expression 'IN' 'the' 'map' identifier
                  'TO' expression ';'
```

**Semantics:** Sets the value associated with a key in a map.

### 2.11. File I/O

```ebnf
file_write_stmt ::= 'IN' 'the' 'file' file_path 'WRITE' expression ';'
file_path       ::= '"' path_string '"'
```

**Semantics:** Writes the evaluated expression to the specified file.

### 2.12. Imports

```ebnf
import_stmt   ::= 'IMPORT' 'the' 'file' '"' file_path '"' ';'
```

**Semantics:** Loads and executes the specified MidShake file, making its functions and variables available.

### 2.13. Termination

```ebnf
terminate_stmt ::= 'TERMINATE' 'the' 'program' ';'
```

**Semantics:** Immediately terminates program execution.

---

## 3. Expression Grammar

Expressions are evaluated to produce values. The grammar below defines operator precedence from lowest (2.1) to highest (2.6).

```ebnf
expression    ::= comparison

comparison    ::= arithmetic ( 'IS' comparator arithmetic )?
comparator    ::= 'greater' 'than' 'or' 'equal' 'to'
                | 'less' 'than' 'or' 'equal' 'to'
                | 'greater' 'than'
                | 'less' 'than'
                | 'equal' 'to'
                | 'equal'
                | 'not' 'equal' 'to'
                | 'not' 'equal'

arithmetic    ::= term { ( 'plus' | 'minus' | '+' | '-' ) term }
term          ::= factor { ( 'times' | 'multiplied' | 'divided' | '*' | '/' ) factor }
factor        ::= primary
```

### 3.1. Primary Expressions

```ebnf
primary       ::= parenthesized
                | list_literal
                | map_literal
                | function_call_expr
                | literal
                | variable_ref
                | response_ref
                | boolean_literal

parenthesized ::= '(' expression ')'
literal       ::= number_literal | string_literal
boolean_literal ::= 'true' | 'false'

variable_ref  ::= 'the' 'value' 'of' identifier
                | 'the' 'string' identifier
                | 'the' 'number' identifier
                | 'the' 'list' identifier
                | 'the' 'map' identifier
                | identifier

response_ref  ::= 'RESPONSE'
                | 'the' 'RESPONSE'
                | 'the' 'answer'
```

### 3.2. List Literals and Operations

```ebnf
list_literal  ::= '[' [ expression { ',' expression } ] ']'

list_get      ::= 'the' 'item' 'at' [ 'position' ] expression 'in' expression
list_append   ::= 'the' 'append' 'of' expression 'to' expression
list_length   ::= 'the' 'size' 'of' expression
```

### 3.3. Map Operations

```ebnf
map_literal   ::= '{' [ map_entry { ',' map_entry } ] '}'
map_entry     ::= ( identifier | string_literal ) ':' expression

map_get       ::= 'the' 'value' 'of' ( identifier | string_literal ) 'in' expression
```

### 3.4. String Function Expressions

```ebnf
string_length     ::= 'the' 'length' 'of' expression
string_substring  ::= 'the' 'substring' 'of' expression
                      'starting' 'at' expression
                      'ending' 'at' expression
string_char_at    ::= 'the' 'character' 'at' expression 'in' expression
string_split      ::= 'the' 'split' 'of' expression 'by' expression
string_trim       ::= 'the' 'trimmed' expression
string_join       ::= 'the' 'join' 'of' expression 'with' expression
string_replace    ::= 'the' 'replace' 'of' expression 'with' expression 'to' expression
string_uppercase  ::= 'the' 'uppercase' 'of' expression
string_lowercase  ::= 'the' 'lowercase' 'of' expression

string_starts_with ::= 'the' 'check' 'if' expression 'starts' 'with' expression
string_ends_with   ::= 'the' 'check' 'if' expression 'ends' 'with' expression
string_is_digit    ::= 'the' 'check' 'if' expression 'is' 'a' 'digit'
string_is_letter   ::= 'the' 'check' 'if' expression 'is' 'a' 'letter'
string_is_whitespace ::= 'the' 'check' 'if' expression 'is' 'whitespace'
```

### 3.5. Math Function Expressions

```ebnf
math_min        ::= 'the' 'minimum' 'of' expression 'and' expression
math_max        ::= 'the' 'maximum' 'of' expression 'and' expression
math_abs        ::= 'the' 'absolute' 'value' 'of' expression
math_round      ::= 'the' 'rounded' 'value' 'of' expression
```

### 3.6. File Read Expression

```ebnf
file_read_expr  ::= 'the' 'content' 'of' 'the' 'file' ( string_literal | variable_ref )
```

---

## 4. Operator Precedence

Operators are listed from lowest precedence (evaluated last) to highest precedence (evaluated first):

| Precedence | Operators | Description |
|------------|-----------|-------------|
| 1 (lowest) | `IS ...` | Comparison operators |
| 2 | `plus`, `minus`, `+`, `-` | Addition and subtraction |
| 3 (highest) | `times`, `multiplied`, `divided`, `*`, `/` | Multiplication and division |

All comparison operators have equal precedence. Arithmetic follows standard mathematical precedence.

---

## 5. Scoping Rules

### 5.1. Variable Scope

- Variables declared with `LET` are scoped to the current block (function body or top-level program).
- Variables declared with `SET` must already exist in the current scope.
- `GLOBAL SET` modifies a variable in the global (top-level) scope, even when called from within a function.

### 5.2. Function Parameters

- Function parameters are local variables within the function body.
- Parameters are bound by position to the arguments provided in a `CALL` statement.

### 5.3. The RESPONSE Variable

- The `RESPONSE` variable is a special global variable that holds the result of the most recent `INQUIRE` or `CALL` operation.
- It is automatically updated by the runtime and should not be directly assigned.

---

## 6. Special Variables

| Variable | Description |
|----------|-------------|
| `RESPONSE` | Holds the result of the last `INQUIRE` or `CALL` |
| `the RESPONSE` | Alias for `RESPONSE` |
| `the answer` | Alias for `RESPONSE` |

---

## 7. Examples

### 7.1. Hello World

```midshake
PROCLAIM the string "Hello, World!";
```

### 7.2. Variable Declaration and Arithmetic

```midshake
LET the variable a BE the number 10;
LET the variable b BE the number 3;
LET the variable sum BE the value of a plus the value of b;
PROCLAIM the value of sum;
```

### 7.3. Conditional

```midshake
IF the value of a IS greater than the number 5 THEN
    PROCLAIM the string "Greater";
ELSE
    PROCLAIM the string "Not greater";
END IF;
```

### 7.4. While Loop

```midshake
LET the variable i BE the number 0;
WHILST the value of i IS less than the number 10 DO
    PROCLAIM the value of i;
    SET the variable i TO the value of i plus the number 1;
END WHILST;
```

### 7.5. Function Definition and Call

```midshake
DEFINE function greet WITH the variable name;
    PROCLAIM the string "Hello, ";
    PROCLAIM the value of name;
END FUNCTION;

CALL greet WITH the string "Ada";
```

### 7.6. List Operations

```midshake
LET the variable items BE [1, 2, 3];
LET the variable first BE the item at position the number 0 in the value of items;
LET the variable extended BE the append of the number 4 to the value of items;
PROCLAIM the size of the value of items;
```

### 7.7. Map Operations

```midshake
LET the variable config BE {name: "MidShake", version: 1};
LET the variable n BE the value of name in config;
SET the key "version" IN the map config TO the number 2;
```

### 7.8. String Functions

```midshake
LET the variable msg BE the string "hello world";
LET the variable upper BE the uppercase of the value of msg;
LET the variable len BE the length of the value of msg;
LET the variable part BE the substring of the value of msg starting at the number 0 ending at the number 5;
```

---

## 8. Grammar Summary

This grammar defines a dynamically typed, statement-oriented programming language with:

- **Lexical analysis**: Comments (`^`, `#`, `//`), identifiers, numeric and string literals.
- **Statements**: Variable declaration/assignment, output, input, conditionals, loops, function definitions, function calls, map operations, file I/O, imports, and program termination.
- **Expressions**: Arithmetic, comparison, function expressions (string, math, list, map), literals, and variable references.
- **Scoping**: Block-scoped variables with global mutation support via `GLOBAL SET`.
- **Type system**: Dynamic typing with runtime type inference (see `docs/types.md`).
