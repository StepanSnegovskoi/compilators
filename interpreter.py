from nodes import PascalVisitor


class Env:
    def __init__(self, parent=None):
        self.b, self.p = {}, parent

    def set(self, n, v):
        n = n.lower()
        if n in self.b:
            self.b[n] = v
        elif self.p:
            self.p.set(n, v)
        else:
            self.b[n] = v

    def get(self, n):
        n = n.lower()
        return self.b.get(n) if n in self.b else (self.p.get(n) if self.p else None)


class Interpreter(PascalVisitor):
    def __init__(self):
        self.env, self.procs = Env(), {}

    def visitProgNode(self, node):
        self.visit(node.block)

    def visitBlockNode(self, node):
        for d in node.decls: self.visit(d)
        for s in node.stmts: self.visit(s)

    def visitVarDeclNode(self, node):
        for n in node.names:
            if isinstance(node.var_type, dict) and node.var_type['kind'] == 'array':
                self.env.b[n.lower()] = {i: 0 for i in
                                         range(node.var_type['bounds'][0], node.var_type['bounds'][1] + 1)}
            else:
                self.env.b[n.lower()] = 0

    def visitProcDeclNode(self, node):
        self.procs[node.name.lower()] = node

    def visitAssignNode(self, node):
        val = self.visit(node.value)
        if node.target.__class__.__name__ == 'ArrayAccessNode':
            self.env.get(node.target.name)[self.visit(node.target.index)] = val
        else:
            self.env.set(node.target.name, val)

    def visitBinOpNode(self, node):
        l, r = self.visit(node.left), self.visit(node.right)
        ops = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y,
               'div': lambda x, y: x // y, 'mod': lambda x, y: x % y, '=': lambda x, y: x == y,
               '<>': lambda x, y: x != y, '>': lambda x, y: x > y, '<': lambda x, y: x < y,
               'and': lambda x, y: x and y, 'or': lambda x, y: x or y}
        return ops[node.op](l, r)

    def visitUnaryOpNode(self, node):
        v = self.visit(node.expr)
        return -v if node.op == '-' else (not v if node.op == 'not' else v)

    def visitVarNode(self, node):
        return self.env.get(node.name)

    def visitArrayAccessNode(self, node):
        return self.env.get(node.name)[self.visit(node.index)]

    def visitNumberNode(self, node):
        return node.value

    def visitCharNode(self, node):
        return node.value

    def visitBoolNode(self, node):
        return node.value

    def visitIfNode(self, node):
        if self.visit(node.cond):
            self.visit(node.then_branch)
        elif node.else_branch:
            self.visit(node.else_branch)

    def visitWhileNode(self, node):
        while self.visit(node.cond): self.visit(node.body)

    def visitDoWhileNode(self, node):
        while True:
            self.visit(node.body)
            if not self.visit(node.cond): break

    def visitForNode(self, node):
        self.env.set(node.var_name, self.visit(node.start))
        while self.env.get(node.var_name) <= self.visit(node.end):
            self.visit(node.body)
            self.env.set(node.var_name, self.env.get(node.var_name) + 1)

    def visitCallNode(self, node):
        name = node.name.lower()

        if name in ['read', 'readln']:
            for arg in node.args:
                val = int(input(f"Ввод -> "))
                if arg.__class__.__name__ == 'VarNode':
                    self.env.set(arg.name, val)
                elif arg.__class__.__name__ == 'ArrayAccessNode':
                    self.env.get(arg.name)[self.visit(arg.index)] = val
            return

        args = [self.visit(a) for a in node.args]

        if name in ['write', 'writeln']:
            print(*(str(a).strip("'") for a in args), end='\n' if name == 'writeln' else ' ')
        elif name in ['inc', 'dec']:
            v_name = node.args[0].name
            self.env.set(v_name, self.env.get(v_name) + (1 if name == 'inc' else -1))
        elif name == 'abs':
            return abs(args[0])
        elif name in self.procs:
            proc = self.procs[name]
            old, self.env = self.env, Env(self.env)
            for (p_name, _), val in zip(proc.params, args):
                self.env.b[p_name.lower()] = val
            self.visit(proc.block)
            self.env = old
