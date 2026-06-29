from midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, Inquire,
    If, While, Terminate,
    Number, String, Variable, Binary, Response,
    FunctionDef, Call, Return
)


class CppCompiler:
    def __init__(self):
        self.lines = []
        self.indent = 0

    def emit(self, line: str = ""):
        self.lines.append("    " * self.indent + line)

    # ------------------------------------------------------------
    # TOP LEVEL
    # ------------------------------------------------------------
    def compile_program(self, program: Program) -> str:
        # includes and namespace
        self.emit('#include "midshake_runtime.hpp"')
        self.emit("using namespace ms;")
        self.emit("")

        # function definitions first
        for section in program.sections:
            for stmt in section.body:
                if isinstance(stmt, FunctionDef):
                    self.compile_function_def(stmt)

        # main()
        self.emit("int main() {")
        self.indent += 1
        self.emit("Environment env;")

        for section in program.sections:
            for stmt in section.body:
                if not isinstance(stmt, FunctionDef):
                    self.compile_stmt(stmt)

        self.emit("return 0;")
        self.indent -= 1
        self.emit("}")

        return "\n".join(self.lines)

    # ------------------------------------------------------------
    # STATEMENTS
    # ------------------------------------------------------------
    def compile_stmt(self, stmt):

        # LET
        if isinstance(stmt, Let):
            value = self.compile_expr(stmt.value)
            self.emit(f'env.set("{stmt.name}", {value});')

        # SET
        elif isinstance(stmt, Set):
            value = self.compile_expr(stmt.value)
            self.emit(f'env.set("{stmt.name}", {value});')

        # PROCLAIM
        elif isinstance(stmt, Proclaim):
            value = self.compile_expr(stmt.value)
            self.emit(f'print({value});')

        # INQUIRE
        elif isinstance(stmt, Inquire):
            if stmt.expected_type == "number":
                self.emit(
                    f'env.set("RESPONSE", inquire_number("{stmt.question}"));'
                )
            else:
                self.emit(
                    f'env.set("RESPONSE", inquire_string("{stmt.question}"));'
                )

        # IF
        elif isinstance(stmt, If):
            cond = self.compile_expr(stmt.expr)
            self.emit(f'if ({cond}.num.value != 0) {{')
            self.indent += 1
            for s in stmt.body:
                self.compile_stmt(s)
            self.indent -= 1
            self.emit("}")
            if stmt.else_body:
                self.emit("else {")
                self.indent += 1
                for s in stmt.else_body:
                    self.compile_stmt(s)
                self.indent -= 1
                self.emit("}")

        # WHILE
        elif isinstance(stmt, While):
            cond = self.compile_expr(stmt.expr)
            self.emit(f'while ({cond}.num.value != 0) {{')
            self.indent += 1
            for s in stmt.body:
                self.compile_stmt(s)
            self.indent -= 1
            self.emit("}")

        # CALL
        elif isinstance(stmt, Call):
            self.emit("{")
            self.indent += 1
            self.emit("std::vector<Value> args;")
            for arg in stmt.args:
                self.emit(f"args.push_back({self.compile_expr(arg)});")
            self.emit(f'{stmt.name}(env, args);')
            self.indent -= 1
            self.emit("}")

        # RETURN
        elif isinstance(stmt, Return):
            value = self.compile_expr(stmt.expr)
            self.emit(f'return {value};')

        # TERMINATE
        elif isinstance(stmt, Terminate):
            self.emit("return Value::from_double(0);")

    # ------------------------------------------------------------
    # EXPRESSIONS
    # ------------------------------------------------------------
    def compile_expr(self, expr):

        if isinstance(expr, Number):
            return f'Value::from_double({expr.value})'

        if isinstance(expr, String):
            # naive escaping; you can improve later
            return f'Value::from_string("{expr.value}")'

        if isinstance(expr, Variable):
            return f'env.get("{expr.name}")'

        if isinstance(expr, Response):
            return 'env.get("RESPONSE")'

        if isinstance(expr, Binary):
            left = self.compile_expr(expr.left)
            right = self.compile_expr(expr.right)

            if expr.op == "+":
                return f'Value(Number({left}.num.value + {right}.num.value))'
            if expr.op == "-":
                return f'Value(Number({left}.num.value - {right}.num.value))'
            if expr.op == "*":
                return f'Value(Number({left}.num.value * {right}.num.value))'
            if expr.op == "/":
                return f'Value(Number({left}.num.value / {right}.num.value))'

            # comparisons: return 1 or 0 as Number
            return (
                f'Value(Number(({left}.num.value {expr.op} '
                f'{right}.num.value) ? 1 : 0))'
            )

        raise ValueError(f"Unknown expression: {expr}")

    # ------------------------------------------------------------
    # FUNCTION DEF
    # ------------------------------------------------------------
    def compile_function_def(self, func: FunctionDef):
        self.emit(
            f"Value {func.name}(Environment& env, "
            f"const std::vector<Value>& args) {{"
        )
        self.indent += 1

        # bind parameters
        for i, name in enumerate(func.param_names):
            self.emit(f'env.set("{name}", args[{i}]);')

        # body
        for stmt in func.body:
            self.compile_stmt(stmt)

        # default return if no explicit RETURN hit
        self.emit('return Value::from_double(0);')

        self.indent -= 1
        self.emit("}")
        self.emit("")
