from utils import NodeVisitor


class Environment:
    def __init__(self, parent=None):
        self.bindings = {}
        self.parent = parent

    def define(self, name, val):
        self.bindings[name] = val

    def set(self, name, val):
        if name in self.bindings:
            self.bindings[name] = val
        elif self.parent:
            self.parent.set(name, val)
        else:
            self.bindings[name] = val

    def get(self, name):
        if name in self.bindings: return self.bindings[name]
        if self.parent: return self.parent.get(name)
        return None


class ASTInterpreter(NodeVisitor):
    def __init__(self):
        self.env = Environment()
        self.procedures = {}

    def visit_program(self, node):
        self.visit(node.children[1])

    def visit_proc_decl(self, node):
        name = str(node.children[0])
        params = [str(i) for p in node.children[1].children for i in p.children[0].children]
        block = node.children[2]
        self.procedures[name] = {'params': params, 'block': block}

    def visit_block(self, node):
        self.generic_visit(node)

    def visit_var_declarations(self, node):
        self.generic_visit(node)

    def visit_var_declaration(self, node):
        for ident in node.children[0].children:
            self.env.define(str(ident), 0)

    def visit_compound_statement(self, node):
        self.visit(node.children[0])

    def visit_statement_list(self, node):
        self.generic_visit(node)

    def visit_number(self, node):
        return int(node.children[0])

    def visit_simple_var(self, node):
        return self.env.get(str(node.children[0]))

    def visit_add(self, node):
        return self.visit(node.children[0]) + self.visit(node.children[1])

    def visit_sub(self, node):
        return self.visit(node.children[0]) - self.visit(node.children[1])

    def visit_mul(self, node):
        return self.visit(node.children[0]) * self.visit(node.children[1])

    def visit_div_int(self, node):
        return self.visit(node.children[0]) // self.visit(node.children[1])

    def visit_assign_statement(self, node):
        var_name = str(node.children[0].children[0])
        self.env.set(var_name, self.visit(node.children[1]))

    def visit_call_statement(self, node):
        name = str(node.children[0])
        args = node.children[1].children if len(node.children) > 1 else []

        if name in ['Write', 'WriteLn']:
            print(" ".join(str(self.visit(a)) for a in args), end='\n' if name == 'WriteLn' else '')
        elif name in self.procedures:
            proc = self.procedures[name]
            old_env = self.env
            self.env = Environment(parent=old_env)
            for p_name, arg_node in zip(proc['params'], args):
                self.env.define(p_name, self.visit(arg_node))
            self.visit(proc['block'])
            self.env = old_env

    def visit_expr_list(self, node):
        pass

    def visit_empty_statement(self, node):
        pass