class CompilerError(Exception):
    pass

class SemanticError(CompilerError):
    pass

class NodeVisitor:
    """Паттерн Посетитель для рекурсивного обхода AST-дерева."""
    def visit(self, node):
        if hasattr(node, 'data'):
            method_name = f'visit_{node.data}'
            method = getattr(self, method_name, self.generic_visit)
            return method(node)
        return node

    def generic_visit(self, node):
        if hasattr(node, 'children'):
            res = None
            for child in node.children:
                res = self.visit(child)
            return res