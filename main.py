import os
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from interpreter import Interpreter
from print_ast import print_tree
from errors import errors


def run():
    if not os.path.exists("examples"):
        os.makedirs("examples")
        return

    files = [f for f in os.listdir('examples') if f.endswith('.pas')]

    for f in files:
        with open(f'examples/{f}', 'r', encoding='utf-8') as file:
            code = file.read()

        print(f"\nФайл: {f}")

        errors.has_error = False

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            SemanticAnalyzer().visit(ast)

            ast = Optimizer().visit(ast)

            print("Дерево AST:")
            print_tree(ast)

            print("\nРезультат выполнения:")
            Interpreter().visit(ast)

        except SystemExit:
            print(f"\nКомпиляция '{f}' прервана из-за ошибок. Переходим к следующему файлу...")
        except Exception as e:
            print(f"\nВнутренняя ошибка в '{f}': {e}")


if __name__ == '__main__':
    run()