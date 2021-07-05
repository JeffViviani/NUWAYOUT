import sys
sys.path.insert(1, 'modules/')
import pygame
import config

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
	ref_tile_x = tile_x_topleft
	ref_tile_y = tile_y_topleft
	frame = pygame.Rect(0, 0, 20, 20)
	print_row = 0
	print_col = 0
	while print_row < PRINT_HEIGHT:
		print("print_row: " + str(print_row))
		frame.left = 0
		print_col = 0
		while print_col < PRINT_WIDTH:
			if ref_tile_x < 0 or ref_tile_y < 0 or ref_tile_y >= len(map) or ref_tile_x >= len(map[ref_tile_y]):
				tile_to_blit = 3
			else:
				tile_to_blit = map[ref_tile_y][ref_tile_x]
			screen.blit(tile_surfaces[tile_to_blit], frame)
			frame.left += 20
			print_col += 1
		frame.top += 20
		print_row += 1
	print("END")

print("WELCOME TO NUWAYOUT MAP MAKER!")
response = input("Load existing map (Y) or create new one? (N)")
if response == 'Y':
	#Load existing map
	sys.exit()
elif response != 'N':
	sys.exit()
else:
	#Create new map
	map = [[]] #Blank map currently
	#MAP VALUES
	# Map tile values are 3 digits each. This means the game can have up to 999
	# distinct tiles! There is no delimited between the tiles in the same row.
	# However, a newline will be a delimiter between the rows themselves.
	
screen = pygame.display.set_mode((576, 432), 0, config.BIT_RESOLUTION)
tile_x_topleft = 0
tile_y_topleft = 0

while True:
	render_full()
	clock.tick(60)
	pygame.display.flip()