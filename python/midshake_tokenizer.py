# midshake_tokenizer.py

import re

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
            stripped = line.strip()
            if not stripped:
                continue

            token = self.tokenize_line(stripped, i)
            tokens.append(token)

        return tokens

    def extract_between(self, text, start, end, line_no):
        pattern = rf"{start}(.*?){end}"
        match = re.search(pattern, text)
        if not match:
            raise ValueError(
                f"MidShake Syntax Error (line {line_no}):\n"
                f"  I could not find text between '{start}' and '{end}'.\n"
                f"  Offending line:\n    {text}"
            )
        return match.group(1).strip()

    def extract_number(self, text, line_no):
        match = re.search(r"number (\d+)", text)
        if not match:
            raise ValueError(
                f"MidShake Syntax Error (line {line_no}):\n"
                f"  I expected 'the number <integer>'.\n"
                f"  Offending line:\n    {text}"
            )
        return int(match.group(1))

    def tokenize_line(self, line: str, line_no: int):
        # Declaration
        if line.startswith("LET the variable"):
            name = self.extract_between(line, "variable", "BE", line_no)
            number = self.extract_number(line, line_no)
            return Token("LET", (name, number), line_no)

        # Assignment
        if line.startswith("SET the variable"):
            name = self.extract_between(line, "variable", "TO", line_no)
            number = self.extract_number(line, line_no)
            return Token("SET", (name, number), line_no)

        # Print
        if line.startswith("PROCLAIM the value of"):
            name = self.extract_between(line, "of", ";", line_no)
            return Token("PROCLAIM", name, line_no)

        # IF
        if line.startswith("IF the value of"):
            name = self.extract_between(line, "of", "IS", line_no)
            number = self.extract_number(line, line_no)
            # require THEN
            if "THEN" not in line:
                raise ValueError(
                    f"MidShake Syntax Error (line {line_no}):\n"
                    f"  I expected 'THEN' after the IF condition.\n"
                    f"  Offending line:\n    {line}"
                )
            return Token("IF", (name, number), line_no)

        # WHILST
        if line.startswith("WHILST the value of"):
            name = self.extract_between(line, "of", "IS", line_no)
            number = self.extract_number(line, line_no)
            # require DO
            if "DO" not in line:
                raise ValueError(
                    f"MidShake Syntax Error (line {line_no}):\n"
                    f"  I expected 'DO' after the WHILST condition.\n"
                    f"  Offending line:\n    {line}"
                )
            return Token("WHILST", (name, number), line_no)

        # END IF
        if line.startswith("END IF"):
            return Token("END_IF", None, line_no)

        # END WHILST
        if line.startswith("END WHILST"):
            return Token("END_WHILST", None, line_no)

        # Termination
        if "TERMINATE the program" in line:
            return Token("TERMINATE", None, line_no)

        raise ValueError(
            f"MidShake Syntax Error (line {line_no}):\n"
            f"  I do not understand this line.\n"
            f"  Offending line:\n    {line}"
        )
