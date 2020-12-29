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

def file_to_1D_list(file):
	lst = []
	item = ""
	while True:
		c = raw_file.read(1)
		if c == '':
			lst.append(sub_lst)
			item = ""
			break
		elif c == '\n':
			lst.append(int(item))
			item = ""
		elif c != '\r':
			item = item + char(c)
	return lst