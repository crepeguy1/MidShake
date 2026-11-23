from midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, Inquire,
    If, While, Terminate,
    Number, String, Variable, Binary, Response,
    FunctionDef, Call, Return, Import,
    FileReadExpression, FileWriteNode, FileWriteStatement,
    ListLiteral, MapLiteral, ListGet, MapGet,
    StringLength, Substring, CharAt, StringSplit, StringTrim, StringJoin,
    ListLength, ListAppend,
    MathMin, MathMax, MathAbs, MathRound,
    StringToUpper, StringToLower, StringStartsWith, StringEndsWith,
    StringIsDigit, StringIsLetter, StringIsWhitespace, StringReplace,
    Boolean, MapSet, Break, Continue, ForIn, GlobalSet
)


class CppCompiler:
    def __init__(self):
        self.lines = []
        self.indent = 0
        self._param_names = set()

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

        # Pre-pass: collect all function definitions, resolving imports
        if not hasattr(self, "_imported_files"):
            self._imported_files = set()

        all_funcs = self._collect_functions(program)
        main_stmts = self._collect_main_stmts(program)

        # emit function definitions
        for func in all_funcs:
            self.compile_function_def(func)

        # main()
        self.emit("int main() {")
        self.indent += 1
        self.emit("Environment env;")

        for stmt in main_stmts:
            self.compile_stmt(stmt)

        self.emit("return 0;")
        self.indent -= 1
        self.emit("}")

        return "\n".join(self.lines)

    def _collect_functions(self, program):
        """Walk the program (resolving imports) and collect all FunctionDef nodes."""
        funcs = []
        for section in program.sections:
            for stmt in section.body:
                if isinstance(stmt, FunctionDef):
                    funcs.append(stmt)
                elif isinstance(stmt, Import):
                    imported_funcs = self._import_program(stmt)
                    if imported_funcs:
                        funcs.extend(imported_funcs)
        return funcs

    def _collect_main_stmts(self, program):
        """Walk the program (resolving imports) and collect non-function statements."""
        stmts = []
        for section in program.sections:
            for stmt in section.body:
                if isinstance(stmt, FunctionDef):
                    continue
                elif isinstance(stmt, Import):
                    imported_stmts = self._import_main_stmts(stmt)
                    if imported_stmts:
                        stmts.extend(imported_stmts)
                else:
                    stmts.append(stmt)
        return stmts

    def _import_program(self, stmt: Import):
        """Load and parse an imported file, returning its FunctionDef nodes."""
        import os
        from midshake_tokenizer import Tokenizer
        from midshake_parser import Parser

        path = str(stmt.path).strip().strip('"').strip("'")
        candidates = [
            os.path.abspath(path),
            os.path.join(os.getcwd(), path),
            os.path.join(os.getcwd(), "stdlib", os.path.basename(path)),
        ]
        resolved = None
        for c in candidates:
            if os.path.isfile(c):
                resolved = c
                break
        if resolved is None:
            return []

        real_path = os.path.realpath(resolved)
        if real_path in self._imported_files:
            return []
        self._imported_files.add(real_path)

        with open(resolved, "r", encoding="utf-8") as f:
            source = f.read()

        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        imported_program = parser.parse()

        funcs = []
        for section in imported_program.sections:
            for s in section.body:
                if isinstance(s, FunctionDef):
                    funcs.append(s)
                elif isinstance(s, Import):
                    imported_funcs = self._import_program(s)
                    if imported_funcs:
                        funcs.extend(imported_funcs)
        return funcs

    def _import_main_stmts(self, stmt: Import):
        """Load and parse an imported file, returning its non-function statements."""
        import os
        from midshake_tokenizer import Tokenizer
        from midshake_parser import Parser

        path = str(stmt.path).strip().strip('"').strip("'")
        candidates = [
            os.path.abspath(path),
            os.path.join(os.getcwd(), path),
            os.path.join(os.getcwd(), "stdlib", os.path.basename(path)),
        ]
        resolved = None
        for c in candidates:
            if os.path.isfile(c):
                resolved = c
                break
        if resolved is None:
            return []

        real_path = os.path.realpath(resolved)
        if real_path in self._imported_files:
            return []
        self._imported_files.add(real_path)

        with open(resolved, "r", encoding="utf-8") as f:
            source = f.read()

        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        imported_program = parser.parse()

        stmts = []
        for section in imported_program.sections:
            for s in section.body:
                if isinstance(s, FunctionDef):
                    continue
                elif isinstance(s, Import):
                    imported_stmts = self._import_main_stmts(s)
                    if imported_stmts:
                        stmts.extend(imported_stmts)
                else:
                    stmts.append(s)
        return stmts

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
            self.emit(f'env.set("RESPONSE", {stmt.name}(env, args));')
            self.indent -= 1
            self.emit("}")

        # RETURN
        elif isinstance(stmt, Return):
            value = self.compile_expr(stmt.expr)
            self.emit(f'return {value};')

        # TERMINATE
        elif isinstance(stmt, Terminate):
            self.emit("return Value::from_double(0);")

        # BREAK
        elif isinstance(stmt, Break):
            self.emit("break;")

        # CONTINUE
        elif isinstance(stmt, Continue):
            self.emit("continue;")

        # FOR ... IN ... DO
        elif isinstance(stmt, ForIn):
            lst = self.compile_expr(stmt.list_expr)
            self.emit(f'for (const auto& {stmt.var_name} : {lst}.lst) {{')
            self.indent += 1
            self.emit(f'env.set("{stmt.var_name}", {stmt.var_name});')
            for s in stmt.body:
                self.compile_stmt(s)
            self.indent -= 1
            self.emit("}")

        # MAP SET: SET the key K IN the map M TO the value V
        elif isinstance(stmt, MapSet):
            mapping = self.compile_expr(stmt.map_expr)
            key = self.compile_expr(stmt.key_expr)
            value = self.compile_expr(stmt.value_expr)
            if isinstance(stmt.map_expr, Variable):
                map_name = stmt.map_expr.name
                self.emit(f'env.set("{map_name}", map_set({mapping}, {key}, {value}));')
            else:
                self.emit(f'map_set({mapping}, {key}, {value});')

        # GLOBAL SET: modify a global variable from within a function
        elif isinstance(stmt, GlobalSet):
            value = self.compile_expr(stmt.value)
            self.emit(f'env.set("{stmt.name}", {value});')

        # FILE WRITE
        elif isinstance(stmt, (FileWriteNode, FileWriteStatement)):
            value = self.compile_expr(stmt.value if isinstance(stmt, FileWriteStatement) else stmt.expr)
            path = str(stmt.path).strip().strip('"').strip("'")
            self.emit(f'file_write("{path}", {value});')

    # ------------------------------------------------------------
    # EXPRESSIONS
    # ------------------------------------------------------------
    def compile_expr(self, expr):

        if isinstance(expr, Number):
            return f'Value::from_double({expr.value})'

        if isinstance(expr, String):
            # Escape special characters for C++ strings
            escaped = str(expr.value)
            escaped = escaped.replace("\\", "\\\\")
            escaped = escaped.replace('"', '\\"')
            escaped = escaped.replace("\n", "\\n")
            escaped = escaped.replace("\t", "\\t")
            escaped = escaped.replace("\r", "\\r")
            return f'Value::from_string("{escaped}")'

        if isinstance(expr, Variable):
            return f'env.get("{expr.name}")'

        if isinstance(expr, Response):
            return 'env.get("RESPONSE")'

        if isinstance(expr, Binary):
            left = self.compile_expr(expr.left)
            right = self.compile_expr(expr.right)

            if expr.op == "+":
                return f'({left} + {right})'
            if expr.op == "-":
                return f'Value(Number({left}.num.value - {right}.num.value))'
            if expr.op == "*":
                return f'Value(Number({left}.num.value * {right}.num.value))'
            if expr.op == "/":
                return f'Value(Number({left}.num.value / {right}.num.value))'

            # comparisons: use value_equals for == and !=, to_string() for ordering
            if expr.op == "==":
                return f'Value(Number(value_equals({left}, {right}) ? 1 : 0))'
            if expr.op == "!=":
                return f'Value(Number(!value_equals({left}, {right}) ? 1 : 0))'
            # For ordering, use numeric comparison (MidShake uses numbers for comparisons)
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

        # List get: the item at position N in LIST
        if isinstance(expr, ListGet):
            lst = self.compile_expr(expr.list_expr)
            idx = self.compile_expr(expr.index_expr)
            return f'list_index({lst}, {idx})'

        # Map get: the value of KEY in MAP
        if isinstance(expr, MapGet):
            mapping = self.compile_expr(expr.map_expr)
            # Treat bare variable keys as string literals unless they are function params
            if isinstance(expr.key_expr, Variable):
                if expr.key_expr.name in self._param_names:
                    key = self.compile_expr(expr.key_expr)
                else:
                    key = f'Value::from_string("{expr.key_expr.name}")'
            else:
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

        # Math min
        if isinstance(expr, MathMin):
            left = self.compile_expr(expr.left)
            right = self.compile_expr(expr.right)
            return f'math_min({left}, {right})'

        # Math max
        if isinstance(expr, MathMax):
            left = self.compile_expr(expr.left)
            right = self.compile_expr(expr.right)
            return f'math_max({left}, {right})'

        # Math abs
        if isinstance(expr, MathAbs):
            e = self.compile_expr(expr.expr)
            return f'math_abs({e})'

        # Math round
        if isinstance(expr, MathRound):
            e = self.compile_expr(expr.expr)
            return f'math_round({e})'

        # String toUpperCase
        if isinstance(expr, StringToUpper):
            s = self.compile_expr(expr.string_expr)
            return f'string_toupper({s})'

        # String toLowerCase
        if isinstance(expr, StringToLower):
            s = self.compile_expr(expr.string_expr)
            return f'string_tolower({s})'

        # String startsWith
        if isinstance(expr, StringStartsWith):
            s = self.compile_expr(expr.string_expr)
            prefix = self.compile_expr(expr.prefix_expr)
            return f'string_startswith({s}, {prefix})'

        # String endsWith
        if isinstance(expr, StringEndsWith):
            s = self.compile_expr(expr.string_expr)
            suffix = self.compile_expr(expr.suffix_expr)
            return f'string_endswith({s}, {suffix})'

        # String isDigit
        if isinstance(expr, StringIsDigit):
            s = self.compile_expr(expr.string_expr)
            return f'string_isdigit({s})'

        # String isLetter
        if isinstance(expr, StringIsLetter):
            s = self.compile_expr(expr.string_expr)
            return f'string_isletter({s})'

        # String isWhitespace
        if isinstance(expr, StringIsWhitespace):
            s = self.compile_expr(expr.string_expr)
            return f'string_iswhitespace({s})'

        # File read: the contents of FILE
        if isinstance(expr, FileReadExpression):
            if isinstance(expr.path, str):
                path = expr.path.strip().strip('"').strip("'")
                return f'file_read("{path}")'
            else:
                # Dynamic path from a variable
                path_expr = self.compile_expr(expr.path)
                return f'file_read({path_expr}.to_string())'

        # Boolean literal
        if isinstance(expr, Boolean):
            return f'Value::from_double({1 if expr.value else 0})'

        # String replace: the replace of STRING with OLD to NEW
        if isinstance(expr, StringReplace):
            s = self.compile_expr(expr.string_expr)
            old = self.compile_expr(expr.old_expr)
            new = self.compile_expr(expr.new_expr)
            return f'string_replace({s}, {old}, {new})'

        raise ValueError(f"Unknown expression: {expr}")

    # ------------------------------------------------------------
    # FUNCTION DEF
    # ------------------------------------------------------------
    def compile_function_def(self, func: FunctionDef):
        self._param_names = set(func.param_names)
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
        self._param_names = set()

