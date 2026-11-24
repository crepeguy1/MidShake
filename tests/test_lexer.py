#!/usr/bin/env python3
"""
Unit tests for the MidShake lexer/tokenizer.
Tests tokenization of all token types, edge cases, and multi-line input.
"""

import sys
import os

# Add python dir to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from midshake_tokenizer import Tokenizer


class LexerTest:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

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

    def run_all(self):
        print("=== Lexer/Tokenizer Unit Tests ===")
        print()
        self.test_number_literals()
        self.test_string_literals()
        self.test_let_statement()
        self.test_set_statement()
        self.test_global_set_statement()
        self.test_proclaim_statement()
        self.test_if_statement()
        self.test_while_statement()
        self.test_for_in_statement()
        self.test_function_definition()
        self.test_call_statement()
        self.test_return_statement()
        self.test_break_continue()
        self.test_terminate()
        self.test_import_statement()
        self.test_inquire_statement()
        self.test_comments()
        self.test_empty_input()
        self.test_multiline_input()
        self.test_list_literal()
        self.test_map_literal()
        self.test_binary_expressions()
        self.test_file_write()
        print()
        print(f"=== Results: {self.passed} passed, {self.failed} failed ===")
        return self.failed == 0

    def test_number_literals(self):
        print("[Number Literals]")
        t = Tokenizer("LET the variable x BE the number 42;")
        tokens = t.tokenize()
        self.check("Single LET tokenizes", len(tokens) >= 1)
        self.check("LET type present", any(tok.type == "LET" for tok in tokens))

        t = Tokenizer("LET the variable y BE the number 3.14;")
        tokens = t.tokenize()
        self.check("Float number tokenizes", len(tokens) >= 1)

    def test_string_literals(self):
        print("[String Literals]")
        t = Tokenizer('PROCLAIM the string "Hello World";')
        tokens = t.tokenize()
        self.check("String literal tokenizes", len(tokens) >= 1)
        self.check("PROCLAIM type present", any(tok.type == "PROCLAIM" for tok in tokens))

        t = Tokenizer('LET the variable msg BE the string "escaped \\" quote";')
        tokens = t.tokenize()
        self.check("Escaped quotes in string", len(tokens) >= 1)

    def test_let_statement(self):
        print("[LET Statement]")
        t = Tokenizer("LET the variable name BE the string \"Alice\";")
        tokens = t.tokenize()
        self.check("LET statement tokenizes", len(tokens) == 1)
        self.check("LET type", tokens[0].type == "LET")
        name, expr = tokens[0].value
        self.check("Variable name extracted", name == "name")

    def test_set_statement(self):
        print("[SET Statement]")
        t = Tokenizer("SET the variable x TO the number 10;")
        tokens = t.tokenize()
        self.check("SET statement tokenizes", len(tokens) == 1)
        self.check("SET type", tokens[0].type == "SET")

    def test_global_set_statement(self):
        print("[GLOBAL SET Statement]")
        t = Tokenizer("GLOBAL SET the variable counter TO the number 1;")
        tokens = t.tokenize()
        self.check("GLOBAL SET tokenizes", len(tokens) == 1)
        self.check("GLOBAL_SET type", tokens[0].type == "GLOBAL_SET")

    def test_proclaim_statement(self):
        print("[PROCLAIM Statement]")
        t = Tokenizer("PROCLAIM the value of x;")
        tokens = t.tokenize()
        self.check("PROCLAIM tokenizes", len(tokens) == 1)
        self.check("PROCLAIM type", tokens[0].type == "PROCLAIM")

    def test_if_statement(self):
        print("[IF Statement]")
        t = Tokenizer("IF the value of x IS greater than the number 5 THEN\n    PROCLAIM the string \"big\";\nEND IF;")
        tokens = t.tokenize()
        self.check("IF statement tokenizes", len(tokens) >= 1)
        self.check("IF type present", any(tok.type == "IF" for tok in tokens))

    def test_while_statement(self):
        print("[WHILST Statement]")
        t = Tokenizer("WHILST the value of i IS less than the number 10 DO\n    PROCLAIM the value of i;\nEND WHILST;")
        tokens = t.tokenize()
        self.check("WHILST statement tokenizes", len(tokens) >= 1)
        self.check("WHILST type present", any(tok.type == "WHILST" for tok in tokens))

    def test_for_in_statement(self):
        print("[FOR IN Statement]")
        t = Tokenizer("FOR the variable item IN the list items DO\n    PROCLAIM the value of item;\nEND FOR;")
        tokens = t.tokenize()
        self.check("FOR IN statement tokenizes", len(tokens) >= 1)
        self.check("FOR_IN type present", any(tok.type == "FOR_IN" for tok in tokens))

    def test_function_definition(self):
        print("[Function Definition]")
        t = Tokenizer("DEFINE function greet WITH the parameter name\n    PROCLAIM the value of name;\nEND FUNCTION;")
        tokens = t.tokenize()
        self.check("Function def tokenizes", len(tokens) >= 1)
        self.check("FUNC_DEF type present", any(tok.type == "FUNC_DEF" for tok in tokens))

    def test_call_statement(self):
        print("[CALL Statement]")
        t = Tokenizer('CALL greet WITH the string "Alice";')
        tokens = t.tokenize()
        self.check("CALL statement tokenizes", len(tokens) >= 1)
        self.check("CALL type present", any(tok.type == "CALL" for tok in tokens))

    def test_return_statement(self):
        print("[RETURN Statement]")
        t = Tokenizer("RETURN the number 42;")
        tokens = t.tokenize()
        self.check("RETURN tokenizes", len(tokens) == 1)
        self.check("RETURN type", tokens[0].type == "RETURN")

    def test_break_continue(self):
        print("[BREAK/CONTINUE]")
        t = Tokenizer("BREAK;")
        tokens = t.tokenize()
        self.check("BREAK tokenizes", len(tokens) == 1)
        self.check("BREAK type", tokens[0].type == "BREAK")

        t = Tokenizer("CONTINUE;")
        tokens = t.tokenize()
        self.check("CONTINUE tokenizes", len(tokens) == 1)
        self.check("CONTINUE type", tokens[0].type == "CONTINUE")

    def test_terminate(self):
        print("[TERMINATE]")
        t = Tokenizer("TERMINATE the program;")
        tokens = t.tokenize()
        self.check("TERMINATE tokenizes", len(tokens) >= 1)
        self.check("TERMINATE type present", any(tok.type == "TERMINATE" for tok in tokens))

    def test_import_statement(self):
        print("[IMPORT Statement]")
        t = Tokenizer('IMPORT the file "stdlib.mish";')
        tokens = t.tokenize()
        self.check("IMPORT tokenizes", len(tokens) >= 1)
        self.check("IMPORT type present", any(tok.type == "IMPORT" for tok in tokens))

    def test_inquire_statement(self):
        print("[INQUIRE Statement]")
        t = Tokenizer('INQUIRE user for the string "Your name?";')
        tokens = t.tokenize()
        self.check("INQUIRE tokenizes", len(tokens) >= 1)
        self.check("INQUIRE type present", any(tok.type == "INQUIRE" for tok in tokens))

    def test_comments(self):
        print("[Comments]")
        t = Tokenizer("^ This is a comment\nLET the variable x BE the number 1;")
        tokens = t.tokenize()
        self.check("Comment + code tokenizes", len(tokens) >= 1)
        self.check("LET found after comment", any(tok.type == "LET" for tok in tokens))

    def test_empty_input(self):
        print("[Empty Input]")
        t = Tokenizer("")
        tokens = t.tokenize()
        self.check("Empty input produces no tokens", len(tokens) == 0)

        t = Tokenizer("   \n\n  ")
        tokens = t.tokenize()
        self.check("Whitespace-only input produces no tokens", len(tokens) == 0)

    def test_multiline_input(self):
        print("[Multi-line Input]")
        code = """LET the variable x BE the number 1;
SET the variable x TO the number 2;
PROCLAIM the value of x;"""
        t = Tokenizer(code)
        tokens = t.tokenize()
        self.check("Multi-line produces multiple tokens", len(tokens) == 3)
        self.check("First token is LET", tokens[0].type == "LET")
        self.check("Second token is SET", tokens[1].type == "SET")
        self.check("Third token is PROCLAIM", tokens[2].type == "PROCLAIM")

    def test_list_literal(self):
        print("[List Literal]")
        t = Tokenizer("LET the variable items BE [1, 2, 3];")
        tokens = t.tokenize()
        self.check("List literal tokenizes", len(tokens) >= 1)
        self.check("LET type", any(tok.type == "LET" for tok in tokens))

    def test_map_literal(self):
        print("[Map Literal]")
        t = Tokenizer('LET the variable person BE {name: "Alice", age: 30};')
        tokens = t.tokenize()
        self.check("Map literal tokenizes", len(tokens) >= 1)
        self.check("LET type", any(tok.type == "LET" for tok in tokens))

    def test_binary_expressions(self):
        print("[Binary Expressions]")
        t = Tokenizer("LET the variable sum BE the number 1 plus the number 2;")
        tokens = t.tokenize()
        self.check("Binary expression tokenizes", len(tokens) >= 1)

        t = Tokenizer("LET the variable diff BE the number 10 minus the number 3;")
        tokens = t.tokenize()
        self.check("Subtraction expression tokenizes", len(tokens) >= 1)

    def test_file_write(self):
        print("[File Write]")
        t = Tokenizer('IN the file "out.txt" WRITE the string "hello";')
        tokens = t.tokenize()
        self.check("File write tokenizes", len(tokens) >= 1)


if __name__ == "__main__":
    test = LexerTest()
    success = test.run_all()
    sys.exit(0 if success else 1)
