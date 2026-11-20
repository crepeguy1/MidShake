from midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, Inquire,
    If, While, Terminate,
    Number, String, Variable, Binary, Response,
    FunctionDef, Call, Return,
    ListLiteral, MapLiteral, ListIndex, MapGet,
    StringLength, Substring, CharAt, StringSplit, StringTrim, StringJoin,
    ListLength, ListAppend
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
        self.emit("using namespace mish;")
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

        # List literal: [1, 2, 3]
        if isinstance(expr, ListLiteral):
            if not expr.elements:
                return 'Value::from_list({})'
            elements = ", ".join(self.compile_expr(e) for e in expr.elements)
            return f'Value::from_list({{{elements}}})'

        # Map literal: {key: value}
        if isinstance(expr, MapLiteral):
            if not expr.keys:
                return 'Value::from_map({})'
            pairs = []
            for k, v in zip(expr.keys, expr.values):
                key_str = self.compile_expr(k)
                val = self.compile_expr(v)
                pairs.append(f'{{{key_str}.to_string(), {val}}}')
            return f'Value::from_map({{{", ".join(pairs)}}})'

        # List index: the item at position N in LIST
        if isinstance(expr, ListIndex):
            lst = self.compile_expr(expr.list_expr)
            idx = self.compile_expr(expr.index_expr)
            return f'list_index({lst}, {idx})'

        # Map get: the value of KEY in MAP
        if isinstance(expr, MapGet):
            mapping = self.compile_expr(expr.map_expr)
            key = self.compile_expr(expr.key_expr)
            return f'map_get({mapping}, {key})'

        # String length: the length of STRING
        if isinstance(expr, StringLength):
            s = self.compile_expr(expr.string_expr)
            return f'string_length({s})'

        # Substring: the substring of STRING starting at START ending at END
        if isinstance(expr, Substring):
            s = self.compile_expr(expr.string_expr)
            start = self.compile_expr(expr.start_expr)
            end = self.compile_expr(expr.end_expr)
            return f'substring({s}, {start}, {end})'

        # Char at: the character at INDEX in STRING
        if isinstance(expr, CharAt):
            s = self.compile_expr(expr.string_expr)
            idx = self.compile_expr(expr.index_expr)
            return f'char_at({s}, {idx})'

        # String split: the split of STRING by DELIMITER
        if isinstance(expr, StringSplit):
            s = self.compile_expr(expr.string_expr)
            delim = self.compile_expr(expr.delimiter_expr)
            return f'string_split({s}, {delim})'

        # String trim: the trimmed STRING
        if isinstance(expr, StringTrim):
            s = self.compile_expr(expr.string_expr)
            return f'string_trim({s})'

        # String join: the join of LIST with DELIMITER
        if isinstance(expr, StringJoin):
            lst = self.compile_expr(expr.list_expr)
            delim = self.compile_expr(expr.delimiter_expr)
            return f'string_join({lst}, {delim})'

        # List length: the size of LIST
        if isinstance(expr, ListLength):
            lst = self.compile_expr(expr.list_expr)
            return f'list_length({lst})'

        # List append: the append of ELEMENT to LIST
        if isinstance(expr, ListAppend):
            lst = self.compile_expr(expr.list_expr)
            elem = self.compile_expr(expr.element_expr)
            return f'list_append({lst}, {elem})'

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

