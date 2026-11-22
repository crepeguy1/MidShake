# midshake_runtime.py

import os
import copy
from typing import Dict, Any
from midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, If, While, Terminate,
    Number, String, Variable, Binary, Inquire,
    Response, FunctionDef, Call, Return, FileReadExpression,
    FileWriteStatement, Import,
    ListLiteral, MapLiteral, ListGet, MapGet, ListAppend, ListLength,
    StringLength, Substring, CharAt, StringSplit, StringTrim, StringJoin,
    MathMin, MathMax, MathAbs, MathRound,
    StringToUpper, StringToLower, StringStartsWith, StringEndsWith,
    StringIsDigit, StringIsLetter, StringIsWhitespace,
    Boolean, MapSet, Break, Continue, ForIn, GlobalSet
)


class Runtime:

    def __init__(self) -> None:
        self.vars: Dict[str, Any] = {}
        self.functions: Dict[str, FunctionDef] = {}
        self.terminated: bool = False
        self.return_value = None
        self.in_function = False
        # Global variables that survive deep copy across function calls
        self.globals: Dict[str, Any] = {}






    # ------------------------------------------------------------
    # PROGRAM EXECUTION
    # ------------------------------------------------------------
    def exec_program(self, program: Program) -> None:
        for section in program.sections:
            if self.terminated:
                break
            self.exec_section(section)

    def exec_section(self, section: Section) -> None:
        for stmt in section.body:
            if self.terminated:
                break
            self.exec_stmt(stmt)

    # ------------------------------------------------------------
    # UTILITIES
    # ------------------------------------------------------------
    def require_declared(self, name: str):
        if name not in self.vars:
            raise ValueError(
                f"MidShake Runtime Error:\n"
                f"  The variable '{name}' was never declared with LET."
            )

    # ------------------------------------------------------------
    # IMPORT
    # ------------------------------------------------------------
    def exec_import(self, stmt: Import) -> None:
        from midshake_tokenizer import Tokenizer
        from midshake_parser import Parser

        path = str(stmt.path).strip().strip('"').strip("'")

        # resolve relative to the current working directory first,
        # then relative to the stdlib directory
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
            raise ValueError(
                f"MidShake Runtime Error:\n"
                f"  Could not find the file '{path}' for IMPORT."
            )

        # prevent circular imports by tracking what's been imported
        if not hasattr(self, "_imported_files"):
            self._imported_files = set()

        real_path = os.path.realpath(resolved)
        if real_path in self._imported_files:
            return  # already imported, skip
        self._imported_files.add(real_path)

        with open(resolved, "r", encoding="utf-8") as f:
            source = f.read()

        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        self.exec_program(program)

    # ------------------------------------------------------------
    # EXPRESSION EVALUATION
    # ------------------------------------------------------------
    def eval_expr(self, expr):
        if isinstance(expr, Number):
            return expr.value

        if isinstance(expr, String):
            return expr.value

        if isinstance(expr, Boolean):
            return expr.value

        if isinstance(expr, Variable):
            self.require_declared(expr.name)
            # Check globals first (for GLOBAL SET variables), then local vars
            if expr.name in self.globals:
                return self.globals[expr.name]
            return self.vars[expr.name]

        if isinstance(expr, Call):
            return self.exec_stmt(expr)

        if isinstance(expr, Response):
            return self.vars.get("RESPONSE")

        if isinstance(expr, Binary):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)

            if expr.op == "+":
                return left + right
            if expr.op == "-":
                return left - right
            if expr.op == "*":
                return left * right
            if expr.op == "/":
                return left / right
            if expr.op == ">":
                return left > right
            if expr.op == "<":
                return left < right
            if expr.op == ">=":
                return left >= right
            if expr.op == "<=":
                return left <= right
            if expr.op == "==":
                return left == right
            if expr.op == "!=":
                return left != right


        if isinstance(expr, FileReadExpression):
            # path can be a string literal or an Expression (variable)
            if isinstance(expr.path, str):
                path = expr.path
            else:
                path = str(self.eval_expr(expr.path))
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Could not read the file '{path}'.\n"
                    f"  Details: {e}"
                )

        # List literal
        if isinstance(expr, ListLiteral):
            return [self.eval_expr(e) for e in expr.elements]

        # Map literal
        if isinstance(expr, MapLiteral):
            result = {}
            for k, v in zip(expr.keys, expr.values):
                # Map keys that are bare identifiers are treated as string keys
                if isinstance(k, Variable):
                    key = k.name
                elif isinstance(k, String):
                    key = k.value
                else:
                    key = self.eval_expr(k)
                    if isinstance(key, (int, float)):
                        key = str(key)
                    elif not isinstance(key, str):
                        key = str(key)
                result[key] = self.eval_expr(v)
            return result

        # List get: the item at position N in LIST
        if isinstance(expr, ListGet):
            lst = self.eval_expr(expr.list_expr)
            idx = self.eval_expr(expr.index_expr)
            if not isinstance(lst, list):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a list but got a different type."
                )
            if idx < 0 or idx >= len(lst):
                # Return empty string instead of crashing - needed for self-hosting loops
                return ""
            return lst[idx]

        # List append: the append of X to LIST
        if isinstance(expr, ListAppend):
            lst = self.eval_expr(expr.list_expr)
            elem = self.eval_expr(expr.element_expr)
            if not isinstance(lst, list):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a list but got a different type."
                )
            return lst + [elem]

        # List length: the size of LIST
        if isinstance(expr, ListLength):
            lst = self.eval_expr(expr.list_expr)
            if not isinstance(lst, list):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a list but got a different type."
                )
            return len(lst)

        # Map get: the value of KEY in MAP
        if isinstance(expr, MapGet):
            mapping = self.eval_expr(expr.map_expr)
            # Map keys: evaluate the key expression to get the actual key value
            if isinstance(expr.key_expr, String):
                # String literal key: use the literal value directly
                key = expr.key_expr.value
            elif isinstance(expr.key_expr, Variable):
                # Bare identifier: first try to evaluate it as a variable
                # (for cases like mapGet where key is a function parameter)
                # If the variable doesn't exist, fall back to using the name as the key
                # (for cases like "the value of name in mymap" where name is a symbol key)
                try:
                    key = self.eval_expr(expr.key_expr)
                    if isinstance(key, (int, float)):
                        key = str(key)
                    elif not isinstance(key, str):
                        key = str(key)
                except ValueError:
                    # Variable not declared — use the identifier name as the string key
                    key = expr.key_expr.name
            else:
                # Other expression: evaluate it to get the key
                key = self.eval_expr(expr.key_expr)
                if isinstance(key, (int, float)):
                    key = str(key)
                elif not isinstance(key, str):
                    key = str(key)
            if not isinstance(mapping, dict):
                return ""
            if key not in mapping:
                return ""
            return mapping[key]

        # String length: the length of STRING
        if isinstance(expr, StringLength):
            s = self.eval_expr(expr.string_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return len(s)

        # Substring: the substring of STRING starting at S ending at E
        if isinstance(expr, Substring):
            s = self.eval_expr(expr.string_expr)
            start = self.eval_expr(expr.start_expr)
            end = self.eval_expr(expr.end_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return s[start:end]

        # Character at: the character at N in STRING
        if isinstance(expr, CharAt):
            s = self.eval_expr(expr.string_expr)
            idx = self.eval_expr(expr.index_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            if idx < 0 or idx >= len(s):
                # Return empty string instead of crashing - needed for self-hosting loops
                # that check bounds before accessing
                return ""
            return s[idx]

        # String split: the split of STRING by DELIMITER
        if isinstance(expr, StringSplit):
            s = self.eval_expr(expr.string_expr)
            delim = self.eval_expr(expr.delimiter_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return s.split(str(delim))

        # String trim: the trimmed STRING
        if isinstance(expr, StringTrim):
            s = self.eval_expr(expr.string_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return s.strip()

        # String join: the join of LIST with DELIMITER
        if isinstance(expr, StringJoin):
            lst = self.eval_expr(expr.list_expr)
            delim = self.eval_expr(expr.delimiter_expr)
            if not isinstance(lst, list):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a list but got a different type."
                )
            return str(delim).join(str(item) for item in lst)

        # Math min: the minimum of A and B
        if isinstance(expr, MathMin):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            return min(left, right)

        # Math max: the maximum of A and B
        if isinstance(expr, MathMax):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            return max(left, right)

        # Math abs: the absolute value of X
        if isinstance(expr, MathAbs):
            val = self.eval_expr(expr.expr)
            return abs(val)

        # Math round: the rounded value of X
        if isinstance(expr, MathRound):
            val = self.eval_expr(expr.expr)
            return round(val)

        # String toUpperCase: the uppercase of STRING
        if isinstance(expr, StringToUpper):
            s = self.eval_expr(expr.string_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return s.upper()

        # String toLowerCase: the lowercase of STRING
        if isinstance(expr, StringToLower):
            s = self.eval_expr(expr.string_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return s.lower()

        # String startsWith: STRING starts with PREFIX
        if isinstance(expr, StringStartsWith):
            s = self.eval_expr(expr.string_expr)
            prefix = self.eval_expr(expr.prefix_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return 1 if str(s).startswith(str(prefix)) else 0

        # String endsWith: STRING ends with SUFFIX
        if isinstance(expr, StringEndsWith):
            s = self.eval_expr(expr.string_expr)
            suffix = self.eval_expr(expr.suffix_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return 1 if str(s).endswith(str(suffix)) else 0

        # String isDigit: the character X is a digit
        if isinstance(expr, StringIsDigit):
            s = self.eval_expr(expr.string_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return 1 if str(s).isdigit() and len(str(s)) == 1 else 0

        # String isLetter: the character X is a letter
        if isinstance(expr, StringIsLetter):
            s = self.eval_expr(expr.string_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return 1 if str(s).isalpha() and len(str(s)) == 1 else 0

        # String isWhitespace: the character X is whitespace
        if isinstance(expr, StringIsWhitespace):
            s = self.eval_expr(expr.string_expr)
            if not isinstance(s, str):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a string but got a different type."
                )
            return 1 if str(s).isspace() and len(str(s)) == 1 else 0

        raise ValueError(
            f"MidShake Runtime Error:\n"
            f"  Unknown expression type: {expr}"
        )

    # ------------------------------------------------------------
    # STATEMENT EXECUTION
    # ------------------------------------------------------------
    def exec_stmt(self, stmt):

        # LET
        if isinstance(stmt, Let):
            self.vars[stmt.name] = self.eval_expr(stmt.value)

        # SET
        elif isinstance(stmt, Set):
            self.require_declared(stmt.name)
            self.vars[stmt.name] = self.eval_expr(stmt.value)

        # PROCLAIM
        elif isinstance(stmt, Proclaim):
            value = self.eval_expr(stmt.value)
            print(value)

        # IF
        elif isinstance(stmt, If):
            if self.eval_expr(stmt.expr):
                for s in stmt.body:
                    result = self.exec_stmt(s)
                    if result is not None and result in ("__break__", "__continue__"):
                        return result
            elif stmt.else_body is not None:
                for s in stmt.else_body:
                    result = self.exec_stmt(s)
                    if result is not None and result in ("__break__", "__continue__"):
                        return result

        # WHILST
        elif isinstance(stmt, While):
            while self.eval_expr(stmt.expr) and not self.terminated:
                should_break = False
                for s in stmt.body:
                    result = self.exec_stmt(s)
                    if result is not None and result == "__break__":
                        should_break = True
                        break
                    if result is not None and result == "__continue__":
                        break
                if should_break:
                    break

        # FOR ... IN ... DO
        elif isinstance(stmt, ForIn):
            lst = self.eval_expr(stmt.list_expr)
            if not isinstance(lst, list):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a list for FOR loop but got a different type."
                )
            for item in lst:
                self.vars[stmt.var_name] = item
                should_break = False
                for s in stmt.body:
                    result = self.exec_stmt(s)
                    if result is not None and result == "__break__":
                        should_break = True
                        break
                    if result is not None and result == "__continue__":
                        break
                if should_break:
                    break

        # BREAK
        elif isinstance(stmt, Break):
            return "__break__"

        # CONTINUE
        elif isinstance(stmt, Continue):
            return "__continue__"

        # MAP SET: SET the key K IN the map M TO the value V
        elif isinstance(stmt, MapSet):
            # Get the map variable name so we can update it in the environment
            if isinstance(stmt.map_expr, Variable):
                map_name = stmt.map_expr.name
            else:
                map_name = None
            mapping = self.eval_expr(stmt.map_expr)
            if not isinstance(mapping, dict):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Expected a map but got a different type."
                )
            # Evaluate key
            if isinstance(stmt.key_expr, Variable):
                key = stmt.key_expr.name
            elif isinstance(stmt.key_expr, String):
                key = stmt.key_expr.value
            else:
                key = self.eval_expr(stmt.key_expr)
                if isinstance(key, (int, float)):
                    key = str(key)
                elif not isinstance(key, str):
                    key = str(key)
            value = self.eval_expr(stmt.value_expr)
            mapping[key] = value
            # Update the variable in the environment
            if map_name and map_name in self.vars:
                self.vars[map_name] = mapping

        # INQUIRE
        elif isinstance(stmt, Inquire):
            raw = input(stmt.question + " ")

            # Convert based on expected type
            if stmt.expected_type == "number":
                try:
                    value = int(raw)
                except ValueError:
                    try:
                        value = float(raw)
                    except ValueError:
                        raise ValueError(f"Expected a number but got: {raw}")
            else:
                value = raw

            # Store in RESPONSE for LET ... BE the RESPONSE
            self.vars["RESPONSE"] = value
            return value

        # FUNCTION DEF
        elif isinstance(stmt, FunctionDef):
            # store function, do not execute body now
            self.functions[stmt.name] = stmt

        # CALL
        elif isinstance(stmt, Call):
            if stmt.name not in self.functions:
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  The function '{stmt.name}' is not defined."
                )

            func = self.functions[stmt.name]

            if len(stmt.args) != len(func.param_names):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Function '{func.name}' expects {len(func.param_names)} argument(s) "
                    f"but got {len(stmt.args)}."
                )

            # save environment with deep copy for recursion support
            saved_vars = copy.deepcopy(self.vars)
            saved_return = self.return_value
            saved_flag = self.in_function

            # bind parameters
            for param_name, arg_expr in zip(func.param_names, stmt.args):
                self.vars[param_name] = self.eval_expr(arg_expr)

            # run function body
            self.return_value = None
            self.in_function = False

            for s in func.body:
                self.exec_stmt(s)
                if self.in_function:  # RETURN was hit
                    break

            # capture return value
            result = self.return_value

            # restore environment
            self.vars = saved_vars
            self.return_value = saved_return
            self.in_function = saved_flag

            # store in RESPONSE for LET ... BE the RESPONSE
            self.vars["RESPONSE"] = result

            # return the function result to the caller
            return result

        # RETURN
        elif isinstance(stmt, Return):
            self.return_value = self.eval_expr(stmt.expr)
            # signal to stop executing the function body
            self.in_function = True

        # FILE WRITE
        elif isinstance(stmt, FileWriteStatement):
            value = self.eval_expr(stmt.value)
            path = str(stmt.path).strip().strip('"').strip("'")
            try:
                parent = os.path.dirname(path)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(value))
            except Exception as e:
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Could not write to the file '{stmt.path}'.\n"
                    f"  Details: {e}"
                )


        # GLOBAL SET: modify a global variable that survives across function calls
        elif isinstance(stmt, GlobalSet):
            val = self.eval_expr(stmt.value)
            self.globals[stmt.name] = val
            # Also update local scope so the current function sees it immediately
            self.vars[stmt.name] = val

        # TERMINATE
        elif isinstance(stmt, Terminate):
            self.terminated = True

        # IMPORT
        elif isinstance(stmt, Import):
            self.exec_import(stmt)

