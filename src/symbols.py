
class SymbolTable(object):
	def __init__(self):
		self.items = {}

	def insert(name, actual_name, data_type, bias=None):
		new_item = (actual_name, data_type, bias)
		self.items[name] = new_item

	def get_item(name):
		return getattr(self.items, name, None)


class SymbolTableChain(self):
	def __init__(self):
		self.depth = 0
		self.tables = list()
		self.tables.append(SymbolTable())

	@property
	def current_table(self):
		return self.tables[-1]

	def push_chain(self):
		self.depth += 1
		self.tables.append(SymbolTable())

	def pop_chain(self):
		self.depth -= 1
		if self.depth < 0:
			raise ValueError('Scope depth cannot be negative.')
		self.tables.pop()

	def insert(name, data_type, bias=None):
		actual_name = "chain_%d_%s" % (self.depth, self.name) 
		self.current_table.insert(name, actual_name, data_type, bias)

	def get_item(name):
		return self.current_table.get_item(name)