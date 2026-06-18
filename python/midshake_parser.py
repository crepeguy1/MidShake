# midshake_parser.py

from midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, If, While, Terminate
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def parse(self):
        sections = []
        current_section = Section("MAIN", [])

        while self.current():
            stmt = self.parse_statement()
            if stmt:
                current_section.body.append(stmt)
            self.advance()

        sections.append(current_section)
        return Program(sections)

    def parse_statement(self):
        tok = self.current()
        if tok is None:
            return None

        if tok.type == "LET":
            name, value = tok.value
            return Let(name, value)

        if tok.type == "SET":
            name, value = tok.value
            return Set(name, value)

        if tok.type == "PROCLAIM":
            return Proclaim(tok.value)

        if tok.type == "IF":
            name, value = tok.value
            return self.parse_if(name, value, tok.line_no)

        if tok.type == "WHILST":
            name, value = tok.value
            return self.parse_while(name, value, tok.line_no)

        if tok.type == "TERMINATE":
            return Terminate()

        raise ValueError(
            f"MidShake Syntax Error (line {tok.line_no}):\n"
            f"  Unexpected token '{tok.type}'."
        )

    def parse_if(self, name, value, line_no):
        body = []
        self.advance()

        while self.current() and self.current().type != "END_IF":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.advance()

        if not self.current() or self.current().type != "END_IF":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  IF block was never closed with 'END IF;'."
            )

        return If(name, value, body)

    def parse_while(self, name, value, line_no):
        body = []
        self.advance()

        while self.current() and self.current().type != "END_WHILST":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.advance()

        if not self.current() or self.current().type != "END_WHILST":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  WHILST block was never closed with 'END WHILST;'."
            )

        return While(name, value, body)
