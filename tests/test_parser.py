#!/usr/bin/env python3
"""
Unit tests for the MidShake parser.
Tests AST construction for all statement and expression types.
"""

import sys
import os

# Add python dir to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from midshake_tokenizer import Tokenizer
from midshake_parser import Parser
from midshake_ast import (
    Program, Section,
    Let, Set, GlobalSet, Proclaim, If, While, Terminate,
    Variable, Binary, Number, String, Response,
    Call, FunctionDef, Return, Import,
    Break, Continue, ForIn, Inquire,
    ListLiteral, MapLiteral, FileWriteStatement
)


class ParserTest:
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

    def parse(self, code):
        """Helper: tokenize and parse code, return Program."""
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def run_all(self):
        print("=== Parser Unit Tests ===")
        print()
        self.test_let_statement()
        self.test_set_statement()
        self.test_global_set_statement()
        self.test_proclaim_statement()
        self.test_if_statement()
        self.test_if_else_statement()
        self.test_while_statement()
        self.test_for_in_statement()
        self.test_function_definition()
        self.test_call_statement()
        self.test_return_statement()
        self.test_break_continue()
        self.test_terminate()
        self.test_import_statement()
        self.test_inquire_statement()
        self.test_list_literal()
        self.test_map_literal()
        self.test_binary_expression()
        self.test_empty_program()
        self.test_multistatement_program()
        self.test_nested_structures()
        self.test_program_structure()
        print()
        print(f"=== Results: {self.passed} passed, {self.failed} failed ===")
        return self.failed == 0

    def test_let_statement(self):
        print("[LET Statement]")
        prog = self.parse('LET the variable x BE the number 42;')
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is Let node", isinstance(section.body[0], Let))
        stmt = section.body[0]
        self.check("Variable name is x", stmt.name == "x")
        self.check("Expression is Number", isinstance(stmt.value, Number))
        self.check("Number value is 42", stmt.value.value == 42)

    def test_set_statement(self):
        print("[SET Statement]")
        prog = self.parse("SET the variable x TO the number 10;")
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is Set node", isinstance(section.body[0], Set))
        stmt = section.body[0]
        self.check("Variable name is x", stmt.name == "x")

    def test_global_set_statement(self):
        print("[GLOBAL SET Statement]")
        prog = self.parse("GLOBAL SET the variable counter TO the number 1;")
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is GlobalSet node", isinstance(section.body[0], GlobalSet))

    def test_proclaim_statement(self):
        print("[PROCLAIM Statement]")
        prog = self.parse('PROCLAIM the string "Hello";')
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is Proclaim node", isinstance(section.body[0], Proclaim))

    def test_if_statement(self):
        print("[IF Statement]")
        code = "IF the value of x IS greater than the number 5 THEN\n    PROCLAIM the string \"big\";\nEND IF;"
        prog = self.parse(code)
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is If node", isinstance(section.body[0], If))

    def test_if_else_statement(self):
        print("[IF/ELSE Statement]")
        code = "IF the value of x IS greater than the number 5 THEN\n    PROCLAIM the string \"big\";\nELSE\n    PROCLAIM the string \"small\";\nEND IF;"
        prog = self.parse(code)
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is If node", isinstance(section.body[0], If))
        stmt = section.body[0]
        self.check("Else body exists", len(stmt.else_body) > 0)

    def test_while_statement(self):
        print("[WHILST Statement]")
        code = "WHILST the value of i IS less than the number 10 DO\n    PROCLAIM the value of i;\nEND WHILST;"
        prog = self.parse(code)
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is While node", isinstance(section.body[0], While))

    def test_for_in_statement(self):
        print("[FOR IN Statement]")
        code = "FOR the variable item IN the list items DO\n    PROCLAIM the value of item;\nEND FOR;"
        prog = self.parse(code)
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is ForIn node", isinstance(section.body[0], ForIn))

    def test_function_definition(self):
        print("[Function Definition]")
        code = "DEFINE function greet WITH the parameter name\n    PROCLAIM the value of name;\nEND FUNCTION;"
        prog = self.parse(code)
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is FunctionDef node", isinstance(section.body[0], FunctionDef))
        func = section.body[0]
        self.check("Function name is greet", func.name == "greet")
        self.check("Has one parameter", len(func.param_names) == 1)
        self.check("Parameter contains name", "name" in func.param_names[0])

    def test_call_statement(self):
        print("[CALL Statement]")
        prog = self.parse('CALL greet WITH the string "Alice";')
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is Call node", isinstance(section.body[0], Call))
        stmt = section.body[0]
        self.check("Function name is greet", stmt.name == "greet")

    def test_return_statement(self):
        print("[RETURN Statement]")
        prog = self.parse("RETURN the number 42;")
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is Return node", isinstance(section.body[0], Return))

    def test_break_continue(self):
        print("[BREAK/CONTINUE]")
        prog = self.parse("BREAK;")
        section = prog.sections[0]
        self.check("BREAK is Break node", isinstance(section.body[0], Break))

        prog = self.parse("CONTINUE;")
        section = prog.sections[0]
        self.check("CONTINUE is Continue node", isinstance(section.body[0], Continue))

    def test_terminate(self):
        print("[TERMINATE]")
        prog = self.parse("TERMINATE the program;")
        section = prog.sections[0]
        self.check("One statement", len(section.body) >= 1)
        self.check("Is Terminate node", isinstance(section.body[0], Terminate))

    def test_import_statement(self):
        print("[IMPORT Statement]")
        prog = self.parse('IMPORT the file "stdlib.mish";')
        section = prog.sections[0]
        self.check("One statement", len(section.body) >= 1)
        self.check("Is Import node", isinstance(section.body[0], Import))

    def test_inquire_statement(self):
        print("[INQUIRE Statement]")
        prog = self.parse('INQUIRE user for the string "Your name?";')
        section = prog.sections[0]
        self.check("One statement", len(section.body) >= 1)
        self.check("Is Inquire node", isinstance(section.body[0], Inquire))

    def test_list_literal(self):
        print("[List Literal]")
        prog = self.parse("LET the variable items BE [1, 2, 3];")
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is Let node", isinstance(section.body[0], Let))
        stmt = section.body[0]
        self.check("Expression is ListLiteral", isinstance(stmt.value, ListLiteral))
        self.check("Three elements", len(stmt.value.elements) == 3)

    def test_map_literal(self):
        print("[Map Literal]")
        prog = self.parse('LET the variable person BE {name: "Alice", age: 30};')
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        self.check("Is Let node", isinstance(section.body[0], Let))
        stmt = section.body[0]
        self.check("Expression is MapLiteral", isinstance(stmt.value, MapLiteral))

    def test_binary_expression(self):
        print("[Binary Expression]")
        prog = self.parse("LET the variable sum BE the number 1 plus the number 2;")
        section = prog.sections[0]
        self.check("One statement", len(section.body) == 1)
        stmt = section.body[0]
        self.check("Expression is Binary", isinstance(stmt.value, Binary))
        self.check("Operator is +", stmt.value.op == "+")

    def test_empty_program(self):
        print("[Empty Program]")
        prog = self.parse("")
        self.check("Has one section", len(prog.sections) == 1)
        self.check("Section body is empty", len(prog.sections[0].body) == 0)

    def test_multistatement_program(self):
        print("[Multi-statement Program]")
        code = """LET the variable x BE the number 1;
SET the variable x TO the number 2;
PROCLAIM the value of x;"""
        prog = self.parse(code)
        section = prog.sections[0]
        self.check("Three statements", len(section.body) == 3)
        self.check("First is Let", isinstance(section.body[0], Let))
        self.check("Second is Set", isinstance(section.body[1], Set))
        self.check("Third is Proclaim", isinstance(section.body[2], Proclaim))

    def test_nested_structures(self):
        print("[Nested Structures]")
        code = """IF the value of x IS greater than the number 5 THEN
    WHILST the value of i IS less than the number 10 DO
        PROCLAIM the value of i;
    END WHILST;
END IF;"""
        prog = self.parse(code)
        section = prog.sections[0]
        self.check("One IF statement", len(section.body) == 1)
        self.check("Is If node", isinstance(section.body[0], If))
        if_stmt = section.body[0]
        self.check("IF body has WHILE", len(if_stmt.body) >= 1)
        self.check("Body contains While", any(isinstance(s, While) for s in if_stmt.body))

    def test_program_structure(self):
        print("[Program Structure]")
        code = 'LET the variable x BE the number 1;'
        prog = self.parse(code)
        self.check("Is Program node", isinstance(prog, Program))
        self.check("Has sections", len(prog.sections) > 0)
        section = prog.sections[0]
        self.check("Is Section node", isinstance(section, Section))
        self.check("Section name is MAIN", section.name == "MAIN")


if __name__ == "__main__":
    test = ParserTest()
    success = test.run_all()
    sys.exit(0 if success else 1)
