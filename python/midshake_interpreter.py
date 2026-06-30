# midshake_interpreter.py

from python.midshake_tokenizer import Tokenizer
from python.midshake_parser import Parser
from python.midshake_runtime import Runtime
from python.midshake_interpreter import Interpreter

import re


# ------------------------------------------------------------
# INTERPRETER CLASS
# ------------------------------------------------------------
class Interpreter:
    def __init__(self):
        # Each interpreter instance gets its own runtime
        self.runtime = Runtime()

    def run(self, text: str):
        tokenizer = Tokenizer(text)
        tokens = tokenizer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        self.runtime.exec_program(program)

    def run_file(self, path):
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

        try:
            self.run(full_source)
        except Exception as e:
            print("\n--- MidShake Error ---")
            print(str(e))
            print("----------------------\n")


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

        match = re.search(r"line (\d+)", message)
        line = int(match.group(1)) - 1 if match else 0

        errors.append({
            "line": line,
            "message": message
        })

    return errors


# ------------------------------------------------------------
# CLI ENTRY POINT
# ------------------------------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python midshake_interpreter.py <file.ms>")
        sys.exit(1)

    interpreter = Interpreter()
    interpreter.run_file(sys.argv[1])
