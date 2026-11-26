#!/usr/bin/env python3
"""
Unit tests for the MidShake C++ code generator.
Tests that AST nodes compile to correct C++ code.
"""

import sys
import os

# Add python dir to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from midshake_tokenizer import Tokenizer
from midshake_parser import Parser
from midshake_compiler import CppCompiler


class CodegenTest:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"  PASS: {name}")
        else:
            self.failed += 1
            msg = f"  FAIL: {name}"
            if detail:
                msg += f" ({detail})"
            print(msg)

    def compile(self, code):
        """Helper: tokenize, parse, and compile code to C++."""
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        compiler = CppCompiler()
        return compiler.compile_program(program)

    def run_all(self):
        print("=== Code Generation Unit Tests ===")
        print()
        self.test_let_compilation()
        self.test_set_compilation()
        self.test_proclaim_compilation()
        self.test_if_compilation()
        self.test_if_else_compilation()
        self.test_while_compilation()
        self.test_for_in_compilation()
        self.test_function_compilation()
        self.test_function_scope_and_global_set()
        self.test_call_compilation()
        self.test_user_function_overrides_standard()
        self.test_return_compilation()
        self.test_break_continue()
        self.test_terminate()
        self.test_list_literal()
        self.test_map_literal()
        self.test_binary_expression()
        self.test_main_function()
        self.test_includes()
        self.test_variable_types()
        self.test_nested_compilation()
        print()
        print(f"=== Results: {self.passed} passed, {self.failed} failed ===")
        return self.failed == 0

    def test_let_compilation(self):
        print("[LET Compilation]")
        cpp = self.compile('LET the variable x BE the number 42;')
        self.check("Contains env.set", 'env.set' in cpp)
        self.check("Contains variable name", '"x"' in cpp or "'x'" in cpp)

    def test_set_compilation(self):
        print("[SET Compilation]")
        cpp = self.compile("SET the variable x TO the number 10;")
        self.check("Contains env.set", 'env.set' in cpp)

    def test_proclaim_compilation(self):
        print("[PROCLAIM Compilation]")
        cpp = self.compile('PROCLAIM the string "Hello";')
        self.check("Contains print", 'print(' in cpp)

    def test_if_compilation(self):
        print("[IF Compilation]")
        code = "IF the value of x IS greater than the number 5 THEN\n    PROCLAIM the string \"big\";\nEND IF;"
        cpp = self.compile(code)
        self.check("Contains if statement", 'if (' in cpp or 'if(' in cpp)

    def test_if_else_compilation(self):
        print("[IF/ELSE Compilation]")
        code = "IF the value of x IS greater than the number 5 THEN\n    PROCLAIM the string \"big\";\nELSE\n    PROCLAIM the string \"small\";\nEND IF;"
        cpp = self.compile(code)
        self.check("Contains if", 'if (' in cpp or 'if(' in cpp)
        self.check("Contains else", '} else {' in cpp or 'else {' in cpp or 'else{' in cpp)

    def test_while_compilation(self):
        print("[WHILST Compilation]")
        code = "WHILST the value of i IS less than the number 10 DO\n    PROCLAIM the value of i;\nEND WHILST;"
        cpp = self.compile(code)
        self.check("Contains while", 'while (' in cpp or 'while(' in cpp)

    def test_for_in_compilation(self):
        print("[FOR IN Compilation]")
        code = "FOR the variable item IN the list items DO\n    PROCLAIM the value of item;\nEND FOR;"
        cpp = self.compile(code)
        # FOR IN may compile to while loop with index
        self.check("Generates code", len(cpp) > 100)

    def test_function_compilation(self):
        print("[Function Compilation]")
        code = "DEFINE function greet WITH the parameter name\n    PROCLAIM the value of name;\nEND FUNCTION;"
        cpp = self.compile(code)
        self.check("Contains function definition", 'void greet' in cpp or 'Value greet' in cpp)
        self.check("Contains parameter", 'name' in cpp)

    def test_function_scope_and_global_set(self):
        print("[Function Scope and GLOBAL SET]")
        code = """LET the variable counter BE the number 0;
DEFINE function increment WITH the variable amount;
    GLOBAL SET the variable counter TO the value of counter plus the value of amount;
END FUNCTION;"""
        cpp = self.compile(code)
        self.check("Creates a function-local environment", "Environment env(parent_env);" in cpp)
        self.check("Writes GLOBAL SET to the root environment", 'env.set_global("counter"' in cpp)

    def test_call_compilation(self):
        print("[CALL Compilation]")
        cpp = self.compile('CALL greet WITH the string "Alice";')
        self.check("Contains function call", 'greet(' in cpp)
        self.check("Stores call result in RESPONSE", 'env.set("RESPONSE", ms_std_greet(env, args));' in cpp)

    def test_user_function_overrides_standard(self):
        print("[User Function Override]")
        code = """DEFINE function greet WITH the variable name;
    RETURN the value of name;
END FUNCTION;
CALL greet WITH the string \"Ada\";"""
        cpp = self.compile(code)
        self.check("Calls the user-defined function", 'env.set("RESPONSE", greet(env, args));' in cpp)
        self.check("Does not call the runtime fallback", 'env.set("RESPONSE", ms_std_greet(env, args));' not in cpp)

    def test_return_compilation(self):
        print("[RETURN Compilation]")
        code = "DEFINE function test\n    RETURN the number 42;\nEND FUNCTION;"
        cpp = self.compile(code)
        self.check("Contains return", 'return' in cpp)

    def test_break_continue(self):
        print("[BREAK/CONTINUE Compilation]")
        code = "WHILST the value of i IS less than the number 10 DO\n    BREAK;\nEND WHILST;"
        cpp = self.compile(code)
        self.check("Contains break", 'break;' in cpp)

        code = "WHILST the value of i IS less than the number 10 DO\n    CONTINUE;\nEND WHILST;"
        cpp = self.compile(code)
        self.check("Contains continue", 'continue;' in cpp)

    def test_terminate(self):
        print("[TERMINATE Compilation]")
        cpp = self.compile("TERMINATE the program;")
        self.check("Contains return 0", 'return 0;' in cpp)

    def test_list_literal(self):
        print("[List Literal Compilation]")
        cpp = self.compile("LET the variable items BE [1, 2, 3];")
        self.check("Generates code", len(cpp) > 100)
        self.check("Contains env.set", 'env.set' in cpp)

    def test_map_literal(self):
        print("[Map Literal Compilation]")
        cpp = self.compile('LET the variable person BE {name: "Alice", age: 30};')
        self.check("Generates code", len(cpp) > 100)
        self.check("Contains env.set", 'env.set' in cpp)

    def test_binary_expression(self):
        print("[Binary Expression Compilation]")
        cpp = self.compile("LET the variable sum BE the number 1 plus the number 2;")
        self.check("Generates code", len(cpp) > 100)
        self.check("Contains operator", '+' in cpp)

    def test_main_function(self):
        print("[Main Function]")
        cpp = self.compile('PROCLAIM the string "test";')
        self.check("Contains int main", 'int main' in cpp)
        self.check("Contains Environment", 'Environment env' in cpp)

    def test_includes(self):
        print("[Includes]")
        cpp = self.compile('PROCLAIM the string "test";')
        self.check("Contains include", '#include' in cpp)
        self.check("Contains runtime header", 'midshake_runtime' in cpp)

    def test_variable_types(self):
        print("[Variable Types]")
        # String variable
        cpp = self.compile('LET the variable msg BE the string "Hello";')
        self.check("String variable compiles", 'env.set' in cpp)

        # Number variable
        cpp = self.compile('LET the variable count BE the number 100;')
        self.check("Number variable compiles", 'env.set' in cpp)

    def test_nested_compilation(self):
        print("[Nested Compilation]")
        code = """IF the value of x IS greater than the number 5 THEN
    WHILST the value of i IS less than the number 10 DO
        PROCLAIM the value of i;
    END WHILST;
END IF;"""
        cpp = self.compile(code)
        self.check("Contains if", 'if (' in cpp or 'if(' in cpp)
        self.check("Contains while", 'while (' in cpp or 'while(' in cpp)
        self.check("Generates substantial code", len(cpp) > 200)


if __name__ == "__main__":
    test = CodegenTest()
    success = test.run_all()
    sys.exit(0 if success else 1)
