# midshake_runtime.py

from typing import Dict, Any
from python.midshake_ast import (
    Program, Section,
    Let, Set, Proclaim, If, While, Terminate,
    Number, String, Variable, Binary, Inquire,
    Response, FunctionDef, Call, Return, 
)


class Runtime:

    def __init__(self) -> None:
        self.vars: Dict[str, Any] = {}
        self.functions: Dict[str, FunctionDef] = {}
        self.terminated: bool = False
        self.return_value = None
        self.in_function = False






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
    # EXPRESSION EVALUATION
    # ------------------------------------------------------------
    def eval_expr(self, expr):
        if isinstance(expr, Number):
            return expr.value

        if isinstance(expr, String):
            return expr.value

        if isinstance(expr, Variable):
            self.require_declared(expr.name)
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
                    self.exec_stmt(s)
            elif stmt.else_body is not None:
                for s in stmt.else_body:
                    self.exec_stmt(s)

        # WHILST
        elif isinstance(stmt, While):
            while self.eval_expr(stmt.expr) and not self.terminated:
                for s in stmt.body:
                    self.exec_stmt(s)

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

            # save environment
            saved_vars = self.vars.copy()
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

            # return the function result to the caller
            return result

        #RETURN
        elif isinstance(stmt, Return):
            self.return_value = self.eval_expr(stmt.expr)
            # signal to stop executing the function body
            self.in_function = True

            
        # FUNCTION DEF
        elif isinstance(stmt, FunctionDef):
            self.functions[stmt.name] = stmt

        elif isinstance(stmt, Call):
            if stmt.name not in self.functions:
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  The function '{stmt.name}' is not defined."
                )

            func = self.functions[stmt.name]

            # argument count check
            if len(stmt.args) != len(func.param_names):
                raise ValueError(
                    f"MidShake Runtime Error:\n"
                    f"  Function '{func.name}' expects {len(func.param_names)} argument(s) "
                    f"but got {len(stmt.args)}."
                )

            # save current environment
            saved_vars = self.vars.copy()

            # bind parameters
            for param_names, arg_expr in zip(func.param_names, stmt.args):
                self.vars[param_names] = self.eval_expr(arg_expr)

            # execute function body
            for s in func.body:
                self.exec_stmt(s)
                if self.terminated:
                    break

            # restore environment
            self.vars = saved_vars



        # TERMINATE
        elif isinstance(stmt, Terminate):
            self.terminated = True

