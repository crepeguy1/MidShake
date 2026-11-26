# MidShake Type System

This document describes the type system of the MidShake programming language. MidShake uses **dynamic typing** with runtime type inference and automatic type coercion in specific contexts.

---

## 1. Overview

MidShake is a dynamically typed language. Variables have no declared type — their type is determined at runtime by the value they hold. Types are properties of values, not of variables. A single variable can hold values of different types at different points in its lifetime.

```midshake
LET the variable x BE the number 42;        ^ x is a Number
SET the variable x TO the string "hello";   ^ x is now a String
SET the variable x TO the value of RESPONSE; ^ x takes whatever type RESPONSE holds
```

---

## 2. Built-in Types

MidShake has six built-in value types:

| Type | Description | Literals | Example |
|------|-------------|----------|---------|
| `Number` | Integer or floating-point numeric values | `the number 42`, `the number 3.14`, `42`, `-7` | Arithmetic, comparisons |
| `String` | Sequences of Unicode characters | `the string "hello"`, `"hello"` | Text, file paths |
| `Boolean` | Truth values | `true`, `false` | Conditionals, string checks |
| `List` | Ordered, indexable sequences of values | `[1, 2, 3]`, `["a", "b"]` | Collections, iteration |
| `Map` | Key-value associative arrays | `{name: "Ada", age: 30}` | Structured data |
| `Response` | Special runtime reference | `RESPONSE`, `the RESPONSE` | Holds last function/input result |

### 2.1. Number

Numbers support integer and floating-point representations. The type is determined by the literal:

- `the number 42` → Integer
- `the number 3.14` → Float
- `-7` → Integer (negative)
- `2.5` → Float

Arithmetic operations between integers and floats produce floats.

### 2.2. String

Strings are immutable sequences of characters enclosed in double quotes. Escape sequences are supported:

| Escape | Meaning |
|--------|---------|
| `\n` | Newline |
| `\t` | Tab |
| `\\` | Backslash |
| `\"` | Double quote |

### 2.3. Boolean

Booleans represent truth values and are produced by:

- Comparison expressions (`IS equal to`, `IS greater than`, etc.)
- String check expressions (`the check if ... starts with`, `the check if ... is a digit`, etc.)
- Literals (`true`, `false`)

### 2.4. List

Lists are ordered, zero-indexed sequences that can hold values of mixed types:

```midshake
LET the variable mixed BE [1, "hello", true];
```

Lists support:
- Indexing: `the item at position the number 0 in the value of items`
- Appending: `the append of the number 4 to the value of items`
- Length: `the size of the value of items`

### 2.5. Map

Maps are unordered key-value associations. Keys are strings (or stringifiable identifiers), and values can be any type:

```midshake
LET the variable config BE {name: "MidShake", version: 1};
```

Maps support:
- Value retrieval: `the value of name in config`
- Value setting: `SET the key "name" IN the map config TO the string "NewName"`

### 2.6. Response

The `RESPONSE` type is a special runtime reference that holds the result of the most recent `CALL` or `INQUIRE` operation. It is not a distinct runtime type but a reference to whatever value was last produced. When evaluated, it yields the underlying value's type.

---

## 3. Type Inference

Type inference in MidShake occurs entirely at runtime. The runtime determines the type of an expression based on:

1. **Literal forms**: `the number 42` → Number, `the string "hi"` → String, `true` → Boolean
2. **Variable lookup**: The type of the value currently bound to the variable
3. **Operation results**: Each operation has a defined return type (see Section 4)
4. **Function return**: The type of the expression in the `RETURN` statement

There is no compile-time type checking. Type errors are detected at runtime when an operation receives an incompatible type.

---

## 4. Operation Return Types

### 4.1. Arithmetic Operations

| Operation | Input Types | Return Type |
|-----------|-------------|-------------|
| `plus`, `+` | Number, Number | Number |
| `plus`, `+` | String, any | String (concatenation) |
| `plus`, `+` | any, String | String (concatenation) |
| `minus`, `-` | Number, Number | Number |
| `times`, `*` | Number, Number | Number |
| `multiplied` | Number, Number | Number |
| `divided`, `/` | Number, Number | Number (float) |

**String concatenation:** When either operand of `+` or `plus` is a String, the other operand is automatically converted to its string representation and concatenated.

```midshake
LET the variable result BE the string "Age: " plus the number 25;
^ result is "Age: 25" (String)
```

### 4.2. Comparison Operations

All comparison operations return `Boolean`:

| Operation | Input Types | Return Type |
|-----------|-------------|-------------|
| `IS equal to` | any, any | Boolean |
| `IS not equal to` | any, any | Boolean |
| `IS greater than` | Number, Number | Boolean |
| `IS less than` | Number, Number | Boolean |
| `IS greater than or equal to` | Number, Number | Boolean |
| `IS less than or equal to` | Number, Number | Boolean |

### 4.3. String Function Expressions

| Expression | Return Type |
|------------|-------------|
| `the length of` | Number |
| `the substring of ... starting at ... ending at` | String |
| `the character at ... in` | String (single character) |
| `the split of ... by` | List of Strings |
| `the trimmed` | String |
| `the join of ... with` | String |
| `the replace of ... with ... to` | String |
| `the uppercase of` | String |
| `the lowercase of` | String |
| `the check if ... starts with` | Boolean |
| `the check if ... ends with` | Boolean |
| `the check if ... is a digit` | Boolean |
| `the check if ... is a letter` | Boolean |
| `the check if ... is whitespace` | Boolean |

### 4.4. Math Function Expressions

| Expression | Return Type |
|------------|-------------|
| `the minimum of ... and` | Number |
| `the maximum of ... and` | Number |
| `the absolute value of` | Number |
| `the rounded value of` | Number |

### 4.5. List Operations

| Expression | Return Type |
|------------|-------------|
| `the size of` | Number |
| `the item at position ... in` | any (element type) |
| `the append of ... to` | List |

### 4.6. File I/O

| Expression | Return Type |
|------------|-------------|
| `the content of the file` | String |
| `IN the file ... WRITE` | void (no return value) |

---

## 5. Type Coercion Rules

MidShake performs automatic type coercion in these contexts:

### 5.1. String Concatenation

When `+` or `plus` is used and either operand is a String, the non-string operand is converted to its string representation:

```midshake
LET the variable msg BE the string "Result: " plus the number 42;
^ msg = "Result: 42"
```

### 5.2. Truthiness in Conditionals

In `IF` and `WHILST` conditions, values are evaluated for truthiness:

| Type | Falsy Values | Truthy Values |
|------|-------------|---------------|
| Boolean | `false` | `true` |
| Number | `0` | Any non-zero number |
| String | `""` (empty string) | Any non-empty string |
| List | `[]` (empty list) | Any non-empty list |
| Map | `{}` (empty map) | Any non-empty map |

### 5.3. Input Type Hints

The `INQUIRE` statement accepts a type hint (`string` or `number`), but the actual type conversion is performed by the runtime. If the user enters text that cannot be parsed as a number when `number` is requested, a runtime error occurs.

---

## 6. Type Errors

Type errors occur at runtime when an operation receives an incompatible type. Common type errors include:

| Error | Cause |
|-------|-------|
| Arithmetic on non-numbers | `the string "a" plus the string "b"` (uses concatenation, not error) |
| Arithmetic on non-numbers | `the string "a" minus the number 1` |
| Comparison of incompatible types | `the string "a" IS greater than the string "b"` |
| Index out of bounds | `the item at position the number 5 in [1, 2, 3]` |
| Map key not found | `the value of missingKey in someMap` |
| File not found | `the content of the file "nonexistent.txt"` |

---

## 7. Type System Properties

### 7.1. Dynamic Typing

Types are associated with values, not variables. A variable can hold any type of value at any time.

### 7.2. No Explicit Type Declarations

MidShake has no type annotation syntax. The type of a variable is inferred from the value assigned to it.

### 7.3. User-Defined Classes

The Python interpreter and Python-to-C++ compiler support classes with single inheritance and `Public`, `Private`, and `Protected` members. Values remain dynamically typed; the self-hosted frontend does not yet support class declarations. Structs, enums, and generic types are not supported.

### 7.4. No Generics

Lists and Maps can hold values of any type. There is no syntax for constraining the types of collection elements.

### 7.5. No Null or Optional Types

MidShake has no explicit null or optional type. Uninitialized variables cause a runtime error when accessed. The `RESPONSE` variable before any `CALL` or `INQUIRE` is undefined.

---

## 8. Type System Design Rationale

The MidShake type system is designed for simplicity and readability:

1. **English-like syntax**: Type-related keywords (`the number`, `the string`, `the value of`) make the language readable for beginners.
2. **Dynamic typing**: Eliminates the need for type declarations, reducing boilerplate and making the language accessible.
3. **Automatic coercion**: String concatenation with `+` works intuitively without explicit conversion.
4. **Runtime safety**: Type errors are caught at runtime with descriptive error messages.

The trade-off is the absence of compile-time type checking, which means type errors are only discovered during execution. Future versions of MidShake may add optional static type checking as a compiler phase.
