import sys
import os
sys.path.insert(1, 'modules/')
import pygame
import config
import math

SET_1 = None;
SET_2 = None;
SET_3 = None;
SET_4 = None;

PRINT_WIDTH = 29
PRINT_HEIGHT = 23

BLACK_TILE = 250

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

######################################
############# GLOBALS ################
######################################
tile_x_topleft = None
tile_y_topleft = None

map_width = 0
map_height = 0

map = None

cnt_alt = 30
alt_state = False

#Load all tiles into array
tile_surfaces = [None] * 999

robot_surfaces = [None] * 3

robot_surfaces[0] = pygame.image.load("Images/Robots/blue_front.png")
robot_surfaces[1] = pygame.image.load("Images/Robots/orange_front.png")
robot_surfaces[2] = pygame.image.load("Images/Robots/red_front.png")

#Load personality indicator dots
personality_dots = [None] * 6
personality_dots[0] = pygame.image.load("Images/Robots/Personality_Dots/0.png")
personality_dots[1] = pygame.image.load("Images/Robots/Personality_Dots/1.png")
personality_dots[2] = pygame.image.load("Images/Robots/Personality_Dots/2.png")
personality_dots[3] = pygame.image.load("Images/Robots/Personality_Dots/3.png")
personality_dots[4] = pygame.image.load("Images/Robots/Personality_Dots/4.png")
personality_dots[5] = pygame.image.load("Images/Robots/Personality_Dots/5.png")

displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
screen_height = displayInfo.current_h

screen = None

file_world_obj_path = None
file_robots_obj_path = None
file_world_obj = None
file_robots_obj = None

#This is a pointer to the data for YOU the player. If a robot is chosen as the
#player robot, then it is the one who you get to control. If it is changed later
#on, this needs to be noted by changing the previously set player's robot to no
#longer be the player robot. This pointer is helpful for that.
player_data = None

def file_roll_call(start_index):
	global tile_surfaces

	tile_index = start_index
	while os.path.isfile("Images/Tiles/" + str(tile_index) + ".png"):
		print("FILE FOUND! INDEX " + str(tile_index))
		tile_surfaces[tile_index] = pygame.image.load("Images/Tiles/" + str(tile_index) + ".png")
		tile_index += 1
	tile_index -= 1
	return tile_index
	

def load_tiles():
	global tile_surfaces, SET_1, SET_2, SET_3, SET_4
	tile_index = None
	
	# First determine the number of tiles of each category.
	SET_1 = file_roll_call(0)
	SET_2 = file_roll_call(250)
	SET_3  = file_roll_call(500)
	SET_4  = file_roll_call(750)

######################################
########## FUNCTIONS #################
######################################
def render_full():
	global screen, tile_x_topleft, tile_y_topleft, map
	ref_tile_y = tile_y_topleft
	frame = pygame.Rect(0, 0, 20, 20)
	print_row = 0
	print_col = 0
	while print_row < PRINT_HEIGHT:
		frame.left = 0
		print_col = 0
		ref_tile_x = tile_x_topleft
		while print_col < PRINT_WIDTH:
			robot_to_blit = None
			personality_to_blit = None
			if ref_tile_x < 0 or ref_tile_y < 0 or ref_tile_y >= len(map) or ref_tile_x >= len(map[ref_tile_y]):
				tile_to_blit = BLACK_TILE
			else:
				dat = map[ref_tile_y][ref_tile_x]
				tile_to_blit = int(dat[0])
				if tile_to_blit >= 500:
					if alt_state:
						tile_to_blit += 1
				robot_to_blit = dat[1]
				personality_to_blit = dat[2]
			
			screen.blit(tile_surfaces[tile_to_blit], frame)
			if robot_to_blit != None:
				screen.blit(robot_surfaces[robot_to_blit], frame)
				screen.blit(personality_dots[personality_to_blit], frame)
			frame.left += 20
			print_col += 1
			ref_tile_x += 1
		frame.top += 20
		print_row += 1
		ref_tile_y += 1
	
def plot(arr, screen_x, screen_y, data):
	global map_height, map_width, tile_x_topleft, tile_y_topleft
	lvl_one = screen_y + tile_y_topleft
	lvl_two = screen_x + tile_x_topleft
	if lvl_one >= map_height:
		cnt = 0
		cnt_max = lvl_one + 1 - map_height
		while cnt < cnt_max:
			arr.append([])
			fill_cnt = 0
			while fill_cnt < map_width:
				arr[len(arr) - 1].append([BLACK_TILE, None, None, None])
				fill_cnt += 1
			cnt += 1
		map_height = lvl_one + 1
	elif lvl_one < 0:
		cnt = 0
		cnt_max = 0 - lvl_one
		while cnt < cnt_max:
			arr.insert(0,[])
			fill_cnt = 0
			while fill_cnt < map_width:
				arr[0].append([BLACK_TILE, None, None, None])
				fill_cnt += 1
			cnt += 1
		map_height = len(arr)
		tile_y_topleft -= lvl_one
		lvl_one = 0
		
	if lvl_two >= map_width:
		cnt = 0
		cnt_max = map_height
		fill_cnt_max = lvl_two + 1 - map_width
		while cnt < cnt_max:
			fill_cnt = 0
			while fill_cnt < fill_cnt_max:
				arr[cnt].append([BLACK_TILE, None, None, None])
				fill_cnt += 1
			cnt += 1
		map_width = lvl_two + 1
	elif lvl_two < 0:
		cnt = 0
		cnt_max = map_height
		fill_cnt_max = 0 - lvl_two
		while cnt < cnt_max:
			fill_cnt = 0
			while fill_cnt < fill_cnt_max:
				arr[cnt].insert(0,[BLACK_TILE, None, None, None])
				fill_cnt += 1
			cnt += 1
		map_width = map_width - lvl_two
		tile_x_topleft -= lvl_two
		lvl_two = 0
		
	arr[lvl_one][lvl_two] = [data, None, None, None]
		
def plot_area(arr, screen_x_1, screen_y_1, screen_x_2, screen_y_2, data):
	cnt_y_max = abs(screen_y_1 - screen_y_2)
	cnt_y = 0
	y = screen_y_1
	adj_y = None
	if screen_y_1 > screen_y_2:
		adj_y = -1
	else:
		adj_y = 1
	cnt_x_max = abs(screen_x_1 - screen_x_2)
	adj_x = None
	if screen_x_1 > screen_x_2:
		adj_x = -1
	else:
		adj_x = 1
	
	while cnt_y <= cnt_y_max:
		cnt_x = 0
		x = screen_x_1
		while cnt_x <= cnt_x_max:
			plot(arr, x, y, data)
			x += adj_x
			cnt_x += 1
		y += adj_y
		cnt_y += 1
		
def int_to_3digit_str(num):
	if num == 0:
		return "000"
	num_str = str(num)
	if len(num_str) < 3:
		cnt = 0
		cnt_max = 3 - len(num_str)
		while cnt < cnt_max:
			num_str = '0' + num_str
			cnt += 1
	elif len(num_str) > 3:
		num_str = num_str[0:3]
	return num_str

#Save the map to a text file. 3 digits per tile. Newline to new row. Robots are
#Saved to their own separate file.
def save():
	global file_world_obj_path, file_robots_obj_path
	file_world = open(file_world_obj_path, 'w')
	file_robots = open(file_robots_obj_path, 'w')
	cnt_y = 0
	length = 0
	while cnt_y < map_height:
		cnt_x = 0
		while cnt_x < map_width:
			tile_string = int_to_3digit_str(map[cnt_y][cnt_x][0])
			file_world.write(tile_string)
			if map[cnt_y][cnt_x][1] != None: # If a robot is on this tile
				if map[cnt_y][cnt_x][3] == 1:
					file_robots.seek(0,0)
				file_robots.write(str(map[cnt_y][cnt_x][1])) #type
				file_robots.write('\n')
				file_robots.write(str(map[cnt_y][cnt_x][2])) #personality
				file_robots.write('\n')
				file_robots.write(str(cnt_x)) # x pos
				file_robots.write('\n')
				file_robots.write(str(cnt_y)) # y pos
				file_robots.write('\n')
				file_robots.seek(0,2)
				length += 8
			cnt_x += 1
		if cnt_y != map_height - 1:
			file_world.write('\n')
		cnt_y += 1
	file_world.close()
	if file_robots.tell() > 0:
		file_robots.seek(length - 2,0)
		#file_robots.truncate()
	file_robots.close()
	
def load():
	global map, file_world_obj_path, file_robots_obj_path, map_height, map_width
	#Load world first then robots
	file_world_obj = open(file_world_obj_path,'r')
	file_robots_obj = open(file_robots_obj_path,'r')
	file_world_obj.seek(0)
	digits_read = 0
	digits = [None] * 3
	height = 1
	map = [[]]
	while True:
		c = file_world_obj.read(1)
		if c == '':
			#End of file
			break
		elif c == '\n':
			#New line.
			map.append([])
			height += 1
		else:
			digits[digits_read] = c
			digits_read += 1
			if digits_read == 3:
				num_str = digits[0] + digits[1] + digits[2]
				map[height - 1].append([int(num_str), None, None, None])
				digits_read = 0
	file_world_obj.close()
	map_height = len(map)
	map_width = len(map[0])
	print("map_height: " + str(map_height))
	print("map width: " + str(map_width))
	
	#Load the robots
	file_robots_obj.seek(0)
	num_str = ""
	num_items = 0
	items = [None] * 4
	while True:
		c = file_robots_obj.read(1)
		if c == '':
			break
		elif c == '\n':
			items[num_items] = int(num_str)
			num_items += 1
			if num_items == 4:
				data_lst = map[items[3]][items[2]] # List pos of robot
				data_lst[1] = items[0] #type
				data_lst[2] = items[1] #personality
				num_items = 0
			num_str = ""
		else:
			num_str = num_str + c
	file_robots_obj.close()
		
def plot_robot(arr, screen_x, screen_y, type):
	lvl_one = screen_y + tile_y_topleft
	lvl_two = screen_x + tile_x_topleft
	if lvl_two > 0 and lvl_two < map_width and lvl_one > 0 and lvl_one < map_height:
		tmp = map[lvl_one][lvl_two][0]
		if tmp < 250 or (tmp >= 500 and tmp < 750):
			current_robot = map[lvl_one][lvl_two][1]
			if current_robot == None:
				map[lvl_one][lvl_two][1] = 0
				map[lvl_one][lvl_two][2] = 0
			elif current_robot == 1:
				map[lvl_one][lvl_two][1] = None
			else:
				current_robot += 1
				map[lvl_one][lvl_two][1] = current_robot
				
def change_personality(arr, screen_x, screen_y, type):
	lvl_one = screen_y + tile_y_topleft
	lvl_two = screen_x + tile_x_topleft
	if lvl_two > 0 and lvl_two < map_width and lvl_one > 0 and lvl_one < map_height:
		if map[lvl_one][lvl_two][1] != None:
			current_personality = map[lvl_one][lvl_two][2] = type
			
def set_player_robot(arr, screen_x, screen_y):
	global player_data
	lvl_one = screen_y + tile_y_topleft
	lvl_two = screen_x + tile_x_topleft
	if lvl_two > 0 and lvl_two < map_width and lvl_one > 0 and lvl_one < map_height:
		if map[lvl_one][lvl_two][1] == 0:
			if player_data != None:
				map[lvl_one][lvl_two][3] = None
			player_data = map[lvl_one][lvl_two]
			player_data[3] = 1
			
def next_tile():
	global current_tile, SET_1, SET_2, SET_3, SET_4
	if current_tile == SET_1:
		if SET_2 >= 250:
			current_tile = 250
			return
		else:
			current_tile = SET_2
	if current_tile == SET_2:
		if SET_3 >= 500:
			current_tile = 500
			return
		else:
			current_tile = SET_3 - 1
	if current_tile == SET_3 - 1:
		if SET_4 >= 750:
			current_tile = 750
			return
		else:
			current_tile = SET_4 - 1
	if current_tile == SET_4 - 1:
		current_tile = 0
		return
	if current_tile < 500:
		current_tile += 1
	else:
		current_tile += 2
		
def prev_tile():
	global current_tile, SET_1, SET_2, SET_3, SET_4
	
	if current_tile == 0:
		if SET_4 >= 750:
			current_tile = SET_4 - 1
		elif SET_3 >= 500:
			current_tile = SET_3 - 1
		elif SET_2 >= 250:
			current_tile = SET_2 - 1
		else:
			current_tile = SET_1
		return
	
	if current_tile == 250:
		current_tile = SET_1
		return
		
	if current_tile == 500:
		if SET_2 >= 250:
			current_tile = SET_2 - 1
		else:
			current_tile = SET_1
		return
		
	if current_tile == 750:
		if SET_3 >= 500:
			current_tile = SET_3
		elif SET_2 >= 250:
			current_tile = SET_2 - 1
		else:
			current_tile = SET_1
		return
	
	if current_tile < 500:
		current_tile -= 1
	else:
		current_tile -= 2
		

print("WELCOME TO NUWAYOUT MAP MAKER!")
response = input("Load existing map (Y) or create new one? (N)")
if response == 'Y':
	file_world_obj_path = input("Enter path to world file:\n")
	file_robots_obj_path = input("Enter path to robots file:\n")
	load_tiles()
	load()
elif response != 'N':
	sys.exit()
else:
	#MAP VALUES
	# Map tile values are 3 digits each. This means the game can have up to 999
	# distinct tiles! There is no delimiter between the tiles in the same row.
	# However, a newline will be a delimiter between the rows themselves.
	file_world_obj_path = input("Enter path to NEW world file:\n")
	file_robots_obj_path = input("Enter path to NEW robots file:\n")
	
	load_tiles()
	#Create new map
	map = [] #Blank map currently
	
screen = pygame.display.set_mode((576, 432), 0, config.BIT_RESOLUTION)
tile_x_topleft = 0
tile_y_topleft = 0

# The current tile selected that is following the mouse pointer. If the mouse
# is clicked, this tile will be placed down. Left and right arrow keys can be used
# to switch among the tiles.
current_tile = 0
current_tile_frame = pygame.Rect(0, 0, 20, 20)

area_fill_x1 = None
area_fill_y1 = None

display_follower = 1

mouse_right_down = False
key_r_down = True
key_h_down = True
key_0_down = True
key_right_down = True
key_left_down = True

cycle_delay = 20


while True:
	#Display the follower tile by the mouse pointer
	mouse_pos = pygame.mouse.get_pos()
	x_pos_on_screen = math.floor((mouse_pos[0]) / 20)
	y_pos_on_screen = math.floor((mouse_pos[1]) / 20)

	#Be able to quit with escape key
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.display.quit()
				pygame.quit()
				sys.exit()
				
	mouse_status = pygame.mouse.get_pressed()
	if mouse_status[0] == True:
		plot(map, x_pos_on_screen, y_pos_on_screen, current_tile)
		area_fill_x1 = None
		area_fill_y1 = None
	if mouse_status[1] == True:
		if not mouse_middle_down:
			mouse_middle_down = True
			if area_fill_x1 == None:
				area_fill_x1 = x_pos_on_screen
				area_fill_y1 = y_pos_on_screen
			else:
				plot_area(map, area_fill_x1, area_fill_y1, x_pos_on_screen, y_pos_on_screen, current_tile)
				area_fill_x1 = None
				area_fill_y1 = None
	else:
		mouse_middle_down = False
	if mouse_status[2] == True:
		if not mouse_right_down:
			cycle_delay = 15
			next_tile()
		elif cycle_delay == 0:
			cycle_delay = 5
			next_tile()
		mouse_right_down = True
	else:
		mouse_right_down = False
		
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_RIGHT]:
		if not key_right_down:
			cycle_delay = 15
			next_tile()
		elif cycle_delay == 0:
			cycle_delay = 5
			next_tile()
		key_right_down = True
	else:
		key_right_down = False
		
	if keys[pygame.K_LEFT]:
		if not key_left_down:
			cycle_delay = 15
			prev_tile()
		elif cycle_delay == 0:
			cycle_delay = 5
			prev_tile()
		key_left_down = True
	else:
		key_left_down = False
		
	if keys[pygame.K_d]:
		tile_x_topleft += 1
		if area_fill_x1 != None:
			area_fill_x1 -= 1
	elif keys[pygame.K_a]:
		tile_x_topleft -= 1
		if area_fill_x1 != None:
			area_fill_x1 += 1
	elif keys[pygame.K_w]:
		tile_y_topleft -= 1
		if area_fill_y1 != None:
			area_fill_y1 += 1
	elif keys[pygame.K_s]:
		tile_y_topleft += 1
		if area_fill_y1 != None:
			area_fill_y1 -= 1
	if keys[pygame.K_r]:
		if not key_r_down:
			plot_robot(map, x_pos_on_screen, y_pos_on_screen, 0)
		key_r_down = True
	else:
		key_r_down = False
		
	if keys[pygame.K_h]:
		if not key_h_down:
			display_follower = 0 - display_follower
		key_h_down = True
	else:
		key_h_down = False
		
	if keys[pygame.K_1]:
		change_personality(map, x_pos_on_screen, y_pos_on_screen, 0)
	elif keys[pygame.K_2]:
		change_personality(map, x_pos_on_screen, y_pos_on_screen, 1)
	elif keys[pygame.K_3]:
		change_personality(map, x_pos_on_screen, y_pos_on_screen, 2)
	elif keys[pygame.K_4]:
		change_personality(map, x_pos_on_screen, y_pos_on_screen, 3)
	elif keys[pygame.K_5]:
		change_personality(map, x_pos_on_screen, y_pos_on_screen, 4)
	elif keys[pygame.K_6]:
		change_personality(map, x_pos_on_screen, y_pos_on_screen, 5)
		
	#0 Key will save the map to the files
	if keys[pygame.K_0]:
		if not key_0_down:
			save()
		key_0_down = True
	else:
		key_0_down = False
		
	if cycle_delay > 0:
		cycle_delay -= 1
		
	#P Key will set the robot the mouse is on to be the player's robot
	if keys[pygame.K_p]:
		set_player_robot(map, x_pos_on_screen, y_pos_on_screen)
		
	#Variables for alternating tiles
	if cnt_alt == 0:
		alt_state = not alt_state
		cnt_alt = 30
	else:
		cnt_alt -= 1
				
	#Render current background
	render_full()

	current_tile_frame.left = x_pos_on_screen * 20
	current_tile_frame.top = y_pos_on_screen * 20
	if display_follower == 1:
		
		screen.blit(tile_surfaces[current_tile], current_tile_frame)
	clock.tick_busy_loop(60)
	pygame.display.flip()