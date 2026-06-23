# midshake_interpreter.py

from midshake_tokenizer import Tokenizer
from midshake_parser import Parser
from midshake_runtime import Runtime
import re


# ------------------------------------------------------------
# RUN A MIDSHAKE PROGRAM FROM TEXT
# ------------------------------------------------------------
def run(text: str):
    tokenizer = Tokenizer(text)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    runtime = Runtime()
    runtime.exec_program(program)
    variables = {}
    
    for t in tokens:
        print(t)


# ------------------------------------------------------------
# ERROR CHECKING FOR LSP / EDITORS
# ------------------------------------------------------------
def check_errors(code):
    errors = []
    try:
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()

        parser = Parser(tokens)
        parser.parse()

    except ValueError as exc:
        message = str(exc)

        # extract line number from error message
        match = re.search(r"line (\d+)", message)
        line = int(match.group(1)) - 1 if match else 0

        errors.append({
            "line": line,
            "message": message
        })

    return errors


# ------------------------------------------------------------
# RUN A MIDSHAKE FILE
# ------------------------------------------------------------
def run_midshake_file(path):
    import os
    print("READING:", path)


    stdlib_path = os.path.join(os.path.dirname(path), "stdlib.ms")
    full_source = ""

    # load stdlib if present
    if os.path.exists(stdlib_path):
        
        with open(stdlib_path, "r") as f:
            full_source += f.read() + "\n"

    # load user file
    with open(path, "r") as f:
        full_source += f.read()
        
        #next part is only needed for debugging
        #with open("debug.txt", "a", encoding="utf-8") as d:
            # Write only the first 200 characters for preview
            #d.write("FILE CONTENT:\n")
            #d.write(full_source[:200] + "\n")
    try:
        run(full_source)
    except Exception as e:
        print("\n--- MidShake Error ---")
        print(str(e))
        print("----------------------\n")




# ------------------------------------------------------------
# CLI ENTRY POINT
# ------------------------------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python midshake_interpreter.py <file.ms>")
        sys.exit(1)

    run_midshake_file(sys.argv[1])
