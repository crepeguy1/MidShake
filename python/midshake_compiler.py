from dataclasses import fields, is_dataclass

from midshake_ast import (
    Program, Section,
    Let, Set, MemberSet, Proclaim, Inquire,
    If, While, Terminate,
    Number, String, Variable, MemberAccess, NewInstance, Binary, Response,
    FunctionDef, ClassDef, Call, Return, Import,
    FileReadExpression, FileWriteNode, FileWriteStatement,
    ListLiteral, MapLiteral, ListGet, MapGet,
    StringLength, Substring, CharAt, StringSplit, StringTrim, StringJoin,
    ListLength, ListAppend,
    MathMin, MathMax, MathAbs, MathRound,
    StringToUpper, StringToLower, StringStartsWith, StringEndsWith,
    StringIsDigit, StringIsLetter, StringIsWhitespace, StringReplace, StringIndexOf,
    Boolean, MapSet, Break, Continue, ForIn, GlobalSet, Private, Protected, Public
)

STDLIB_RUNTIME_FUNCTIONS = {
    "println", "greet", "add_and_print", "repeat", "min", "max", "abs", "round",
    "toupper", "tolower", "startsWith", "endsWith", "isDigit", "isLetter",
    "isWhitespace", "readFile", "length", "charAt", "substring", "split", "join",
    "trim", "replace", "size", "append", "getItem", "mapSet", "mapGet", "indexOf",
}


class CppCompiler:
    def __init__(self):
        self.lines = []
        self.indent = 0
        self._param_names = set()
        self._current_class = None

    def emit(self, line: str = ""):
        self.lines.append("    " * self.indent + line)

    @staticmethod
    def _function_symbol(func):
        if func.owner_class:
            return f"ms_class_{func.owner_class}_{func.name}"
        return func.name

    @staticmethod
    def _field_initializer_symbol(class_def, field):
        return f"ms_field_{class_def.name}_{field.name}"

    @staticmethod
    def _access_level(visibility):
        if isinstance(visibility, Private):
            return "AccessLevel::Private"
        if isinstance(visibility, Protected):
            return "AccessLevel::Protected"
        return "AccessLevel::Public"

    # ------------------------------------------------------------
    # TOP LEVEL
    # ------------------------------------------------------------
    def compile_program(self, program: Program) -> str:
        self._validate_import_visibility(program)
        self._imported_function_files = set()
        self._imported_main_files = set()

        # includes and namespace
        self.emit('#include "midshake_runtime.hpp"')
        self.emit("using namespace ms;")
        self.emit("")

        # Pre-pass: collect declarations, resolving imports.
        all_funcs = self._collect_functions(program)
        self._classes = self._collect_classes(program)
        main_stmts = self._collect_main_stmts(program)

        # Deduplicate functions by name (later definitions override earlier ones)
        seen_names = set()
        unique_funcs = []
        for func in reversed(all_funcs):
            symbol = self._function_symbol(func)
            if symbol not in seen_names:
                seen_names.add(symbol)
                unique_funcs.append(func)
        unique_funcs.reverse()
        self._defined_function_names = {self._function_symbol(func) for func in unique_funcs if not func.owner_class}

        for func in unique_funcs:
            symbol = self._function_symbol(func)
            self.emit(f"Value {symbol}(Environment&, const std::vector<Value>&);")
        for class_def in self._classes:
            for member in class_def.members:
                if isinstance(member, Let):
                    symbol = self._field_initializer_symbol(class_def, member)
                    self.emit(f"Value {symbol}(Environment&);")
        self.emit("")

        # Emit field initializers and function definitions.
        for class_def in self._classes:
            for member in class_def.members:
                if isinstance(member, Let):
                    self.compile_field_initializer(class_def, member)
        for func in unique_funcs:
            self.compile_function_def(func)

        # main() with command-line argument support
        self.emit("int main(int argc, char* argv[]) {")
        self.indent += 1
        self.emit("Environment env(argc, argv);")

        for class_def in self._classes:
            base_name = class_def.base_name or ""
            self.emit(f'register_class("{class_def.name}", "{base_name}");')
        for class_def in self._classes:
            for member in class_def.members:
                if isinstance(member, Let):
                    self.emit(
                        f'register_class_field("{class_def.name}", "{member.name}", '
                        f'{self._access_level(member.visibility)}, &{self._field_initializer_symbol(class_def, member)});'
                    )
                elif isinstance(member, FunctionDef):
                    self.emit(
                        f'register_class_method("{class_def.name}", "{member.name}", '
                        f'{self._access_level(member.visibility)}, {len(member.param_names)}, '
                        f'&{self._function_symbol(member)});'
                    )

        for stmt in main_stmts:
            self.compile_stmt(stmt)

        self.emit("return 0;")
        self.indent -= 1
        self.emit("}")

        return "\n".join(self.lines)

    def _parse_visibility_import(self, stmt):
        import os
        from midshake_tokenizer import Tokenizer
        from midshake_parser import Parser

        path = str(stmt.path).strip().strip('"').strip("'")
        normalized_path = path.replace("\\", "/")
        if os.path.basename(normalized_path) == "stdlib.mish":
            return None

        candidates = [
            os.path.abspath(path),
            os.path.join(os.getcwd(), path),
            os.path.join(os.getcwd(), "stdlib", os.path.basename(path)),
        ]
        resolved = next((candidate for candidate in candidates if os.path.isfile(candidate)), None)
        if resolved is None:
            return None

        with open(resolved, "r", encoding="utf-8") as source_file:
            source = source_file.read()
        return Parser(Tokenizer(source).tokenize()).parse(), os.path.realpath(resolved)

    def _validate_import_visibility(self, program):
        private_vars = set()
        private_functions = set()
        private_classes = set()

        imported_files = set()

        def collect_import_visibility(stmt):
            imported_result = self._parse_visibility_import(stmt)
            if imported_result is None:
                return
            imported_program, real_path = imported_result
            if real_path in imported_files:
                return
            imported_files.add(real_path)

            for imported_section in imported_program.sections:
                for imported_stmt in imported_section.body:
                    if isinstance(imported_stmt, Let) and isinstance(imported_stmt.visibility, Private):
                        private_vars.add(imported_stmt.name)
                    elif isinstance(imported_stmt, FunctionDef) and isinstance(imported_stmt.visibility, Private):
                        private_functions.add(imported_stmt.name)
                    elif isinstance(imported_stmt, ClassDef) and isinstance(imported_stmt.visibility, Private):
                        private_classes.add(imported_stmt.name)
                    elif isinstance(imported_stmt, Import):
                        collect_import_visibility(imported_stmt)

        for section in program.sections:
            for stmt in section.body:
                if isinstance(stmt, Import):
                    collect_import_visibility(stmt)

        local_vars = {
            stmt.name
            for section in program.sections
            for stmt in section.body
            if isinstance(stmt, Let)
        }
        local_functions = {
            stmt.name
            for section in program.sections
            for stmt in section.body
            if isinstance(stmt, FunctionDef)
        }

        def declared_local_vars(statements):
            names = set()
            for stmt in statements:
                if isinstance(stmt, Let):
                    names.add(stmt.name)
                elif isinstance(stmt, FunctionDef):
                    continue
                elif is_dataclass(stmt):
                    for descriptor in fields(stmt):
                        value = getattr(stmt, descriptor.name)
                        if isinstance(value, list):
                            names.update(declared_local_vars(value))
            return names

        def check_access(node, visible_vars, visible_functions):
            if isinstance(node, Variable):
                if node.name in private_vars and node.name not in visible_vars:
                    raise ValueError(
                        f"MidShake Access Error:\n"
                        f"  Variable '{node.name}' is Private in an imported file and cannot be accessed directly."
                    )
                return

            if isinstance(node, Call):
                if "." not in node.name and node.name in private_functions and node.name not in visible_functions:
                    raise ValueError(
                        f"MidShake Access Error:\n"
                        f"  Function '{node.name}' is Private in an imported file and cannot be called directly."
                    )
                for argument in node.args:
                    check_access(argument, visible_vars, visible_functions)
                return

            if isinstance(node, NewInstance):
                if node.class_name in private_classes:
                    raise ValueError(
                        f"MidShake Access Error:\n"
                        f"  Class '{node.class_name}' is Private in an imported file and cannot be instantiated directly."
                    )
                return

            if isinstance(node, (Set, GlobalSet)):
                if node.name in private_vars and node.name not in visible_vars:
                    raise ValueError(
                        f"MidShake Access Error:\n"
                        f"  Variable '{node.name}' is Private in an imported file and cannot be modified directly."
                    )
                check_access(node.value, visible_vars, visible_functions)
                return

            if isinstance(node, FunctionDef):
                function_vars = set(visible_vars)
                function_vars.update(node.param_names)
                function_vars.update(declared_local_vars(node.body))
                for body_stmt in node.body:
                    check_access(body_stmt, function_vars, visible_functions)
                return

            if isinstance(node, MapLiteral):
                for key, value in zip(node.keys, node.values):
                    if not isinstance(key, Variable):
                        check_access(key, visible_vars, visible_functions)
                    check_access(value, visible_vars, visible_functions)
                return

            if isinstance(node, MapGet):
                check_access(node.map_expr, visible_vars, visible_functions)
                if not isinstance(node.key_expr, Variable):
                    check_access(node.key_expr, visible_vars, visible_functions)
                return

            if isinstance(node, Import):
                return

            if isinstance(node, (list, tuple)):
                for child in node:
                    check_access(child, visible_vars, visible_functions)
                return

            if is_dataclass(node):
                for descriptor in fields(node):
                    check_access(getattr(node, descriptor.name), visible_vars, visible_functions)

        for section in program.sections:
            for stmt in section.body:
                check_access(stmt, local_vars, local_functions)

    def _collect_functions(self, program):
        """Walk the program (resolving imports) and collect all FunctionDef nodes."""
        funcs = []
        for section in program.sections:
            for stmt in section.body:
                if isinstance(stmt, FunctionDef):
                    funcs.append(stmt)
                elif isinstance(stmt, ClassDef):
                    funcs.extend(member for member in stmt.members if isinstance(member, FunctionDef))
                elif isinstance(stmt, Import):
                    imported_funcs = self._import_program(stmt)
                    if imported_funcs:
                        funcs.extend(imported_funcs)
        return funcs

    def _collect_classes(self, program):
        classes = []
        seen_files = set()

        def collect(current_program):
            for section in current_program.sections:
                for stmt in section.body:
                    if isinstance(stmt, ClassDef):
                        classes.append(stmt)
                    elif isinstance(stmt, Import):
                        imported = self._parse_visibility_import(stmt)
                        if imported is None:
                            continue
                        imported_program, real_path = imported
                        if real_path in seen_files:
                            continue
                        seen_files.add(real_path)
                        collect(imported_program)

        collect(program)
        return classes

    def _collect_main_stmts(self, program):
        """Walk the program (resolving imports) and collect non-function statements."""
        stmts = []
        for section in program.sections:
            for stmt in section.body:
                if isinstance(stmt, (FunctionDef, ClassDef)):
                    continue
                elif isinstance(stmt, Import):
                    imported_stmts = self._import_main_stmts(stmt)
                    if imported_stmts:
                        stmts.extend(imported_stmts)
                else:
                    stmts.append(stmt)
        return stmts

    def _resolve_call_name(self, name):
        if name in self._defined_function_names:
            return name
        if name in STDLIB_RUNTIME_FUNCTIONS:
            return f"ms_std_{name}"
        return name

    def _import_program(self, stmt: Import):
        """Load and parse an imported file, returning its FunctionDef nodes."""
        import os
        from midshake_tokenizer import Tokenizer
        from midshake_parser import Parser

        path = str(stmt.path).strip().strip('"').strip("'")
        normalized_path = path.replace("\\", "/")
        if normalized_path == "stdlib/stdlib.mish" or os.path.basename(normalized_path) == "stdlib.mish":
            return []
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
        if real_path in self._imported_function_files:
            return []
        self._imported_function_files.add(real_path)

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
                elif isinstance(s, ClassDef):
                    funcs.extend(member for member in s.members if isinstance(member, FunctionDef))
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
        normalized_path = path.replace("\\", "/")
        if normalized_path == "stdlib/stdlib.mish" or os.path.basename(normalized_path) == "stdlib.mish":
            return []
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
        if real_path in self._imported_main_files:
            return []
        self._imported_main_files.add(real_path)

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
            if "." in stmt.name:
                target_name, method_name = stmt.name.rsplit(".", 1)
                target = self.compile_expr(self._member_target_expression(target_name))
                caller_class = self._current_class or ""
                self.emit(
                    f'env.set("RESPONSE", call_object_method(env, {target}, "{method_name}", '
                    f'args, "{caller_class}"));'
                )
            else:
                call_name = self._resolve_call_name(stmt.name)
                self.emit(f'env.set("RESPONSE", {call_name}(env, args));')
            self.indent -= 1
            self.emit("}")

        # RETURN
        elif isinstance(stmt, Return):
            value = self.compile_expr(stmt.expr)
            self.emit(f'return {value};')

        # TERMINATE
        elif isinstance(stmt, Terminate):
            self.emit("return 0;")

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

        elif isinstance(stmt, MemberSet):
            target = self.compile_expr(stmt.target)
            value = self.compile_expr(stmt.value)
            caller_class = self._current_class or ""
            self.emit(
                f'object_set_member({target}, "{stmt.name}", {value}, "{caller_class}");'
            )

        elif isinstance(stmt, ClassDef):
            return

        # GLOBAL SET: modify a global variable from within a function
        elif isinstance(stmt, GlobalSet):
            value = self.compile_expr(stmt.value)
            self.emit(f'env.set_global("{stmt.name}", {value});')

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

        if isinstance(expr, MemberAccess):
            target = self.compile_expr(expr.target)
            caller_class = self._current_class or ""
            return f'object_get_member({target}, "{expr.name}", "{caller_class}")'

        if isinstance(expr, NewInstance):
            args = ", ".join(self.compile_expr(arg) for arg in expr.args)
            return (
                f'create_object(env, "{expr.class_name}", '
                f'std::vector<Value>{{{args}}})'
            )

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
                # Treat bare identifier keys as string literals
                if isinstance(k, Variable):
                    key_str = f'Value::from_string("{k.name}")'
                else:
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

        # String indexOf: the index of SUBSTR in STRING
        if isinstance(expr, StringIndexOf):
            s = self.compile_expr(expr.string_expr)
            sub = self.compile_expr(expr.substr_expr)
            return f'string_indexof({s}, {sub})'

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
        self._current_class = func.owner_class
        function_symbol = self._function_symbol(func)
        self.emit(
            f"Value {function_symbol}(Environment& parent_env, "
            f"const std::vector<Value>& args) {{"
        )
        self.indent += 1
        self.emit("Environment env(parent_env);")

        # Bind the implicit instance before method parameters.
        arg_offset = 0
        if func.owner_class:
            self.emit('env.set("this", args.at(0));')
            arg_offset = 1

        # bind parameters
        for i, name in enumerate(func.param_names):
            self.emit(f'env.set("{name}", args.at({i + arg_offset}));')

        # body
        for stmt in func.body:
            self.compile_stmt(stmt)

        # default return if no explicit RETURN hit
        self.emit('return Value::from_double(0);')

        self.indent -= 1
        self.emit("}")
        self.emit("")
        self._param_names = set()
        self._current_class = None

    def compile_field_initializer(self, class_def, field):
        self._current_class = None
        self.emit(f"Value {self._field_initializer_symbol(class_def, field)}(Environment& env) {{")
        self.indent += 1
        self.emit(f"return {self.compile_expr(field.value)};")
        self.indent -= 1
        self.emit("}")
        self.emit("")

    @staticmethod
    def _member_target_expression(target_name):
        parts = [part.strip() for part in target_name.split(".")]
        target = Variable(parts[0])
        for part in parts[1:]:
            target = MemberAccess(target, part)
        return target

