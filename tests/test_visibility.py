import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from midshake_interpreter import Interpreter
from midshake_compiler import CppCompiler
from midshake_parser import Parser
from midshake_tokenizer import Tokenizer


class VisibilityTest:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"  PASS: {name}")
        else:
            suffix = f" ({detail})" if detail else ""
            print(f"  FAIL: {name}{suffix}")
            self.failed += 1

    def module_source(self, module_path, body):
        normalized_path = os.path.abspath(module_path).replace("\\", "/")
        return f'IMPORT the file "{normalized_path}";\n{body}'

    def run_all(self):
        print("=== Visibility Tests ===")
        self.test_public_function_can_use_private_members()
        self.test_private_variable_is_inaccessible()
        self.test_private_variable_cannot_be_modified()
        self.test_private_function_is_inaccessible()
        self.test_class_members_enforce_visibility()
        self.test_imported_class_visibility()
        self.test_native_compiler_enforces_visibility()
        print(f"=== Results: {self.passed} passed, {self.failed} failed ===")
        return self.failed == 0

    def test_public_function_can_use_private_members(self):
        with tempfile.TemporaryDirectory() as directory:
            module_path = os.path.join(directory, "account.mish")
            with open(module_path, "w", encoding="utf-8") as module_file:
                module_file.write(
                    "Private LET the variable balance BE the number 41;\n"
                    "Private DEFINE function nextBalance;\n"
                    "    RETURN the value of balance plus the number 1;\n"
                    "END FUNCTION;\n"
                    "Public DEFINE function getNextBalance;\n"
                    "    CALL nextBalance;\n"
                    "    RETURN the RESPONSE;\n"
                    "END FUNCTION;\n"
                )

            interpreter = Interpreter()
            interpreter.run(self.module_source(
                module_path,
                "CALL getNextBalance;\nLET the variable result BE the RESPONSE;",
            ))
            self.check(
                "Public function retains access to its module's Private members",
                interpreter.runtime.vars.get("result") == 42,
                interpreter.runtime.vars.get("result"),
            )

    def test_private_variable_is_inaccessible(self):
        with tempfile.TemporaryDirectory() as directory:
            module_path = os.path.join(directory, "account.mish")
            with open(module_path, "w", encoding="utf-8") as module_file:
                module_file.write("Private LET the variable balance BE the number 41;\n")

            interpreter = Interpreter()
            try:
                interpreter.run(self.module_source(
                    module_path,
                    "PROCLAIM the value of balance;",
                ))
            except ValueError as exc:
                self.check("Private variable access is rejected", "Access Error" in str(exc))
            else:
                self.check("Private variable access is rejected", False, "no error raised")

    def test_private_function_is_inaccessible(self):
        with tempfile.TemporaryDirectory() as directory:
            module_path = os.path.join(directory, "account.mish")
            with open(module_path, "w", encoding="utf-8") as module_file:
                module_file.write(
                    "Private DEFINE function verify;\n"
                    "    RETURN the number 1;\n"
                    "END FUNCTION;\n"
                )

            interpreter = Interpreter()
            try:
                interpreter.run(self.module_source(module_path, "CALL verify;"))
            except ValueError as exc:
                self.check("Private function access is rejected", "Access Error" in str(exc))
            else:
                self.check("Private function access is rejected", False, "no error raised")

    def test_private_variable_cannot_be_modified(self):
        with tempfile.TemporaryDirectory() as directory:
            module_path = os.path.join(directory, "account.mish")
            with open(module_path, "w", encoding="utf-8") as module_file:
                module_file.write("Private LET the variable balance BE the number 41;\n")

            for name, statement in (
                ("SET cannot modify an imported Private variable", "SET the variable balance TO the number 0;"),
                (
                    "GLOBAL SET cannot modify an imported Private variable",
                    "GLOBAL SET the variable balance TO the number 0;",
                ),
            ):
                interpreter = Interpreter()
                try:
                    interpreter.run(self.module_source(module_path, statement))
                except ValueError as exc:
                    self.check(name, "Access Error" in str(exc))
                else:
                    self.check(name, False, "no error raised")

    def test_class_members_enforce_visibility(self):
        fixture_path = os.path.join(os.path.dirname(__file__), "test_class_encapsulation.mish")
        with open(fixture_path, "r", encoding="utf-8") as source_file:
            source = source_file.read()

        interpreter = Interpreter()
        interpreter.run(source)
        self.check(
            "Subclass can call a Protected method that updates a Private field",
            interpreter.runtime.vars.get("RESPONSE") == 1,
            interpreter.runtime.vars.get("RESPONSE"),
        )

        for name, illegal_access in (
            ("Private field access is rejected", "PROCLAIM the value of counter.value;"),
            ("Private method calls are rejected", "CALL counter.readValue;"),
            ("Protected field access is rejected outside the hierarchy", "PROCLAIM the value of counter.tally;"),
            ("Protected method calls are rejected outside the hierarchy", "CALL counter.increase WITH the number 1;"),
        ):
            try:
                Interpreter().run(source + "\n" + illegal_access)
            except ValueError as exc:
                self.check(name, "Access Error" in str(exc), str(exc))
            else:
                self.check(name, False, "no error raised")

    def test_imported_class_visibility(self):
        module_path = os.path.join(os.path.dirname(__file__), "test_class_module.mish")
        public_source = self.module_source(
            module_path,
            "LET the variable counter BE the new Counter;\nCALL counter.read;",
        )
        interpreter = Interpreter()
        interpreter.run(public_source)
        self.check(
            "Imported Public class can be instantiated and called",
            interpreter.runtime.vars.get("RESPONSE") == 5,
            interpreter.runtime.vars.get("RESPONSE"),
        )

        private_source = self.module_source(
            module_path,
            "LET the variable counter BE the new HiddenCounter;",
        )
        try:
            Interpreter().run(private_source)
        except ValueError as exc:
            self.check("Imported Private class cannot be instantiated", "Access Error" in str(exc))
        else:
            self.check("Imported Private class cannot be instantiated", False, "no error raised")

        try:
            program = Parser(Tokenizer(private_source).tokenize()).parse()
            CppCompiler().compile_program(program)
        except ValueError as exc:
            self.check("Native compiler rejects imported Private class", "Private" in str(exc))
        else:
            self.check("Native compiler rejects imported Private class", False, "no error raised")

    def test_native_compiler_enforces_visibility(self):
        with tempfile.TemporaryDirectory() as directory:
            module_path = os.path.join(directory, "account.mish")
            with open(module_path, "w", encoding="utf-8") as module_file:
                module_file.write(
                    "Private LET the variable balance BE the number 41;\n"
                    "Private DEFINE function verify;\n"
                    "    RETURN the number 1;\n"
                    "END FUNCTION;\n"
                    "Public DEFINE function getBalance;\n"
                    "    RETURN the value of balance;\n"
                    "END FUNCTION;\n"
                )

            def compile_source(body):
                source = self.module_source(module_path, body)
                program = Parser(Tokenizer(source).tokenize()).parse()
                return CppCompiler().compile_program(program)

            for name, body, expected_message in (
                (
                    "Native compilation rejects Private variable access",
                    "PROCLAIM the value of balance;",
                    "Variable 'balance' is Private",
                ),
                (
                    "Native compilation rejects Private function calls",
                    "CALL verify;",
                    "Function 'verify' is Private",
                ),
            ):
                try:
                    compile_source(body)
                except ValueError as exc:
                    self.check(name, expected_message in str(exc), str(exc))
                else:
                    self.check(name, False, "no error raised")

            try:
                generated = compile_source("CALL getBalance;")
            except ValueError as exc:
                self.check("Native public function can retain Private module state", False, str(exc))
            else:
                self.check(
                    "Native public function can retain Private module state",
                    'env.set("balance"' in generated and 'env.get("balance")' in generated,
                )


if __name__ == "__main__":
    sys.exit(0 if VisibilityTest().run_all() else 1)