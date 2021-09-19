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
	digits_accumulated = 0
	last_width = 0
	width = 0
	height = 0
	lst = []
	stnd = True
	raw_file = open(file, mode='r')
	digits = [None] * 3
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
			digits[digits_accumulated] = c
			digits_accumulated += 1
			if digits_accumulated == 3:
				digit_str = digits[0] + digits[1] + digits[2]
				stnd = True
				width = width + 1
				lst.append(int(digit_str))
				digits_accumulated = 0
	return (lst, last_width, height)

def file_to_1D_list(file):
	lst = []
	item = ""
	raw_file = open(file, mode='r')
	while True:
		c = raw_file.read(1)
		if c == '':
			if item != '':
				lst.append(int(item))
				item = ""
			break
		elif c == '\n':
			lst.append(int(item))
			item = ""
		elif c != '\r':
			item = item + str(c)
	return lst

#Takes an any-dimensional list and replaces all instances of values where func(value) returns True with 'value'. All other values are
#changed to 'ow'.
#
# func is a function to be passed to this function.
def list_consolidate(lst, func, value, ow):
	for item in range(len(lst)):
		if isinstance(lst[item], list):
			list_consolidate(lst[item], target, value, ow)
		elif isinstance(item, int):
			if func(lst[item]):
				lst[item] = value
			else:
				lst[item] = ow