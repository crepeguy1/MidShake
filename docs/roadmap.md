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
- [x] **Self-hosted semantic analysis** — `selfhost/semantic.mish` (277 lines) with symbol table, type inference, and error detection

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
- [x] **map_get safety** — C++ runtime returns empty string for missing keys instead of throwing
- [x] **Semantic analyzer import resolution** — Added self-host globals and stdlib functions to builtins
- [x] **Native bootstrap verification** — The Python seed builds the self-hosted compiler; two native generations match byte-for-byte and pass a recursion/scope smoke test.
- [x] **Self-compiling demo** — `minicodegen.mish` (~300 lines) compiles itself end-to-end, generating 51 lines of C++
- [ ] **Second self-compiling file** — Compile parser.mish using the self-hosted compiler

**What works:**
- Python compiler generates correct C++ for all 16 integration test files → compiles with g++ → runs correctly
- Compiled codegen.exe generates correct C++ for functions.mish, conditionals.mish → compiles and runs
- IF/ELSE branches compile and execute correctly in both directions
- Map literals, function deduplication, and TERMINATE all work
- codegen.mish passes semantic analysis with 0 errors

**Remaining limitations:**
- Native programs still require the shared C++ runtime and a C++17 compiler.
- The self-hosted interpreter and semantic analyzer do not yet match every Python implementation feature.

**Estimated effort:** 3–5 days (core items complete)

---

## Phase 4: Build Test Suite ✓ **COMPLETE**

Create systematic tests for each compiler phase.

- [x] **Test runner** — `tests/run_tests.py` runs unit + integration tests, reports combined results
- [x] **Integration tests** — 16 test files covering all language constructs, all passing
- [x] **Semantic analysis tests** — `test_semantic_errors.mish` validates error detection
- [x] **Lexer unit tests** — `tests/test_lexer.py` (52 tests covering all token types)
- [x] **Parser unit tests** — `tests/test_parser.py` (63 tests covering all AST node types)
- [x] **Code generation unit tests** — `tests/test_codegen.py` (36 tests verifying C++ output)
- [x] **Edge case tests** — Empty input, nested structures, multi-statement programs

**Test results:**
| Category | Tests | Status |
|----------|-------|--------|
| Lexer unit tests | 52 | ✓ All pass |
| Parser unit tests | 63 | ✓ All pass |
| Codegen unit tests | 36 | ✓ All pass |
| Integration tests | 16 | ✓ All pass |
| Semantic error detection | 5 errors | ✓ Detected |
| **Total** | **177** | **✓ 167 pass, 0 fail, 10 skipped** |

**Estimated effort:** 2–3 days (completed)

---

## Phase 5: Documentation Polish ✓ **COMPLETE**

Final documentation for presentation and evaluation.

- [x] **Design document** — `docs/design.md` explains architecture, lexical environment frames, self-compilation strategy, and known limitations
- [x] **Build/run instructions** — README updated with source build instructions, CLI command table, project structure, and compiler pipeline
- [x] **Demo presentation** — `docs/demo.md` shows the self-compilation process with command output evidence
- [x] **Test coverage report** — Roadmap includes test results table; 167 active tests passing, 10 skipped

**Estimated effort:** 1–2 days (complete)

---

## Current Compiler Status

| Component | Python | Self-Hosted (`.mish`) | Notes |
|-----------|--------|----------------------|-------|
| Lexer/Tokenizer | ✓ | ✓ | `selfhost/lexer.mish`, `selfhost/tokenizer.mish` |
| Parser (AST) | ✓ | ✓ | `selfhost/parser.mish` (IF/ELSE body collection) |
| Semantic Analysis | ✓ | ✓ | `python/midshake_semantic.py` (721 lines) + `selfhost/semantic.mish` (277 lines) |
| Interpreter | ✓ | ~ | `selfhost/interpreter.mish` (partial) |
| C++ Code Generator | ✓ | ✓ | `selfhost/codegen.mish` (native bootstrap verified) |
| Self-Compilation | — | ✓ | Python seed → stage 1 → stage 2, identical generated sources |
| Test Suite | ✓ | — | `tests/run_tests.py` (151 unit + 16 integration tests; 10 skipped) |

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
| Phase 3: Fix Self-Compilation | 3–5 days | **✓ Complete** (with known limitations) |
| Phase 4: Test Suite | 2–3 days | **✓ Complete** |
| Phase 5: Documentation Polish | 1–2 days | **✓ Complete** |

## Future Work

The following items remain for future development:

1. **Shared runtime independence** — Replace external C++ runtime dependencies with runtime implementations in MidShake.
2. **Semantic import analysis** — Resolve imported declarations during semantic analysis.
3. **Interpreter parity** — Expand self-hosted interpreter coverage and test it against the Python implementation.
