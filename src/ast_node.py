
indent = 0

assign_operators = ['=', '*=', '/=', '%=', '+=', '-=', '<<=', '>>=', '&=', '^=', '|=']

temp_var_count = 0

def generate_unique_tempname():
	global temp_var_count
	temp_var_count += 1
	return 'temp_var_%d' % temp_var_count

def print_code(*args):
	print(*args, end='')


def type_checking(data_type, value_node):
	if data_type in ['int', 'char', 'short', 'long']:
		if value_node.data_type in ['float', 'double']:
			raise TypeError("%s type cannot be assigned to a %s type." \
							% (value_node.data_type, data_type))
	else:
		value_node.data_type = 'float'
		if value_node.value:
			value_node.value = float(value_node.value)


class BaseNode(object):
	def __init__(self):
		pass

	def traverse(self):
		for key in self.__dict__.keys():

			if isinstance(self.__dict__[key], BaseNode):
				self.__dict__[key].traverse()

	def generate_code(self):
		return None

	def is_leaf(self):
		is_leaf = isinstance(self, ConstantNode) \
						or isinstance(self, StringLiteralNode) \
						or isinstance(self, IdentifierNode) \
						or isinstance(self, ArrayNode)
		return is_leaf



class ConstantNode(BaseNode):
	def __init__(self, value):
		self.value = value
		if isinstance(self.value, int):
			self.data_type = 'int'
		else:
			self.data_type = 'float'

	def generate_code(self):
		print_code(self.value)


class StringLiteralNode(BaseNode):
	def __init__(self, value):
		self.value = value
		self.data_type = 'str'


class IdentifierNode(BaseNode):
	def __init__(self, item):
		self.value = None
		self.item = item
		self.data_type = None

	def generate_code(self):
		print_code(self.item['actual_name'])


class ArrayNode(BaseNode):
	def __init__(self, item, bias):
		self.item = item
		self.data_type = item.data_type
		self.value = None
		self.bias = bias


	def generate_code(self):
		pos = self
		array_bias = list()
		while isinstance(pos, ArrayNode):
			array_bias.append(pos.bias.value)
			pos = pos.item
		array_bias.reverse()

		flattened_bias = 0
		factor = 1
		i = len(array_bias) - 1
		while i >= 0:
			flattened_bias += factor * array_bias[i]
			factor *= pos.item['array_size'][i]
			i -= 1
		print_code("%s[%d]" % (pos.item['actual_name'], flattened_bias))


class FunctionCallNode(BaseNode):
	def __init__(self, func, argument_list):
		self.func = func
		self.argument_list = argument_list


class ArgumentListNode(BaseNode):
	def __init__(self, previous_args, next_arg):
		self.previous_args = previous_args
		self.next_arg = next_arg


class ExpressionNode(BaseNode):

	@classmethod
	def cal_unary_expression(cls, op, operator):
		if operator == '+':
			return op
		elif operator == '-':
			return -op
		elif operator == '!':
			return (not op)
		else:
			raise NotImplementedError('Unary operator %s is not implemented.' % operator)
		
	@classmethod
	def cal_binary_expression(cls, op1, operator, op2):
		if operator == '||':
			return int(op1 or op2)
		elif operator == '&&':
			return int(op1 and op2)
		elif operator == '|':
			return op1 | op2
		elif operator == '^':
			return op1 ^ op2
		elif operator == '&':
			return op1 & op2
		elif operator == '==':
			return int(op1 == op2)
		elif operator == '!=':
			return int(op1 != op2)
		elif operator == '<':
			return int(op1 < op2)
		elif operator == '>':
			return int(op1 > op2)
		elif operator == '<=':
			return int(op1 <= op2)
		elif operator == '>=':
			return int(op1 >= op2)
		elif operator == '<<':
			return op1 << op2
		elif operator == '>>':
			return op1 >> op2
		elif operator == '+':
			return op1 + op2
		elif operator == '-':
			return op1 - op2
		elif operator == '*':
			return op1 * op2
		elif operator == '/':
			# TODO: type checking
			return op1 / op2
		elif operator == '%':
			return op1 % op2


	def __init__(self, op1, operator, op2):
		self.op1 = op1
		self.op2 = op2
		self.operator = operator

		# TODO: type checking
		self.data_type = op1.data_type

		# TODO: type checking
		self.value = None
		if op2 is None:
			if op1.value is not None:
				self.value = self.cal_unary_expression(op1.value, operator)

		else:
			if op1.value is not None and op2.value is not None:
				self.value = self.cal_binary_expression(op1.value, operator, op2.value)
		#print(self.value)

	def generate_code(self):
		new_symbol_name = None
		if self.op2 is not None:
			is_leaf_1 = self.op1.is_leaf()
			is_leaf_2 = self.op2.is_leaf()
			if self.operator in assign_operators:
				if is_leaf_2 == False and self.op2.value is None:
					temp_op2 = self.op2.generate_code()
				print_code(' ' * indent)
				self.op1.generate_code()
				print_code(' %s ' % self.operator)
				if is_leaf_2:
					self.op2.generate_code()
				elif self.op2.value is not None:
					print_code(self.op2.value)
				else:
					print_code(temp_op2)
				print_code('\n')
			else:
				if is_leaf_1 == False and self.op1.value is None:
					temp_op1 = self.op1.generate_code()
				if is_leaf_2 == False and self.op2.value is None:
					temp_op2 = self.op2.generate_code()
				print_code(' ' * indent)
				new_symbol_name = generate_unique_tempname()
				print_code('%s = ' % new_symbol_name)
				if is_leaf_1:
					self.op1.generate_code()
				elif self.op1.value is not None:
					print_code(self.op1.value)
				else:
					print_code(temp_op1)
				print_code(' %s ' % self.operator)
				if is_leaf_2:
					self.op2.generate_code()
				elif self.op2.value is not None:
					print_code(self.op2.value)
				else:
					print_code(temp_op2)
				print_code('\n')
				return new_symbol_name
				#print_code('fuck = ')
		else:
			pass



class ExpressionListNode(BaseNode):
	def __init__(self, previous_exprs, next_expr):
		self.previous_exprs = previous_exprs
		self.next_expr = next_expr


class DeclarationNode(BaseNode):
	def __init__(self, data_type, init_declarator_list):
		self.data_type = data_type
		self.init_declarator_list = init_declarator_list


	def add_into_table(self, table):
		self.init_declarator_list.add_into_table(self.data_type, table)


	def generate_code(self):
		self.init_declarator_list.generate_code()


class DeclarationListNode(BaseNode):
	def __init__(self, previous_declarations, next_declaration):
		self.previous_declarations = previous_declarations
		self.next_declaration = next_declaration

	def generate_code(self):
		self.previous_declarations.generate_code()
		self.next_declaration.generate_code()


class InitDeclaratorListNode(BaseNode):
	def __init__(self, previous_declarators, next_declarator):
		self.previous_declarators = previous_declarators
		self.next_declarator = next_declarator


	def add_into_table(self, data_type, table):
		pos = self
		while isinstance(pos, InitDeclaratorListNode):
			pos.next_declarator.add_into_table(data_type, table)
			pos = pos.previous_declarators
		pos.add_into_table(data_type, table)

	def generate_code(self):
		pos = self
		self.previous_declarators.generate_code()
		self.next_declarator.generate_code()


class InitDeclaratorNode(BaseNode):
	def __init__(self, declarator, initializer):
		self.declarator = declarator
		self.initializer = initializer


	def add_into_table(self, data_type, table):
		pos = self.declarator
		array_size = list()
		while isinstance(pos, DeclaratorArrayNode):
			array_size.append(pos.constant_expression.value)
			pos = pos.declarator
		array_size.reverse()
		name = pos.item

		# Type checking
		if self.initializer:
			type_checking(data_type, self.initializer)

		pos.item = table.insert(name, data_type, array_size)


	def generate_code(self):
		array_size = list()
		item = None
		if isinstance(self.declarator, DeclaratorArrayNode):
			(item, array_size) = self.declarator.array_meta
		else:
			item = self.declarator.item
		
		if len(array_size) > 0:
			flattened_array_size = 1
			for n in array_size:
				flattened_array_size *= n
			print_code(' ' * indent)
			print_code("%s = [0] * %d\n" % (item['actual_name'], flattened_array_size))
		else:
			if self.initializer is not None:
				if self.initializer.is_leaf():
					print_code(' ' * indent)
					print_code("%s = " % item['actual_name'])
					self.initializer.generate_code()
					print_code('\n')
				else:
					temp_ini = self.initializer.generate_code()
					print_code(' ' * indent)
					print_code("%s = %s\n" % (item['actual_name'], temp_ini))

				"""
				if self.declarator.item['data_type'] == 'int' and self.initializer.data_type == 'int':
					print_code("%s = %d\n" % (item['actual_name'], self.initializer.value))
				else:
					print_code("%s = %f\n" % (item['actual_name'], self.initializer.value))"""
			else:
				print_code("%s = None\n" % item['actual_name'])


class DeclaratorFunctionNode(BaseNode):
	def __init__(self, declarator, param_type_list):
		self.declarator = declarator
		self.param_type_list = param_type_list

	def generate_code(self):
		global indent
		print_code(self.declarator.item['actual_name'])
		print_code("(")

		if self.param_type_list is not None:
			self.param_type_list.generate_code()

		print_code(")")

		

class DeclaratorArrayNode(BaseNode):
	def __init__(self, declarator, constant_expression):
		self.declarator = declarator
		self.constant_expression = constant_expression

	@property
	def array_meta(self):
		pos = self
		array_size = list()
		while isinstance(pos, DeclaratorArrayNode):
			array_size.append(pos.constant_expression.value)
			pos = pos.declarator
		array_size.reverse()
		return (pos.item, array_size)


class ParameterTypeListNode(BaseNode):
	def __init__(self, previous_declarations, next_declaration):
		self.previous_declarations = previous_declarations
		self.next_declaration = next_declaration


	def generate_code(self):
		self.previous_declarations.generate_code()
		print_code(", ")
		self.next_declaration.generate_code()


class ParameterDeclarationNode(BaseNode):
	def __init__(self, data_type, declarator):
		self.data_type = data_type
		self.declarator = declarator


	def add_into_table(self, table):
		pos = self.declarator
		array_size = list()
		while isinstance(pos, DeclaratorArrayNode):
			array_size.append(pos.constant_expression.value)
			pos = pos.declarator
		array_size.reverse()
		name = pos.item
		pos.item = table.insert(name, self.data_type, array_size)


	def generate_code(self):
		pos = self.declarator
		while isinstance(pos, DeclaratorArrayNode):
			pos = pos.declarator
		print_code(pos.item['actual_name'])


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

	def generate_code(self):
		if self.declaration_list is not None:
			self.declaration_list.generate_code()
		if self.statement_list is not None:
			self.statement_list.generate_code()

		if self.declaration_list is None and self.statement_list is None:
			print_code(' ' * indent)
			print_code('pass\n')


class StatementListNode(BaseNode):
	def __init__(self, previous_statements, next_statement):
		self.previous_statements = previous_statements
		self.next_statement = next_statement

	def generate_code(self):
		self.previous_statements.generate_code()
		self.next_statement.generate_code()


class ExpressionStatementNode(BaseNode):
	def __init__(self, expression):
		self.expression = expression

	def generate_code(self):
		self.expression.generate_code()


class SelectionStatementNode(BaseNode):
	def __init__(self, condition, true_statement, false_statement):
		self.condition = condition
		self.true_statement = true_statement
		self.false_statement = false_statement

	def generate_code(self):
		global indent
		if self.condition.is_leaf() == False:
			temp_cond = self.condition.generate_code()
		print_code(' ' * indent)
		print_code('if ')
		if self.condition.is_leaf():
			self.condition.generate_code()
		else:
			print_code(temp_cond)
		print_code(':\n')
		indent += 4
		self.true_statement.generate_code()
		indent -= 4
		if self.false_statement is not None:
			print_code(' ' * indent)
			print_code('else:\n')
			indent += 4
			self.false_statement.generate_code()
			indent -= 4
		


class IterationStatementNode(BaseNode):
	def __init__(self, condition, statement):
		self.condition = condition
		self.statement = statement

	def generate_code(self):
		global indent
		print_code(' ' * indent)
		print_code('while ')
		if self.condition.is_leaf():
			self.condition.generate_code()
		else:
			print_code('True')
		print_code(':\n')
		indent += 4
		if self.condition.is_leaf() == False:
			temp_cond = self.condition.generate_code()
			print_code(' ' * indent)
			print_code('if !%s:\n' % temp_cond)
			print_code(' ' * (indent + 4))
			print_code('break\n')
		self.statement.generate_code()
		indent -= 4


class JumpStatementNode(BaseNode):
	def __init__(self, jump_type, expression):
		self.jump_type = jump_type
		self.expression = expression

	def generate_code(self):
		if self.jump_type == 'continue' or self.jump_type == 'break':
			print_code(' ' * indent)
			print_code(self.jump_type)
			print_code('\n')
		elif self.jump_type == 'return':
			if self.expression is None:
				print_code(' ' * indent)
				print_code("return\n")
			else:
				if self.expression.is_leaf():
					print_code(' ' * indent)
					print_code("return ")
					self.expression.generate_code()
					print_code("\n")
				else:
					ret_val = self.expression.generate_code()
					print_code(' ' * indent)
					print_code("return %s\n" % ret_val)


class TranslationUnitNode(BaseNode):
	def __init__(self, previous_units, next_unit):
		self.previous_units = previous_units
		self.next_unit = next_unit

	def generate_code(self):
		self.previous_units.generate_code()
		self.next_unit.generate_code()


class FunctionDefinition(BaseNode):
	def __init__(self, return_type, declarator, statements):
		self.return_type = return_type
		self.declarator = declarator
		self.statements = statements

	def generate_code(self):
		global indent
		print_code("def ")
		self.declarator.generate_code()
		print_code(":\n")
		indent += 4
		self.statements.generate_code()
		print_code("\n")
		indent -= 4
