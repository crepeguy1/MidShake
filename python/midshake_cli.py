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
except ModuleNotFoundError:
    python_dir = os.path.join(MEIPASS, "python") if MEIPASS else os.path.join(SCRIPT_DIR)
    if os.path.isdir(python_dir):
        if python_dir not in sys.path:
            sys.path.insert(0, python_dir)
        from midshake_tokenizer import Tokenizer
        from midshake_parser import Parser
        from midshake_runtime import Runtime
        from midshake_interpreter import Interpreter
    else:
        raise




# ------------------------------------------------------------
# Helper: load stdlib.ms automatically
# ------------------------------------------------------------
def load_stdlib(interpreter):
    candidates = [
        os.path.join(os.getcwd(), "stdlib", "stdlib.ms"),
        os.path.join(PROJECT_ROOT, "stdlib", "stdlib.ms"),
        os.path.join(SCRIPT_DIR, "stdlib", "stdlib.ms"),
        os.path.join(MEIPASS, "stdlib", "stdlib.ms") if MEIPASS else "",
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
    try:
        interpreter.run_file(path)
    except Exception:
        return 1
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

import os

def command_tfind(path):
    # 1. Check if the file exists
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}")
        return
        
    # 2. Read the file content
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
        
    # 3. Tokenize the source code
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    
    # 4. Get user input for the target token
    trequest = input("What token would you like to find? ")
    
    # 5. Initialize tracking variables
    count = 0
    found_lines = []
    
    # Split the original text into lines to track line numbers (1-indexed)
    lines = source.splitlines()
    
    # 6. Search through tokens and match with original lines
    # (Assuming your Tokenizer objects or tokens have a .value attribute)
    for token in tokens:
        # Adjust 'token' to 'token.value' if your Tokenizer returns token objects
        if token == trequest: 
            count += 1
            
    # Find the line numbers where the raw text/token appears
    for line_num, line_content in enumerate(lines, start=1):
        if trequest in line_content:
            found_lines.append(str(line_num))
            
    # 7. Print the final summaries (outside the loop)
    print(f"'{trequest}' has been found {count} times.")
    if count > 0:
        print(f"'{trequest}' found on lines: {', '.join(found_lines)}")
    else:
        print(f"'{trequest}' was not found in the file.")

        

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
    print("  midshake run <file.mish>       Run a MidShake program")
    print("  midshake tokens <file.mish>    Show tokens")
    print("  midshake tfind <file.mish>     Find tokens")
    print("  midshake ast <file.mish>       Show AST")
    print("  midshake contents <file.mish>  Show file contents")
    print("  midshake version             Show version")
    print("  midshake help                Show this help message")
    print("")
    print("Examples:")
    print("  midshake run examples/hello.mish")
    print("  midshake tokens examples/full.mish")
    print("  midshake ast examples/functions.mish")


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
