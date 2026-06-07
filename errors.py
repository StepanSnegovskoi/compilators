import sys

class Errors:
    def __init__(self):
        self.has_error = False

    def error(self, message, line=None, column=None):
        self.has_error = True
        if line and column:
            print(f"Ошибка [строка {line}, колонка {column}]: {message}")
        else:
            print(f"Ошибка: {message}")
        sys.exit(1)

errors = Errors()