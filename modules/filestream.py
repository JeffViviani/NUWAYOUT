def file_to_2D_list(file):
	lst = []
	sub_lst = []
	raw_file = open(file, mode='r')
	while True:
		c = raw_file.read(1)
		if c == '':
			lst.append(sub_lst)
			break
		elif c == '\n':
			lst.append(sub_lst)
			sub_lst = []
		elif c != '\r':
			sub_lst.append(int(c))
	return lst
	
def file_to_fake_2D_list_ints(file):
	last_width = 0
	width = 0
	height = 0
	lst = []
	stnd = True
	raw_file = open(file, mode='r')
	while True:
		c = raw_file.read(1)
		if c == '':
			break;
		elif c == '\r' or c == '\n':
			if stnd == True:
				last_width = width
				width = 0
				height = height + 1
				stnd = False
		elif c != '\n' and c != '\r':
			if not str.isdigit(c):
				c = '1'
			stnd = True
			width = width + 1
			lst.append(int(c))
	return (lst, last_width, height)

def file_to_1D_list(file):
	lst = []
	item = ""
	raw_file = open(file, mode='r')
	while True:
		c = raw_file.read(1)
		if c == '':
			lst.append(int(item))
			item = ""
			break
		elif c == '\n':
			lst.append(int(item))
			item = ""
		elif c != '\r':
			item = item + str(c)
	return lst

#Takes an any-dimensional list and replaces all instances of 'target' with 'value'. All other values are
#changed to 'ow'.
def list_consolidate(lst, target, value, ow):
	for item in range(len(lst)):
		if isinstance(lst[item], list):
			list_consolidate(lst[item], target, value, ow)
		elif isinstance(item, int):
			if lst[item] == target:
				lst[item] = value
			else:
				lst[item] = ow