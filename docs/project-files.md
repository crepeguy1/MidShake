# MidShake Project File Guide

This guide describes the purpose of the project's maintained source, documentation, examples, tests, and support files. It also identifies generated and legacy files so they are not confused with the compiler's authoritative sources.

## How the project fits together

The main Python toolchain in `python/` tokenizes `.mish` source, parses it into the AST, performs semantic checks, then either interprets it or generates C++ for native compilation. The self-hosted implementation in `selfhost/` contains MidShake versions of the tokenizer, lexer, parser, semantic analyzer, interpreter, and C++ code generator. Generated native programs link to the shared C++ runtime in `selfhost/runtime/`. The regression tests are in `tests/`, the language and architecture references are in `docs/`, and `tools/bootstrap.py` verifies successive native compiler generations.

## Project root

| File | Purpose |
| --- | --- |
| `README.md` | Project introduction, prerequisites, quick start, CLI command overview, test instructions, and self-compilation workflow. |
| `RELEASE.md` | Release notes, claimed feature status, test summary, and release-oriented usage information. |
| `LICENSE` | License terms for the project. |
| `.gitignore` | Excludes generated build directories, caches, local environments, and other listed transient files from Git. |
| `.gitattributes` | Defines text normalization and line-ending rules for source, documentation, and editor syntax files. |
| `midshake.spec` | PyInstaller configuration for packaging `python/midshake_cli.py` and its runtime data as the standalone `midshake.exe`. |
| `MyProgram.mish` | Small root-level interactive file-I/O example; asks for a name, writes text to `tests/text.txt`, and prints a completion message. |
| `midshake.exe` | Packaged Windows CLI executable. It is a distribution artifact, not the source implementation. |
| `the value of trimmedPath` | Empty file in the current tree; no source, documentation, or runtime role is apparent. |

## Python implementation (`python/`)

| File | Purpose |
| --- | --- |
| `python/__init__.py` | Empty package marker for Python tooling that imports the directory as a package. |
| `python/midshake_ast.py` | Defines the AST data classes for expressions, statements, functions, visibility, and program sections. |
| `python/midshake_tokenizer.py` | Splits source into statements, recognizes MidShake constructs, and produces the token objects consumed by the parser. It also parses the expression forms embedded in statements. |
| `python/midshake_parser.py` | Turns statement tokens into a `Program` AST, including nested control-flow and function bodies. |
| `python/midshake_semantic.py` | Performs symbol and scope analysis, type inference, and semantic error checks before compilation. |
| `python/midshake_runtime.py` | Implements execution of AST statements and expressions, including variables, function calls, imports, collections, and I/O. |
| `python/midshake_interpreter.py` | Public interpreter wrapper: tokenizes, parses, and executes source or a file; also exposes syntax-error checking used by the language server. |
| `python/midshake_compiler.py` | Converts the Python AST into C++ that uses the shared MidShake runtime; handles imports, function definitions/calls, and expression/statement code generation. |
| `python/midshake_cli.py` | Main Python command-line interface for running, checking, inspecting, highlighting, and compiling MidShake programs. Its `compile` command writes generated files under `build/` and invokes a native compiler. |
| `python/midshake_lsp.py` | Minimal standard-library-only Language Server Protocol process that publishes tokenizer/parser diagnostics to an editor. |
| `python/midshake_compile.py` | Older interactive helper that selects an example, runs the parse/semantic/code-generation pipeline, and writes C++ under `cpp/`; the main supported CLI is `midshake_cli.py`. |
| `python/midshake.py` | Early, limited line-oriented interpreter prototype. It is not the complete interpreter or the recommended CLI entry point. |

## Self-hosted compiler (`selfhost/`)

| File | Purpose |
| --- | --- |
| `selfhost/README.md` | Explains the self-hosting goal, current implementation status, bootstrap command, runtime requirement, and directory layout. |
| `selfhost/ROADMAP.md` | Earlier high-level roadmap covering language polish, library growth, tooling, modules, and runtime/compiler improvements. |
| `selfhost/tokenizer.mish` | MidShake implementation of a line/statement-oriented tokenizer used in the self-hosted toolchain. |
| `selfhost/lexer.mish` | MidShake character-level lexer that scans source text and produces lexical tokens. |
| `selfhost/parser.mish` | MidShake implementation of the parser; constructs nested AST data for statements, expressions, and blocks. |
| `selfhost/semantic.mish` | Self-hosted semantic-analysis implementation, including symbol/type tracking and checks. |
| `selfhost/interpreter.mish` | Self-hosted AST interpreter for executing parsed MidShake programs. |
| `selfhost/codegen.mish` | Main self-hosted C++ code generator. It parses source through the self-hosted parser and emits C++ that links to `selfhost/runtime/`. |
| `selfhost/fixtures/*.mish` | Imported-module visibility regressions for public access and denied private reads, writes, function calls, and class construction. |
| `selfhost/minicodegen.mish` | Smaller compiler demonstration used to exercise the self-compilation idea independently of the full code generator. |
| `selfhost/compiler/midshake_compiler.py` | Earlier/reference Python C++ generator retained alongside the MidShake implementation; it is separate from the current `python/midshake_compiler.py` CLI path. |
| `selfhost/tools/midshake_highlight.py` | Earlier syntax-highlighting implementation and vocabulary lists associated with the self-hosted tooling. |

### Self-hosted examples

| File | Purpose |
| --- | --- |
| `selfhost/examples/fileio.mish` | Demonstrates file-reading and file-writing operations. |
| `selfhost/examples/lists.mish` | Demonstrates list creation and list operations. |
| `selfhost/examples/maps.mish` | Demonstrates map creation, lookup, and mutation. |
| `selfhost/examples/math.mish` | Demonstrates math helper functions. |
| `selfhost/examples/strings.mish` | Demonstrates common string operations. |
| `selfhost/examples/stringutils.mish` | Demonstrates character and string utility operations. |

### Native runtime (`selfhost/runtime/`)

| File | Purpose |
| --- | --- |
| `selfhost/runtime/midshake_runtime_types.hpp` | Defines C++ runtime values and their number, string, list, and map representations, plus basic conversions/operators. |
| `selfhost/runtime/midshake_runtime.hpp` | Declares the C++ runtime API and `Environment`, including variable lookup, parent-linked function frames, global assignment, standard-library entry points, and I/O helpers. |
| `selfhost/runtime/midshake_runtime.cpp` | Implements runtime printing, input, file operations, value/collection/string/math helpers, and C++ bindings for standard-library calls. |
| `selfhost/runtime/stdlib.hpp` | Contains older hand-written C++ implementations of a few standard-library functions; current generated-code support is primarily declared/implemented through the shared runtime. |

## Standard library (`stdlib/`)

| File | Purpose |
| --- | --- |
| `stdlib/stdlib.mish` | MidShake-level library functions for printing, greetings, math, strings, lists, maps, and file reading. The interpreter and native compiler may provide corresponding built-ins through their respective runtimes. |

## Command-line tools (`tools/`)

| File | Purpose |
| --- | --- |
| `tools/bootstrap.py` | Builds the Python-seeded compiler, compiles and runs native self-hosted compiler generations, compares their generated C++, and verifies scope, classes, base constructors, and module visibility. Outputs are placed under `build/`. |
| `tools/inspect_tokens.py` | Prints the tokens produced from a selected `.mish` file; useful when diagnosing tokenization. |
| `tools/midshake_highlight.py` | Applies ANSI terminal colors to MidShake source for quick command-line inspection. |

## Documentation (`docs/`)

| File | Purpose |
| --- | --- |
| `docs/project-files.md` | This file: catalog of significant project files and their roles. |
| `docs/design.md` | Explains the compiler pipeline, AST, scopes/runtime frames, bootstrap approach, testing strategy, and known limitations. |
| `docs/demo.md` | Walkthrough of the self-compilation demonstration and its commands/evidence. |
| `docs/examples.md` | Collects readable language examples and explains their intended use. |
| `docs/grammar.md` | Formal EBNF grammar for the MidShake language. |
| `docs/language-reference.md` | Detailed reference for language statements, expressions, and built-in operations. |
| `docs/roadmap.md` | Project-level roadmap for language/toolchain development. |
| `docs/semantic-analysis.md` | Describes the static semantic-analysis phase, its symbol/scoping model, inferred types, and diagnostics. |
| `docs/stdlib_reference.md` | User-facing overview of standard-library functions and the library's intended direction. |
| `docs/syntax.md` | Introductory guide to the English-like MidShake syntax. |
| `docs/types.md` | Describes MidShake's value types, dynamic behavior, inference, and coercion. |

## User examples (`examples/`)

These `.mish` files are runnable examples rather than compiler implementation files.

| File | Purpose |
| --- | --- |
| `examples/hello.mish` | Minimal starter/output example. |
| `examples/functions.mish` | Demonstrates defining and calling functions. |
| `examples/conditionals.mish` | Demonstrates conditional branches. |
| `examples/controlflow.mish` | Demonstrates control-flow constructs. |
| `examples/user_input.mish` | Demonstrates prompting for and using user input. |
| `examples/using_stdlib.mish` | Demonstrates calls to standard-library helpers. |
| `examples/stdlib.mish` | Example program focused on standard-library use. |
| `examples/bank.mish` | Small banking/account-style program example. |
| `examples/full.mish` | Broader example combining multiple language features. |
| `examples/main.mish` | Main/combined program example. |
| `examples/test.mish` | Small test or scratch program used during development. |
| `examples/error.mish` | Example input for demonstrating error behavior. |

## Tests and fixtures (`tests/`)

| File | Purpose |
| --- | --- |
| `tests/run_tests.py` | Main test runner; executes Python unit tests, compiles selected `.mish` integration cases, and checks their output. Native integration runs require a C++17 compiler. |
| `tests/test_all.bat` | Legacy Windows batch runner with machine-specific hard-coded paths; it is not the portable/current test entry point. |
| `tests/test_lexer.py` | Unit tests for Python tokenization. |
| `tests/test_parser.py` | Unit tests for Python parsing and AST construction. |
| `tests/test_codegen.py` | Unit tests for Python-to-C++ generation. |
| `tests/test_file_write.py` | Python unit test for parsing and executing file-write statements. |
| `tests/test_bootstrap_scope.mish` | Smoke program covering recursive calls, local scope, and global updates in the native bootstrap. |
| `tests/test_class_encapsulation.mish` | Integration coverage for public, private, and protected class-member access. |
| `tests/test_class_module.mish` | Integration coverage for defining and using a class from an imported module. |
| `tests/test_collections.mish` | Integration coverage for list/map and collection behavior. |
| `tests/test_continue.mish` | Integration input for `CONTINUE` loop behavior. |
| `tests/test_function_calls.mish` | Integration coverage for user-defined function calls. |
| `tests/test_global_set.mish` | Integration coverage for updating global variables from functions. |
| `tests/test_if_else.mish` | Integration coverage for conditional and `ELSE` branches. |
| `tests/test_import.mish` | Integration input for importing MidShake files. |
| `tests/test_imported_class.mish` | Integration input for importing a class and invoking its members. |
| `tests/test_map.mish` | Integration input for basic map operations. |
| `tests/test_map_global.mish` | Integration input for map operations involving global state. |
| `tests/test_map_nested.mish` | Integration input for nested maps/collection values. |
| `tests/test_new_features.mish` | Integration input covering a collection of newer language features. |
| `tests/test_params.mish` | Integration input for function parameters. |
| `tests/test_recursion.mish` | Integration input for recursive function calls. |
| `tests/test_simple_call.mish` | Minimal function-call integration case. |
| `tests/test_selfhost_classes.mish` | Self-hosted compiler regression for inheritance, constructor forwarding, and member visibility. |
| `tests/test_startswith.mish` | Integration input for the string `startsWith` operation. |
| `tests/test_while_simple.mish` | Integration input for a basic `WHILST` loop. |
| `tests/test_semantic_errors.mish` | Intentionally invalid source used to exercise semantic diagnostics; the main integration runner skips it. |
| `tests/test_parse_20_30.mish` | Legacy parser/debug fixture; currently skipped by the main integration runner. |
| `tests/test_parse_codegen.mish` | Legacy parser/code-generator fixture; currently skipped by the main integration runner. |
| `tests/test_parse_first20.mish` | Legacy parser/debug fixture; currently skipped by the main integration runner. |
| `tests/test_parse_full.mish` | Legacy full-input parser/debug fixture; currently skipped by the main integration runner. |
| `tests/test_parse_func.mish` | Legacy function-parsing fixture; currently skipped by the main integration runner. |
| `tests/test_parse_line20.mish` | Legacy parser/debug fixture; currently skipped by the main integration runner. |
| `tests/test_parse_line25.mish` | Legacy parser/debug fixture; currently skipped by the main integration runner. |
| `tests/test_parse_loop.mish` | Legacy loop-parsing fixture; currently skipped by the main integration runner. |
| `tests/test_parse_step.mish` | Legacy parser/debug fixture; currently skipped by the main integration runner. |
| `tests/test_fileio_data.txt` | Multi-line input data used by file-I/O tests/examples. |
| `tests/text.txt` | File-I/O output target used by `MyProgram.mish`. |
| `tests/number_output.txt` | Small numeric output fixture. |
| `tests/output_test.txt` | Small text output fixture. |
| `tests/combined_test.txt` | Small combined/multi-part text fixture. |

## Editor support (`ide/`)

These files provide syntax coloring/editor metadata; they do not implement parsing or compilation.

| File | Purpose |
| --- | --- |
| `ide/README.md` | Overview/instructions for the available editor syntax support. |
| `ide/atom/grammar.json` | Atom grammar for highlighting MidShake syntax. |
| `ide/intellij/README.md` | Instructions for installing/configuring the IntelliJ-family syntax definition. |
| `ide/intellij/Syntaxes/midshake.tmLanguage.json` | TextMate grammar used by the IntelliJ syntax package. |
| `ide/intellij/Syntaxes/midshake.tmPreferences` | TextMate scope/editor preferences associated with the grammar. |
| `ide/intellij/info.plist` | Bundle metadata for the IntelliJ/TextMate syntax definition. |
| `ide/sublime/midshake.sublime-syntax` | Sublime Text syntax definition. |
| `ide/vim/midshake.vim` | Vim syntax-highlighting rules. |

## Experimental C++ binding (`bindings/`)

| File | Purpose |
| --- | --- |
| `bindings/CMakeLists.txt` | CMake configuration for a pybind11 module using C++17. |
| `bindings/midshake_bindings.cpp` | Exposes tokenization and parsing functions from an older C++ engine to Python. The current tree does not contain the `cpp/midshake_engine.cpp` and related engine header referenced by this scaffold, so it is not part of the verified compiler path. |

## Generated and distribution artifacts

| Path | Purpose / guidance |
| --- | --- |
| `build/` | Ignored directory for compiler outputs, bootstrap generations, and temporary generated C++ files. It is reproducible and is not source-of-truth. |
| `cpp/output/` | Contains checked-in/generated C++ program outputs and compiled executables from earlier runs. These are outputs of the compiler, not the implementation to edit; regenerate from `.mish` sources when needed. |
| `cpp/full.cpp` | Older standalone generated-C++ example for a program using the C++ runtime and standard library. |
| `output/generated.cpp` | Generated C++ output written by the self-hosted compiler's default output path. |
| `output.txt` | Captured text output from an earlier program run; not a compiler input. |
| `dist/midshake.exe` | Packaged executable distribution artifact. |

For normal development, start with `README.md`, use `python/midshake_cli.py` for language commands, run `python tests/run_tests.py` for regression tests, and use `python tools/bootstrap.py` to verify the self-hosting chain.