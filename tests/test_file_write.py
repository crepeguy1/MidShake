import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from midshake_ast import FileWriteStatement
from midshake_parser import Parser
from midshake_runtime import Runtime
from midshake_tokenizer import Tokenizer


class FileWriteTests(unittest.TestCase):
    def test_file_write_statement_is_parsed_and_executes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.txt")
            source = f'IN the file "{path}" WRITE "hello";'

            tokens = Tokenizer(source).tokenize()
            program = Parser(tokens).parse()

            self.assertEqual(len(program.sections[0].body), 1)
            self.assertIsInstance(program.sections[0].body[0], FileWriteStatement)

            Runtime().exec_program(program)

            with open(path, "r", encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "hello")


if __name__ == "__main__":
    unittest.main()
