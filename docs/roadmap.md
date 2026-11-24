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

## Phase 2: Add Semantic Analysis ✓ **COMPLETE**

Implement the semantic analysis phase — the biggest gap for a college compiler course.

- [x] **Symbol table** — `python/midshake_semantic.py` tracks variable declarations, function definitions, and scope resolution
- [x] **Type inference** — Infers types for all expression types (literals, variables, binary ops, string/math/list/map functions)
- [x] **Variable declaration checking** — Detects undeclared variables, duplicate declarations, SET without LET
- [x] **Function validation** — Checks that called functions are defined, validates RETURN/BREAK/CONTINUE context
- [x] **Scope resolution** — Nested scopes for global, function, block, and loop levels with parent chain lookup
- [x] **CLI integration** — `midshake check <file>` command for standalone semantic analysis
- [x] **Compile pipeline integration** — Semantic analysis runs automatically during `midshake compile`
- [ ] **Self-hosted semantic analysis** — Port the semantic analyzer to MidShake (`selfhost/`)

**Deliverables:**
| Component | File | Status |
|-----------|------|--------|
| Semantic Analyzer | `python/midshake_semantic.py` | ✓ Complete (697 lines) |
| CLI Command | `python/midshake_cli.py` (check) | ✓ Integrated |
| Compile Pipeline | `python/midshake_cli.py` (compile) | ✓ Integrated |
| Compile Script | `python/midshake_compile.py` | ✓ Integrated |
| Error Test | `tests/test_semantic_errors.mish` | ✓ Created |

**Error types detected:**
- Undeclared variable usage
- Duplicate variable declaration
- SET without prior LET
- RETURN outside function
- BREAK/CONTINUE outside loop
- Undefined function calls
- Invalid INQUIRE type hints

**Estimated effort:** 3–5 days (completed in 1 day)

---

## Phase 3: Fix Self-Compilation ✓ **COMPLETE**

Make the self-hosted compiler produce correct, runnable output when compiling itself.

- [x] **Bootstrap chain** — Python compiler → compiles codegen.mish → codegen.exe → compiles simple programs → valid C++
- [x] **Binary expression compilation** — Added `X plus Y` and `X minus Y` handling in compileExpr
- [x] **Recursive condition compilation** — compileCondition now compiles sub-expressions to C++
- [x] **Condition THEN stripping** — Fixed condition parsing to strip trailing `THEN` keywords
- [x] **CLI compile pipeline** — Fixed include paths so `midshake compile` links against the correct runtime
- [x] **IF/ELSE handling** — Parser collects ELSE body, codegen generates C++ else branches
- [x] **TERMINATE fix** — Generates `return 0;` instead of `return Value::from_double(0);`
- [x] **Function deduplication** — Later function definitions override imported ones
- [x] **Map literal keys** — Bare identifiers treated as string literals in map literals
- [ ] **Full self-compilation** — codegen.exe compiling itself still hangs (self-hosted parser limitation with 800+ line files)
- [ ] **Second self-compiling file** — Compile parser.mish using the self-hosted compiler

**What works:**
- Python compiler generates correct C++ for all 15 test files → compiles with g++ → runs correctly
- Compiled codegen.exe generates correct C++ for functions.mish, conditionals.mish → compiles and runs
- IF/ELSE branches compile and execute correctly in both directions
- Map literals, function deduplication, and TERMINATE all work

**Remaining blockers:**
- Self-hosted parser hangs on 800+ line files (codegen.mish itself)
- Array index float formatting (`args[0.000000]` instead of `args[0]`)

**Estimated effort:** 3–5 days (core items complete)

---

## Phase 4: Build Test Suite **IN PROGRESS**

Create systematic tests for each compiler phase.

- [x] **Test runner** — `tests/run_tests.py` compiles and runs all .mish test files, reports pass/fail
- [x] **Integration tests** — 15 test files covering all language constructs, all passing
- [x] **Semantic analysis tests** — `test_semantic_errors.mish` validates error detection
- [ ] **Lexer unit tests** — Verify tokenization of all token types, edge cases, and error reporting
- [ ] **Parser unit tests** — Verify AST construction for all statement and expression types
- [ ] **Code generation unit tests** — Verify C++ output correctness for all constructs
- [ ] **Edge case tests** — Nested functions, recursion, complex expressions, empty inputs

**Test coverage:**
| Category | Tests | Status |
|----------|-------|--------|
| Collections (lists, maps) | test_collections.mish | ✓ Pass |
| GLOBAL SET | test_global_set.mish | ✓ Pass |
| IF/ELSE | test_if_else.mish | ✓ Pass |
| CONTINUE | test_continue.mish | ✓ Pass |
| Function calls | test_function_calls.mish | ✓ Pass |
| Imports | test_import.mish | ✓ Pass |
| Maps | test_map.mish, test_map_global.mish, test_map_nested.mish | ✓ Pass |
| New features | test_new_features.mish | ✓ Pass |
| Parameters | test_params.mish | ✓ Pass |
| Recursion | test_recursion.mish | ✓ Pass |
| Simple calls | test_simple_call.mish | ✓ Pass |
| String checks | test_startswith.mish | ✓ Pass |
| While loops | test_while_simple.mish | ✓ Pass |
| Semantic errors | test_semantic_errors.mish | ✓ Detected |

**Estimated effort:** 2–3 days (test runner + integration tests complete)

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
| Parser (AST) | ✓ | ✓ | `selfhost/parser.mish` (IF/ELSE body collection) |
| Semantic Analysis | ✓ | ✗ | `python/midshake_semantic.py` (symbol table, type inference, scope resolution) |
| Interpreter | ✓ | ~ | `selfhost/interpreter.mish` (partial) |
| C++ Code Generator | ✓ | ~ | `selfhost/codegen.mish` (functions, IF/ELSE, binary expressions) |
| Self-Compilation | — | ~ | Python compiler → codegen.exe → compiles simple programs; full self-compilation in progress |
| Test Suite | ✓ | — | `tests/run_tests.py` (15 integration tests, all passing) |

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
| Type checking | ✓ (Phase 2) |
| Formal grammar | ✓ (Phase 1) |

---

## Timeline

| Phase | Estimated Time | Priority |
|-------|---------------|----------|
| Phase 1: Formalize Language | 1–2 days | **✓ Complete** |
| Phase 2: Semantic Analysis | 3–5 days | **✓ Complete** |
| Phase 3: Fix Self-Compilation | 3–5 days | Highest |
| Phase 4: Test Suite | 2–3 days | High |
| Phase 5: Documentation Polish | 1–2 days | Medium |
