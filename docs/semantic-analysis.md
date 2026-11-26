# MidShake Semantic Analysis

This document describes the semantic analysis phase of the MidShake compiler, including the symbol table design, type inference system, scope resolution, and error detection.

---

## 1. Overview

Semantic analysis is the third phase of the MidShake compiler pipeline, following tokenization and parsing. While the parser checks **syntax** (is the code structurally correct?), semantic analysis checks **meaning** (does the code make sense?).

### Compiler Pipeline

```
Source Code → Tokenizer → Tokens → Parser → AST → Semantic Analysis → Annotated AST → Code Generator → C++
```

### What Semantic Analysis Does

1. **Builds a symbol table** — Tracks every variable and function declaration with its type and scope
2. **Infers types** — Determines the type of every expression at compile time
3. **Checks declarations** — Ensures variables are declared before use and functions exist before being called
4. **Resolves scopes** — Verifies that variable references can see their declarations through the scope chain
5. **Detects errors** — Reports semantic errors with descriptive messages

---

## 2. Symbol Table Design

### 2.1. Symbol

Each entry in the symbol table is a `Symbol` object:

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | The identifier name (e.g., `"counter"`) |
| `symbol_type` | `str` | Inferred type (`"Number"`, `"String"`, `"List"`, `"Map"`, `"Function"`, `"Any"`) |
| `kind` | `str` | Kind of symbol (`"variable"`, `"function"`, `"parameter"`, `"loop_var"`, `"builtin"`) |
| `is_mutable` | `bool` | Whether the symbol can be reassigned (always `True` in MidShake) |

### 2.2. Scope

The symbol table is organized as a stack of nested `Scope` objects:

| Scope Type | Created By | Parent |
|------------|-----------|--------|
| `global` | Program start | None |
| `function` | `DEFINE function` | Global |
| `block` | `IF ... THEN`, `ELSE` | Enclosing scope |
| `loop` | `WHILST ... DO`, `FOR ... IN ... DO` | Enclosing scope |

Each scope maintains:
- `symbols` — Dictionary of name → Symbol for variables declared in this scope
- `functions` — Dictionary of name → Symbol for functions defined in this scope
- `parent` — Reference to the enclosing scope (for lookup chaining)

### 2.3. Scope Resolution

When a variable is referenced, the analyzer walks up the scope chain:

```
Current scope → Parent scope → Grandparent scope → ... → Global scope
```

If the symbol is found at any level, the reference is valid. If the chain is exhausted without finding the symbol, an "undeclared variable" error is reported.

---

## 3. Type Inference

MidShake uses **dynamic typing** at runtime, but the semantic analyzer performs **compile-time type inference** to detect obvious type errors.

### 3.1. Literal Types

| Expression | Inferred Type |
|------------|---------------|
| `the number 42` | `Number` |
| `the string "hello"` | `String` |
| `true`, `false` | `Boolean` |
| `[1, 2, 3]` | `List` |
| `{name: "Alice"}` | `Map` |

### 3.2. Variable Types

A variable's type is the type inferred from its initial `LET` declaration:

```midshake
LET the variable x BE the number 42;    ^ x: Number
LET the variable msg BE "hello";         ^ msg: String
LET the variable items BE [1, 2, 3];    ^ items: List
```

### 3.3. Expression Types

| Expression Pattern | Inferred Type |
|-------------------|---------------|
| `a plus b` (both Number) | `Number` |
| `a plus b` (either String) | `String` (concatenation) |
| `the item at 0 in list` | `Any` |
| `the value of key in map` | `Any` |
| `the append of x to list` | `List` |
| `the size of list` | `Number` |
| `the length of string` | `Number` |
| `the substring of ...` | `String` |
| `the character at ...` | `String` |
| `the split of ... by ...` | `List` |
| `the join of ... with ...` | `String` |
| `the uppercase of ...` | `String` |
| `the lowercase of ...` | `String` |
| `the trimmed ...` | `String` |
| `the replace of ...` | `String` |
| `the check if ... starts with ...` | `Boolean` |
| `the check if ... is a digit` | `Boolean` |
| `the minimum of a and b` | `Number` |
| `the maximum of a and b` | `Number` |
| `the absolute value of ...` | `Number` |
| `the rounded value of ...` | `Number` |
| `RESPONSE` | `Any` |

---

## 4. Semantic Checks

### 4.1. Variable Declaration

**Rule:** Every variable must be declared with `LET` before it is used with `SET` or referenced in an expression.

```midshake
^ Correct
LET the variable x BE the number 10;
SET the variable x TO the number 20;
PROCLAIM the value of x;

^ Error: 'y' is not declared
SET the variable y TO the number 30;
```

### 4.2. Duplicate Declaration

**Rule:** A variable cannot be declared twice in the same scope.

```midshake
^ Correct
LET the variable x BE the number 10;

^ Error: 'x' is already declared
LET the variable x BE the number 20;
```

### 4.3. Function Calls

**Rule:** A function must be defined before it is called (or imported from a file).

```midshake
^ Correct
DEFINE function greet WITH the variable name;
    PROCLAIM the value of name;
END FUNCTION;
CALL greet WITH the string "Ada";

^ Error: 'undefined_func' is not defined
CALL undefined_func WITH the number 1;
```

### 4.4. RETURN Context

**Rule:** `RETURN` must appear inside a function body.

```midshake
^ Error: RETURN is not inside a function
RETURN the number 42;
```

### 4.5. BREAK/CONTINUE Context

**Rule:** `BREAK` and `CONTINUE` must appear inside a loop body.

```midshake
^ Error: BREAK is not inside a loop
BREAK;

^ Correct
WHILST the value of i IS less than the number 10 DO
    IF the value of i IS equal to the number 5 THEN
        BREAK;
    END IF;
END WHILST;
```

### 4.6. INQUIRE Type Hint

**Rule:** The type hint in `INQUIRE` must be `"string"` or `"number"`.

```midshake
^ Correct
INQUIRE user for string "What is your name?";
INQUIRE user for number "How old are you?";

^ Error: 'boolean' is not a valid type hint
INQUIRE user for boolean "Are you sure?";
```

---

## 5. Two-Pass Analysis

The semantic analyzer uses a two-pass approach:

### Pass 1: Collect Function Definitions

Before analyzing statements, the analyzer scans the entire program to register all function definitions in the global scope. This allows forward references — a function can be called before it is defined in the source code:

```midshake
^ This is valid: greet is registered in Pass 1
CALL greet WITH the string "Ada";

DEFINE function greet WITH the variable name;
    PROCLAIM the value of name;
END FUNCTION;
```

### Pass 2: Analyze All Statements

With full function knowledge, the analyzer walks every statement, building the symbol table, inferring types, and checking for errors.

---

## 6. Error Reporting

Each semantic error is a `SemanticError` object with:

| Field | Type | Description |
|-------|------|-------------|
| `error_type` | `str` | Category (`"undeclared"`, `"redeclared"`, `"undefined_function"`, `"invalid_context"`, `"invalid_type"`) |
| `message` | `str` | Human-readable description |
| `line_no` | `int` | Source line number (when available) |

### Error Categories

| Category | Trigger | Example Message |
|----------|---------|-----------------|
| `undeclared` | Variable used without LET | "Variable 'x' is not declared. Use 'LET' to declare it first." |
| `redeclared` | LET for existing variable | "Variable 'x' is already declared in this scope." |
| `undefined_function` | CALL to undefined function | "Function 'foo' is not defined." |
| `invalid_context` | RETURN/BREAK/CONTINUE in wrong place | "RETURN statement is not inside a function." |
| `invalid_type` | Bad INQUIRE type hint | "INQUIRE expected type 'boolean' is not valid." |

---

## 7. Integration

### 7.1. CLI Command

The semantic analyzer is accessible via the `midshake check` command:

```bash
python python/midshake_cli.py check examples/functions.mish
```

Output:
```
No semantic errors found.

=== Symbol Table Summary ===

Global Scope:
  RESPONSE: Any (builtin)
  greet: Function (function)

Total functions defined: 1
Total semantic errors: 0
```

### 7.2. Compile Pipeline

Semantic analysis runs automatically during `midshake compile`:

```bash
python python/midshake_cli.py compile examples/functions.mish
```

Output:
```
Semantic analysis passed: no errors found.
=== Symbol Table Summary ===
...
Generated: build/output/functions.cpp
```

If errors are found, compilation proceeds with a warning:
```
Semantic analysis found 2 error(s):
  - Semantic Error: Variable 'x' is not declared.
  - Semantic Error: Function 'foo' is not defined.

Proceeding with compilation despite semantic errors...
```

---

## 8. Design Decisions

### 8.1. Why Dynamic Type Inference?

MidShake is dynamically typed at runtime — variables can hold any type. The semantic analyzer infers types from initial values but does not enforce strict type checking. This design choice:

- **Matches the language semantics** — MidShake variables are truly dynamic
- **Catches obvious errors** — Undeclared variables and undefined functions are caught early
- **Avoids false positives** — No strict type errors means no "type mismatch" false alarms for valid MidShake code

### 8.2. Why Two-Pass Analysis?

The two-pass approach allows forward function references, which is a common pattern in MidShake where `CALL` statements appear before `DEFINE` statements. A single-pass analyzer would require functions to be defined before use.

### 8.3. Map Key Handling

Bare identifiers used as map keys (e.g., `the value of name in mymap` or `{name: "Alice"}`) are not treated as variable references. This prevents false "undeclared variable" errors for map keys that happen to share names with undeclared variables.

---

## 9. Limitations & Future Work

### 9.1. Import Resolution

The current semantic analyzer does not follow `IMPORT` statements to resolve function definitions from imported files. Functions imported from `stdlib.mish` or other files are not registered in the symbol table, causing false "undefined function" errors.

**Future work:** Add import resolution to the semantic analyzer so it loads and analyzes imported files.

### 9.2. Type Mismatch Detection

The analyzer infers types but does not check for type mismatches in operations (e.g., adding a string to a number). Since MidShake auto-coerces types at runtime, this is a deliberate design choice.

**Future work:** Add optional strict type checking mode that warns about potential type mismatches.

### 9.3. Self-Hosted Version

The semantic analyzer exists only in Python (`python/midshake_semantic.py`). A self-hosted version in MidShake (`selfhost/semantic.mish`) is needed for full self-compilation.

**Future work:** Port the semantic analyzer to MidShake.

---

## 10. Testing

The semantic analyzer is tested with:

- **`tests/test_semantic_errors.mish`** — Intentionally contains 5 semantic errors (undeclared variable, SET without LET, duplicate declaration, RETURN outside function, BREAK outside loop)
- **`tests/test_collections.mish`** — Tests map key handling (no false positives for map keys)
- **`tests/test_global_set.mish`** — Tests function definitions and GLOBAL SET
- **`examples/functions.mish`** — Tests function definition and call validation
- **`examples/conditionals.mish`** — Tests IF/WHILST scope handling
