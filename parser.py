from nodes import *
from errors import errors


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]

    def match(self, type_, value=None):
        tok = self.current()
        if tok.type == type_ and (value is None or tok.value == value):
            self.pos += 1
            return tok
        errors.error(f"Ожидался {type_} {value if value else ''}, получено {tok.type} '{tok.value}'", tok.line,
                     tok.column)

    def is_match(self, type_, value=None):
        tok = self.current()
        if tok.type == type_ and (value is None or tok.value == value):
            self.pos += 1
            return True
        return False

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        tok = self.match("KEYWORD", "program")
        name = self.match("NAME").value
        self.match("PUNCT", ";")
        block = self.parse_block()
        self.match("PUNCT", ".")
        return ProgNode(name, block, tok.line, tok.column)

    def parse_block(self):
        tok = self.current()
        decls = []
        while self.current().type == "KEYWORD" and self.current().value in ["var", "procedure", "function"]:
            if self.is_match("KEYWORD", "var"):
                while self.current().type == "NAME":
                    names = [self.match("NAME").value]
                    while self.is_match("PUNCT", ","):
                        names.append(self.match("NAME").value)
                    self.match("OPERATOR", ":")
                    v_type = self.parse_type()
                    self.match("PUNCT", ";")
                    decls.append(VarDeclNode(names, v_type, tok.line, tok.column))
            elif self.current().value in ["procedure", "function"]:
                is_func = self.is_match("KEYWORD", "function")
                if not is_func: self.match("KEYWORD", "procedure")
                name = self.match("NAME").value
                params = []
                if self.is_match("PUNCT", "("):
                    if not self.current().value == ")":
                        while True:
                            p_names = [self.match("NAME").value]
                            while self.is_match("PUNCT", ","): p_names.append(self.match("NAME").value)
                            self.match("OPERATOR", ":")
                            p_type = self.parse_type()
                            for n in p_names: params.append((n, p_type))
                            if not self.is_match("PUNCT", ";"): break
                    self.match("PUNCT", ")")
                if is_func:
                    self.match("OPERATOR", ":")
                    self.parse_type()
                self.match("PUNCT", ";")
                block = self.parse_block()
                self.match("PUNCT", ";")
                decls.append(ProcDeclNode(name, params, block, tok.line, tok.column))

        stmts = self.parse_compound()
        return BlockNode(decls, stmts, tok.line, tok.column)

    def parse_type(self):
        if self.is_match("KEYWORD", "array"):
            self.match("PUNCT", "[")
            left = self.match("NUMBER").value
            self.match("PUNCT", "..")
            right = self.match("NUMBER").value
            self.match("PUNCT", "]")
            self.match("KEYWORD", "of")
            base = self.match("KEYWORD").value
            return {"kind": "array", "type": base, "bounds": (left, right)}
        return self.match("KEYWORD").value

    def parse_compound(self):
        self.match("KEYWORD", "begin")
        stmts = []
        while not self.is_match("KEYWORD", "end"):
            stmts.append(self.parse_statement())
            self.is_match("PUNCT", ";")
        return stmts

    def parse_statement(self):
        tok = self.current()
        if self.current().value == "begin":
            return BlockNode([], self.parse_compound(), tok.line, tok.column)
        if self.is_match("KEYWORD", "if"):
            cond = self.parse_expr()
            self.match("KEYWORD", "then")
            then_b = self.parse_statement()
            else_b = self.parse_statement() if self.is_match("KEYWORD", "else") else None
            return IfNode(cond, then_b, else_b, tok.line, tok.column)
        if self.is_match("KEYWORD", "while"):
            cond = self.parse_expr()
            self.match("KEYWORD", "do")
            body = self.parse_statement()
            return WhileNode(cond, body, tok.line, tok.column)
        if self.is_match("KEYWORD", "do"):
            body = self.parse_statement()
            self.match("KEYWORD", "while")
            cond = self.parse_expr()
            return DoWhileNode(body, cond, tok.line, tok.column)
        if self.is_match("KEYWORD", "for"):
            var_name = self.match("NAME").value
            self.match("OPERATOR", ":=")
            start = self.parse_expr()
            self.match("KEYWORD", "to")
            end = self.parse_expr()
            self.match("KEYWORD", "do")
            body = self.parse_statement()
            return ForNode(var_name, start, end, body, tok.line, tok.column)

        if tok.type == "NAME" or tok.value in ["read", "readln", "write", "writeln", "inc", "dec", "abs"]:
            name = self.current().value
            self.pos += 1
            if self.is_match("OPERATOR", ":="):
                return AssignNode(VarNode(name, tok.line, tok.column), self.parse_expr(), tok.line, tok.column)
            elif self.is_match("PUNCT", "["):
                idx = self.parse_expr()
                self.match("PUNCT", "]")
                self.match("OPERATOR", ":=")
                return AssignNode(ArrayAccessNode(name, idx, tok.line, tok.column), self.parse_expr(), tok.line,
                                  tok.column)
            else:
                args = []
                if self.is_match("PUNCT", "("):
                    if not self.current().value == ")":
                        args.append(self.parse_expr())
                        while self.is_match("PUNCT", ","): args.append(self.parse_expr())
                    self.match("PUNCT", ")")
                return CallNode(name, args, tok.line, tok.column)
        return EmptyNode(tok.line, tok.column)

    def parse_expr(self):
        left = self.parse_and_expr()
        while self.current().value == "or":
            op = self.current().value;
            self.pos += 1
            left = BinOpNode(left, op, self.parse_and_expr(), left.line, left.col)
        return left

    def parse_and_expr(self):
        left = self.parse_rel()
        while self.current().value == "and":
            op = self.current().value;
            self.pos += 1
            left = BinOpNode(left, op, self.parse_rel(), left.line, left.col)
        return left

    def parse_rel(self):
        left = self.parse_add()
        if self.current().value in ["=", "<>", "<", ">", "<=", ">="]:
            op = self.current().value;
            self.pos += 1
            left = BinOpNode(left, op, self.parse_add(), left.line, left.col)
        return left

    def parse_add(self):
        left = self.parse_term()
        while self.current().value in ["+", "-"]:
            op = self.current().value;
            self.pos += 1
            left = BinOpNode(left, op, self.parse_term(), left.line, left.col)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current().value in ["*", "/", "div", "mod"]:
            op = self.current().value;
            self.pos += 1
            left = BinOpNode(left, op, self.parse_factor(), left.line, left.col)
        return left

    def parse_factor(self):
        tok = self.current()
        if self.is_match("OPERATOR", "+") or self.is_match("OPERATOR", "-") or self.is_match("KEYWORD", "not"):
            return UnaryOpNode(tok.value, self.parse_factor(), tok.line, tok.column)
        if self.is_match("NUMBER"): return NumberNode(tok.value, tok.line, tok.column)
        if self.is_match("STRING"): return CharNode(tok.value, tok.line, tok.column)
        if self.is_match("KEYWORD", "true"): return BoolNode(True, tok.line, tok.column)
        if self.is_match("KEYWORD", "false"): return BoolNode(False, tok.line, tok.column)
        if self.is_match("PUNCT", "("):
            node = self.parse_expr()
            self.match("PUNCT", ")")
            return node
        if tok.type == "NAME" or tok.value == "abs":
            name = self.current().value;
            self.pos += 1
            if self.is_match("PUNCT", "["):
                idx = self.parse_expr()
                self.match("PUNCT", "]")
                return ArrayAccessNode(name, idx, tok.line, tok.column)
            if self.is_match("PUNCT", "("):
                args = []
                if not self.current().value == ")":
                    args.append(self.parse_expr())
                    while self.is_match("PUNCT", ","): args.append(self.parse_expr())
                self.match("PUNCT", ")")
                return CallNode(name, args, tok.line, tok.column)
            return VarNode(name, tok.line, tok.column)
        errors.error(f"Неожиданный токен {tok}", tok.line, tok.column)