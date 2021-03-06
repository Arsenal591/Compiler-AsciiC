
class SymbolTable(object):
	def __init__(self):
		self.items = {}

	def insert(self, name, actual_name, data_type, array_size=None):
		new_item = {
			'actual_name': actual_name,
			'data_type': data_type,
			'array_size': array_size,
		}
		self.items[name] = new_item
		return new_item

	def get_item(self, name):
		return self.items.get(name)


class SymbolTableChain(object):
	def __init__(self):
		self.depth = 0
		self.tables = list()
		self.tables.append(SymbolTable())

	@property
	def current_table(self):
		return self.tables[-1]

	def push_chain(self):
		self.depth += 1
		new_table = SymbolTable()
		for key in self.current_table.items.keys():
			new_table.items[key] = self.current_table.items[key]
		self.tables.append(new_table)

	def pop_chain(self):
		self.depth -= 1
		if self.depth < 0:
			raise ValueError('Scope depth cannot be negative.')
		self.tables.pop()

	def insert(self, name, data_type, array_size=None):
		#actual_name = "chain_%d_%s" % (self.depth, self.name) 
		actual_name = name
		if array_size is None:
			array_size = list()
		if data_type in ['int', 'long', 'short']:
			data_type = 'int'
		elif data_type in ['float', 'double']:
			data_type = 'float'
		return self.current_table.insert(name, actual_name, data_type, array_size)

	def get_item(self, name):
		return self.current_table.get_item(name)


class FunctionTable(object):
	def __init__(self):
		self.items = {}

	def insert(self, name, return_type, param_type_list):
		new_item = {
			'return_type' : return_type,
			'param_type_list' : param_type_list,
			'actual_name' : name,
		}
		self.items[name] = new_item
		return new_item

	def get_item(self, name):
		return self.items.get(name)
		
		