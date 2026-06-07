import os
from grammar import get_parser
from semantic import SemanticAnalyzer
from optimizer import ASTOptimizer
from interpreter import ASTInterpreter
from lark import Tree


def print_tree(node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "
    label = node.data if isinstance(node, Tree) else str(node)
    print(prefix + connector + label)

    prefix += "    " if is_last else "│   "
    children = [c for c in node.children if isinstance(c, Tree)]

    for i, child in enumerate(children):
        print_tree(child, prefix, i == len(children) - 1)


def run():
    parser = get_parser()
    for f in [f for f in os.listdir('examples') if f.endswith('.pas')]:
        with open(f'examples/{f}') as file:
            code = file.read()

        tree = parser.parse(code)
        SemanticAnalyzer().visit(tree)
        tree = ASTOptimizer().optimize(tree)

        print(f"\nФайл: {f}")
        print("Оптимизированное дерево AST:")
        print_tree(tree)

        print("\nРезультат выполнения:")
        ASTInterpreter().visit(tree)


if __name__ == '__main__':
    run()