print("WELCOME! This will allow you to compile a robot list from those robots encoded into a world file. Please enter the name of the file:\n")
file_to_open = input()
file_out = open("ROBOT_OUTPUT.txt", 'w')
file_in = open(file_to_open, 'r')

last_width = 0
x = 0
y = 0
stnd = True
while True:
	c = file_in.read(1)
	if c == '':
		break;
	elif c == '\r' or c == '\n':
		if stnd == True:
			y = y + 1
			x = 0
			stnd = False
	elif c != '\n' and c != '\r':
		stnd = True
		x = x + 1
		if c == 'X':
			file_out.write("2\n")
			file_out.write("0\n")
			file_out.write(str(x) + '\n')
			file_out.write(str(y) + '\n')

file_out.close()
file_in.close()