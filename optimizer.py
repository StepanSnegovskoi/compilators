from nodes import PascalVisitor, NumberNode


class Optimizer(PascalVisitor):
    def visitProgNode(self, node):
        node.block = self.visit(node.block)
        return node

    def visitBlockNode(self, node):
        node.decls = [self.visit(d) for d in node.decls]
        node.stmts = [self.visit(s) for s in node.stmts]
        return node

    def visitAssignNode(self, node):
        node.target = self.visit(node.target)
        node.value = self.visit(node.value)
        return node

    def visitBinOpNode(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        if isinstance(node.left, NumberNode) and isinstance(node.right, NumberNode):
            v1, v2 = node.left.value, node.right.value
            if node.op == '+': return NumberNode(v1 + v2, node.line, node.col)
            if node.op == '-': return NumberNode(v1 - v2, node.line, node.col)
            if node.op == '*': return NumberNode(v1 * v2, node.line, node.col)
            if node.op == 'div' and v2 != 0: return NumberNode(v1 // v2, node.line, node.col)
        return node

    def visitIfNode(self, node):
        node.cond = self.visit(node.cond)
        node.then_branch = self.visit(node.then_branch)
        if node.else_branch: node.else_branch = self.visit(node.else_branch)
        return node

    def visitForNode(self, node):
        node.start = self.visit(node.start)
        node.end = self.visit(node.end)
        node.body = self.visit(node.body)
        return node

    def visitWhileNode(self, node):
        node.cond = self.visit(node.cond)
        node.body = self.visit(node.body)
        return node

    def visitDoWhileNode(self, node):
        node.body = self.visit(node.body)
        node.cond = self.visit(node.cond)
        return node

    def visitCallNode(self, node):
        node.args = [self.visit(a) for a in node.args]
        return node

    def visitUnaryOpNode(self, node):
        node.expr = self.visit(node.expr)
        return node

    def visitArrayAccessNode(self, node):
        node.index = self.visit(node.index)
        return node