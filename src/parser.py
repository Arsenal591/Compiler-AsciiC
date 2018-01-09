from ply import yacc
from lexer import tokens
from ast_node import *
from symbols import *

symbol_table_chain = SymbolTableChain()

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

    # TODO: symbol table
    p[0] = IdentifierNode(p[1])


def p_constant(p):
    '''
    constant : CONSTANT

    '''

    p[0] = ConstantNode(p[1])


def p_string_literal(p):
    '''
    string_literal : STRING_LITERAL

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
        p[0] = ArgumentListNode(p[1], p[3])


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

    p[0] = p[1]


def p_unary_expression(p):
    '''
    unary_expression : postfix_expression
        | unary_operator unary_expression
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ExpressionNode(None, p[1], p[2])


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

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ExpressionNode(p[1], p[2], p[3])


def p_expression(p):
    '''
    expression : assignment_expression
        | expression ',' assignment_expression
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ExpressionNode(p[1], p[2], p[3])


def p_constant_expression(p):
    '''
    constant_expression : conditional_expression
    '''

    p[0] = p[1]


def p_declaration(p):
    '''
    declaration :  type_specifier init_declarator_list ';'
    '''

    p[0] = DeclarationNode(p[1], p[2])
    p[0].add_into_table(symbol_table_chain)


def p_init_declarator_list(p):
    '''
    init_declarator_list : init_declarator
        | init_declarator_list ',' init_declarator
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = InitDeclaratorListNode(p[1], p[3])



def p_init_declarator(p):
    '''
    init_declarator : declarator
        | declarator '=' assignment_expression
    '''

    if len(p) == 2:
        p[0] = InitDeclaratorNode(p[1], None)
    else:
        p[0] = InitDeclaratorNode(p[1], p[3])



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

    p[0] = p[1]


def p_declarator(p):
    '''
    declarator : identifier
        | '(' declarator ')'
        | declarator '[' constant_expression ']'
        | declarator '[' ']'
        | declarator '(' parameter_type_list ')'
        | declarator '(' ')'
    '''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        elif p[2] == '[':
            p[0] = DeclaratorArrayNode(p[1], None)
        elif p[2] == '(':
            p[0] = DeclaratorFunctionNode(p[1], None)
    else:
        if p[2] == '[':
            p[0] = DeclaratorArrayNode(p[1], p[3])
        elif p[2] == '(':
            p[0] = DeclaratorFunctionNode(p[1], p[3])



def p_parameter_type_list(p):
    '''
    parameter_type_list : parameter_declaration
        | parameter_type_list ',' parameter_declaration
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ParameterTypeListNode(p[1], p[3])


def p_parameter_declaration(p):
    '''
    parameter_declaration : type_specifier declarator
        | type_specifier
    '''

    if len(p) == 2:
        p[0] = ParameterDeclarationNode(p[1], None)
    else:
        p[0] = ParameterDeclarationNode(p[1], p[2])


def p_statement(p):
    '''
    statement : generate_symbol_table compound_statement pop_symbol_table
        | expression_statement
        | selection_statement
        | iteration_statement
        | jump_statement
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_compound_statement(p):
    '''
    compound_statement : '{' '}'
        | compound_statement_only
        | compound_declaration_only
        | '{' declaration_list statement_list '}'
    '''

    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '}':
        p[0] = CompoundStatementNode(None, None)
    else:
        p[0] = CompoundStatementNode(p[2], p[3])


def p_compound_declaration_only(p):
    '''
    compound_declaration_only : '{' declaration_list '}'
    '''

    p[0] = CompoundStatementNode(p[2], None)


def p_compound_statement_only(p):
    '''
    compound_statement_only : '{' statement_list '}'
    '''

    p[0] = CompoundStatementNode(None, p[2])



def p_declaration_list(p):
    '''
    declaration_list : declaration
        | declaration_list declaration
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = DeclarationListNode(p[1], p[2])

def p_statement_list(p):
    '''
    statement_list : statement
        | statement_list statement
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = StatementListNode(p[1], p[2])


def p_expression_statement(p):
    '''
    expression_statement : ';'
        | expression ';'
    '''

    if p[1] == ';':
        p[0] = ExpressionStatementNode(None)
    else:
        p[0] = ExpressionStatementNode(p[1])


def p_selection_statement(p):
    '''
    selection_statement : IF '(' expression ')' statement
        | IF '(' expression ')' statement ELSE statement
    '''

    if len(p) == 6:
        p[0] = SelectionStatementNode(p[3], p[5], None)
    else:
        p[0] = SelectionStatementNode(p[3], p[5], p[7])


def p_iteration_statement(p):
    '''
    iteration_statement : WHILE '(' expression ')' statement
    '''

    p[0] = IterationStatementNode(p[3], p[5])


def p_jump_statement(p):
    '''
    jump_statement : CONTINUE ';'
        | BREAK ';'
        | RETURN ';'
        | RETURN expression ';'
    '''

    if len(p) == 3:
        p[0] = JumpStatementNode(p[1], None)
    else:
        p[0] = JumpStatementNode(p[1], p[2])


def p_translation_unit(p):
    '''
    translation_unit : external_declaration
        | translation_unit external_declaration
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = TranslationUnitNode(p[1], p[2])


def p_external_declaration(p):
    '''
	external_declaration : function_definition
		| declaration
	'''

    p[0] = p[1]


def p_function_definition(p):
    '''
    function_definition : type_specifier declarator generate_symbol_table compound_statement pop_symbol_table
    '''

    p[0] = FunctionDefinition(p[1], p[2], p[4])
    

def p_generate_symbol_table(p):
    '''
    generate_symbol_table :
    '''
    symbol_table_chain.push_chain()
    # if it is next to a function definition
    if isinstance(p[-1], DeclaratorFunctionNode):
    	if p[-1].param_type_list is None:
    		pass
    	elif isinstance(p[-1].param_type_list, ParameterDeclarationNode):
    		p[-1].param_type_list.add_into_table(symbol_table_chain)
    	elif isinstance(p[-1].param_type_list, ParameterTypeListNode):
    		pos = p[-1].param_type_list
    		while isinstance(pos, ParameterTypeListNode):
    			pos.next_declaration.add_into_table(symbol_table_chain)
    			pos = pos.previous_declarations
    		pos.add_into_table(symbol_table_chain)
    	else:
    		raise TypeError()

    	pass
    #print(p[-1].param_type_list.declarator.constant_expression.value)

    #if p[-1]
    #print(p[-1])


def p_pop_symbol_table(p):
    '''
    pop_symbol_table : 
    '''
    #symbol_table_chain.pop_chain()


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
int foo(int x[5][9], int y)
{
	int m, n = 7, q = 12;
	char ee[122];
}
"""

node = parser.parse(data, debug=log)
node.generate_code()
#print(node.statements.declaration_list.init_declarator_list.declarator.item)
#print(symbol_table_chain.get_item('x'))
print(symbol_table_chain.current_table.items)
exit(0)

