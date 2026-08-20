# midshake_interpreter.py

from midshake_tokenizer import Tokenizer
from midshake_parser import Parser
from midshake_runtime import Runtime
#from python.midshake_interpreter import Interpreter

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

    def run_file(self, path, file_name=None):
        import os

        requested_path = os.fspath(path)
        if file_name is not None:
            requested_path = os.path.join(requested_path, os.fspath(file_name))

        abs_path = os.path.abspath(requested_path)

        if os.path.isdir(abs_path):
            raise IsADirectoryError(
                f"Expected a .ms script file, but got a directory: {requested_path}"
            )

        if not os.path.isfile(abs_path):
            raise FileNotFoundError(f"File not found: {requested_path}")

        stdlib_path = os.path.join(os.path.dirname(abs_path), "stdlib.ms")
        full_source = ""

        # load stdlib if present
        if os.path.exists(stdlib_path):
            with open(stdlib_path, "r", encoding="utf-8") as f:
                full_source += f.read() + "\n"

        # load user file
        with open(abs_path, "r", encoding="utf-8") as f:
            full_source += f.read()

        try:
            self.run(full_source)
        except Exception as exc:
            print("\n--- MidShake Error ---")
            print(str(exc))
            print("----------------------\n")
            raise


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
