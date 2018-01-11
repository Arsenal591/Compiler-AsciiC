import cparser
import sys
import ast_node
import os

if __name__ == '__main__':
	file = open(sys.argv[1], 'r')
	ast_node.output_file = open(sys.argv[2], 'w')

	data = file.read(8192)
	file.close()
	cparser.generate_code(data)
	ast_node.output_file.close()

	if len(sys.argv) > 3 and sys.argv[3] == 'run':
		os.system('python %s' % sys.argv[2])
