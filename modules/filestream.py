def file_to_list(file):
	lst = []
	sub_lst = []
	raw_file = open(file, mode='r', errors='strict')
	eof = False
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
