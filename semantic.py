from utils import NodeVisitor, SemanticError


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def declare(self, name, sym_type, kind='var', info=None):
        if name in self.symbols:
            raise SemanticError(f"Идентификатор '{name}' уже объявлен.")
        self.symbols[name] = {'type': sym_type, 'kind': kind, 'info': info}

    def lookup(self, name):
        if name in self.symbols: return self.symbols[name]
        if self.parent: return self.parent.lookup(name)
        return None


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        for p in ['Write', 'WriteLn', 'Read', 'ReadLn', 'Inc', 'Dec']:
            self.global_scope.declare(p, 'void', 'proc')
        self.global_scope.declare('Abs', 'integer', 'func')

    def visit_program(self, node):
        self.visit(node.children[1])

    def visit_block(self, node):
        for child in node.children:
            self.visit(child)

    def visit_var_declarations(self, node):
        for child in node.children:
            self.visit(child)

    def visit_var_declaration(self, node):
        type_node = node.children[1]

        if type_node.data == 'array_type':
            sym_type = {'kind': 'array', 'type': type_node.children[2].data.replace('type_', '')}
        elif type_node.data == 'type_spec':
            sym_type = type_node.children[0].data.replace('type_', '')
        else:
            sym_type = type_node.data.replace('type_', '')

        for ident in node.children[0].children:
            self.current_scope.declare(str(ident), sym_type, 'var')

    def visit_compound_statement(self, node):
        self.visit(node.children[0])

    def visit_statement_list(self, node):
        for child in node.children:
            self.visit(child)

    def visit_number(self, node):
        return 'integer'

    def visit_true_const(self, node):
        return 'boolean'

    def visit_false_const(self, node):
        return 'boolean'

    def visit_char_const(self, node):
        return 'char'

    def visit_simple_var(self, node):
        name = str(node.children[0])
        sym = self.current_scope.lookup(name)
        if not sym: raise SemanticError(f"Переменная '{name}' не объявлена.")
        return sym['type']

    def check_binary(self, node, expected, result):
        t1 = self.visit(node.children[0])
        t2 = self.visit(node.children[1])
        if t1 != expected or t2 != expected:
            raise SemanticError(f"Ошибка типов в '{node.data}': ожидалось {expected}, получено {t1} и {t2}")
        return result

    def visit_add(self, node):
        return self.check_binary(node, 'integer', 'integer')

    def visit_sub(self, node):
        return self.check_binary(node, 'integer', 'integer')

    def visit_mul(self, node):
        return self.check_binary(node, 'integer', 'integer')

    def visit_div_int(self, node):
        return self.check_binary(node, 'integer', 'integer')

    def visit_div_float(self, node):
        t1 = self.visit(node.children[0])
        t2 = self.visit(node.children[1])
        if t1 == 'integer' and t2 == 'integer':
            node.data = 'div_int'
            return 'integer'
        raise SemanticError("Оператор '/' применим только к типу integer.")

    def visit_log_or(self, node):
        return self.check_binary(node, 'boolean', 'boolean')

    def visit_log_and(self, node):
        return self.check_binary(node, 'boolean', 'boolean')

    def check_relational(self, node):
        t1 = self.visit(node.children[0])
        t2 = self.visit(node.children[1])
        if t1 != t2: raise SemanticError(f"Нельзя сравнивать типы {t1} и {t2}")
        return 'boolean'

    def visit_gt(self, node):
        return self.check_relational(node)

    def visit_lt(self, node):
        return self.check_relational(node)

    def visit_eq(self, node):
        return self.check_relational(node)

    def visit_neq(self, node):
        return self.check_relational(node)

    def visit_assign_statement(self, node):
        var_type = self.visit(node.children[0])
        expr_type = self.visit(node.children[1])
        if var_type != expr_type:
            raise SemanticError(f"Несовпадение типов при присваивании: ожидался {var_type}, получен {expr_type}.")

    def visit_if_statement(self, node):
        if self.visit(node.children[0]) != 'boolean': raise SemanticError("Условие if должно быть boolean.")
        self.visit(node.children[1])
        if len(node.children) == 3: self.visit(node.children[2])

    def visit_while_statement(self, node):
        if self.visit(node.children[0]) != 'boolean': raise SemanticError("Условие while должно быть boolean.")
        self.visit(node.children[1])

    def visit_call_statement(self, node):
        name = str(node.children[0])
        sym = self.current_scope.lookup(name)
        if not sym: raise SemanticError(f"Процедура '{name}' не объявлена.")

        if len(node.children) > 1:
            args = node.children[1].children
            if 'params' in (sym.get('info') or {}):
                expected = len(sym['info']['params'])
                if len(args) != expected:
                    raise SemanticError(f"Процедура {name} ожидает {expected} аргументов.")

            for arg in args:
                self.visit(arg)

    def visit_expr_list(self, node):
        for child in node.children:
            self.visit(child)

    def visit_empty_statement(self, node):
        pass

    def visit_proc_decl(self, node):
        name = str(node.children[0])
        params = []
        if len(node.children) > 2:
            param_list = node.children[1]
            for p_decl in param_list.children:
                idents = p_decl.children[0].children
                p_type = p_decl.children[1].data.replace('type_', '')
                for ident in idents:
                    params.append((str(ident), p_type))

        self.current_scope.declare(name, 'void', 'proc', info={'params': params})

        old_scope = self.current_scope
        self.current_scope = SymbolTable(parent=old_scope)

        for p_name, p_type in params:
            self.current_scope.declare(p_name, p_type, 'var')

        block_node = node.children[-1]
        self.visit(block_node)

        self.current_scope = old_scope