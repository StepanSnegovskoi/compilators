class Node:
    def __init__(self, line=0, col=0):
        self.line = line
        self.col = col

class ProgNode(Node):
    def __init__(self, name, block, line, col):
        super().__init__(line, col)
        self.name = name
        self.block = block


class BlockNode(Node):
    def __init__(self, decls, stmts, line, col):
        super().__init__(line, col)
        self.decls = decls
        self.stmts = stmts


class VarDeclNode(Node):
    def __init__(self, names, var_type, line, col):
        super().__init__(line, col)
        self.names = names
        self.var_type = var_type


class ProcDeclNode(Node):
    def __init__(self, name, params, block, line, col):
        super().__init__(line, col)
        self.name, self.params, self.block = name, params, block


class AssignNode(Node):
    def __init__(self, target, value, line, col):
        super().__init__(line, col)
        self.target, self.value = target, value


class IfNode(Node):
    def __init__(self, cond, then_branch, else_branch, line, col):
        super().__init__(line, col)
        self.cond, self.then_branch, self.else_branch = cond, then_branch, else_branch


class WhileNode(Node):
    def __init__(self, cond, body, line, col):
        super().__init__(line, col)
        self.cond, self.body = cond, body


class DoWhileNode(Node):
    def __init__(self, body, cond, line, col):
        super().__init__(line, col)
        self.body, self.cond = body, cond


class ForNode(Node):
    def __init__(self, var_name, start, end, body, line, col):
        super().__init__(line, col)
        self.var_name, self.start, self.end, self.body = var_name, start, end, body


class CallNode(Node):
    def __init__(self, name, args, line, col):
        super().__init__(line, col)
        self.name, self.args = name, args


class BinOpNode(Node):
    def __init__(self, left, op, right, line, col):
        super().__init__(line, col)
        self.left, self.op, self.right = left, op, right


class UnaryOpNode(Node):
    def __init__(self, op, expr, line, col):
        super().__init__(line, col)
        self.op, self.expr = op, expr


class VarNode(Node):
    def __init__(self, name, line, col):
        super().__init__(line, col)
        self.name = name


class ArrayAccessNode(Node):
    def __init__(self, name, index, line, col):
        super().__init__(line, col)
        self.name, self.index = name, index


class NumberNode(Node):
    def __init__(self, value, line, col):
        super().__init__(line, col)
        self.value = value


class CharNode(Node):
    def __init__(self, value, line, col):
        super().__init__(line, col)
        self.value = value


class BoolNode(Node):
    def __init__(self, value, line, col):
        super().__init__(line, col)
        self.value = value


class EmptyNode(Node): pass


class PascalVisitor:
    def visit(self, node):
        if node is None: return None
        method = getattr(self, f"visit{node.__class__.__name__}", self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        return node