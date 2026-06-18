# midshake_runtime.py

from typing import Dict
from midshake_ast import (
    Program, Section, Statement,
    Let, Set, Proclaim, If, While, Terminate
)


class Runtime:
    def __init__(self) -> None:
        self.vars: Dict[str, int] = {}
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

    def exec_stmt(self, stmt: Statement) -> None:
        if isinstance(stmt, Let):
            self.vars[stmt.name] = stmt.value

        elif isinstance(stmt, Set):
            self.require_declared(stmt.name)
            self.vars[stmt.name] = stmt.value

        elif isinstance(stmt, Proclaim):
            self.require_declared(stmt.name)
            print(self.vars.get(stmt.name, 0))

        elif isinstance(stmt, If):
            self.require_declared(stmt.name)
            if self.vars.get(stmt.name, 0) == stmt.value:
                for s in stmt.body:
                    self.exec_stmt(s)

        elif isinstance(stmt, While):
            self.require_declared(stmt.name)
            while self.vars.get(stmt.name, 0) == stmt.value and not self.terminated:
                for s in stmt.body:
                    self.exec_stmt(s)

        elif isinstance(stmt, Terminate):
            self.terminated = True
