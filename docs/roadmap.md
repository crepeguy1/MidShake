# MidShake Project Roadmap

This document tracks the development of MidShake toward meeting the requirements of a college-level compiler course project, with the ultimate goal of full self-compilation.

---

## Phase 1: Formalize the Language ✓ **COMPLETE**

Define the language formally so it can be evaluated against academic standards.

- [x] **Formal BNF/EBNF grammar** — `docs/grammar.md` defines the complete lexical and syntax grammar
- [x] **Type system documentation** — `docs/types.md` describes the dynamic type system, built-in types, coercion rules, and type errors
- [x] **Language reference manual** — `docs/language-reference.md` provides comprehensive documentation of every construct, statement, expression, and built-in function
- [x] **Existing syntax guide** — `docs/syntax.md` (pre-existing, supplemented by the new documents)

**Deliverables:**
| Document | File | Status |
|----------|------|--------|
| Formal Grammar | `docs/grammar.md` | ✓ Complete |
| Type System | `docs/types.md` | ✓ Complete |
| Language Reference | `docs/language-reference.md` | ✓ Complete |
| Syntax Guide | `docs/syntax.md` | ✓ Pre-existing |

---

## Phase 2: Add Semantic Analysis

Implement the semantic analysis phase — the biggest gap for a college compiler course.

- [ ] **Symbol table** — Track variable declarations, function definitions, and scope resolution
- [ ] **Type checking** — Catch type errors at compile time (e.g., arithmetic on strings)
- [ ] **Scope resolution** — Verify variable visibility and detect shadowing
- [ ] **Error detection** — Report undeclared variables, duplicate definitions, and type mismatches
- [ ] **Self-hosted semantic analysis** — Port the semantic analyzer to MidShake (`selfhost/`)

**Estimated effort:** 3–5 days

---

## Phase 3: Fix Self-Compilation

Make the self-hosted compiler produce correct, runnable output when compiling itself.

- [ ] **Refine code generator** — Fix `codegen.mish` so the C++ it generates from itself compiles and runs correctly
- [ ] **Expression compilation** — Ensure all expression types (string functions, math, list/map ops) compile to valid C++
- [ ] **Full bootstrap demo** — Python compiler → compiles codegen.mish → codegen.exe → compiles codegen.mish → valid, runnable output
- [ ] **Second self-compiling file** — Compile parser.mish using the self-hosted compiler to prove it's not a one-off

**Estimated effort:** 3–5 days

---

## Phase 4: Build Test Suite

Create systematic tests for each compiler phase.

- [ ] **Lexer tests** — Verify tokenization of all token types, edge cases, and error reporting
- [ ] **Parser tests** — Verify AST construction for all statement and expression types
- [ ] **Semantic analysis tests** — Verify type checking, scope resolution, and error detection
- [ ] **Code generation tests** — Verify C++ output correctness for all constructs
- [ ] **Integration tests** — End-to-end compilation and execution of example programs
- [ ] **Edge case tests** — Nested functions, recursion, complex expressions, empty inputs

**Estimated effort:** 2–3 days

---

## Phase 5: Documentation Polish

Final documentation for presentation and evaluation.

- [ ] **Design document** — Explain architecture decisions, trade-offs, and the deep-copy scope model
- [ ] **Build/run instructions** — Clear README with setup, compilation, and execution steps
- [ ] **Demo presentation** — Show the self-compilation process with screenshots or video
- [ ] **Test coverage report** — Document what is tested and coverage metrics

**Estimated effort:** 1–2 days

---

## Current Compiler Status

| Component | Python | Self-Hosted (`.mish`) | Notes |
|-----------|--------|----------------------|-------|
| Lexer/Tokenizer | ✓ | ✓ | `selfhost/lexer.mish`, `selfhost/tokenizer.mish` |
| Parser (AST) | ✓ | ✓ | `selfhost/parser.mish` |
| Semantic Analysis | ✗ | ✗ | **Phase 2** |
| Interpreter | ✓ | ~ | `selfhost/interpreter.mish` (partial) |
| C++ Code Generator | ✓ | ~ | `selfhost/codegen.mish` (self-parses, output needs refinement) |
| Self-Compilation | — | ~ | Parses itself, generates C++, but self-compiled output not yet runnable |

---

## Language Features Summary

| Feature | Status |
|---------|--------|
| Variables (LET/SET/GLOBAL SET) | ✓ |
| Arithmetic (+, -, *, /) | ✓ |
| Comparisons (IS equal to, IS greater than, etc.) | ✓ |
| Conditionals (IF/THEN/ELSE/END IF) | ✓ |
| While loops (WHILST/DO/END WHILST) | ✓ |
| For-in loops (FOR/IN/DO/END FOR) | ✓ |
| Loop control (BREAK, CONTINUE) | ✓ |
| Functions (DEFINE/CALL/RETURN) | ✓ |
| String operations (length, substring, split, join, etc.) | ✓ |
| String checks (startsWith, isDigit, etc.) | ✓ |
| Math functions (min, max, abs, round) | ✓ |
| Lists (literals, get, append, size) | ✓ |
| Maps (literals, get, set) | ✓ |
| File I/O (read, write) | ✓ |
| Imports | ✓ |
| User input (INQUIRE) | ✓ |
| Type checking | ✗ (Phase 2) |
| Formal grammar | ✓ (Phase 1) |

---

## Timeline

| Phase | Estimated Time | Priority |
|-------|---------------|----------|
| Phase 1: Formalize Language | 1–2 days | **✓ Complete** |
| Phase 2: Semantic Analysis | 3–5 days | Highest |
| Phase 3: Fix Self-Compilation | 3–5 days | Highest |
| Phase 4: Test Suite | 2–3 days | High |
| Phase 5: Documentation Polish | 1–2 days | Medium |
