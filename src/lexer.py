from ply import lex as lex
from ply.lex import TOKEN

tab_width = 4

data_type_tokens = [
	'CHAR', 'SHORT', 'INT', 'LONG', 
	'FLOAT', 'DOUBLE', 'CONST', 'VOID', 
	'STRUCT', 'UNION', 'ENUM',
]

operation_tokens = [
	'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP',
	'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 
	'NE_OP',  'AND_OP', 'OR_OP',
]

assign_tokens = [
	'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN',
	'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN',
	'XOR_ASSIGN', 'OR_ASSIGN'
]

control_flow_tokens = [
	'IF', 'ELSE', 'WHILE', 'BREAK', 'CONTINUE', 'RETURN',
]

variable_tokens = [
	'IDENTIFIER', 'CONSTANT', 'STRING_LITERAL'
]

literals = [';', '{', '}', ',', ':', '=', '(', ')', 
			'[', ']', '.', '&', '!', '~', '-', '+',
			'*', '/', '%', '<', '>', '^', '|', '?',
]

reserved_keywords = dict()
for item in (data_type_tokens + control_flow_tokens):
	reserved_keywords[item.lower()] = item


constant_patterns = {
	r'0[xX][a-fA-F0-9]+': 'hex',
	r'0[0-9]+': 'oct',
	r'[0-9]+': 'dec',
	r'[0-9]+[Ee][+-]?[0-9]+': 'exp',
	r'[0-9]*\.[0-9]+([Ee][+-]?[0-9]+)?': 'float',
	r'[0-9]+\.[0-9]*([Ee][+-]?[0-9]+)?': 'float',
}

t_ignore = r' \t\v\n\f'

def t_IDENTIFIER(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved_keywords.get(t.value, 'IDENTIFIER')
	return t


@TOKEN('|'.join(constant_patterns.keys()))
def t_CONSTANT(t):
	t.value = float(t.value)
	return t


def t_STRING_LITERAL(t):
	r'"(\\.|[^\\"])*"'

t_LEFT_ASSIGN = r'<<='
t_RIGHT_ASSIGN = r'>>='
t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_XOR_ASSIGN = r'^='
t_OR_ASSIGN = r'\|='

t_LEFT_OP = r'<<'
t_RIGHT_OP = r'>>'
t_INC_OP = r'\+\+'
t_DEC_OP = r'--'
t_PTR_OP = r'->'
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_LE_OP = r'<='
t_GE_OP = r'>='
t_EQ_OP = r'=='
t_NE_OP = r'!='
