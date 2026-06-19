# midshake_interpreter.py

from midshake_tokenizer import Tokenizer
from midshake_parser import Parser
from midshake_runtime_stub import Runtime


def run(text: str):
    tokenizer = Tokenizer(text)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    runtime = Runtime()
    runtime.exec_program(program)


def run_midshake_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    run(text)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python midshake_interpreter.py <file.ms>")
        sys.exit(1)

    run_midshake_file(sys.argv[1])
