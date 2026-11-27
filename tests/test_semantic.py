import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from midshake_parser import Parser
from midshake_semantic import SemanticAnalyzer
from midshake_tokenizer import Tokenizer


def main():
    source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_stdlib_native.mish")
    with open(source_path, "r", encoding="utf-8") as source_file:
        program = Parser(Tokenizer(source_file.read()).tokenize()).parse()

    errors = SemanticAnalyzer().analyze(program)
    if errors:
        print(f"  FAIL: Implicit standard-library functions are recognized ({errors})")
        return False

    print("  PASS: Implicit standard-library functions are recognized")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)