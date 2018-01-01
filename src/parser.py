from ply import yacc
from lexer import tokens

def p_primary_expression(p):
	'''
	primary_expression : IDENTIFIER
		| CONSTANT
		| STRING_LITERAL
		| '(' expression ')'

	'''
	pass


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
	pass


def p_argument_expression_list(p):
	'''
	argument_expression_list : assignment_expression
		| argument_expression_list ',' assignment_expression
	'''
	pass


def p_assignment_expression(p):
	'''
	assignment_expression : conditional_expression
		| postfix_expression assignment_operator assignment_expression
	'''
	pass


def p_conditional_expression(p):
	'''
	conditional_expression : binary_expression
		| general_expression '?' expression ':' conditional_expression
	'''
	pass


def p_unary_operator(p):
	'''
	unary_operator : INC_OP | DEC_OP | '&' | '*' | '+' | '-' | '~' | '!'
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
		| binary_expression'EQ_OP binary_expression
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


yacc.yacc()
