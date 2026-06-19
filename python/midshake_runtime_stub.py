# midshake_runtime.py

from typing import Dict, Any
from midshake_ast import (
    Program, Section, Statement,
    Let, Set, Proclaim, If, While, Terminate,
    Number, String, Variable, Binary
)


class Runtime:
    def __init__(self) -> None:
        self.vars: Dict[str, Any] = {}
        self.terminated: bool = False

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

    def require_declared(self, name: str):
        if name not in self.vars:
            raise ValueError(
                f"MidShake Runtime Error:\n"
                f"  The variable '{name}' was never declared with LET."
            )

    def eval_expr(self, expr):
        if isinstance(expr, Number):
            return expr.value
        if isinstance(expr, String):
            return expr.value
        if isinstance(expr, Variable):
            self.require_declared(expr.name)
            return self.vars[expr.name]
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
        raise ValueError(f"MidShake Runtime Error:\n  Unknown expression: {expr}")

    def exec_stmt(self, stmt: Statement) -> None:
        if isinstance(stmt, Let):
            self.vars[stmt.name] = self.eval_expr(stmt.value)

        elif isinstance(stmt, Set):
            self.require_declared(stmt.name)
            self.vars[stmt.name] = self.eval_expr(stmt.value)

        elif isinstance(stmt, Proclaim):
            value = self.eval_expr(stmt.value)
            print(value)

        elif isinstance(stmt, If):
            self.require_declared(stmt.name)
            left = self.vars[stmt.name]
            right = self.eval_expr(stmt.value)
            if left == right:
                for s in stmt.body:
                    self.exec_stmt(s)
            elif stmt.else_body is not None:
                for s in stmt.else_body:
                    self.exec_stmt(s)

        elif isinstance(stmt, While):
            self.require_declared(stmt.name)
            while self.vars[stmt.name] == self.eval_expr(stmt.value) and not self.terminated:
                for s in stmt.body:
                    self.exec_stmt(s)

        elif isinstance(stmt, Terminate):
            self.terminated = True
