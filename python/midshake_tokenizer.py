# midshake_tokenizer.py

import re

from midshake_ast import Number, String, Variable, Binary


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
            "TERMINATE the program",
        }

        while i < len(self.text):
            c = self.text[i]
            nxt = self.text[i + 1] if i + 1 < len(self.text) else ""

            if c == '"':
                in_string = not in_string
                current.append(c)
                i += 1
                continue

            if not in_string and c == '/' and nxt == '/':
                while i < len(self.text) and self.text[i] != '\n':
                    i += 1
                continue

            if not in_string and c == '#':
                while i < len(self.text) and self.text[i] != '\n':
                    i += 1
                continue

            if not in_string and c == ';':
                statement = ''.join(current).strip()
                if statement:
                    statements.append((statement, start_line))
                current = []
                start_line = line_no
                i += 1
                continue

            if c == '\n':
                line_no += 1
                if not in_string:
                    possible = ''.join(current).strip()
                    if possible in standalone:
                        statements.append((possible, start_line))
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
        if line.strip().startswith("^"):
            return None  # Treat as comment, no tokens

        if line.startswith("LET the variable"):
            name = self.extract_between(line, "variable", "BE", line_no).strip()
            value_text = self.extract_after(line, "BE", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("LET", (name, expr), line_no)

        if line.startswith("SET the variable"):
            name = self.extract_between(line, "variable", "TO", line_no).strip()
            value_text = self.extract_after(line, "TO", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("SET", (name, expr), line_no)

        if line.startswith("PROCLAIM"):
            value_text = self.extract_after(line, "PROCLAIM", line_no).strip()
            expr = self.parse_expression(value_text, line_no)
            return Token("PROCLAIM", expr, line_no)

        if line.startswith("IF the value of"):
            condition_text = line[len("IF "):line.index("THEN")].strip()
            expr = self.parse_expression(condition_text, line_no)
            return Token("IF", expr, line_no)

        if line == "ELSE":
            return Token("ELSE", None, line_no)

        if line.startswith("END IF"):
            return Token("END_IF", None, line_no)

        if line.startswith("WHILST the value of"):
            condition_text = line[len("WHILST "):line.index("DO")].strip()
            expr = self.parse_expression(condition_text, line_no)
            return Token("WHILST", expr, line_no)

        if line.startswith("END WHILST"):
            return Token("END_WHILST", None, line_no)

        if line.strip() == "TERMINATE" or line.startswith("TERMINATE the program"):
            return Token("TERMINATE", None, line_no)

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

            if self.text[self.pos:].startswith("the number") or self.text[self.pos:].startswith("the string") or self.text[self.pos:].startswith("the value of") or self.current_char().isdigit() or self.current_char() == '"':
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
        while idx < len(self.text) and self.text[idx] not in "+-*/()":
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

        token = self.current_token

        if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            return self.parse_number_literal()

        if token.startswith('"') and token.endswith('"'):
            return self.parse_string_literal()

        if token.startswith("the number"):
            return self.parse_number_phrase()

        if token.startswith("the value of"):
            return self.parse_variable_phrase()

        if token.startswith("the string"):
            self.pos += len("the string")
            self.skip_whitespace()
            token = self.current_token
            if token.startswith('"') and token.endswith('"'):
                return self.parse_string_literal()
            raise SyntaxError(
                f"MidShake Syntax Error (line {self.line_no}): Expected a quoted string after 'the string'"
            )

        if token.replace(" ", "").isalpha():
            return Variable(token)

        raise SyntaxError(
            f"MidShake Syntax Error (line {self.line_no}): Unexpected token '{token}'"
        )

    # -----------------------------
    # NUMBER / VARIABLE / STRING
    # -----------------------------
    def parse_number_phrase(self):
        self.pos += len("the number")
        self.skip_whitespace()
        return self.parse_number_literal()

    def parse_variable_phrase(self):
        if self.text[self.pos:].startswith("the value of"):
            self.pos += len("the value of")
        self.skip_whitespace()
        start = self.pos
        stop_phrases = [
            " plus", " minus", " times", " multiplied", " divided",
            " IS", " IS ", "IS ", "IS"
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
        text = self.text[start:self.pos]
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
            self.pos += 1
        if self.is_at_end():
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Unterminated string literal."
            )
        value = self.text[start:self.pos]
        self.pos += 1
        return String(value)
