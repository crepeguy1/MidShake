import os
import sys
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from midshake_ast import Throw, TryCatch
from midshake_compiler import CppCompiler
from midshake_parser import Parser
from midshake_runtime import Runtime, ThrownValue
from midshake_tokenizer import Tokenizer


class ExceptionTest:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"  PASS: {name}")
        else:
            self.failed += 1
            suffix = f" ({detail})" if detail else ""
            print(f"  FAIL: {name}{suffix}")

    @staticmethod
    def parse(source):
        return Parser(Tokenizer(source).tokenize()).parse()

    def run_all(self):
        print("=== Exception Tests ===")
        self.test_parser_and_interpreter()
        self.test_cpp_generation()
        self.test_runtime_errors_are_not_caught()
        self.test_uncaught_value_is_reported()
        self.test_invalid_throw_and_try_syntax()
        print(f"=== Results: {self.passed} passed, {self.failed} failed ===")
        return self.failed == 0

    def test_parser_and_interpreter(self):
        source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_exception_handling.mish")
        with open(source_path, encoding="utf-8") as source_file:
            source = source_file.read()
        program = self.parse(source)
        statements = program.sections[0].body
        try_stmt = statements[1]
        self.check(
            "TRY/CATCH node and thrown value are represented",
            isinstance(try_stmt, TryCatch)
            and isinstance(try_stmt.body[0].catch_body[0], Throw),
        )

        output = StringIO()
        with redirect_stdout(output):
            Runtime().exec_program(program)
        self.check(
            "Thrown values propagate through calls and nested handlers",
            output.getvalue().splitlines() == ["caught across a function call", "execution continued"],
            output.getvalue(),
        )

    def test_cpp_generation(self):
        source = (
            'TRY\n'
            '    THROW the string "native";\n'
            'CATCH the variable problem\n'
            '    PROCLAIM the value of problem;\n'
            'END TRY;\n'
        )
        generated = CppCompiler().compile_program(self.parse(source))
        self.check(
            "Native output catches language throws and reports uncaught values",
            "catch (const ThrownValue& thrown)" in generated
            and "throw ThrownValue(" in generated
            and "Uncaught MidShake exception:" in generated,
        )

    def test_runtime_errors_are_not_caught(self):
        program = self.parse(
            "TRY\n"
            "    PROCLAIM the value of undeclared;\n"
            "CATCH the variable problem\n"
            "    PROCLAIM the string \"incorrectly caught\";\n"
            "END TRY;\n"
        )
        try:
            Runtime().exec_program(program)
        except ValueError as error:
            self.check("Ordinary runtime errors bypass CATCH", "never declared" in str(error))
        else:
            self.check("Ordinary runtime errors bypass CATCH", False, "runtime error was swallowed")

    def test_uncaught_value_is_reported(self):
        try:
            Runtime().exec_program(self.parse('THROW the string "unhandled";'))
        except ThrownValue as error:
            self.check("Uncaught values have a clear diagnostic", "Uncaught MidShake exception: unhandled" in str(error))
        else:
            self.check("Uncaught values have a clear diagnostic", False, "no exception raised")

    def test_invalid_throw_and_try_syntax(self):
        for label, source in (
            ("THROW requires a value", "THROW;"),
            ("TRY requires a CATCH clause", "TRY\nEND TRY;"),
        ):
            try:
                self.parse(source)
            except ValueError:
                self.check(label, True)
            else:
                self.check(label, False, "invalid source parsed successfully")


if __name__ == "__main__":
    success = ExceptionTest().run_all()
    sys.exit(0 if success else 1)