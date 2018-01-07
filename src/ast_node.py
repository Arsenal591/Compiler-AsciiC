
class BaseNode(object):
    def __init__(self):
        pass


class ConstantNode(BaseNode):
    def __init__(self, value):
        self.value = value
        self.data_type = 'float'


class StringLiteralNode(BaseNode):
    def __init__(self, value):
        self.value = value
        self.data_type = 'str'


class IdentifierNode(BaseNode):
    def __init__(self, item):
        self.item = item
        self.data_type = item.data_type


class ArrayNode(BaseNode):
    def __init__(self, item, bias):
        self.item = item.item
        self.data_type = item.data_type
        if isinstance(item, IdentifierNode):
            self.bias = bias
        else:
            # TODO
            pass


class FunctionCallNode(BaseNode):
    def __init__(self, func, argument_list):
        self.func = func
        self.argument_list = argument_list


class ArgumentListNode(BaseNode):
    def __init__(self, previous_args, next_arg):
        self.previous_args = previous_args
        self.next_arg = next_arg


class ExpressionNode(BaseNode):
    def __init__(self, op1, op2, operator):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

        # TODO: type checking
        self.data_type = op1.data_type


class ExpressionListNode(BaseNode):
    def __init__(self, previous_exprs, next_expr):
        self.previous_exprs = previous_exprs
        self.next_expr = next_expr


class DeclarationNode(BaseNode):
	def __init__(self, data_type, init_declatation_list):
		self.data_type = data_type
		self.init_declatation_list = init_declatation_list


class InitDeclarationListNode(BaseNode):
    def __init__(self, previous_declarations, next_declaration):
        self.previous_declarations = previous_declarations
        self.next_declaration = next_declaration


class InitDeclaratorNode(BaseNode):
    def __init__(self, declarator, intializer):
        self.declarator = declarator
        self.intializer = intializer


class DeclaratorNode(BaseNode):
    def __init__(self, declarator, param_type_list):
        self.param_type_list = param_type_list
        self.item = declarator.item


class ParameterTypeListNode(BaseNode):
    def __init__(self, previous_declarations, next_declaration):
        self.previous_declarations = previous_declarations
        self.next_declaration = next_declaration


class ParameterDeclarationListNode(BaseNode):
	def __init__(self, data_type, declarator):
		self.data_type = data_type
		self.declarator = declarator


class InitializerNode(BaseNode):
	def __init__(self, initializer_list):
		self.initializer_list = initializer_list


class IntializerListNode(BaseNode):
	def __init__(self, previous_initializers, next_initializer):
		self.previous_initializers = previous_initializers
		self.next_initializer = next_initializer


class CompoundStatementNode(BaseNode):
	def __init__(self, declaration_list, statement_list):
		self.declaration_list = declaration_list
		self.statement_list = statement_list


class DeclarationListNode(BaseNode):
	def __init__(self, previous_declarations, next_declaration):
		self.previous_declarations = previous_declarations
		self.next_declaration = next_declarationE


class StatementListNode(BaseNode):
	def __init__(self, previous_statements, next_statement):
		self.previous_statements = previous_statements
		self.next_statement = next_statement


class ExpressionStatementNode(BaseNode):
	def __init__(self, expression):
		self.expression = expression


class SelectionStatementNode(BaseNode):
	def __init__(self, condition, true_statement, false_statement):
		self.condition = condition
		self.true_statement = true_statement
		self.false_statement = false_statement


class IterationStatementNode(BaseNode):
	def __init__(self, condition, statement):
		self.condition = condition
		self.statement = statement


class JumpStatementNode(BaseNode):
	def __init__(self, jump_type, expression):
		self.jump_type = jump_type
		self.expression = expression


class TranslationUnitNode(BaseNode):
	def __init__(self, previous_units, next_unit):
		self.previous_units = previous_units
		self.next_unit = next_unit


class FunctionDefinition(BaseNode):
	def __init__(self, return_type, declarator, statements):
		self.return_type = return_type
		self.declarator = declarator
		self.statements = statements
