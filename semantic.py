from nodes import PascalVisitor
from errors import errors


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name, type_, info=None):
        self.symbols[name.lower()] = {'type': type_, 'info': info}

    def lookup(self, name):
        name = name.lower()
        if name in self.symbols:
            return self.symbols[name]
        return self.parent.lookup(name) if self.parent else None


class SemanticAnalyzer(PascalVisitor):
    def __init__(self):
        self.env = SymbolTable()
        self.semantic_errors = []

        for p in ['write', 'writeln', 'read', 'readln', 'inc', 'dec']:
            self.env.define(p, 'void')
        self.env.define('abs', 'integer')

    def report(self, msg, line, col):
        self.semantic_errors.append(f"Семантическая ошибка [{line}:{col}]: {msg}")

    def visitProgNode(self, node):
        self.visit(node.block)
        if self.semantic_errors:
            for err in self.semantic_errors:
                print(err)
            errors.error("Семантический анализ завершился с ошибками.", node.line, node.col)

    def visitBlockNode(self, node):
        for d in node.decls: self.visit(d)
        for s in node.stmts: self.visit(s)

    def visitVarDeclNode(self, node):
        for name in node.names:
            if node.var_type == 'void':
                self.report(f"Переменная '{name}' не может иметь тип void", node.line, node.col)
            self.env.define(name, node.var_type)

    def visitProcDeclNode(self, node):
        self.env.define(node.name, 'void', {'params': node.params, 'num_params': len(node.params)})

        old_env = self.env
        self.env = SymbolTable(parent=old_env)

        for p_name, p_type in node.params:
            self.env.define(p_name, p_type)

        self.visit(node.block)
        self.env = old_env

    def visitAssignNode(self, node):
        t1 = self.visit(node.target)
        t2 = self.visit(node.value)
        if t1 != t2 and t1 is not None and t2 is not None:
            self.report(f"Несовпадение типов: нельзя присвоить '{t2}' переменной типа '{t1}'", node.line, node.col)

    def visitBinOpNode(self, node):
        t1 = self.visit(node.left)
        t2 = self.visit(node.right)

        if node.op in ['+', '-', '*', 'div', 'mod']:
            if t1 == 'boolean' or t2 == 'boolean':
                self.report("Арифметические операции неприменимы к boolean", node.line, node.col)
            return 'integer'

        if node.op == '/':
            if t1 == 'integer' and t2 == 'integer':
                node.op = 'div'
                return 'integer'

        if node.op in ['>', '<', '>=', '<=', '=', '<>']:
            return 'boolean'
        if node.op in ['and', 'or']:
            return 'boolean'

        return t1

    def visitUnaryOpNode(self, node):
        return self.visit(node.expr)

    def visitVarNode(self, node):
        sym = self.env.lookup(node.name)
        if not sym:
            self.report(f"Использование необъявленной переменной '{node.name}'", node.line, node.col)
            return 'unknown'
        return sym['type']

    def visitArrayAccessNode(self, node):
        sym = self.env.lookup(node.name)
        if not sym or not isinstance(sym['type'], dict) or sym['type'].get('kind') != 'array':
            self.report(f"'{node.name}' не является массивом", node.line, node.col)
            return 'unknown'

        index_type = self.visit(node.index)
        if index_type != 'integer':
            self.report(f"Индекс массива должен быть integer, получен '{index_type}'", node.line, node.col)

        return sym['type']['type']

    def visitNumberNode(self, node):
        return 'integer'

    def visitCharNode(self, node):
        return 'char'

    def visitBoolNode(self, node):
        return 'boolean'

    def visitCallNode(self, node):
        name = node.name.lower()
        sym = self.env.lookup(name)

        if not sym:
            self.report(f"Процедура или функция '{node.name}' не объявлена", node.line, node.col)
            return 'unknown'

        if sym['info'] and 'num_params' in sym['info']:
            expected = sym['info']['num_params']
            actual = len(node.args)
            if expected != actual:
                self.report(f"Процедура '{node.name}' ожидает {expected} аргументов, но передано {actual}", node.line,
                            node.col)

        for a in node.args:
            self.visit(a)

        if name == 'abs': return 'integer'
        return sym['type']

    def visitIfNode(self, node):
        cond_type = self.visit(node.cond)
        if cond_type != 'boolean' and cond_type is not None:
            self.report("Условие if должно иметь тип boolean", node.line, node.col)
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visitWhileNode(self, node):
        self.visit(node.cond)
        self.visit(node.body)

    def visitDoWhileNode(self, node):
        self.visit(node.body)
        self.visit(node.cond)

    def visitForNode(self, node):
        self.visit(node.start)
        self.visit(node.end)
        self.visit(node.body)