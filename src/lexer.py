from ply import lex as lex

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

