import sys
import os

# Import MidShake internals
from python.midshake_tokenizer import Tokenizer
from python.midshake_parser import Parser
from python.midshake_runtime import Runtime
from python.midshake_interpreter import Interpreter




# ------------------------------------------------------------
# Helper: load stdlib.ms automatically
# ------------------------------------------------------------
def load_stdlib(interpreter):
    # stdlib folder will be next to midshake.exe after packaging
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stdlib_path = os.path.join(base_dir, "..", "stdlib", "stdlib.ms")

    if os.path.isfile(stdlib_path):
        with open(stdlib_path, "r", encoding="utf-8") as f:
            source = f.read()

        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter.run(program)


# ------------------------------------------------------------
# Command: run .ms file
# ------------------------------------------------------------
def command_run(path):
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return

    interpreter = Interpreter()

    # Load stdlib first
    load_stdlib(interpreter)

    # Run user file (Interpreter handles tokenizing + parsing)
    interpreter.run_file(path)



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
# Command: help
# ------------------------------------------------------------
def command_help():
    print("MidShake CLI")
    print("")
    print("Usage:")
    print("  midshake run <file.ms>       Run a MidShake program")
    print("  midshake tokens <file.ms>    Show tokens")
    print("  midshake ast <file.ms>       Show AST")
    print("  midshake version             Show version")
    print("  midshake help                Show this help message")
    print("")
    print("Examples:")
    print("  midshake run examples/hello.ms")
    print("  midshake tokens examples/full.ms")
    print("  midshake ast examples/functions.ms")


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
        command_run(sys.argv[2])

    elif command == "tokens":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        command_tokens(sys.argv[2])

    elif command == "ast":
        if len(sys.argv) < 3:
            print("Error: Missing file path.")
            return
        command_ast(sys.argv[2])

    elif command == "version":
        command_version()

    elif command == "help":
        command_help()

    else:
        print(f"Unknown command: {command}")
        command_help()


if __name__ == "__main__":
    main()
