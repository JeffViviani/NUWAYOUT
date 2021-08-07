import sys
sys.path.insert(1, 'modules/')
import pygame
import config
import math

PRINT_WIDTH = 29
PRINT_HEIGHT = 23

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

#Load all tiles into array
tile_surfaces = []
tile_surfaces.append(pygame.image.load("Images/Tiles/tile0.png"))
tile_surfaces.append(pygame.image.load("Images/Tiles/tile1.png"))
tile_surfaces.append(pygame.image.load("Images/Tiles/tile2.png"))
tile_surfaces.append(pygame.image.load("Images/Tiles/tile3.png"))

displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
screen_height = displayInfo.current_h

screen = None

######################################
########## FUNCTIONS #################
######################################
def render_full():
	global screen, tile_x_topleft, tile_y_topleft
	ref_tile_y = tile_y_topleft
	frame = pygame.Rect(0, 0, 20, 20)
	print_row = 0
	print_col = 0
	while print_row < PRINT_HEIGHT:
		frame.left = 0
		print_col = 0
		ref_tile_x = tile_x_topleft
		while print_col < PRINT_WIDTH:
			if ref_tile_x < 0 or ref_tile_y < 0 or ref_tile_y >= len(map) or ref_tile_x >= len(map[ref_tile_y]):
				tile_to_blit = 3
			else:
				tile_to_blit = int(map[ref_tile_y][ref_tile_x])
			screen.blit(tile_surfaces[tile_to_blit], frame)
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
				arr[len(arr) - 1].append(3)
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
				arr[0].append(3)
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
				arr[cnt].append(3)
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
				arr[cnt].insert(0,3)
				fill_cnt += 1
			cnt += 1
		map_width = map_width - lvl_two
		tile_x_topleft -= lvl_two
		lvl_two = 0
		
	arr[lvl_one][lvl_two] = data
		
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
		

print("WELCOME TO NUWAYOUT MAP MAKER!")
response = input("Load existing map (Y) or create new one? (N)")
if response == 'Y':
	#Load existing map
	sys.exit()
elif response != 'N':
	sys.exit()
else:
	#Create new map
	map = [] #Blank map currently
	#MAP VALUES
	# Map tile values are 3 digits each. This means the game can have up to 999
	# distinct tiles! There is no delimiter between the tiles in the same row.
	# However, a newline will be a delimiter between the rows themselves.
	
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

mouse_right_down = False

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
			mouse_right_down = True
			current_tile += 1
			if current_tile == 4:
				current_tile = 0
	else:
		mouse_right_down = False
		
	keys = pygame.key.get_pressed()
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
				
	#Render current background
	render_full()

	current_tile_frame.left = x_pos_on_screen * 20
	current_tile_frame.top = y_pos_on_screen * 20
	screen.blit(tile_surfaces[current_tile], current_tile_frame)
	clock.tick_busy_loop(60)
	pygame.display.flip()