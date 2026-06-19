# midshake_ast.py
from dataclasses import dataclass
from typing import List, Optional


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
class If(Statement):
    name: str
    value: Expression
    body: List[Statement]
    else_body: Optional[List[Statement]] = None


@dataclass
class While(Statement):
    name: str
    value: Expression
    body: List[Statement]


@dataclass
class Terminate(Statement):
    pass


@dataclass
class Section:
    name: str
    body: List[Statement]


@dataclass
class Program:
    sections: List[Section]
