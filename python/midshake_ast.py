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


@dataclass
class Response(Expression):
    pass


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


@dataclass
class Set(Statement):
    name: str
    value: Expression


@dataclass
class Proclaim(Statement):
    value: Expression


@dataclass
class Inquire(Statement):
    expected_type: str
    question: str


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
# FUNCTIONS
# -----------------------------

@dataclass
class FunctionDef(Statement):
    name: str
    param_names: List[str]
    body: List[Statement]


@dataclass
class Call(Statement):
    name: str
    args: List[Expression]


@dataclass
class Return(Statement):
    expr: Expression


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
