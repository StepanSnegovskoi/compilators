from lark import Lark

pascal_grammar = """
?start: program
program: "program" IDENTIFIER ";" block "."
block: declarations compound_statement | compound_statement
declarations: var_declarations func_declarations | var_declarations | func_declarations
var_declarations: "var" var_declaration+
var_declaration: ident_list ":" type_spec ";"

func_declarations: func_declaration+
?func_declaration: proc_decl | func_decl
proc_decl: "procedure" IDENTIFIER ["(" param_list ")"] ";" block ";"
func_decl: "function" IDENTIFIER ["(" param_list ")"] ":" simple_type ";" block ";"

param_list: param_decl (";" param_decl)*
param_decl: ident_list ":" simple_type
ident_list: IDENTIFIER ("," IDENTIFIER)*

?type_spec: simple_type | "array" "[" SIGNED_INT ".." SIGNED_INT "]" "of" simple_type -> array_type
simple_type: "integer" -> type_integer | "boolean" -> type_boolean | "char" -> type_char

compound_statement: "begin" statement_list "end"
statement_list: statement (";" statement)*

?statement: compound_statement | assign_statement | if_statement | while_statement | do_while_statement | for_statement | call_statement | empty_statement

assign_statement: variable ":=" expr
if_statement: "if" expr "then" statement ["else" statement]
while_statement: "while" expr "do" statement
do_while_statement: "do" statement "while" expr
for_statement: "for" IDENTIFIER ":=" expr "to" expr "do" statement
call_statement: IDENTIFIER ["(" expr_list ")"]

expr_list: expr ("," expr)*

?expr: logic_or
?logic_or: logic_and | logic_or "or" logic_and -> log_or
?logic_and: equality | logic_and "and" equality -> log_and
?equality: relational | equality "=" relational -> eq | equality "<>" relational -> neq
?relational: addition | relational ">" addition -> gt | relational "<" addition -> lt | relational ">=" addition -> gte | relational "<=" addition -> lte
?addition: term | addition "+" term -> add | addition "-" term -> sub
?term: factor | term "*" factor -> mul | term "/" factor -> div_float | term "div" factor -> div_int | term "mod" factor -> modulo

?factor: "+" factor -> unary_plus | "-" factor -> unary_minus | "not" factor -> unary_not
       | TRUE -> true_const | FALSE -> false_const | "(" expr ")" | function_call
       | variable | SIGNED_INT -> number | CHAR_CONST -> char_const

function_call: IDENTIFIER "(" expr_list ")"
variable: IDENTIFIER -> simple_var | IDENTIFIER "[" expr "]" -> array_access
empty_statement: 

%import common.CNAME -> IDENTIFIER
%import common.SIGNED_INT
%import common.WS

TRUE.2: "true" | "True" | "TRUE"
FALSE.2: "false" | "False" | "FALSE"

CHAR_CONST: /'[^']*'/
COMMENT: /{[^}]*}/

%ignore WS
%ignore COMMENT
"""

def get_parser():
    return Lark(pascal_grammar, parser='earley', lexer='dynamic')