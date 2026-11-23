# midshake_tokenizer.py

import re

from midshake_ast import Number, String, Variable, Binary, Response


class Token:
    def __init__(self, type_, value=None, line_no=None):
        self.type = type_
        self.value = value
        self.line_no = line_no

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line_no})"


class Tokenizer:
    def __init__(self, text: str):
        self.text = text

    # ------------------------------------------------------------
    # MAIN TOKENIZATION
    # ------------------------------------------------------------
    def tokenize(self):
        tokens = []
        for statement, line_no in self.split_statements():
            normalized = statement.strip()
            if not normalized:
                continue

            token = self.tokenize_line(normalized, line_no)
            if token is not None:
                tokens.append(token)

        return tokens

    # ------------------------------------------------------------
    # STATEMENT SPLITTING
    # ------------------------------------------------------------
    def split_statements(self):
        statements = []
        current = []
        line_no = 1
        start_line = 1
        in_string = False
        i = 0

        standalone = {
            "ELSE",
            "END IF",
            "END WHILST",
            "END FUNCTION",
            "END FOR",
            "TERMINATE the program",
            "BREAK",
            "CONTINUE",
        }

        while i < len(self.text):
            c = self.text[i]
            nxt = self.text[i + 1] if i + 1 < len(self.text) else ""

            # toggle string mode (skip escaped quotes)
            if c == '"':
                if not (i > 0 and self.text[i - 1] == '\\'):
                    in_string = not in_string
                current.append(c)
                i += 1
                continue

            # // comments
            if not in_string and c == '/' and nxt == '/':
                while i < len(self.text) and self.text[i] != '\n':
                    i += 1
                continue

            # # comments
            if not in_string and c == '#':
                while i < len(self.text) and self.text[i] != '\n':
                    i += 1
                continue

            # semicolon ends a statement
            if not in_string and c == ';':
                statement = ''.join(current).strip()
                if statement:
                    statements.append((statement, start_line))
                current = []
                start_line = line_no
                i += 1
                continue

            # newline
            if c == '\n':
                line_no += 1
                if not in_string:
                    possible = ''.join(current).strip()

                    # treat caret comment lines as standalone so they don't
                    # get joined with following lines (which can hide
                    # standalone DEFINE function statements)
                    if possible.startswith("^"):
                        statements.append((possible, start_line))
                        current = []
                        start_line = line_no
                        i += 1
                        continue

                    # treat DEFINE function as standalone
                    if possible.startswith("DEFINE function"):
                        statements.append((possible, start_line))
                        current = []
                        start_line = line_no
                        i += 1
                        continue

                    # treat FOR ... DO header like WHILST ... DO header
                    if possible.startswith("FOR the variable") and " DO" in possible:
                        statements.append((possible, start_line))
                        current = []
                        start_line = line_no
                        i += 1
                        continue

                    # Check if the accumulated text starts a new statement type
                    # that should be separated from the previous line
                    stmt_keywords = [
                        "PROCLAIM", "LET the variable", "SET the variable", "GLOBAL SET the variable",
                        "CALL", "IF the value of", "WHILST the value of",
                        "INQUIRE", "RETURN", "DEFINE function",
                        "the string", "the number",
                    ]
                    is_new_stmt = False
                    for kw in stmt_keywords:
                        if possible.startswith(kw):
                            is_new_stmt = True
                            break
                    
                    if possible in standalone or is_new_stmt:
                        # Flush any previously accumulated text (e.g., WHILST ... DO header)
                        prev = ''.join(current).strip()
                        if prev and prev != possible:
                            statements.append((prev, start_line))
                        statements.append((possible, line_no - 1))
                        current = []
                        start_line = line_no
                    else:
                        current.append(' ')
                i += 1
                continue

            current.append(c)
            i += 1

        final_statement = ''.join(current).strip()
        if final_statement:
            statements.append((final_statement, start_line))

        return statements

    # ------------------------------------------------------------
    # UTILITY EXTRACTORS
    # ------------------------------------------------------------
    def extract_between(self, text, start, end, line_no):
        pattern = rf"{re.escape(start)}(.*?){re.escape(end)}"
        match = re.search(pattern, text)
        if not match:
            raise ValueError(
                f"MidShake Syntax Error (line {line_no}):\n"
                f"  I could not find text between '{start}' and '{end}'.\n"
                f"  Offending line:\n    {text}"
            )
        return match.group(1).strip()

    def extract_after(self, text, start, line_no):
        if start not in text:
            raise ValueError(
                f"MidShake Syntax Error (line {line_no}):\n"
                f"  I expected '{start}'.\n"
                f"  Offending line:\n    {text}"
            )
        return text.split(start, 1)[1].strip()

    # ------------------------------------------------------------
    # EXPRESSION PARSING ENTRY
    # ------------------------------------------------------------
    def parse_expression(self, text: str, line_no: int):
        parser = ExpressionParser(text, line_no)
        return parser.parse()

    # ------------------------------------------------------------
    # STATEMENT TOKENIZATION
    # ------------------------------------------------------------
    def tokenize_line(self, line: str, line_no: int):
        # Strip leading/trailing whitespace so indented lines inside functions work
        line = line.strip()

        # caret comments
        if line.startswith("^"):
            return None

        # LET
        if line.startswith("LET the variable"):
            name = self.extract_between(line, "variable", "BE", line_no).strip()
            value_text = self.extract_after(line, "BE", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("LET", (name, expr), line_no)

        # GLOBAL SET — allows functions to modify global variables (enables recursion with shared state)
        if line.startswith("GLOBAL SET the variable"):
            name = self.extract_between(line, "variable", "TO", line_no).strip()
            value_text = self.extract_after(line, "TO", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("GLOBAL_SET", (name, expr), line_no)

        # SET
        if line.startswith("SET the variable"):
            name = self.extract_between(line, "variable", "TO", line_no).strip()
            value_text = self.extract_after(line, "TO", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("SET", (name, expr), line_no)

        # PROCLAIM
        if line.startswith("PROCLAIM"):
            value_text = self.extract_after(line, "PROCLAIM", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("PROCLAIM", expr, line_no)

        # IF — handle any expression prefix, not just "the value of"
        if line.startswith("IF ") and " THEN" in line:
            condition_text = line[len("IF "):line.index(" THEN")].strip()
            expr = self.parse_expression(condition_text, line_no)
            return Token("IF", expr, line_no)

        # ELSE
        if line == "ELSE":
            return Token("ELSE", None, line_no)

        # END IF
        if line.startswith("END IF"):
            return Token("END_IF", None, line_no)

        # WHILST — handle any expression prefix, not just "the value of"
        if line.startswith("WHILST ") and " DO" in line:
            condition_text = line[len("WHILST "):line.index(" DO")].strip()
            expr = self.parse_expression(condition_text, line_no)
            return Token("WHILST", expr, line_no)

        # END WHILST
        if line.startswith("END WHILST"):
            return Token("END_WHILST", None, line_no)

        # RETURN
        if line.startswith("RETURN"):
            value_text = self.extract_after(line, "RETURN", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("RETURN", expr, line_no)

        # TERMINATE
        if line.strip() == "TERMINATE" or line.startswith("TERMINATE the program"):
            return Token("TERMINATE", None, line_no)

        # BREAK
        if line.strip() == "BREAK" or line.strip() == "BREAK;":
            return Token("BREAK", None, line_no)

        # CONTINUE
        if line.strip() == "CONTINUE" or line.strip() == "CONTINUE;":
            return Token("CONTINUE", None, line_no)

        # FOR ... IN ... DO
        if line.startswith("FOR the variable") and "IN" in line and "DO" in line:
            # Extract variable name
            var_part = self.extract_between(line, "FOR the variable", "IN", line_no).strip()
            # Extract list expression
            list_part = line[line.index("IN") + 2:line.index("DO")].strip()
            list_expr = self.parse_expression(list_part, line_no)
            return Token("FOR_IN", (var_part, list_expr), line_no)

        # END FOR
        if line.startswith("END FOR"):
            return Token("END_FOR", None, line_no)

        # SET the key ... IN the map ... TO ...
        if line.startswith("SET the key") and "IN" in line and "TO" in line:
            # SET the key "keyName" IN the map myMap TO the value expr
            key_part = self.extract_between(line, "SET the key", "IN", line_no).strip()
            rest_after_in = line[line.index("IN") + 2:]
            # Find "TO" in the rest
            if "TO" in rest_after_in:
                map_part = rest_after_in[:rest_after_in.index("TO")].strip()
                value_part = rest_after_in[rest_after_in.index("TO") + 2:].strip()
                # Parse map name
                if map_part.startswith("the map"):
                    map_name = map_part[len("the map"):].strip()
                elif map_part.startswith("the value of"):
                    map_name = map_part[len("the value of"):].strip()
                else:
                    map_name = map_part.strip()
                # Parse key
                if key_part.startswith("the value of"):
                    key_expr = self.parse_expression(key_part[len("the value of"):].strip(), line_no)
                else:
                    key_expr = self.parse_expression(key_part, line_no)
                # Parse value
                value_expr = self.parse_expression(value_part, line_no)
                return Token("MAP_SET", (map_name, key_expr, value_expr), line_no)

        # ------------------------------------------------------------
        # FUNCTION DEFINITIONS
        # ------------------------------------------------------------
        if line.startswith("DEFINE function"):
            rest = line[len("DEFINE function"):].strip()
            param_names = []

            if "WITH" in rest:
                name_part, params_part = rest.split("WITH", 1)
                func_name = name_part.strip().rstrip(";")

                params_text = params_part.strip().rstrip(";")
                params_text = (
                    params_text.replace("the variables", "")
                               .replace("the variable", "")
                               .replace("and", ",")
                               .replace("AND", ",")
                               .strip()
                )

                if params_text:
                    raw_params = [p.strip() for p in params_text.split(",") if p.strip()]
                    for p in raw_params:
                        if isinstance(p, list):
                            raise ValueError(
                                f"MidShake Syntax Error (line {line_no}):\n"
                                f"  Parameter name cannot be a list.\n"
                                f"  Offending line:\n    {line}"
                            )
                    param_names = raw_params
            else:
                func_name = rest.strip().rstrip(";")

            return Token("FUNC_DEF", (func_name, param_names), line_no)

        if line.strip() == "END FUNCTION":
            return Token("END_FUNC", None, line_no)

        # ------------------------------------------------------------
        # FUNCTION CALLS
        # ------------------------------------------------------------
        if line.startswith("CALL"):
            rest = line[len("CALL"):].strip()
            args = []

            if "WITH" in rest:
                name_part, args_part = rest.split("WITH", 1)
                func_name = name_part.strip().rstrip(";")
                args_text = args_part.strip().rstrip(";")

                # Split args by comma, but not inside strings
                arg_pieces = []
                current_piece = []
                in_str = False
                for ch in args_text:
                    if ch == '"':
                        in_str = not in_str
                        current_piece.append(ch)
                    elif ch == ',' and not in_str:
                        arg_pieces.append(''.join(current_piece).strip())
                        current_piece = []
                    else:
                        current_piece.append(ch)
                remaining = ''.join(current_piece).strip()
                if remaining:
                    arg_pieces.append(remaining)

                for piece in arg_pieces:
                    if piece:
                        arg_expr = self.parse_expression(piece, line_no)
                        args.append(arg_expr)
            else:
                func_name = rest.strip().rstrip(";")

            return Token("CALL", (func_name, args), line_no)

        # INQUIRE
        if line.startswith("INQUIRE user for"):
            rest = line[len("INQUIRE user for"):].strip()
            if '"' not in rest:
                raise ValueError(
                    f"MidShake Syntax Error (line {line_no}):\n"
                    f"  Expected a quoted question in INQUIRE.\n"
                    f"  Offending line:\n    {line}"
                )
            type_part, question_part = rest.split('"', 1)
            expected_type = type_part.strip()
            question = question_part.rstrip('"')
            return Token("INQUIRE", (expected_type, question), line_no)


        # IMPORT: IMPORT the file "path/to/file.mish";
        if line.startswith("IMPORT the file"):
            path = self.extract_after(line, "IMPORT the file", line_no).strip()
            path = path.strip('"').strip("'").rstrip(";").strip()
            return Token("IMPORT", path, line_no)

        # FILE WRITE: IN the file "path" WRITE <expression>
        if line.startswith("IN the file"):
            path = self.extract_between(line, "IN the file", "WRITE", line_no).strip()
            path = path.strip('"').strip("'")
            value_text = self.extract_after(line, "WRITE", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("FILE_WRITE", (path, expr), line_no)
        # FILE READ inside LET / SET / PROCLAIM expressions
        # (handled automatically by ExpressionParser)

        raise ValueError(
            f"MidShake Syntax Error (line {line_no}):\n"
            f"  I do not understand this line.\n"
            f"  Offending line:\n    {line}"
        )


# ============================================================
# EXPRESSION PARSER
# ============================================================

class ExpressionParser:
    OPERATORS = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "multiplied": "*",
        "divided": "/",
        "+": "+",
        "-": "-",
        "*": "*",
        "/": "/",
    }

    def __init__(self, text: str, line_no: int):
        self.text = text.strip()
        self.line_no = line_no
        self.pos = 0

    # -----------------------------
    # MAIN ENTRY
    # -----------------------------
    def parse(self):
        expr = self.parse_comparison()
        self.skip_whitespace()
        if not self.is_at_end():
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Unexpected text in expression: '{self.text[self.pos:]}'"
            )
        return expr

    def parse_comparison(self):
        expr = self.parse_term()
        self.skip_whitespace()

        if self.text[self.pos:].startswith("IS"):
            self.pos += len("IS")
            self.skip_whitespace()

            comparators = [
                ("greater than or equal to", ">="),
                ("less than or equal to", "<="),
                ("greater than", ">"),
                ("less than", "<"),
                ("not equal to", "!="),
                ("not equal", "!="),
                ("equal to", "=="),
                ("equal", "=="),
            ]

            for phrase, op in comparators:
                if self.text[self.pos:].startswith(phrase):
                    self.pos += len(phrase)
                    self.skip_whitespace()
                    right = self.parse_term()
                    return Binary(op, expr, right)
            
            
            
            if (
                self.text[self.pos:].startswith("the number")
                or self.text[self.pos:].startswith("the string")
                or self.text[self.pos:].startswith("the value of")
                or self.current_char().isdigit()
                or self.current_char() == '"'
            ):
                right = self.parse_term()
                return Binary("==", expr, right)

            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected comparison after 'IS'."
            )

        return expr

    # -----------------------------
    # HELPERS
    # -----------------------------
    def is_at_end(self):
        return self.pos >= len(self.text)

    def current_char(self):
        return self.text[self.pos] if not self.is_at_end() else ""

    def skip_whitespace(self):
        while not self.is_at_end() and self.current_char().isspace():
            self.pos += 1

    @property
    def current_token(self):
        self.skip_whitespace()
        if self.is_at_end():
            return ""

        if self.current_char() == '"':
            end = self.text.find('"', self.pos + 1)
            if end == -1:
                return self.text[self.pos:]
            return self.text[self.pos:end + 1]

        start = self.pos
        idx = self.pos
        while idx < len(self.text) and self.text[idx] not in "+-*/()[]{},:":
            idx += 1
        return self.text[start:idx].strip()

    # -----------------------------
    # GRAMMAR
    # -----------------------------
    def parse_term(self):
        expr = self.parse_factor()
        while True:
            self.skip_whitespace()
            if self.match_operator(["+", "-", "plus", "minus"]):
                op = self.last_operator
            else:
                break
            right = self.parse_factor()
            expr = Binary(op, expr, right)
        return expr

    def parse_factor(self):
        expr = self.parse_primary()
        while True:
            self.skip_whitespace()
            if self.match_operator(["*", "/", "times", "multiplied", "divided"]):
                op = self.last_operator
            else:
                break
            right = self.parse_primary()
            expr = Binary(op, expr, right)
        return expr

    def match_operator(self, candidates):
        self.skip_whitespace()
        for candidate in sorted(candidates, key=len, reverse=True):
            if self.text[self.pos:].startswith(candidate):
                end = self.pos + len(candidate)
                if candidate.isalpha() and end < len(self.text) and self.text[end].isalpha():
                    continue
                self.pos = end
                self.last_operator = self.OPERATORS[candidate]
                return True
        return False

    # -----------------------------
    # PRIMARY EXPRESSIONS
    # -----------------------------
    def parse_primary(self):
        self.skip_whitespace()

        if self.is_at_end():
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected an expression but found nothing."
            )

        if self.current_char() == '(':
            self.pos += 1
            expr = self.parse_term()
            self.skip_whitespace()
            if self.current_char() != ')':
                raise ValueError(
                    f"MidShake Syntax Error (line {self.line_no}):\n"
                    f"  Expected ')'"
                )
            self.pos += 1
            return expr

        if self.current_char() == '+':
            self.pos += 1
            return self.parse_primary()

        # List literal: [1, 2, 3]
        if self.current_char() == '[':
            return self.parse_list_literal()

        # Map literal: {key: value, key: value}
        if self.current_char() == '{':
            return self.parse_map_literal()

        token = self.current_token

        if token == "RESPONSE":
            self.pos += len("RESPONSE")
            return Response()

        if self.text[self.pos:].startswith("the RESPONSE"):
            self.pos += len("the RESPONSE")
            return Response()

        if self.text[self.pos:].startswith("the answer"):
            self.pos += len("the answer")
            return Response()


        # FILE READ: the content of the file "path" or the content of the file the value of VAR
        if self.text[self.pos:].startswith("the content of the file"):
            self.pos += len("the content of the file")
            self.skip_whitespace()
            from midshake_ast import FileReadExpression
            if self.text[self.pos:].startswith("the value of"):
                var_expr = self.parse_variable_phrase()
                # For variable paths, we need a runtime-evaluated path
                # We'll store the variable and evaluate at runtime
                return FileReadExpression(var_expr)
            elif not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
                return FileReadExpression(string_expr.value)
            else:
                raise SyntaxError(
                    f"MidShake Syntax Error (line {self.line_no}):\n"
                    f"  Expected a quoted file path or 'the value of' variable."
                )

        # String functions
        if self.text[self.pos:].startswith("the length of"):
            self.pos += len("the length of")
            self.skip_whitespace()
            if self.text[self.pos:].startswith("the value of"):
                string_expr = self.parse_variable_phrase()
            elif not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
            else:
                string_expr = self.parse_variable_name()
            from midshake_ast import StringLength
            return StringLength(string_expr)

        if self.text[self.pos:].startswith("the substring of"):
            self.pos += len("the substring of")
            self.skip_whitespace()
            if self.text[self.pos:].startswith("the value of"):
                string_expr = self.parse_variable_phrase()
            elif not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
            else:
                string_expr = self.parse_variable_name()
            self.skip_whitespace()
            # Expect "starting at"
            if self.text[self.pos:].startswith("starting at"):
                self.pos += len("starting at")
                self.skip_whitespace()
                if self.text[self.pos:].startswith("the value of"):
                    start_expr = self.parse_variable_phrase()
                elif self.text[self.pos:].startswith("the number"):
                    start_expr = self.parse_number_phrase()
                else:
                    start_expr = self.parse_number_literal()
                self.skip_whitespace()
                # Expect "ending at"
                if self.text[self.pos:].startswith("ending at"):
                    self.pos += len("ending at")
                    self.skip_whitespace()
                    if self.text[self.pos:].startswith("the value of"):
                        end_expr = self.parse_variable_phrase()
                    elif self.text[self.pos:].startswith("the number"):
                        end_expr = self.parse_number_phrase()
                    else:
                        end_expr = self.parse_number_literal()
                    from midshake_ast import Substring
                    return Substring(string_expr, start_expr, end_expr)
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'starting at' after 'the substring of'."
            )

        if self.text[self.pos:].startswith("the character at"):
            self.pos += len("the character at")
            self.skip_whitespace()
            # Parse the index — could be "the number N", "the value of VAR", or just a number
            if self.text[self.pos:].startswith("the number"):
                index_expr = self.parse_number_phrase()
            elif self.text[self.pos:].startswith("the value of"):
                index_expr = self.parse_variable_phrase()
            else:
                index_expr = self.parse_number_literal()
            self.skip_whitespace()
            # Expect "in"
            if self.text[self.pos:].startswith("in"):
                self.pos += len("in")
                self.skip_whitespace()
                if self.text[self.pos:].startswith("the value of"):
                    string_expr = self.parse_variable_phrase()
                elif not self.is_at_end() and self.current_char() == '"':
                    string_expr = self.parse_string_literal()
                else:
                    string_expr = self.parse_variable_name()
                from midshake_ast import CharAt
                return CharAt(string_expr, index_expr)
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'in' after 'the character at'."
            )

        if self.text[self.pos:].startswith("the split of"):
            self.pos += len("the split of")
            self.skip_whitespace()
            if not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
            elif self.text[self.pos:].startswith("the value of"):
                string_expr = self.parse_variable_phrase()
            else:
                string_expr = self.parse_variable_name()
            self.skip_whitespace()
            # Expect "by"
            if self.text[self.pos:].startswith("by"):
                self.pos += len("by")
                self.skip_whitespace()
                if self.text[self.pos:].startswith("the value of"):
                    delimiter_expr = self.parse_variable_phrase()
                elif not self.is_at_end() and self.current_char() == '"':
                    delimiter_expr = self.parse_string_literal()
                else:
                    delimiter_expr = self.parse_variable_name()
                from midshake_ast import StringSplit
                return StringSplit(string_expr, delimiter_expr)
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'by' after 'the split of'."
            )

        if self.text[self.pos:].startswith("the trimmed"):
            self.pos += len("the trimmed")
            self.skip_whitespace()
            if not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
            elif self.text[self.pos:].startswith("the value of"):
                string_expr = self.parse_variable_phrase()
            else:
                string_expr = self.parse_variable_name()
            from midshake_ast import StringTrim
            return StringTrim(string_expr)

        if self.text[self.pos:].startswith("the join of"):
            self.pos += len("the join of")
            self.skip_whitespace()
            if self.text[self.pos:].startswith("the value of"):
                list_expr = self.parse_variable_phrase()
            else:
                list_expr = self.parse_variable_name()
            self.skip_whitespace()
            # Expect "with"
            if self.text[self.pos:].startswith("with"):
                self.pos += len("with")
                self.skip_whitespace()
                if self.text[self.pos:].startswith("the value of"):
                    delimiter_expr = self.parse_variable_phrase()
                elif not self.is_at_end() and self.current_char() == '"':
                    delimiter_expr = self.parse_string_literal()
                else:
                    delimiter_expr = self.parse_variable_name()
                from midshake_ast import StringJoin
                return StringJoin(list_expr, delimiter_expr)
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'with' after 'the join of'."
            )

        if self.text[self.pos:].startswith("the replace of"):
            self.pos += len("the replace of")
            self.skip_whitespace()
            # Parse: the replace of STRING with OLD to NEW
            if self.text[self.pos:].startswith("the value of"):
                string_expr = self.parse_variable_phrase()
            elif not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
            else:
                string_expr = self.parse_variable_name()
            self.skip_whitespace()
            if self.text[self.pos:].startswith("with"):
                self.pos += len("with")
                self.skip_whitespace()
                if self.text[self.pos:].startswith("the value of"):
                    old_expr = self.parse_variable_phrase()
                elif not self.is_at_end() and self.current_char() == '"':
                    old_expr = self.parse_string_literal()
                else:
                    old_expr = self.parse_variable_name()
                self.skip_whitespace()
                if self.text[self.pos:].startswith("to"):
                    self.pos += len("to")
                    self.skip_whitespace()
                    if self.text[self.pos:].startswith("the value of"):
                        new_expr = self.parse_variable_phrase()
                    elif not self.is_at_end() and self.current_char() == '"':
                        new_expr = self.parse_string_literal()
                    else:
                        new_expr = self.parse_variable_name()
                    from midshake_ast import StringReplace
                    return StringReplace(string_expr, old_expr, new_expr)
                raise ValueError(
                    f"MidShake Syntax Error (line {self.line_no}):\n"
                    f"  Expected 'to' after 'the replace of ... with ...'."
                )
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'with' after 'the replace of'."
            )

        # Math functions — check against self.text[self.pos:] because current_token
        # stops at spaces, so "the minimum of" would be split into just "the".
        if self.text[self.pos:].startswith("the minimum of"):
            self.pos += len("the minimum of")
            self.skip_whitespace()
            left = self.parse_primary()
            self.skip_whitespace()
            if self.text[self.pos:].startswith("and"):
                self.pos += len("and")
                self.skip_whitespace()
                right = self.parse_primary()
                from midshake_ast import MathMin
                return MathMin(left, right)
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'and' after 'the minimum of'."
            )

        if self.text[self.pos:].startswith("the maximum of"):
            self.pos += len("the maximum of")
            self.skip_whitespace()
            left = self.parse_primary()
            self.skip_whitespace()
            if self.text[self.pos:].startswith("and"):
                self.pos += len("and")
                self.skip_whitespace()
                right = self.parse_primary()
                from midshake_ast import MathMax
                return MathMax(left, right)
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'and' after 'the maximum of'."
            )

        if self.text[self.pos:].startswith("the absolute value of"):
            self.pos += len("the absolute value of")
            self.skip_whitespace()
            expr = self.parse_primary()
            from midshake_ast import MathAbs
            return MathAbs(expr)

        if self.text[self.pos:].startswith("the rounded value of"):
            self.pos += len("the rounded value of")
            self.skip_whitespace()
            expr = self.parse_primary()
            from midshake_ast import MathRound
            return MathRound(expr)

        # String utility functions
        if self.text[self.pos:].startswith("the uppercase of"):
            self.pos += len("the uppercase of")
            self.skip_whitespace()
            if not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
            elif self.text[self.pos:].startswith("the value of"):
                string_expr = self.parse_variable_phrase()
            else:
                string_expr = self.parse_variable_name()
            from midshake_ast import StringToUpper
            return StringToUpper(string_expr)

        if self.text[self.pos:].startswith("the lowercase of"):
            self.pos += len("the lowercase of")
            self.skip_whitespace()
            if not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
            elif self.text[self.pos:].startswith("the value of"):
                string_expr = self.parse_variable_phrase()
            else:
                string_expr = self.parse_variable_name()
            from midshake_ast import StringToLower
            return StringToLower(string_expr)

        if self.text[self.pos:].startswith("the check if"):
            saved_pos = self.pos
            self.pos += len("the check if")
            self.skip_whitespace()
            # Parse the string expression (variable, "the value of X", or literal)
            if not self.is_at_end() and self.current_char() == '"':
                string_expr = self.parse_string_literal()
            elif self.text[self.pos:].startswith("the value of"):
                string_expr = self.parse_variable_phrase()
            else:
                string_expr = self.parse_variable_name()
            self.skip_whitespace()
            # Check for "starts with"
            if self.text[self.pos:].startswith("starts with"):
                self.pos += len("starts with")
                self.skip_whitespace()
                if not self.is_at_end() and self.current_char() == '"':
                    prefix_expr = self.parse_string_literal()
                elif self.text[self.pos:].startswith("the value of"):
                    prefix_expr = self.parse_variable_phrase()
                else:
                    prefix_expr = self.parse_variable_name()
                from midshake_ast import StringStartsWith
                return StringStartsWith(string_expr, prefix_expr)
            # Check for "ends with"
            if self.text[self.pos:].startswith("ends with"):
                self.pos += len("ends with")
                self.skip_whitespace()
                if not self.is_at_end() and self.current_char() == '"':
                    suffix_expr = self.parse_string_literal()
                elif self.text[self.pos:].startswith("the value of"):
                    suffix_expr = self.parse_variable_phrase()
                else:
                    suffix_expr = self.parse_variable_name()
                from midshake_ast import StringEndsWith
                return StringEndsWith(string_expr, suffix_expr)
            # Check for "is a digit"
            if self.text[self.pos:].startswith("is a digit"):
                self.pos += len("is a digit")
                from midshake_ast import StringIsDigit
                return StringIsDigit(string_expr)
            # Check for "is a letter"
            if self.text[self.pos:].startswith("is a letter"):
                self.pos += len("is a letter")
                from midshake_ast import StringIsLetter
                return StringIsLetter(string_expr)
            # Check for "is whitespace"
            if self.text[self.pos:].startswith("is whitespace"):
                self.pos += len("is whitespace")
                from midshake_ast import StringIsWhitespace
                return StringIsWhitespace(string_expr)
            # Restore and continue parsing
            self.pos = saved_pos
            return self.parse_variable_phrase()

        # List functions
        if self.text[self.pos:].startswith("the size of"):
            self.pos += len("the size of")
            self.skip_whitespace()
            if self.text[self.pos:].startswith("the value of"):
                list_expr = self.parse_variable_phrase()
            else:
                list_expr = self.parse_variable_name()
            from midshake_ast import ListLength
            return ListLength(list_expr)

        if self.text[self.pos:].startswith("the append of"):
            self.pos += len("the append of")
            self.skip_whitespace()
            # Parse the element - could be a number, string, or variable
            if not self.is_at_end() and self.current_char().isdigit():
                element_expr = self.parse_number_literal()
            elif not self.is_at_end() and self.current_char() == '"':
                element_expr = self.parse_string_literal()
            else:
                element_expr = self.parse_primary()
            self.skip_whitespace()
            # Expect "to"
            if self.text[self.pos:].startswith("to"):
                self.pos += len("to")
                self.skip_whitespace()
                if self.text[self.pos:].startswith("the value of"):
                    list_expr = self.parse_variable_phrase()
                else:
                    list_expr = self.parse_variable_name()
                from midshake_ast import ListAppend
                return ListAppend(element_expr, list_expr)
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'to' after 'the append of'."
            )

        if self.text[self.pos:].startswith("the item at"):
            self.pos += len("the item at")
            self.skip_whitespace()
            # Expect "position" — handle "the item at position" and "the item at"
            if self.text[self.pos:].startswith("position"):
                self.pos += len("position")
                self.skip_whitespace()
            # Parse the index - could be a number literal, "the number N", or "the value of VAR"
            if self.text[self.pos:].startswith("the value of"):
                index_expr = self.parse_variable_phrase()
            elif self.text[self.pos:].startswith("the number"):
                index_expr = self.parse_number_phrase()
            else:
                index_expr = self.parse_number_literal()
            self.skip_whitespace()
            # Expect "in"
            if self.text[self.pos:].startswith("in"):
                self.pos += len("in")
                self.skip_whitespace()
                if self.text[self.pos:].startswith("the value of"):
                    list_expr = self.parse_variable_phrase()
                else:
                    list_expr = self.parse_variable_name()
                from midshake_ast import ListGet
                return ListGet(list_expr, index_expr)
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected 'in' after index in 'the item at'."
            )

        # Map functions: the value of KEY in MAP
        if self.text[self.pos:].startswith("the value of"):
            saved_pos = self.pos
            self.pos += len("the value of")
            self.skip_whitespace()
            # Try to parse a key (variable or string)
            if not self.is_at_end() and self.current_char() == '"':
                key_expr = self.parse_string_literal()
                self.skip_whitespace()
                if self.text[self.pos:].startswith("in"):
                    self.pos += len("in")
                    self.skip_whitespace()
                    map_expr = self.parse_variable_name()
                    from midshake_ast import MapGet
                    return MapGet(map_expr, key_expr)
            else:
                key_expr = self.parse_variable_name()
                self.skip_whitespace()
                if self.text[self.pos:].startswith("in"):
                    self.pos += len("in")
                    self.skip_whitespace()
                    map_expr = self.parse_variable_name()
                    from midshake_ast import MapGet
                    return MapGet(map_expr, key_expr)
            # Not a map access, restore and parse as variable phrase
            self.pos = saved_pos
            return self.parse_variable_phrase()

        if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            return self.parse_number_literal()

        if token.startswith('"') and token.endswith('"'):
            return self.parse_string_literal()

        if self.text[self.pos:].startswith("the number"):
            return self.parse_number_phrase()

        if self.text[self.pos:].startswith("the string"):
            self.pos += len("the string")
            self.skip_whitespace()
            # Check if what follows is a string literal or a variable name
            if not self.is_at_end() and self.current_char() == '"':
                return self.parse_string_literal()
            else:
                # It's a variable name like "the string name"
                return self.parse_variable_name()

        if self.text[self.pos:].startswith("the list"):
            self.pos += len("the list")
            self.skip_whitespace()
            return self.parse_variable_name()

        if self.text[self.pos:].startswith("the map"):
            self.pos += len("the map")
            self.skip_whitespace()
            return self.parse_variable_name()

        # Boolean literals: true / false
        if token.lower() == "true":
            self.pos += len(token)
            from midshake_ast import Boolean
            return Boolean(True)

        if token.lower() == "false":
            self.pos += len(token)
            from midshake_ast import Boolean
            return Boolean(False)

        if token.replace(" ", "").isalpha():
            self.pos += len(token)
            return Variable(token)

        raise SyntaxError(
            f"MidShake Syntax Error (line {self.line_no}): Unexpected token '{token}'"
        )

    def parse_list_literal(self):
        """Parse [elem1, elem2, ...]"""
        self.pos += 1  # skip '['
        from midshake_ast import ListLiteral
        elements = []
        self.skip_whitespace()
        while not self.is_at_end() and self.current_char() != ']':
            elem = self.parse_term()
            elements.append(elem)
            self.skip_whitespace()
            if self.current_char() == ',':
                self.pos += 1
                self.skip_whitespace()
        if self.is_at_end():
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected ']'"
            )
        self.pos += 1  # skip ']'
        return ListLiteral(elements)

    def parse_map_literal(self):
        """Parse {key: value, key: value, ...}"""
        self.pos += 1  # skip '{'
        from midshake_ast import MapLiteral
        keys = []
        values = []
        self.skip_whitespace()
        while not self.is_at_end() and self.current_char() != '}':
            # Parse key (bare identifier or string)
            self.skip_whitespace()
            if self.current_char() == '"':
                key = self.parse_string_literal()
            else:
                # Bare identifier as key
                start = self.pos
                while not self.is_at_end() and self.current_char() not in ":,} ":
                    self.pos += 1
                key_name = self.text[start:self.pos].strip()
                from midshake_ast import Variable
                key = Variable(key_name)
            self.skip_whitespace()
            # Expect ':'
            if self.current_char() != ':':
                raise ValueError(
                    f"MidShake Syntax Error (line {self.line_no}):\n"
                    f"  Expected ':' in map literal."
                )
            self.pos += 1
            self.skip_whitespace()
            # Parse value
            value = self.parse_term()
            keys.append(key)
            values.append(value)
            self.skip_whitespace()
            if self.current_char() == ',':
                self.pos += 1
                self.skip_whitespace()
        if self.is_at_end():
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected '}}'"
            )
        self.pos += 1  # skip '}'
        return MapLiteral(keys, values)

    # -----------------------------
    # NUMBER / VARIABLE / STRING
    # -----------------------------
    def parse_number_phrase(self):
        self.pos += len("the number")
        self.skip_whitespace()
        # Check if what follows is a number literal or a variable name
        if not self.is_at_end() and self.current_char().isdigit():
            return self.parse_number_literal()
        elif not self.is_at_end() and self.current_char() == '-':
            return self.parse_number_literal()
        else:
            # It's a variable name like "the number first"
            return self.parse_variable_name()

    def parse_variable_name(self):
        self.skip_whitespace()
        start = self.pos
        while not self.is_at_end() and self.current_char() not in "+-*/()[]{},: ":
            # Stop at common expression keywords that follow variable names
            remaining = self.text[self.pos:]
            if remaining.startswith(" plus") or remaining.startswith(" minus") or \
               remaining.startswith(" times") or remaining.startswith(" multiplied") or \
               remaining.startswith(" divided") or remaining.startswith(" IS") or \
               remaining.startswith(" and") or remaining.startswith(" AND") or \
               remaining.startswith(" in ") or remaining.startswith(" to ") or \
               remaining.startswith(" by ") or remaining.startswith(" with ") or \
               remaining.startswith(" starting at") or remaining.startswith(" ending at"):
                break
            self.pos += 1
        name = self.text[start:self.pos].strip()
        if not name:
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected a variable name."
            )
        return Variable(name)

    def parse_variable_phrase(self):
        if self.text[self.pos:].startswith("the value of"):
            self.pos += len("the value of")
        self.skip_whitespace()
        start = self.pos
        stop_phrases = [
            " plus", " minus", " times", " multiplied", " divided",
            " IS", " IS ", "IS ", "IS",
            " and", " AND",
            " starts with", " ends with",
            " is a digit", " is a letter", " is whitespace",
            " in ", " in\n", " in;", " in",
            " to ", " to\n", " to;", " to",
            " by ", " by\n", " by;", " by",
            " with ", " with\n", " with;", " with",
            " starting at", " ending at",
            " of ", " of\n", " of;", " of",
            " variable ", " variable\n", " variable;", " variable",
        ]
        while not self.is_at_end():
            if self.current_char() in "+-*/()":
                break
            if any(self.text[self.pos:].startswith(w) for w in stop_phrases):
                break
            self.pos += 1
        name = self.text[start:self.pos].strip()
        if not name:
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected a variable name."
            )
        return Variable(name)

    def parse_number_literal(self):
        start = self.pos
        if self.current_char() == '-':
            self.pos += 1
        while not self.is_at_end() and self.current_char().isdigit():
            self.pos += 1
        # Support decimal numbers
        if not self.is_at_end() and self.current_char() == '.':
            self.pos += 1
            while not self.is_at_end() and self.current_char().isdigit():
                self.pos += 1
        text = self.text[start:self.pos]
        if not text or text == '-':
            # Return 0 as a safe default instead of crashing on empty input
            return Number(0)
        if '.' in text:
            return Number(float(text))
        return Number(int(text))

    def parse_string_literal(self):
        token = self.text[self.pos:]
        if not (token.startswith('"') and '"' in token[1:]):
            raise SyntaxError(
                f"MidShake Syntax Error (line {self.line_no}): Expected a quoted string."
            )

        self.pos += 1
        start = self.pos
        while not self.is_at_end() and self.current_char() != '"':
            if self.current_char() == '\\':
                self.pos += 1  # skip the backslash
                if not self.is_at_end():
                    self.pos += 1  # skip the escaped character
            else:
                self.pos += 1
        if self.is_at_end():
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Unterminated string literal."
            )
        raw = self.text[start:self.pos]
        self.pos += 1
        # Process escape sequences
        value = raw.replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\").replace('\\"', '"')
        return String(value)

