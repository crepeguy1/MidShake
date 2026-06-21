# midshake_runtime.py

from typing import Dict, Any
from midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, If, While, Terminate,
    Number, String, Variable, Binary, Inquire,
    Response
)


class Runtime:
    def __init__(self) -> None:
        self.vars: Dict[str, Any] = {}
        self.terminated: bool = False

    # ------------------------------------------------------------
    # PROGRAM EXECUTION
    # ------------------------------------------------------------
    def exec_program(self, program: Program) -> None:
        for section in program.sections:
            if self.terminated:
                break
            self.exec_section(section)

    def exec_section(self, section: Section) -> None:
        for stmt in section.body:
            if self.terminated:
                break
            self.exec_stmt(stmt)

    # ------------------------------------------------------------
    # UTILITIES
    # ------------------------------------------------------------
    def require_declared(self, name: str):
        if name not in self.vars:
            raise ValueError(
                f"MidShake Runtime Error:\n"
                f"  The variable '{name}' was never declared with LET."
            )

    # ------------------------------------------------------------
    # EXPRESSION EVALUATION
    # ------------------------------------------------------------
    def eval_expr(self, expr):
        if isinstance(expr, Number):
            return expr.value

        if isinstance(expr, String):
            return expr.value

        if isinstance(expr, Variable):
            self.require_declared(expr.name)
            return self.vars[expr.name]
        
        if isinstance(expr, Response):
            return self.vars.get("RESPONSE")
        
        if isinstance(expr, Binary):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
       
            
            if expr.op == "+":
                return left + right
            if expr.op == "-":
                return left - right
            if expr.op == "*":
                return left * right
            if expr.op == "/":
                return left / right
            if expr.op == ">":
                return left > right
            if expr.op == "<":
                return left < right
            if expr.op == ">=":
                return left >= right
            if expr.op == "<=":
                return left <= right
            if expr.op == "==":
                return left == right
            if expr.op == "!=":
                return left != right
        

        raise ValueError(
            f"MidShake Runtime Error:\n"
            f"  Unknown expression type: {expr}"
        )

    # ------------------------------------------------------------
    # STATEMENT EXECUTION
    # ------------------------------------------------------------
    def exec_stmt(self, stmt):
        # LET
        if isinstance(stmt, Let):
            self.vars[stmt.name] = self.eval_expr(stmt.value)

        # SET
        elif isinstance(stmt, Set):
            self.require_declared(stmt.name)
            self.vars[stmt.name] = self.eval_expr(stmt.value)

        # PROCLAIM
        elif isinstance(stmt, Proclaim):
            value = self.eval_expr(stmt.value)
            print(value)

        # IF
        elif isinstance(stmt, If):
            if self.eval_expr(stmt.expr):
                for s in stmt.body:
                    self.exec_stmt(s)
            elif stmt.else_body is not None:
                for s in stmt.else_body:
                    self.exec_stmt(s)

        # WHILST
        elif isinstance(stmt, While):
            while self.eval_expr(stmt.expr) and not self.terminated:
                for s in stmt.body:
                    self.exec_stmt(s)

        # Inquire
        elif isinstance(stmt, Inquire):
            print(stmt.question)
            raw = input("> ")

            if stmt.expected_type == "number":
                try:
                    self.vars["RESPONSE"] = int(raw)
                except:
                    raise ValueError("Expected a number from user input.")
            else:
                self.vars["RESPONSE"] = raw

        # TERMINATE
        elif isinstance(stmt, Terminate):
            self.terminated = True
