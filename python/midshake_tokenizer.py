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
        self.lines = text.splitlines()

    def tokenize(self):
        tokens = []
        for i, line in enumerate(self.lines, start=1):
            normalized = self.normalize_line(line)
            if not normalized:
                continue

            token = self.tokenize_line(normalized, i)
            tokens.append(token)

        return tokens

    def normalize_line(self, line: str) -> str:
        line = re.sub(r"(//|#).*", "", line)
        line = line.strip()
        if line.endswith(";"):
            line = line[:-1].rstrip()
        return line

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

    def extract_number(self, text, line_no):
        match = re.search(r"the number (-?\d+)", text)
        if not match:
            raise ValueError(
                f"MidShake Syntax Error (line {line_no}):\n"
                f"  I expected 'the number <integer>'.\n"
                f"  Offending line:\n    {text}"
            )
        return int(match.group(1))

    def parse_expression(self, text: str, line_no: int):
        parser = ExpressionParser(text, line_no)
        expr = parser.parse()
        return expr

    def tokenize_line(self, line: str, line_no: int):
        if line.startswith("LET the variable"):
            name = self.extract_between(line, "variable", "BE", line_no)
            value_text = self.extract_after(line, "BE", line_no)
            expr = self.parse_expression(value_text, line_no)
            return Token("LET", (name, expr), line_no)

        if line.startswith("SET the variable"):
            name = self.extract_between(line, "variable", "TO", line_no)
            value_text = self.extract_after(line, "TO", line_no)
            expr = self.parse_expression(value_text, line_no)
            return Token("SET", (name, expr), line_no)

        if line.startswith("PROCLAIM"):
            value_text = self.extract_after(line, "PROCLAIM", line_no)
            expr = self.parse_expression(value_text, line_no)
            return Token("PROCLAIM", expr, line_no)

        if line.startswith("IF the value of"):
            name = self.extract_between(line, "of", "IS", line_no)
            value_text = self.extract_between(line, "IS", "THEN", line_no)
            expr = self.parse_expression(value_text, line_no)
            return Token("IF", (name, expr), line_no)

        if line == "ELSE":
            return Token("ELSE", None, line_no)

        if line.startswith("END IF"):
            return Token("END_IF", None, line_no)

        if line.startswith("WHILST the value of"):
            name = self.extract_between(line, "of", "IS", line_no)
            value_text = self.extract_between(line, "IS", "DO", line_no)
            expr = self.parse_expression(value_text, line_no)
            return Token("WHILST", (name, expr), line_no)

        if line.startswith("END WHILST"):
            return Token("END_WHILST", None, line_no)

        if "TERMINATE the program" in line:
            return Token("TERMINATE", None, line_no)

        if line.startswith("DECLARE a function"):
            name = self.extract_between(line, "named", "that", line_no)
            return Token("DECLARE_FUNCTION", name, line_no)

        raise ValueError(
            f"MidShake Syntax Error (line {line_no}):\n"
            f"  I do not understand this line.\n"
            f"  Offending line:\n    {line}"
        )


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

    def parse(self):
        expr = self.parse_term()
        self.skip_whitespace()
        if not self.is_at_end():
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Unexpected text in expression: '{self.text[self.pos:]}'."
            )
        return expr

    def is_at_end(self):
        return self.pos >= len(self.text)

    def current_char(self):
        return self.text[self.pos] if not self.is_at_end() else ""

    def skip_whitespace(self):
        while not self.is_at_end() and self.current_char().isspace():
            self.pos += 1

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
            if self.text[self.pos :].startswith(candidate):
                end = self.pos + len(candidate)
                if candidate.isalpha() and end < len(self.text) and self.text[end].isalpha():
                    continue
                self.pos = end
                self.last_operator = self.OPERATORS[candidate]
                return True
        return False

    def parse_primary(self):
        self.skip_whitespace()
        if self.is_at_end():
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected an expression but found nothing."
            )

        if self.current_char() == '"':
            return self.parse_string_literal()

        if self.current_char() == '(':
            self.pos += 1
            expr = self.parse_term()
            self.skip_whitespace()
            if self.current_char() != ')':
                raise ValueError(
                    f"MidShake Syntax Error (line {self.line_no}):\n"
                    f"  Expected ')' in expression."
                )
            self.pos += 1
            return expr

        if self.text[self.pos :].startswith("the number"):
            return self.parse_number_phrase()

        if self.text[self.pos :].startswith("the value of"):
            return self.parse_variable_phrase()

        if self.text[self.pos :].startswith("the string"):
            self.pos += len("the string")
            return self.parse_string_literal()

        if self.current_char().isdigit() or self.current_char() == '-':
            return self.parse_number_literal()

        return self.parse_variable_phrase()

    def parse_number_phrase(self):
        self.pos += len("the number")
        self.skip_whitespace()
        return self.parse_number_literal()

    def parse_variable_phrase(self):
        if self.text[self.pos :].startswith("the value of"):
            self.pos += len("the value of")
        self.skip_whitespace()
        start = self.pos
        while not self.is_at_end():
            if self.current_char() in "+-*/()":
                break
            if self.text[self.pos :].startswith(" plus") or self.text[self.pos :].startswith(" minus") or self.text[self.pos :].startswith(" times") or self.text[self.pos :].startswith(" multiplied") or self.text[self.pos :].startswith(" divided"):
                break
            self.pos += 1
        name = self.text[start : self.pos].strip()
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
        text = self.text[start : self.pos]
        try:
            return Number(int(text))
        except ValueError:
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Invalid number literal '{text}'."
            )

    def parse_string_literal(self):
        if self.current_char() != '"':
            raise ValueError(
                f"MidShake Syntax Error (line {self.line_no}):\n"
                f"  Expected a quoted string starting with '\"'."
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
        value = self.text[start : self.pos]
        self.pos += 1
        return String(value)
