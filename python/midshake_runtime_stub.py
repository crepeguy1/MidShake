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

    def exec_stmt(self, stmt: Statement) -> None:
        if isinstance(stmt, Let):
            self.vars[stmt.name] = stmt.value
        elif isinstance(stmt, Set):
            self.vars[stmt.name] = stmt.value
        elif isinstance(stmt, Proclaim):
            print(self.vars.get(stmt.name, 0))
        elif isinstance(stmt, If):
            if self.vars.get(stmt.name, 0) == stmt.value:
                for s in stmt.body:
                    self.exec_stmt(s)
        elif isinstance(stmt, While):
            while self.vars.get(stmt.name, 0) == stmt.value and not self.terminated:
                for s in stmt.body:
                    self.exec_stmt(s)
        elif isinstance(stmt, Terminate):
            self.terminated = True
