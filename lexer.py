from errors import errors
from token import *


class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        tokens = []
        keywords = {
            "program", "var", "integer", "boolean", "char", "array", "of",
            "procedure", "function", "begin", "end", "if", "then", "else",
            "while", "do", "for", "to", "not", "div", "mod", "true", "false",
            "read", "readln", "write", "writeln", "inc", "dec", "abs"
        }

        while self.pos < len(self.code):
            char = self.code[self.pos]

            if char in " \t\r":
                self.pos += 1
                self.column += 1
                continue

            if char == "\n":
                self.pos += 1
                self.line += 1
                self.column = 1
                continue

            if char == "{":
                while self.pos < len(self.code) and self.code[self.pos] != "}":
                    if self.code[self.pos] == "\n":
                        self.line += 1
                        self.column = 0
                    self.pos += 1
                    self.column += 1
                self.pos += 1
                self.column += 1
                continue

            if char.isdigit():
                start = self.pos
                while self.pos < len(self.code) and self.code[self.pos].isdigit():
                    self.pos += 1
                value = int(self.code[start:self.pos])
                tokens.append(Token("NUMBER", value, self.line, self.column))
                self.column += self.pos - start
                continue

            if char == "'":
                self.pos += 1
                start = self.pos
                while self.pos < len(self.code) and self.code[self.pos] != "'":
                    self.pos += 1
                value = self.code[start:self.pos]
                self.pos += 1
                tokens.append(Token("STRING", value, self.line, self.column))
                self.column += len(value) + 2
                continue

            if char.isalpha() or char == "_":
                start = self.pos
                while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == "_"):
                    self.pos += 1
                name = self.code[start:self.pos]
                lower_name = name.lower()

                if lower_name in keywords:
                    tokens.append(Token("KEYWORD", lower_name, self.line, self.column))
                else:
                    tokens.append(Token("NAME", name, self.line, self.column))
                self.column += self.pos - start
                continue

            if char in "+-*/=<>:":
                op = char
                self.pos += 1
                if self.pos < len(self.code) and (op + self.code[self.pos]) in [":=", "<=", ">=", "<>"]:
                    op += self.code[self.pos]
                    self.pos += 1
                tokens.append(Token("OPERATOR", op, self.line, self.column))
                self.column += len(op)
                continue

            if char == ".":
                self.pos += 1
                if self.pos < len(self.code) and self.code[self.pos] == ".":
                    self.pos += 1
                    tokens.append(Token("PUNCT", "..", self.line, self.column))
                    self.column += 2
                else:
                    tokens.append(Token("PUNCT", ".", self.line, self.column))
                    self.column += 1
                continue

            if char in "();,[]":
                tokens.append(Token("PUNCT", char, self.line, self.column))
                self.pos += 1
                self.column += 1
                continue

            errors.error(f"Неизвестный символ '{char}'", self.line, self.column)

        tokens.append(Token("EOF", None, self.line, self.column))
        return tokens