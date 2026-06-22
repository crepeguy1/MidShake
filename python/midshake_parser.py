from midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, If, While, Terminate,
    Variable, Binary, Inquire, Response,
    Call, FunctionDef
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
            self.advance()

        sections.append(current_section)
        return Program(sections)

    # -----------------------------
    # STATEMENTS
    # ----------------------------
    
    def parse_function(self, name, param_names, line_no):
        body = []

        # move past FUNC_DEF token
        self.advance()

        # read until END_FUNC
        while self.current() and self.current().type != "END_FUNC":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.advance()

        if not self.current() or self.current().type != "END_FUNC":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  FUNCTION '{name}' was never closed with 'END FUNCTION'."
            )

        return FunctionDef(name, param_names, body)


    def parse_statement(self):
        tok = self.current()
        if tok is None:
            return None

        # LET
        if tok.type == "LET":
            name, expr = tok.value
            return Let(name, expr)

        # SET
        if tok.type == "SET":
            name, expr = tok.value
            return Set(name, expr)

        # PROCLAIM
        if tok.type == "PROCLAIM":
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
            return Inquire(expected_type, question)

        # FUNCTION DEF
        if tok.type == "FUNC_DEF":
            func_name, param_names = tok.value
            return self.parse_function(func_name, param_names, tok.line_no)

        # CALL
        if tok.type == "CALL":
            func_name, args = tok.value
            return Call(func_name, args)


        # TERMINATE
        if tok.type == "TERMINATE":
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

        # move past IF token
        self.advance()

        # read body until ELSE or END_IF
        while self.current() and self.current().type not in ("END_IF", "ELSE"):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.advance()

        # ELSE block
        if self.current() and self.current().type == "ELSE":
            else_body = []
            self.advance()
            while self.current() and self.current().type != "END_IF":
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
                self.advance()

        # must end with END_IF
        if not self.current() or self.current().type != "END_IF":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  IF block was never closed with 'END IF'."
            )

        return If(expr, body, else_body)

    # -----------------------------
    # WHILST / END WHILST
    # -----------------------------
    def parse_while(self, expr, line_no):
        body = []

        # move past WHILST token
        self.advance()

        # read until END_WHILST
        while self.current() and self.current().type != "END_WHILST":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.advance()

        if not self.current() or self.current().type != "END_WHILST":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  WHILST block was never closed with 'END WHILST'."
            )

        return While(expr, body)
