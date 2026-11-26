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
    ClassDef, MemberAccess, MemberSet, NewInstance, Private, Protected,
    ListLiteral, MapLiteral, ListGet, MapGet, ListAppend, ListLength,
    StringLength, Substring, CharAt, StringSplit, StringTrim, StringJoin, StringReplace,
    MathMin, MathMax, MathAbs, MathRound,
    StringToUpper, StringToLower, StringStartsWith, StringEndsWith,
    StringIsDigit, StringIsLetter, StringIsWhitespace, StringIndexOf,
    Boolean, MapSet, Break, Continue, ForIn, GlobalSet, Public
)


class ObjectInstance:
    def __init__(self, class_name):
        self.class_name = class_name
        self.fields = {}


class Runtime:

    def __init__(self) -> None:
        self.vars: Dict[str, Any] = {}
        self.functions: Dict[str, FunctionDef] = {}
        self.terminated: bool = False
        self.return_value = None
        self.in_function = False
        self.globals: Dict[str, Any] = {}
        self.classes: Dict[str, ClassDef] = {}
        self.current_class = None

        # Track Private symbols imported from other files.
        self.private_vars: set[str] = set()
        self.private_functions: set[str] = set()
        self.private_classes: set[str] = set()






    # ------------------------------------------------------------
    # PROGRAM EXECUTION
    # ------------------------------------------------------------
    def exec_program(self, program: Program) -> None:
        for section in program.sections:
            for stmt in section.body:
                if isinstance(stmt, ClassDef):
                    self.classes[stmt.name] = stmt
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
        if name not in self.vars and name not in self.globals:
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

        candidates = [
            os.path.abspath(path),
            os.path.join(os.getcwd(), path),
            os.path.join(os.getcwd(), "stdlib", os.path.basename(path)),
        ]

        resolved = next((c for c in candidates if os.path.isfile(c)), None)
        if resolved is None:
            raise ValueError(
                f"MidShake Runtime Error:\n"
                f"  Could not find the file '{path}' for IMPORT."
            )

        if not hasattr(self, "_imported_files"):
            self._imported_files = set()

        real_path = os.path.realpath(resolved)
        if real_path in self._imported_files:
            return
        self._imported_files.add(real_path)

        with open(resolved, "r", encoding="utf-8") as f:
            source = f.read()

        program = Parser(Tokenizer(source).tokenize()).parse()

        # Execute the imported file in its own sub-runtime
        module_runtime = Runtime()
        module_runtime._imported_files = self._imported_files
        module_runtime.exec_program(program)

        # Export Public variables; record Private variables for access diagnostics.
        for var_name, val in module_runtime.vars.items():
            if var_name in module_runtime.private_vars:
                self.private_vars.add(var_name)
            else:
                self.vars[var_name] = val

        # Export Public functions; record Private functions.
        for func_name, func_def in module_runtime.functions.items():
            if isinstance(func_def.visibility, Private):
                self.private_functions.add(func_name)
            else:
                # Keep exported functions bound to their defining module.
                func_def._module_runtime = module_runtime
                self.functions[func_name] = func_def

        for class_name, class_def in module_runtime.classes.items():
            if isinstance(class_def.visibility, Private):
                self.private_classes.add(class_name)
            class_def._module_runtime = module_runtime
            self.classes[class_name] = class_def

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
            if expr.name in self.private_vars and expr.name not in self.vars:
                raise ValueError(
                    f"MidShake Access Error:\n"
                    f"  '{expr.name}' is Private in an imported file and cannot be accessed directly."
                )
            self.require_declared(expr.name)
            if expr.name in self.globals:
                return self.globals[expr.name]
            return self.vars.get(expr.name, "")

        if isinstance(expr, MemberAccess):
            target = self.eval_expr(expr.target)
            return self._get_member(target, expr.name, self.current_class)

        if isinstance(expr, NewInstance):
            args = [self.eval_expr(arg) for arg in expr.args]
            return self._new_instance(expr.class_name, args)

        if isinstance(expr, Call):
            return self.exec_stmt(expr)

        if isinstance(expr, Response):
            return self.vars.get("RESPONSE")

        if isinstance(expr, Binary):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)

            if expr.op == "+":
                if isinstance(left, str) and isinstance(right, (int, float)):
                    return left + str(right)
                if isinstance(right, str) and isinstance(left, (int, float)):
                    return str(left) + right
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
            # Map keys: for bare identifiers, use the identifier name as the key directly
            # without requiring it to be declared as a variable
            if isinstance(expr.key_expr, String):
                key = expr.key_expr.value
            elif isinstance(expr.key_expr, Variable):
                # Use the variable name as the map key directly (symbol key)
                # Only try to evaluate as a variable if the key doesn't exist in the map
                key = expr.key_expr.name
                if key not in mapping:
                    # Try evaluating as a variable reference
                    try:
                        evaluated = self.eval_expr(expr.key_expr)
                        if isinstance(evaluated, (int, float)):
                            key = str(evaluated)
                        elif isinstance(evaluated, str):
                            key = evaluated
                        else:
                            key = str(evaluated)
                    except ValueError:
                        pass  # Keep the original key name
            else:
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

        # String replace: the replace of STRING with OLD to NEW
        if isinstance(expr, StringReplace):
            s = self.eval_expr(expr.string_expr)
            old = self.eval_expr(expr.old_expr)
            new = self.eval_expr(expr.new_expr)
            if not isinstance(s, str):
                s = str(s)
            if not isinstance(old, str):
                old = str(old)
            if not isinstance(new, str):
                new = str(new)
            return s.replace(old, new)

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
                s = str(s)
            return 1.0 if (len(s) == 1 and s.isspace()) else 0.0

        # String indexOf: the index of SUBSTR in STRING
        if isinstance(expr, StringIndexOf):
            s = self.eval_expr(expr.string_expr)
            sub = self.eval_expr(expr.substr_expr)
            if not isinstance(s, str):
                s = str(s)
            if not isinstance(sub, str):
                sub = str(sub)
            idx = s.find(sub)
            return float(idx)

        raise ValueError(
            f"MidShake Runtime Error:\n"
            f"  Unknown expression type: {expr}"
        )

    def _class_chain(self, class_name):
        chain = []
        seen = set()
        while class_name:
            if class_name in seen:
                raise ValueError(f"MidShake Class Error: inheritance cycle involving '{class_name}'.")
            seen.add(class_name)
            class_def = self.classes.get(class_name)
            if class_def is None:
                raise ValueError(f"MidShake Class Error: class '{class_name}' is not defined.")
            chain.append(class_def)
            class_name = class_def.base_name
        return chain

    def _is_subclass(self, class_name, base_name):
        if class_name is None:
            return False
        return any(class_def.name == base_name for class_def in self._class_chain(class_name))

    def _find_class_member(self, class_name, name, member_type):
        for class_def in self._class_chain(class_name):
            for member in class_def.members:
                if isinstance(member, member_type) and member.name == name:
                    return class_def, member
        return None, None

    def _check_member_access(self, name, visibility, owner_class, caller_class):
        if isinstance(visibility, Public):
            return
        if isinstance(visibility, Private) and caller_class == owner_class:
            return
        if isinstance(visibility, Protected) and self._is_subclass(caller_class, owner_class):
            return
        access = type(visibility).__name__.lower()
        raise ValueError(
            f"MidShake Access Error: {access.title()} member '{owner_class}.{name}' "
            f"cannot be accessed from outside its permitted scope."
        )

    def _new_instance(self, class_name, args=None):
        args = args or []
        if class_name in self.private_classes:
            raise ValueError(
                f"MidShake Access Error: class '{class_name}' is Private in an imported file."
            )
        chain = self._class_chain(class_name)
        instance = ObjectInstance(class_name)
        for class_def in reversed(chain):
            class_runtime = getattr(class_def, "_module_runtime", self)
            for member in class_def.members:
                if isinstance(member, Let):
                    instance.fields[member.name] = class_runtime.eval_expr(member.value)

        for class_def in reversed(chain):
            _, constructor = self._find_class_member(class_def.name, "constructor", FunctionDef)
            if constructor is not None and constructor.owner_class == class_def.name:
                constructor_args = args if class_def.name == class_name else []
                if len(constructor_args) != len(constructor.param_names):
                    raise ValueError(
                        f"MidShake Runtime Error: constructor for '{class_def.name}' expects "
                        f"{len(constructor.param_names)} argument(s) but got {len(constructor_args)}."
                    )
                module_runtime = getattr(constructor, "_module_runtime", self)
                module_runtime._execute_function(
                    constructor, constructor_args, instance, class_def.name
                )
            elif class_def.name == class_name and args:
                raise ValueError(
                    f"MidShake Runtime Error: class '{class_name}' has no constructor "
                    f"that accepts {len(args)} argument(s)."
                )
        return instance

    def _get_member(self, target, name, caller_class):
        if not isinstance(target, ObjectInstance):
            raise ValueError("MidShake Runtime Error: member access requires a class instance.")
        owner, member = self._find_class_member(target.class_name, name, Let)
        if member is None:
            raise ValueError(f"MidShake Class Error: field '{name}' is not defined on '{target.class_name}'.")
        self._check_member_access(name, member.visibility, owner.name, caller_class)
        return target.fields[name]

    def _set_member(self, target, name, value, caller_class):
        if not isinstance(target, ObjectInstance):
            raise ValueError("MidShake Runtime Error: member assignment requires a class instance.")
        owner, member = self._find_class_member(target.class_name, name, Let)
        if member is None:
            raise ValueError(f"MidShake Class Error: field '{name}' is not defined on '{target.class_name}'.")
        self._check_member_access(name, member.visibility, owner.name, caller_class)
        target.fields[name] = value

    def _call_method(self, target, name, args, caller_class):
        if not isinstance(target, ObjectInstance):
            raise ValueError("MidShake Runtime Error: method call requires a class instance.")
        owner, method = self._find_class_member(target.class_name, name, FunctionDef)
        if method is None:
            raise ValueError(f"MidShake Class Error: method '{name}' is not defined on '{target.class_name}'.")
        self._check_member_access(name, method.visibility, owner.name, caller_class)
        if len(args) != len(method.param_names):
            raise ValueError(
                f"MidShake Runtime Error: method '{name}' expects {len(method.param_names)} argument(s) "
                f"but got {len(args)}."
            )
        module_runtime = getattr(method, "_module_runtime", self)
        return module_runtime._execute_function(method, args, target, method.owner_class)

    # ------------------------------------------------------------
    # STATEMENT EXECUTION
    # ------------------------------------------------------------
    def exec_stmt(self, stmt):

        # LET
        if isinstance(stmt, Let):
            val = self.eval_expr(stmt.value)
            self.vars[stmt.name] = val
            if isinstance(stmt.visibility, Private):
                self.private_vars.add(stmt.name)
            else:
                self.private_vars.discard(stmt.name)


        # SET
        elif isinstance(stmt, Set):
            if stmt.name in self.private_vars and stmt.name not in self.vars:
                raise ValueError(
                    f"MidShake Access Error:\n"
                    f"  '{stmt.name}' is Private in an imported file and cannot be modified directly."
                )
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

        # CLASS MEMBER SET
        elif isinstance(stmt, MemberSet):
            target = self.eval_expr(stmt.target)
            value = self.eval_expr(stmt.value)
            self._set_member(target, stmt.name, value, self.current_class)

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

        # CLASS DEFINITION
        elif isinstance(stmt, ClassDef):
            self.classes[stmt.name] = stmt
            for member in stmt.members:
                if isinstance(member, FunctionDef):
                    member.owner_class = stmt.name
                    member._module_runtime = self

        # CALL
        elif isinstance(stmt, Call):
            if "." in stmt.name:
                target_name, method_name = stmt.name.rsplit(".", 1)
                target_parts = target_name.split(".")
                target_expr = Variable(target_parts[0])
                for part in target_parts[1:]:
                    target_expr = MemberAccess(target_expr, part)
                target = self.eval_expr(target_expr)
                args = [self.eval_expr(arg_expr) for arg_expr in stmt.args]
                result = self._call_method(target, method_name, args, self.current_class)
                self.vars["RESPONSE"] = result
                return result

            if stmt.name in self.private_functions and stmt.name not in self.functions:
                raise ValueError(
                    f"MidShake Access Error:\n"
                    f"  Function '{stmt.name}' is Private in an imported file and cannot be called directly."
                )

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

            arg_values = [self.eval_expr(arg_expr) for arg_expr in stmt.args]
            function_runtime = getattr(func, "_module_runtime", self)
            result = function_runtime._execute_function(func, arg_values)
            self.vars["RESPONSE"] = result
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
            if stmt.name in self.private_vars and stmt.name not in self.vars:
                raise ValueError(
                    f"MidShake Access Error:\n"
                    f"  '{stmt.name}' is Private in an imported file and cannot be modified directly."
                )
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

    def _execute_function(self, func: FunctionDef, arg_values, this_obj=None, owner_class=None):
        global_names = set(self.globals.keys())
        saved_locals = {}
        for name, value in self.vars.items():
            if name in global_names:
                saved_locals[name] = value
            elif isinstance(value, (list, dict)):
                saved_locals[name] = copy.deepcopy(value)
            else:
                saved_locals[name] = value

        saved_return = self.return_value
        saved_flag = self.in_function
        saved_class = self.current_class

        for param_name, arg_value in zip(func.param_names, arg_values):
            self.vars[param_name] = arg_value
        if this_obj is not None:
            self.vars["this"] = this_obj

        self.return_value = None
        self.in_function = False
        self.current_class = owner_class

        for stmt in func.body:
            self.exec_stmt(stmt)
            if self.in_function:
                break

        result = self.return_value
        self.vars = saved_locals
        for global_name, global_value in self.globals.items():
            self.vars[global_name] = global_value
        self.return_value = saved_return
        self.in_function = saved_flag
        self.current_class = saved_class
        self.vars["RESPONSE"] = result
        return result

