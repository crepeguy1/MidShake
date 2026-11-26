import sys
import os

# Make the local project modules importable whether this file is run
# directly from the python/ folder, from the repo root, or from a bundled exe.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEIPASS = getattr(sys, "_MEIPASS", "")

for path in (
    PROJECT_ROOT,
    SCRIPT_DIR,
    os.path.join(MEIPASS, "python") if MEIPASS else "",
    MEIPASS,
):
    if path and os.path.isdir(path) and path not in sys.path:
        sys.path.insert(0, path)

# Import MidShake internals. PyInstaller bundles modules under a temp extraction
# directory, so make sure the python directory is in sys.path before importing.
try:
    from midshake_tokenizer import Tokenizer
    from midshake_parser import Parser
    from midshake_runtime import Runtime
    from midshake_interpreter import Interpreter
    from midshake_compiler import CppCompiler
    from midshake_semantic import SemanticAnalyzer
except ModuleNotFoundError:
    python_dir = os.path.join(MEIPASS, "python") if MEIPASS else os.path.join(SCRIPT_DIR)
    if os.path.isdir(python_dir):
        if python_dir not in sys.path:
            sys.path.insert(0, python_dir)
        from midshake_tokenizer import Tokenizer
        from midshake_parser import Parser
        from midshake_runtime import Runtime
        from midshake_interpreter import Interpreter
        from midshake_compiler import CppCompiler
        from midshake_semantic import SemanticAnalyzer
    else:
        raise




# ------------------------------------------------------------
# Helper: load stdlib.mish automatically
# ------------------------------------------------------------
def load_stdlib(interpreter):
    candidates = [
        os.path.join(os.getcwd(), "stdlib", "stdlib.mish"),
        os.path.join(PROJECT_ROOT, "stdlib", "stdlib.mish"),
        os.path.join(SCRIPT_DIR, "stdlib", "stdlib.mish"),
        os.path.join(MEIPASS, "stdlib", "stdlib.mish") if MEIPASS else "",
    ]
    stdlib_path = next((p for p in candidates if p and os.path.isfile(p)), None)

    if stdlib_path:
        with open(stdlib_path, "r", encoding="utf-8") as f:
            source = f.read()

        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter.runtime.exec_program(program)



# ------------------------------------------------------------
# Command: run .mish file
# ------------------------------------------------------------
def command_run(path):
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return

    interpreter = Interpreter()

    # Load stdlib first
    load_stdlib(interpreter)

    # Run user file (Interpreter handles tokenizing + parsing)
    try:
        interpreter.run_file(path)
    except Exception:
        return 1
    return 0



# ------------------------------------------------------------
# Command: compile .mish file to native executable
# ------------------------------------------------------------
def command_compile(path, output_name=None):
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return

    # 1. Read and parse the MidShake source
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    # 2. Semantic analysis
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(program)
    if errors:
        print(f"Semantic analysis found {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        print("\nProceeding with compilation despite semantic errors...")
    else:
        print("Semantic analysis passed: no errors found.")

    # 3. Compile to C++ source
    compiler = CppCompiler()
    try:
        cpp_source = compiler.compile_program(program)
    except ValueError as exc:
        print(str(exc))
        return 1

    # 3. Determine output directory and names
    out_dir = os.path.join(PROJECT_ROOT, "build", "output")
    os.makedirs(out_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(path))[0]
    if output_name is None:
        output_name = base

    cpp_file = os.path.join(out_dir, f"{output_name}.cpp")
    exe_ext = ".exe"
    exe_file = os.path.join(out_dir, f"{output_name}{exe_ext}")

    # Print symbol table summary
    print(analyzer.get_symbol_table_summary())

    # 4. Write the generated C++ file
    with open(cpp_file, "w", encoding="utf-8") as f:
        f.write(cpp_source)
    print(f"Generated: {cpp_file}")

    # 5. Find the runtime source files
    runtime_dir = os.path.join(PROJECT_ROOT, "selfhost", "runtime")
    runtime_cpp = os.path.join(runtime_dir, "midshake_runtime.cpp")

    # 6. Find g++ compiler
    import shutil
    gpp = shutil.which("g++")
    if gpp is None:
        print("Error: g++ not found in PATH. Install MinGW or MSYS2 to compile C++ output.")
        return

    # 7. Compile with g++
    import subprocess
    cmd = [
        gpp,
        "-std=c++17",
        "-I" + runtime_dir,
        cpp_file,
        runtime_cpp,
        "-o", exe_file
    ]
    print(f"Compiling: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Compilation failed:")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
        return 1

    print(f"Success: {exe_file}")
    return 0


# ------------------------------------------------------------
# Command: print tokens
# ------------------------------------------------------------
def command_tokens(path):
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()

    for t in tokens:
        print(t)

def command_tfind(path):
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()

    trequest = input("What token would you like to find")

    for t in tokens:
        pass

# ------------------------------------------------------------
# Command: print AST
# ------------------------------------------------------------
def command_ast(path):
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    print(program)


# ------------------------------------------------------------
# Command: version
# ------------------------------------------------------------
def command_version():
    print("MidShake 0.1.0 — Experimental Programming Language")


# ------------------------------------------------------------
# Command: highlight (syntax-colored output)
# ------------------------------------------------------------
def command_highlight(path):
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    # Import the highlighter from tools/
    tools_dir = os.path.join(PROJECT_ROOT, "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)

    try:
        from midshake_highlight import highlight
        colored = highlight(source)
        print(colored)
    except ImportError:
        print("Error: Syntax highlighter not found. Make sure tools/midshake_highlight.py exists.")
        return 1
    return 0


# ------------------------------------------------------------
# Command: semantic analysis (check)
# ------------------------------------------------------------
def command_check(path):
    """Run semantic analysis on a MidShake file and report errors."""
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(program)

    # Print results
    analyzer.print_errors()
    print("")
    print(analyzer.get_symbol_table_summary())

    if errors:
        return 1
    return 0


# ------------------------------------------------------------
# Command: help
# ------------------------------------------------------------
def command_help():
    print("MidShake CLI")
    print("")
    print("Usage:")
    print("  midshake run <file.mish>       Run a MidShake program (interpreter)")
    print("  midshake compile <file.mish>   Compile to native executable")
    print("  midshake tokens <file.mish>    Show tokens")
    print("  midshake tfind <file.mish>     Find tokens")
    print("  midshake ast <file.mish>       Show AST")
    print("  midshake check <file.mish>     Run semantic analysis (type checking)")
    print("  midshake contents <file.mish>  Show file contents")
    print("  midshake highlight <file.mish> Show syntax-highlighted code")
    print("  midshake version               Show version")
    print("  midshake help                  Show this help message")
    print("")
    print("Examples:")
    print("  midshake run examples/hello.mish")
    print("  midshake compile examples/hello.mish")
    print("  midshake tokens examples/full.mish")
    print("  midshake ast examples/functions.mish")
    print("  midshake check examples/functions.mish")
    print("  midshake highlight examples/hello.mish")


# ------------------------------------------------------------
# Main CLI entry point
# ------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        command_help()
        return

    command = sys.argv[1]

    if command == "run":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        return command_run(os.path.abspath(sys.argv[2]))

    elif command == "compile":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        path = sys.argv[2]
        output_name = sys.argv[3] if len(sys.argv) >= 4 else None
        return command_compile(path, output_name)

    elif command == "tokens":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        command_tokens(sys.argv[2])
        return 0

        
        
    elif command == "tfind":

        if len(sys.argv) < 3:            
            print("Error: Missing file path.")
            return
        command_tfind(sys.argv[2])
        return 0
    
    elif command == "ast":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        command_ast(sys.argv[2])
        return 0

    elif command == "check":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        return command_check(sys.argv[2])

    # for printing the contents of a file
    elif command == "contents":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        file_path = sys.argv[2]
        if not os.path.isfile(file_path):
            print(f"Error: File not found: {file_path}")
            return
        with open(file_path, "r", encoding="utf-8") as f:
            contents = f.read()
        print(contents)

    elif command == "highlight":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        return command_highlight(sys.argv[2])

    elif command == "version":
        command_version()
        return 0

    elif command == "help":
        command_help()
        return 0

    else:
        print(f"Unknown command: {command}")
        command_help()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
