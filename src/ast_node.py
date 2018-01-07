
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


class InitDeclarationListNode(BaseNode):
	def __init__(self, previous_declarations, next_declaration):
		self.previous_declarations = previous_declarations
		self.next_declaration = next_declaration


class InitDeclarationNode(BaseNode):
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


class ParameterDeclarationList(BaseNode):
	def __init__(self, type_specifier, declarator):
		self.type_specifier = type_specifier
		self.declarator = declarator