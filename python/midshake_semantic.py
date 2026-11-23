"""
MidShake Semantic Analysis Phase

This module performs semantic analysis on the MidShake AST, including:
- Symbol table construction with nested scopes
- Type inference for literals and expressions
- Variable declaration checking (LET declares, SET requires prior declaration)
- Function definition tracking and call validation
- Scope resolution for block-scoped variables
- Error reporting with line numbers

Usage:
    from midshake_semantic import SemanticAnalyzer

    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(program_ast)
    if errors:
        for error in errors:
            print(error)
"""

from midshake_ast import (
    # Expressions
    Expression, Number, String, Variable, Binary, Response, Boolean,
    ListLiteral, MapLiteral, ListGet, MapGet, ListAppend, ListLength,
    StringLength, Substring, CharAt, StringSplit, StringTrim, StringJoin,
    StringReplace, StringToUpper, StringToLower,
    StringStartsWith, StringEndsWith, StringIsDigit, StringIsLetter, StringIsWhitespace,
    MathMin, MathMax, MathAbs, MathRound,
    FileReadExpression,
    # Statements
    Statement, Let, Set, GlobalSet, Proclaim, Inquire,
    If, While, ForIn, Break, Continue, Terminate,
    FunctionDef, Call, Return,
    MapSet, FileWriteStatement, Import,
    # Program structure
    Program, Section
)


# ---------------------------------------------------------------------------
# Symbol Table Entry
# ---------------------------------------------------------------------------

class Symbol:
    """Represents a single symbol (variable or function) in the symbol table."""

    def __init__(self, name, symbol_type, kind="variable"):
        """
        :param name: Symbol name (e.g. "counter", "greet")
        :param symbol_type: Inferred type (e.g. "Number", "String", "List", "Map", "Function")
        :param kind: "variable", "function", "parameter", or "loop_var"
        """
        self.name = name
        self.symbol_type = symbol_type
        self.kind = kind
        self.is_mutable = True  # All MidShake variables are mutable by default

    def __repr__(self):
        return f"Symbol({self.name}, {self.symbol_type}, {self.kind})"


# ---------------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------------

class Scope:
    """Represents a single scope level (global, function, block)."""

    def __init__(self, scope_type="global", parent=None):
        """
        :param scope_type: "global", "function", "block", or "loop"
        :param parent: Parent scope (None for global)
        """
        self.scope_type = scope_type
        self.parent = parent
        self.symbols = {}       # name -> Symbol
        self.functions = {}     # name -> Symbol (function definitions)

    def declare(self, name, symbol_type, kind="variable"):
        """Declare a new symbol in this scope. Returns True if successful."""
        if name in self.symbols:
            return False  # Duplicate declaration
        self.symbols[name] = Symbol(name, symbol_type, kind)
        return True

    def declare_function(self, name, param_count):
        """Declare a function in this scope."""
        self.functions[name] = Symbol(name, "Function", "function")
        self.symbols[name] = Symbol(name, "Function", "function")
        return True

    def lookup(self, name):
        """Look up a symbol, walking up the scope chain."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def lookup_function(self, name):
        """Look up a function, walking up the scope chain."""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.lookup_function(name)
        return None


# ---------------------------------------------------------------------------
# Semantic Error
# ---------------------------------------------------------------------------

class SemanticError:
    """Represents a semantic analysis error."""

    def __init__(self, error_type, message, line_no=None):
        self.error_type = error_type  # "undeclared", "redeclared", "type_mismatch", etc.
        self.message = message
        self.line_no = line_no

    def __str__(self):
        prefix = f"Semantic Error (line {self.line_no}): " if self.line_no else "Semantic Error: "
        return f"{prefix}{self.message}"

    def __repr__(self):
        return f"SemanticError({self.error_type}, {self.message})"


# ---------------------------------------------------------------------------
# Semantic Analyzer
# ---------------------------------------------------------------------------

class SemanticAnalyzer:
    """
    Performs semantic analysis on a MidShake AST.

    The analyzer builds a symbol table, infers types, and checks for common
    semantic errors like undeclared variables, duplicate declarations, and
    undefined function calls.
    """

    # Built-in special variables
    BUILTINS = {"RESPONSE", "the RESPONSE", "the answer"}

    def __init__(self):
        self.errors = []          # List of SemanticError
        self.scope_stack = []     # Stack of Scope objects
        self.global_scope = None  # The root global scope
        self.functions = {}       # name -> FunctionDef (for cross-reference)

    # -------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------

    def analyze(self, program: Program) -> list:
        """
        Analyze a complete program AST.

        :param program: The root Program AST node
        :return: List of SemanticError objects (empty means no errors)
        """
        self.errors = []
        self.scope_stack = []
        self.functions = {}

        # Create global scope
        self.global_scope = Scope("global")
        self.scope_stack.append(self.global_scope)

        # Register built-in special variables
        for builtin in self.BUILTINS:
            self.global_scope.declare(builtin, "Any", "builtin")

        # Two-pass analysis:
        # Pass 1: Collect all function definitions
        # Pass 2: Analyze all statements with full function knowledge

        # Pass 1: Collect function definitions
        for section in program.sections:
            self._collect_functions(section)

        # Pass 2: Analyze all statements
        for section in program.sections:
            self._analyze_section(section)

        return self.errors

    # -------------------------------------------------------------------
    # Pass 1: Collect function definitions
    # -------------------------------------------------------------------

    def _collect_functions(self, section: Section):
        """First pass: register all function definitions in the global scope."""
        for stmt in section.body:
            if isinstance(stmt, FunctionDef):
                self.functions[stmt.name] = stmt
                self.global_scope.declare_function(stmt.name, len(stmt.param_names))

    # -------------------------------------------------------------------
    # Pass 2: Analyze sections and statements
    # -------------------------------------------------------------------

    def _analyze_section(self, section: Section):
        """Analyze all statements in a section."""
        for stmt in section.body:
            self._analyze_statement(stmt)

    def _analyze_statement(self, stmt):
        """Dispatch to the appropriate analyzer based on statement type."""
        if isinstance(stmt, Let):
            self._analyze_let(stmt)
        elif isinstance(stmt, Set):
            self._analyze_set(stmt)
        elif isinstance(stmt, GlobalSet):
            self._analyze_global_set(stmt)
        elif isinstance(stmt, Proclaim):
            self._analyze_proclaim(stmt)
        elif isinstance(stmt, Inquire):
            self._analyze_inquire(stmt)
        elif isinstance(stmt, If):
            self._analyze_if(stmt)
        elif isinstance(stmt, While):
            self._analyze_while(stmt)
        elif isinstance(stmt, ForIn):
            self._analyze_for_in(stmt)
        elif isinstance(stmt, Break):
            self._analyze_break(stmt)
        elif isinstance(stmt, Continue):
            self._analyze_continue(stmt)
        elif isinstance(stmt, Terminate):
            pass  # Always valid
        elif isinstance(stmt, FunctionDef):
            self._analyze_function_def(stmt)
        elif isinstance(stmt, Call):
            self._analyze_call(stmt)
        elif isinstance(stmt, Return):
            self._analyze_return(stmt)
        elif isinstance(stmt, MapSet):
            self._analyze_map_set(stmt)
        elif isinstance(stmt, FileWriteStatement):
            self._analyze_file_write(stmt)
        elif isinstance(stmt, Import):
            pass  # Import resolution is handled at compile time
        else:
            pass  # Unknown statement type, skip

    # -------------------------------------------------------------------
    # Variable declarations and assignments
    # -------------------------------------------------------------------

    def _analyze_let(self, stmt: Let):
        """Analyze LET statement: declare a new variable."""
        current_scope = self.scope_stack[-1]

        # Check for duplicate declaration
        if current_scope.lookup(stmt.name) is not None:
            self.errors.append(SemanticError(
                "redeclared",
                f"Variable '{stmt.name}' is already declared in this scope."
            ))
            return

        # Infer type from the value expression
        inferred_type = self._infer_type(stmt.value)

        # Declare the variable
        current_scope.declare(stmt.name, inferred_type, "variable")

        # Analyze the value expression for any errors
        self._analyze_expression(stmt.value)

    def _analyze_set(self, stmt: Set):
        """Analyze SET statement: assign to an existing variable."""
        current_scope = self.scope_stack[-1]

        # Check if variable is declared
        symbol = current_scope.lookup(stmt.name)
        if symbol is None:
            self.errors.append(SemanticError(
                "undeclared",
                f"Variable '{stmt.name}' is not declared. Use 'LET' to declare it first."
            ))
            return

        # Analyze the value expression
        self._analyze_expression(stmt.value)

    def _analyze_global_set(self, stmt: GlobalSet):
        """Analyze GLOBAL SET statement: assign to a global variable."""
        if len(self.scope_stack) < 1:
            return

        # Look up in global scope
        symbol = self.global_scope.lookup(stmt.name)
        if symbol is None:
            self.errors.append(SemanticError(
                "undeclared",
                f"Global variable '{stmt.name}' is not declared."
            ))
            return

        # Analyze the value expression
        self._analyze_expression(stmt.value)

    # -------------------------------------------------------------------
    # Output and input
    # -------------------------------------------------------------------

    def _analyze_proclaim(self, stmt: Proclaim):
        """Analyze PROCLAIM statement: evaluate and print an expression."""
        self._analyze_expression(stmt.value)

    def _analyze_inquire(self, stmt: Inquire):
        """Analyze INQUIRE statement: prompt user for input."""
        # INQUIRE always sets RESPONSE, which is a builtin
        # Validate the expected type hint
        valid_types = {"string", "number"}
        if stmt.expected_type not in valid_types:
            self.errors.append(SemanticError(
                "invalid_type",
                f"INQUIRE expected type '{stmt.expected_type}' is not valid. Use 'string' or 'number'."
            ))

    # -------------------------------------------------------------------
    # Control flow
    # -------------------------------------------------------------------

    def _analyze_if(self, stmt: If):
        """Analyze IF statement: condition + then body + optional else body."""
        # Analyze condition expression
        self._analyze_expression(stmt.expr)

        # Create a new block scope for the THEN body
        self.scope_stack.append(Scope("block", self.scope_stack[-1]))
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.scope_stack.pop()

        # Analyze ELSE body if present
        if stmt.else_body:
            self.scope_stack.append(Scope("block", self.scope_stack[-1]))
            for else_stmt in stmt.else_body:
                self._analyze_statement(else_stmt)
            self.scope_stack.pop()

    def _analyze_while(self, stmt: While):
        """Analyze WHILST statement: condition + body."""
        # Analyze condition expression
        self._analyze_expression(stmt.expr)

        # Create a new loop scope for the body
        self.scope_stack.append(Scope("loop", self.scope_stack[-1]))
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.scope_stack.pop()

    def _analyze_for_in(self, stmt: ForIn):
        """Analyze FOR-IN statement: loop variable + list expression + body."""
        # Analyze the list expression
        list_type = self._infer_type(stmt.list_expr)
        self._analyze_expression(stmt.list_expr)

        # Declare the loop variable in a new loop scope
        self.scope_stack.append(Scope("loop", self.scope_stack[-1]))
        self.scope_stack[-1].declare(stmt.var_name, "Any", "loop_var")

        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.scope_stack.pop()

    def _analyze_break(self, stmt: Break):
        """Analyze BREAK statement: must be inside a loop."""
        # Find a loop scope in the stack
        in_loop = False
        for scope in reversed(self.scope_stack):
            if scope.scope_type == "loop":
                in_loop = True
                break
        if not in_loop:
            self.errors.append(SemanticError(
                "invalid_context",
                "BREAK statement is not inside a loop."
            ))

    def _analyze_continue(self, stmt: Continue):
        """Analyze CONTINUE statement: must be inside a loop."""
        in_loop = False
        for scope in reversed(self.scope_stack):
            if scope.scope_type == "loop":
                in_loop = True
                break
        if not in_loop:
            self.errors.append(SemanticError(
                "invalid_context",
                "CONTINUE statement is not inside a loop."
            ))

    # -------------------------------------------------------------------
    # Functions
    # -------------------------------------------------------------------

    def _analyze_function_def(self, stmt: FunctionDef):
        """Analyze a function definition: parameters + body."""
        # Create a new function scope
        func_scope = Scope("function", self.global_scope)

        # Declare parameters
        for param_name in stmt.param_names:
            func_scope.declare(param_name, "Any", "parameter")

        # Analyze body
        self.scope_stack.append(func_scope)
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.scope_stack.pop()

    def _analyze_call(self, stmt: Call):
        """Analyze CALL statement: function must be defined."""
        # Check if function is defined
        symbol = self.scope_stack[-1].lookup_function(stmt.name)
        if symbol is None:
            # Check if it's a known stdlib function
            stdlib_funcs = {
                "trim", "uppercase", "lowercase", "length", "substring",
                "split", "join", "replace", "append", "minimum", "maximum",
                "absolute", "rounded", "starts_with", "ends_with",
                "is_digit", "is_letter", "is_whitespace",
                "read_file", "write_file"
            }
            if stmt.name not in stdlib_funcs:
                self.errors.append(SemanticError(
                    "undefined_function",
                    f"Function '{stmt.name}' is not defined."
                ))

        # Analyze arguments
        for arg in stmt.args:
            self._analyze_expression(arg)

    def _analyze_return(self, stmt: Return):
        """Analyze RETURN statement: must be inside a function."""
        in_function = False
        for scope in reversed(self.scope_stack):
            if scope.scope_type == "function":
                in_function = True
                break
        if not in_function:
            self.errors.append(SemanticError(
                "invalid_context",
                "RETURN statement is not inside a function."
            ))

        # Analyze the return expression
        self._analyze_expression(stmt.expr)

    # -------------------------------------------------------------------
    # Map and file operations
    # -------------------------------------------------------------------

    def _analyze_map_set(self, stmt: MapSet):
        """Analyze SET key IN map statement."""
        self._analyze_expression(stmt.map_expr)
        self._analyze_expression(stmt.key_expr)
        self._analyze_expression(stmt.value_expr)

    def _analyze_file_write(self, stmt: FileWriteStatement):
        """Analyze file write statement."""
        self._analyze_expression(stmt.value)

    # -------------------------------------------------------------------
    # Expression analysis and type inference
    # -------------------------------------------------------------------

    def _analyze_expression(self, expr):
        """Analyze an expression for semantic errors."""
        if expr is None:
            return

        if isinstance(expr, Number):
            pass  # Literal, always valid
        elif isinstance(expr, String):
            pass  # Literal, always valid
        elif isinstance(expr, Boolean):
            pass  # Literal, always valid
        elif isinstance(expr, Variable):
            self._analyze_variable(expr)
        elif isinstance(expr, Response):
            pass  # Built-in special variable
        elif isinstance(expr, Binary):
            self._analyze_expression(expr.left)
            self._analyze_expression(expr.right)
        elif isinstance(expr, ListLiteral):
            for elem in expr.elements:
                self._analyze_expression(elem)
        elif isinstance(expr, MapLiteral):
            for key, value in zip(expr.keys, expr.values):
                # Map literal keys can be bare identifiers — skip variable check for keys
                if not isinstance(key, Variable):
                    self._analyze_expression(key)
                self._analyze_expression(value)
        elif isinstance(expr, ListGet):
            self._analyze_expression(expr.list_expr)
            self._analyze_expression(expr.index_expr)
        elif isinstance(expr, MapGet):
            self._analyze_expression(expr.map_expr)
            # Map keys can be bare identifiers (not declared variables) — skip variable check for keys
            # Only analyze if the key is not a bare Variable (which is a common map key pattern)
            if not isinstance(expr.key_expr, Variable):
                self._analyze_expression(expr.key_expr)
        elif isinstance(expr, ListAppend):
            self._analyze_expression(expr.element_expr)
            self._analyze_expression(expr.list_expr)
        elif isinstance(expr, ListLength):
            self._analyze_expression(expr.list_expr)
        elif isinstance(expr, StringLength):
            self._analyze_expression(expr.string_expr)
        elif isinstance(expr, Substring):
            self._analyze_expression(expr.string_expr)
            self._analyze_expression(expr.start_expr)
            self._analyze_expression(expr.end_expr)
        elif isinstance(expr, CharAt):
            self._analyze_expression(expr.string_expr)
            self._analyze_expression(expr.index_expr)
        elif isinstance(expr, StringSplit):
            self._analyze_expression(expr.string_expr)
            self._analyze_expression(expr.delimiter_expr)
        elif isinstance(expr, StringTrim):
            self._analyze_expression(expr.string_expr)
        elif isinstance(expr, StringJoin):
            self._analyze_expression(expr.list_expr)
            self._analyze_expression(expr.delimiter_expr)
        elif isinstance(expr, StringReplace):
            self._analyze_expression(expr.string_expr)
            self._analyze_expression(expr.old_expr)
            self._analyze_expression(expr.new_expr)
        elif isinstance(expr, StringToUpper):
            self._analyze_expression(expr.string_expr)
        elif isinstance(expr, StringToLower):
            self._analyze_expression(expr.string_expr)
        elif isinstance(expr, StringStartsWith):
            self._analyze_expression(expr.string_expr)
            self._analyze_expression(expr.prefix_expr)
        elif isinstance(expr, StringEndsWith):
            self._analyze_expression(expr.string_expr)
            self._analyze_expression(expr.suffix_expr)
        elif isinstance(expr, StringIsDigit):
            self._analyze_expression(expr.string_expr)
        elif isinstance(expr, StringIsLetter):
            self._analyze_expression(expr.string_expr)
        elif isinstance(expr, StringIsWhitespace):
            self._analyze_expression(expr.string_expr)
        elif isinstance(expr, MathMin):
            self._analyze_expression(expr.left)
            self._analyze_expression(expr.right)
        elif isinstance(expr, MathMax):
            self._analyze_expression(expr.left)
            self._analyze_expression(expr.right)
        elif isinstance(expr, MathAbs):
            self._analyze_expression(expr.expr)
        elif isinstance(expr, MathRound):
            self._analyze_expression(expr.expr)
        elif isinstance(expr, FileReadExpression):
            pass  # File path is a string literal or variable
        else:
            pass  # Unknown expression type, skip

    def _analyze_variable(self, expr: Variable):
        """Check that a variable reference is declared."""
        symbol = self.scope_stack[-1].lookup(expr.name)
        if symbol is None:
            # Check if it's a known stdlib function used as a variable (common pattern)
            stdlib_vars = {"trim", "uppercase", "lowercase"}  # Functions that might be referenced
            if expr.name not in stdlib_vars:
                self.errors.append(SemanticError(
                    "undeclared",
                    f"Variable '{expr.name}' is not declared."
                ))

    def _infer_type(self, expr) -> str:
        """
        Infer the type of an expression.

        :param expr: AST expression node
        :return: Type string ("Number", "String", "Boolean", "List", "Map", "Any")
        """
        if expr is None:
            return "Any"

        if isinstance(expr, Number):
            return "Number"
        elif isinstance(expr, String):
            return "String"
        elif isinstance(expr, Boolean):
            return "Boolean"
        elif isinstance(expr, Variable):
            symbol = self.scope_stack[-1].lookup(expr.name)
            if symbol:
                return symbol.symbol_type
            return "Any"  # Unknown variable
        elif isinstance(expr, Response):
            return "Any"  # RESPONSE can hold any type
        elif isinstance(expr, Binary):
            # Binary operations typically return Number or String
            left_type = self._infer_type(expr.left)
            right_type = self._infer_type(expr.right)
            if left_type == "Number" and right_type == "Number":
                return "Number"
            elif left_type == "String" or right_type == "String":
                return "String"
            return "Any"
        elif isinstance(expr, ListLiteral):
            return "List"
        elif isinstance(expr, MapLiteral):
            return "Map"
        elif isinstance(expr, ListGet):
            return "Any"  # Element type depends on the list
        elif isinstance(expr, MapGet):
            return "Any"  # Value type depends on the map
        elif isinstance(expr, ListAppend):
            return "List"
        elif isinstance(expr, ListLength):
            return "Number"
        elif isinstance(expr, StringLength):
            return "Number"
        elif isinstance(expr, Substring):
            return "String"
        elif isinstance(expr, CharAt):
            return "String"
        elif isinstance(expr, StringSplit):
            return "List"
        elif isinstance(expr, StringTrim):
            return "String"
        elif isinstance(expr, StringJoin):
            return "String"
        elif isinstance(expr, StringReplace):
            return "String"
        elif isinstance(expr, StringToUpper):
            return "String"
        elif isinstance(expr, StringToLower):
            return "String"
        elif isinstance(expr, StringStartsWith):
            return "Boolean"
        elif isinstance(expr, StringEndsWith):
            return "Boolean"
        elif isinstance(expr, StringIsDigit):
            return "Boolean"
        elif isinstance(expr, StringIsLetter):
            return "Boolean"
        elif isinstance(expr, StringIsWhitespace):
            return "Boolean"
        elif isinstance(expr, MathMin):
            return "Number"
        elif isinstance(expr, MathMax):
            return "Number"
        elif isinstance(expr, MathAbs):
            return "Number"
        elif isinstance(expr, MathRound):
            return "Number"
        elif isinstance(expr, FileReadExpression):
            return "String"
        else:
            return "Any"

    # -------------------------------------------------------------------
    # Reporting
    # -------------------------------------------------------------------

    def get_symbol_table_summary(self) -> str:
        """Generate a human-readable summary of the symbol table."""
        lines = []
        lines.append("=== Symbol Table Summary ===")
        lines.append("")

        # Global scope
        lines.append("Global Scope:")
        if self.global_scope:
            for name, symbol in self.global_scope.symbols.items():
                lines.append(f"  {name}: {symbol.symbol_type} ({symbol.kind})")
            for name, symbol in self.global_scope.functions.items():
                lines.append(f"  {name}(): Function")

        lines.append("")
        lines.append(f"Total functions defined: {len(self.functions)}")
        lines.append(f"Total semantic errors: {len(self.errors)}")

        return "\n".join(lines)

    def print_errors(self):
        """Print all semantic errors to stdout."""
        if not self.errors:
            print("No semantic errors found.")
            return
        print(f"Found {len(self.errors)} semantic error(s):")
        for error in self.errors:
            print(f"  - {error}")
