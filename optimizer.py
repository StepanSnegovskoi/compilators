from lark import Tree, Token


class ASTOptimizer:
    def optimize(self, node):
        if not isinstance(node, Tree):
            return node

        new_children = []
        for child in node.children:
            new_children.append(self.optimize(child))
        node.children = new_children

        if node.data in ['add', 'sub', 'mul', 'div_int']:
            return self.optimize_arithmetic(node)

        if node.data in ['gt', 'lt', 'eq', 'neq']:
            return self.optimize_relational(node)

        if node.data == 'if_statement':
            return self.optimize_if(node)
        if node.data == 'while_statement':
            return self.optimize_while(node)

        return node

    def optimize_arithmetic(self, node):
        left, right = node.children[0], node.children[1]

        if left.data == 'number' and right.data == 'number':
            v1, v2 = int(left.children[0]), int(right.children[0])
            if node.data == 'add':
                res = v1 + v2
            elif node.data == 'sub':
                res = v1 - v2
            elif node.data == 'mul':
                res = v1 * v2
            elif node.data == 'div_int':
                if v2 == 0: return node
                res = v1 // v2
            return Tree('number', [Token('SIGNED_INT', str(res))])

        if right.data == 'number':
            v2 = int(right.children[0])
            if node.data == 'add' and v2 == 0: return left
            if node.data == 'sub' and v2 == 0: return left
            if node.data == 'mul' and v2 == 1: return left
            if node.data == 'mul' and v2 == 0:
                return Tree('number', [Token('SIGNED_INT', '0')])
        return node

    def optimize_relational(self, node):
        left, right = node.children[0], node.children[1]
        if left.data == 'number' and right.data == 'number':
            v1, v2 = int(left.children[0]), int(right.children[0])
            if node.data == 'gt':
                res = v1 > v2
            elif node.data == 'lt':
                res = v1 < v2
            elif node.data == 'eq':
                res = v1 == v2
            elif node.data == 'neq':
                res = v1 != v2
            return Tree('true_const' if res else 'false_const', [])
        return node

    def optimize_if(self, node):
        cond = node.children[0]
        if cond.data == 'true_const':
            return node.children[1]
        elif cond.data == 'false_const':
            if len(node.children) == 3:
                return node.children[2]
            return Tree('empty_statement', [])
        return node

    def optimize_while(self, node):
        cond = node.children[0]
        if cond.data == 'false_const':
            return Tree('empty_statement', [])
        return node