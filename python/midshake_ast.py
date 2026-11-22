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
# FILE I/O EXPRESSIONS
# -----------------------------

@dataclass
class FileReadExpression(Expression):
    path: str  # Can be a string literal or an Expression for dynamic paths

@dataclass
class FileWriteNode:
    def __init__(self, path, expr):
        self.path = path
        self.expr = expr


# -----------------------------
# COLLECTION EXPRESSIONS
# -----------------------------

@dataclass
class ListLiteral(Expression):
    elements: List[Expression]


@dataclass
class MapLiteral(Expression):
    keys: List[Expression]
    values: List[Expression]


@dataclass
class ListGet(Expression):
    list_expr: Expression
    index_expr: Expression


@dataclass
class MapGet(Expression):
    map_expr: Expression
    key_expr: Expression


@dataclass
class ListAppend(Expression):
    element_expr: Expression
    list_expr: Expression


@dataclass
class ListLength(Expression):
    list_expr: Expression


# -----------------------------
# STRING FUNCTION EXPRESSIONS
# -----------------------------

@dataclass
class StringLength(Expression):
    string_expr: Expression


@dataclass
class Substring(Expression):
    string_expr: Expression
    start_expr: Expression
    end_expr: Expression


@dataclass
class CharAt(Expression):
    string_expr: Expression
    index_expr: Expression


@dataclass
class StringSplit(Expression):
    string_expr: Expression
    delimiter_expr: Expression


@dataclass
class StringTrim(Expression):
    string_expr: Expression


@dataclass
class StringJoin(Expression):
    list_expr: Expression
    delimiter_expr: Expression


# -----------------------------
# MATH FUNCTION EXPRESSIONS
# -----------------------------

@dataclass
class MathMin(Expression):
    left: Expression
    right: Expression

@dataclass
class MathMax(Expression):
    left: Expression
    right: Expression

@dataclass
class MathAbs(Expression):
    expr: Expression

@dataclass
class MathRound(Expression):
    expr: Expression


# -----------------------------
# STRING UTILITY EXPRESSIONS
# -----------------------------

@dataclass
class StringToUpper(Expression):
    string_expr: Expression

@dataclass
class StringToLower(Expression):
    string_expr: Expression

@dataclass
class StringStartsWith(Expression):
    string_expr: Expression
    prefix_expr: Expression

@dataclass
class StringEndsWith(Expression):
    string_expr: Expression
    suffix_expr: Expression

@dataclass
class StringIsDigit(Expression):
    string_expr: Expression

@dataclass
class StringIsLetter(Expression):
    string_expr: Expression

@dataclass
class StringIsWhitespace(Expression):
    string_expr: Expression


# -----------------------------
# BOOLEAN EXPRESSIONS
# -----------------------------

@dataclass
class Boolean(Expression):
    value: bool


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
class ForIn(Statement):
    var_name: str
    list_expr: Expression
    body: List[Statement]


@dataclass
class Break(Statement):
    pass


@dataclass
class Continue(Statement):
    pass


@dataclass
class Terminate(Statement):
    pass


# -----------------------------
# GLOBAL STATEMENTS
# -----------------------------

@dataclass
class GlobalSet(Statement):
    """Set a global variable from within a function (enables recursion with shared state)."""
    name: str
    value: Expression


# -----------------------------
# MAP STATEMENTS
# -----------------------------

@dataclass
class MapSet(Statement):
    map_expr: Expression
    key_expr: Expression
    value_expr: Expression


# -----------------------------
# FILE I/O STATEMENTS
# -----------------------------

@dataclass
class FileWriteStatement(Statement):
    path: str  #try and fix things that have to do with path to include actual file
    value: Expression


# -----------------------------
# IMPORT / INCLUDE
# -----------------------------

@dataclass
class Import(Statement):
    path: str  # file path to import



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
class Return:
    def __init__(self, expr):
        self.expr = expr




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
