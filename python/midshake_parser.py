import token

from midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, If, While, Terminate,
    Variable, Binary, Inquire, Response,
    Call, FunctionDef, Return, FileWriteStatement, Import,
    Break, Continue, ForIn, MapSet, GlobalSet, Public, Private, Protected,
    ClassDef, MemberAccess, MemberSet, TryCatch, Throw
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.class_stack = []

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
    def parse_function(self, func_name, param_names, line_no, visibility=None, owner_class=None):
        body = []
        self.advance()  # move past FUNC_DEF

        while self.current() and self.current().type != "END_FUNC":
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)

        if not self.current():
            raise ValueError(
                f"MidShake Syntax Error (line {line_no}):\n"
                f"  Missing 'END FUNCTION' for function '{func_name}'."
            )

        self.advance()  # consume END_FUNC
        vis = visibility if visibility is not None else (Private() if owner_class else Public())
        return FunctionDef(func_name, param_names, body, visibility=vis, owner_class=owner_class)

    def parse_class(self, name, base_name, line_no, visibility=None):
        members = []
        self.class_stack.append(name)
        self.advance()  # move past CLASS_DEF

        while self.current() and self.current().type != "END_CLASS":
            tok = self.current()
            if tok.type == "FUNC_DEF":
                func_name, param_names = tok.value
                members.append(self.parse_function(
                    func_name, param_names, tok.line_no, tok.visibility, owner_class=name
                ))
                continue
            if tok.type == "LET":
                member = self.parse_statement()
                if member.visibility is None:
                    member.visibility = Private()
                members.append(member)
                continue
            raise ValueError(
                f"MidShake Syntax Error (line {tok.line_no}):\n"
                f"  Classes may contain only field declarations and function definitions."
            )

        if not self.current():
            raise ValueError(
                f"MidShake Syntax Error (line {line_no}):\n"
                f"  Missing 'END CLASS' for class '{name}'."
            )

        self.advance()  # consume END_CLASS
        self.class_stack.pop()
        vis = visibility if visibility is not None else Public()
        return ClassDef(name, base_name, members, visibility=vis)

    # -----------------------------
    # STATEMENTS
    # -----------------------------
    def parse_statement(self):
        tok = self.current()
        if tok is None:
            return None

        # Access modifiers apply only to declarations.
        if tok.visibility is not None and tok.type not in ("LET", "FUNC_DEF", "CLASS_DEF"):
            modifier = type(tok.visibility).__name__
            raise ValueError(
                f"MidShake Syntax Error (line {tok.line_no}):\n"
                f"  '{modifier}' cannot be used before '{tok.type}'."
            )
        if isinstance(tok.visibility, Protected) and not self.class_stack:
            raise ValueError(
                f"MidShake Syntax Error (line {tok.line_no}):\n"
                f"  'Protected' can only be used for class members."
            )

        # LET
        if tok.type == "LET":
            name, expr = tok.value
            vis = tok.visibility if tok.visibility is not None else (
                Private() if self.class_stack else Public()
            )
            self.advance()
            return Let(name, expr, visibility=vis)

        # SET
        if tok.type == "SET":
            name, expr = tok.value
            self.advance()
            if "." in name:
                target_name, member_name = name.rsplit(".", 1)
                target_parts = target_name.split(".")
                target = Variable(target_parts[0])
                for part in target_parts[1:]:
                    target = MemberAccess(target, part)
                return MemberSet(target, member_name, expr)
            return Set(name, expr)

        # GLOBAL SET
        if tok.type == "GLOBAL_SET":
            name, expr = tok.value
            self.advance()
            return GlobalSet(name, expr)

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

        # TRY / CATCH
        if tok.type == "TRY":
            return self.parse_try_catch(tok.line_no)

        # INQUIRE
        if tok.type == "INQUIRE":
            expected_type, question = tok.value
            self.advance()
            return Inquire(expected_type, question)

        # FUNCTION DEF
        if tok.type == "FUNC_DEF":
            func_name, param_names = tok.value
            return self.parse_function(func_name, param_names, tok.line_no, tok.visibility)

        # CLASS DEF
        if tok.type == "CLASS_DEF":
            name, base_name = tok.value
            return self.parse_class(name, base_name, tok.line_no, tok.visibility)

        # CALL
        if tok.type == "CALL":
            func_name, args = tok.value
            self.advance()
            return Call(func_name, args)
        
        elif tok.type == "FILE_WRITE":
            path, expr = tok.value
            self.advance()
            return FileWriteStatement(path, expr)

        # IMPORT
        if tok.type == "IMPORT":
            path = tok.value
            self.advance()
            return Import(path)

        # RETURN
        if tok.type == "RETURN":
            expr = tok.value
            self.advance()
            return Return(expr)

        # THROW
        if tok.type == "THROW":
            expr = tok.value
            self.advance()
            return Throw(expr)

        # TERMINATE
        if tok.type == "TERMINATE":
            self.advance()
            return Terminate()

        # BREAK
        if tok.type == "BREAK":
            self.advance()
            return Break()

        # CONTINUE
        if tok.type == "CONTINUE":
            self.advance()
            return Continue()

        # FOR_IN
        if tok.type == "FOR_IN":
            var_name, list_expr = tok.value
            return self.parse_for_in(var_name, list_expr, tok.line_no)

        # MAP_SET
        if tok.type == "MAP_SET":
            map_name, key_expr, value_expr = tok.value
            self.advance()
            return MapSet(Variable(map_name), key_expr, value_expr)

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

    def parse_try_catch(self, line_no):
        body = []
        catch_body = []
        self.advance()  # move past TRY

        while self.current() and self.current().type not in ("CATCH", "END_TRY"):
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)

        if not self.current() or self.current().type != "CATCH":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  TRY block requires a CATCH clause."
            )
        catch_name = self.current().value
        self.advance()  # consume CATCH

        while self.current() and self.current().type != "END_TRY":
            stmt = self.parse_statement()
            if stmt is not None:
                catch_body.append(stmt)

        if not self.current() or self.current().type != "END_TRY":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  TRY block was never closed with 'END TRY'."
            )

        self.advance()  # consume END_TRY
        return TryCatch(body, catch_name, catch_body)

    # -----------------------------
    # FOR ... IN ... DO / END FOR
    # -----------------------------
    def parse_for_in(self, var_name, list_expr, line_no):
        body = []

        self.advance()  # move past FOR_IN

        while self.current() and self.current().type != "END_FOR":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        if not self.current() or self.current().type != "END_FOR":
            raise ValueError(
                f"MidShake Syntax Error (around line {line_no}):\n"
                f"  FOR block was never closed with 'END FOR'."
            )

        self.advance()  # consume END_FOR
        return ForIn(var_name, list_expr, body)
