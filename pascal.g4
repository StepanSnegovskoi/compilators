grammar pascal;

start: program EOF ;

program: PROGRAM IDENTIFIER SEMI block DOT ;

block: declarations compound_statement
     | compound_statement
     ;

declarations: var_declarations func_declarations
            | var_declarations
            | func_declarations
            ;

var_declarations: VAR var_declaration+ ;
var_declaration: ident_list COLON type_spec SEMI ;

func_declarations: func_declaration+ ;
func_declaration: proc_decl | func_decl ;

proc_decl: PROCEDURE IDENTIFIER (LPAREN param_list RPAREN)? SEMI block SEMI ;
func_decl: FUNCTION IDENTIFIER (LPAREN param_list RPAREN)? COLON simple_type SEMI block SEMI ;

param_list: param_decl (SEMI param_decl)* ;
param_decl: ident_list COLON simple_type ;

ident_list: IDENTIFIER (COMMA IDENTIFIER)* ;

type_spec: simple_type
         | ARRAY LBRACK SIGNED_INT DOTDOT SIGNED_INT RBRACK OF simple_type
         ;

simple_type: INTEGER | BOOLEAN | CHAR_TYPE ;

compound_statement: BEGIN statement_list END ;
statement_list: statement (SEMI statement)* ;

statement: compound_statement
         | assign_statement
         | if_statement
         | while_statement
         | do_while_statement
         | for_statement
         | call_statement
         | empty_statement
         ;

assign_statement: variable ASSIGN expr ;
if_statement: IF expr THEN statement (ELSE statement)? ;
while_statement: WHILE expr DO statement ;
do_while_statement: DO statement WHILE expr ;
for_statement: FOR IDENTIFIER ASSIGN expr TO expr DO statement ;
call_statement: IDENTIFIER (LPAREN expr_list RPAREN)? ;

expr_list: expr (COMMA expr)* ;

expr: factor
    | expr (STAR | SLASH | DIV | MOD) expr
    | expr (PLUS | MINUS) expr
    | expr (GT | LT | GTE | LTE) expr
    | expr (EQ | NEQ) expr
    | expr AND expr
    | expr OR expr
    ;

factor: (PLUS | MINUS | NOT) factor
      | variable
      | SIGNED_INT
      | CHAR_CONST
      | TRUE
      | FALSE
      | LPAREN expr RPAREN
      | function_call
      ;

function_call: IDENTIFIER LPAREN expr_list RPAREN ;

variable: IDENTIFIER
        | IDENTIFIER LBRACK expr RBRACK
        ;

empty_statement: ;

PROGRAM:   'program' ;
VAR:       'var' ;
PROCEDURE: 'procedure' ;
FUNCTION:  'function' ;
ARRAY:     'array' ;
OF:        'of' ;
INTEGER:   'integer' ;
BOOLEAN:   'boolean' ;
CHAR_TYPE: 'char' ;
BEGIN:     'begin' ;
END:       'end' ;
IF:        'if' ;
THEN:      'then' ;
ELSE:      'else' ;
WHILE:     'while' ;
DO:        'do' ;
FOR:       'for' ;
TO:        'to' ;
DIV:       'div' ;
MOD:       'mod' ;
AND:       'and' ;
OR:        'or' ;
NOT:       'not' ;
TRUE:      'true' ;
FALSE:     'false' ;

PLUS:   '+' ;
MINUS:  '-' ;
STAR:   '*' ;
SLASH:  '/' ;
ASSIGN: ':=' ;
EQ:     '=' ;
NEQ:    '<>' ;
GT:     '>' ;
LT:     '<' ;
GTE:    '>=' ;
LTE:    '<=' ;
LPAREN: '(' ;
RPAREN: ')' ;
LBRACK: '[' ;
RBRACK: ']' ;
DOTDOT: '..' ;
DOT:    '.' ;
COMMA:  ',' ;
COLON:  ':' ;
SEMI:   ';' ;

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]* ;
SIGNED_INT: '-'? [0-9]+ ;
CHAR_CONST: '\'' ~['\r\n]* '\'' ;

WS: [ \t\r\n]+ -> skip ;
COMMENT: '{' .*? '}' -> skip ;