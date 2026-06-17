# midshake_ast.py
from dataclasses import dataclass
from typing import List


@dataclass
class Statement:
    pass


@dataclass
class Let(Statement):
    name: str
    value: int


@dataclass
class Set(Statement):
    name: str
    value: int


@dataclass
class Proclaim(Statement):
    name: str


@dataclass
class If(Statement):
    name: str
    value: int
    body: List[Statement]


@dataclass
class While(Statement):
    name: str
    value: int
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
