from python.midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, If, While, Terminate,
    Variable, Binary, Inquire, Response,
    Call, FunctionDef, Return
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # -----------------------------
    # BASIC TOKEN HELPERS
    # -----------------------------
    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    # -----------------------------
    # MAIN PARSE ENTRY
    # -----------------------------
    def parse(self):
        sections = []
        current_section = Section("MAIN", [])

        while self.current():
            stmt = self.parse_statement()
            if stmt:
                current_section.body.append(stmt)
            # DO NOT auto-advance here — parse_statement handles it

        sections.append(current_section)
        return Program(sections)

    # -----------------------------
    # FUNCTION PARSER
    # -----------------------------
    def parse_function(self, func_name, param_names, line_no):
        body = []
        self.advance()  # move past FUNC_DEF

        while self.current() and self.current().type != "END_FUNC":
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
            # self.advance() might be the cause of the problem

        if not self.current():
            raise ValueError(
                f"MidShake Syntax Error (line {line_no}):\n"
                f"  Missing 'END FUNCTION' for function '{func_name}'."
            )

        self.advance()  # consume END_FUNC
        return FunctionDef(func_name, param_names, body)

    # -----------------------------
    # STATEMENTS
    # -----------------------------
    def parse_statement(self):
        tok = self.current()
        if tok is None:
            return None

        # LET
        if tok.type == "LET":
            name, expr = tok.value
            self.advance()
            return Let(name, expr)

        # SET
        if tok.type == "SET":
            name, expr = tok.value
            self.advance()
            return Set(name, expr)

        # PROCLAIM
        if tok.type == "PROCLAIM":
            self.advance()
            return Proclaim(tok.value)

        # IF
        if tok.type == "IF":
            expr = tok.value
            return self.parse_if(expr, tok.line_no)

        # WHILST
        if tok.type == "WHILST":
            expr = tok.value
            return self.parse_while(expr, tok.line_no)

        # INQUIRE
        if tok.type == "INQUIRE":
            expected_type, question = tok.value
            self.advance()
            return Inquire(expected_type, question)

        # FUNCTION DEF
        if tok.type == "FUNC_DEF":
            func_name, param_names = tok.value
            return self.parse_function(func_name, param_names, tok.line_no)

        # CALL
        if tok.type == "CALL":
            func_name, args = tok.value
            self.advance()
            return Call(func_name, args)

        # RETURN
        if tok.type == "RETURN":
            expr = tok.value
            self.advance()
            return Return(expr)

        # TERMINATE
        if tok.type == "TERMINATE":
            self.advance()
            return Terminate()

        raise ValueError(
            f"MidShake Syntax Error (line {tok.line_no}):\n"
            f"  Unexpected token '{tok.type}'."
        )

    # -----------------------------
    # IF / ELSE / END IF
    # -----------------------------
    def parse_if(self, expr, line_no):
        body = []
        else_body = None

        self.advance()  # move past IF

        while self.current() and self.current().type not in ("END_IF", "ELSE"):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        if self.current() and self.current().type == "ELSE":
            else_body = []
            self.advance()
            while self.current() and self.current().type != "END_IF":
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)

        if not self.current() or self.current().type != "END_IF":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  IF block was never closed with 'END IF'."
            )

        self.advance()  # consume END_IF
        return If(expr, body, else_body)

    # -----------------------------
    # WHILST / END WHILST
    # -----------------------------
    def parse_while(self, expr, line_no):
        body = []

        self.advance()  # move past WHILST

        while self.current() and self.current().type != "END_WHILST":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        if not self.current() or self.current().type != "END_WHILST":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  WHILST block was never closed with 'END WHILST'."
            )

        self.advance()  # consume END_WHILST
        return While(expr, body)
