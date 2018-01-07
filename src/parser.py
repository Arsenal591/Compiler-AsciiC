from ply import yacc
from lexer import tokens
from ast_node import *

precedence = (
    ('left', 'OR_OP'),
    ('left', 'AND_OP'),
    ('left', '|'),
    ('left', '^'),
    ('left', '&'),
    ('left', 'EQ_OP', 'NE_OP'),
    ('left', '<', '>', 'LE_OP', 'GE_OP'),
    ('left', 'LEFT_OP', 'RIGHT_OP'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
)

def p_identifier(p):
    '''
    identifier : IDENTIFIER

    '''

    p[0] = IdentifierNode(p[1])


def p_constant(p):
    '''
    constant: CONSTANT

    '''

    p[0] = ConstantNode(p[1])


def p_string_literal(p):
    '''
    string_literal: STRING_LITERAL

    '''

    p[0] = StringLiteralNode(p[1])


def p_primary_expression(p):
    '''
    primary_expression : identifier
        | constant
        | string_literal
        | '(' expression ')'

    '''

    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_postfix_expression(p):
    '''
    postfix_expression : primary_expression
        | postfix_expression '[' expression ']'
        | postfix_expression '(' ')'
        | postfix_expression '(' argument_expression_list ')'
        | postfix_expression '.' IDENTIFIER
        | postfix_expression PTR_OP IDENTIFIER
        | postfix_expression INC_OP
        | postfix_expression DEC_OP
    '''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ExpressionNode(p[1], p[2], None)
    elif len(p) == 4:
        if p[2] == '(':
            p[0] = FunctionCallNode(p[1], None)
        else:
            p[0] = ExpressionNode(p[1], p[2], p[3])
    else:
        if p[2] == '(':
            p[0] = FunctionCallNode(p[1], p[3])
        else:
            p[0] = ArrayNode(p[1], p[3])


def p_argument_expression_list(p):
    '''
    argument_expression_list : assignment_expression
        | argument_expression_list ',' assignment_expression
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ArgumentListNode(p[1], p[2])


def p_assignment_operator(p):
    '''
    assignment_operator : '='
        | MUL_ASSIGN
        | DIV_ASSIGN
        | MOD_ASSIGN
        | ADD_ASSIGN
        | SUB_ASSIGN
        | LEFT_ASSIGN
        | RIGHT_ASSIGN
        | AND_ASSIGN
        | XOR_ASSIGN
        | OR_ASSIGN
    '''

    p[0] = p[1]


def p_assignment_expression(p):
    '''
    assignment_expression : conditional_expression
        | postfix_expression assignment_operator assignment_expression
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ExpressionNode(p[1], p[2], p[3])


def p_conditional_expression(p):
    '''
    conditional_expression : binary_expression
        | binary_expression '?' expression ':' conditional_expression
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        # TODO: ternary expression
        pass


def p_unary_operator(p):
    '''
    unary_operator : INC_OP
        | DEC_OP
        | '&'
        | '+'
        | '-'
        | '~'
        | '!'
    '''
    pass


def p_unary_expression(p):
    '''
    unary_expression : postfix_expression
        | unary_operator unary_expression
    '''
    pass


def p_binary_expression(p):
    '''
    binary_expression : unary_expression
        | binary_expression OR_OP binary_expression
        | binary_expression AND_OP binary_expression
        | binary_expression '|' binary_expression
        | binary_expression '^' binary_expression
        | binary_expression '&' binary_expression
        | binary_expression EQ_OP binary_expression
        | binary_expression NE_OP binary_expression
        | binary_expression '<' binary_expression
        | binary_expression '>' binary_expression
        | binary_expression LE_OP binary_expression
        | binary_expression GE_OP binary_expression
        | binary_expression LEFT_OP binary_expression
        | binary_expression RIGHT_OP binary_expression
        | binary_expression '+' binary_expression
        | binary_expression '-' binary_expression
        | binary_expression '*' binary_expression
        | binary_expression '/' binary_expression
        | binary_expression '%' binary_expression
    '''
    pass


def p_expression(p):
    '''
    expression : assignment_expression
        | expression ',' assignment_expression
    '''
    pass


def p_constant_expression(p):
    '''
    constant_expression : conditional_expression
    '''
    pass


def p_declaration(p):
    '''
    declaration :  type_specifier init_declaration_list ';'
    '''
    pass


def p_init_declaration_list(p):
    '''
    init_declaration_list : init_declarator
        | init_declaration_list ',' init_declarator
    '''
    pass


def p_init_declarator(p):
    '''
    init_declarator : declarator
        | declarator '=' assignment_expression
    '''
    pass


#  struct_or_union_specifier
#	enum_specifier
def p_type_specifier(p):
    '''
    type_specifier : VOID
        | CHAR
        | SHORT
        | INT
        | LONG
        | FLOAT
        | DOUBLE
        | IDENTIFIER
    '''
    pass


def p_declarator(p):
    '''
    declarator : IDENTIFIER
        | '(' declarator ')'
        | declarator '[' constant_expression ']'
        | declarator '[' ']'
        | declarator '(' parameter_type_list ')'
        | declarator '(' ')'
    '''
    pass


def p_parameter_type_list(p):
    '''
    parameter_type_list : parameter_declaration
        | parameter_type_list ',' parameter_declaration
    '''
    pass


def p_parameter_declaration(p):
    '''
    parameter_declaration : type_specifier declarator
        | type_specifier
    '''
    pass


def p_statement(p):
    '''
    statement : generate_symbol_table compound_statement pop_symbol_table
        | expression_statement
        | selection_statement
        | iteration_statement
        | jump_statement
    '''
    pass


def p_compound_statement(p):
    '''
    compound_statement : '{' '}'
        | '{' statement_list '}'
        | '{' declaration_list '}'
        | '{' declaration_list statement_list '}'
    '''
    pass


def p_declaration_list(p):
    '''
    declaration_list : declaration
        | declaration_list declaration
    '''
    pass


def p_statement_list(p):
    '''
    statement_list : statement
        | statement_list statement
    '''
    pass


def p_expression_statement(p):
    '''
    expression_statement : ';'
        | expression ';'
    '''
    pass


def p_selection_statement(p):
    '''
    selection_statement : IF '(' expression ')' statement
        | IF '(' expression ')' statement ELSE statement
    '''
    pass


def p_iteration_statement(p):
    '''
    iteration_statement : WHILE '(' expression ')' statement
    '''
    pass


def p_jump_statement(p):
    '''
    jump_statement : CONTINUE ';'
        | BREAK ';'
        | RETURN ';'
        | RETURN expression ';'
    '''
    pass


def p_translation_unit(p):
    '''
    translation_unit : external_declaration
        | translation_unit external_declaration
    '''


def p_external_declaration(p):
	'''
	external_declaration : function_definition
		| declaration
	'''

	pass


def p_function_definition(p):
	'''
	function_definition : type_specifier declarator generate_symbol_table compound_statement pop_symbol_table
	'''
	print('fuck')
	pass

def p_generate_symbol_table(p):
	'''
	generate_symbol_table :
	'''

def p_pop_symbol_table(p):
	'''
	pop_symbol_table : 
	'''

import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

parser = yacc.yacc(start='translation_unit', debug=True, debuglog=log)

data = """
int a[800],b;
char c, d;
int e = 5;
int main(void)
{

	int a = 2 + 3;
	char b[1000];
	b[2] = b[3 + 4] - a;
	d = f(a, b[5]);
	return 0;
}
"""

parser.parse(data, debug=log)
