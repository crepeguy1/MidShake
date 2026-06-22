# midshake_ast.py

from dataclasses import dataclass
from typing import List, Optional


# -----------------------------
# EXPRESSIONS
# -----------------------------

@dataclass
class Expression:
    pass


@dataclass
class Number(Expression):
    value: int


@dataclass
class String(Expression):
    value: str


@dataclass
class Variable(Expression):
    name: str


@dataclass
class Binary(Expression):
    op: str
    left: Expression
    right: Expression


# -----------------------------
# STATEMENTS
# -----------------------------

@dataclass
class Statement:
    pass


@dataclass
class Let(Statement):
    name: str
    value: Expression

class Inquire:
    def __init__(self, expected_type, question):
        self.expected_type = expected_type  # "number" or "string"
        self.question = question

class Response:
    pass
    
class Set(Statement):
    name: str
    value: Expression

class FunctionDef:
    def __init__(self, name, param_names, body):
        self.name = name              # str
        self.param_names = param_names  # list[str]
        self.body = body              # list of statements


class Call:
    def __init__(self, name, args):
        self.name = name      # str
        self.args = args      # list of expressions


@dataclass
class Proclaim(Statement):
    value: Expression


@dataclass
class If(Statement):
    expr: Expression
    body: List[Statement]
    else_body: Optional[List[Statement]] = None


@dataclass
class While(Statement):
    expr: Expression
    body: List[Statement]


@dataclass
class Terminate(Statement):
    pass


# -----------------------------
# PROGRAM STRUCTURE
# -----------------------------

@dataclass
class Section:
    name: str
    body: List[Statement]


@dataclass
class Program:
    sections: List[Section]
