
# ABOVE LINE LEFT BLANK INTENTIONALLY
################################################################################
# FILE: exec.py
# DESCRIPTION: The main runtime file for NUWAYOUT. Run this file from the
# command line to run the game.
################################################################################

import sys
sys.path.insert(1, 'modules/')

import pygame
import config
from filestream import *
from world import *
from robot import *
from laser import *
from pagetable import *
from typewriter import *
from math import floor


################################################################################
#################################  FUNCTIONS  ##################################
################################################################################

# NAME: load_robots
# DESCRIPTION: Loads all of the robots from a text file 'file' into the world
#   'world' and PageTable 'pagetable'.
# REQUIREMENTS: 'world' must be an object of type World. 'pagetable' must be an
#   object of type PageTable. 'file' must be a string that represents the file
#   location of a text file. The text file must be formatted in a specific
#   manner. The text file must consist of blocks of data. A block of data is
#   three integers. These integers must be separated by Crlf. One block
#   represents a single robot's spawn information. It is arranged as such:
#
#   type
#   personality
#   tile_x
#   tile_y
#
#   Where 'type' is the type of robot, and 'tile_x' and 'tile_y' are its spawn
#   coordinates. For example, considering a text file as so:
#
#   0
#   10
#   10
#   1
#   120
#   77
#
#   The above text file would generate two robots. One of type "0" at coordinate
#   (10, 10), and the other of type '1' at coordinate (120, 77).
#
# ALTERS: Both 'world' and 'pagetable' are altered. 'world.occupancy' is updated
#   to include the new robots. 'pagetable' is updated to include the new robots
#   in its pages.
# RETURNS: Returns the first Robot from the text file.
def load_robots(world, pagetable, file):
	robot_list = file_to_1D_list(file)
	num_items = len(robot_list)
	item = 0
	first = 0
	new_robot = None
	firstRef = None
	while item < num_items:
		if robot_list[item] == 99:
			#Load coin
			world.occupancy[world.bgnd_tiles_width * robot_list[item + 3] + robot_list[item + 2]] = 8
		else:
			#Load robot
			new_robot = Robot(world, pagetable, robot_list[item], robot_list[item + 1], robot_list[item + 2], robot_list[item + 3])
		item = item + 4
		if first == 0 and new_robot != None:
			first = 1
			firstRef = new_robot
	return firstRef

# NAME: render_page
# DESCRIPTION: Renders all of the Robots from the page inside the 'pagetable'
#   specified by 'page_row' and 'page_col' to the screen.
# REQUIREMENTS: 'pagetable' must be an object of type PageTable. 'page_row' and
#   'page_col' must be integers. All objects inside of the page must be Robot
#   objects.
# ALTERS: Nothing
# RETURNS: Nothing
def render_page(pagetable, page_row, page_col):
	try:
		for robot in pagetable.get_page(page_row, page_col):
			robot.render()
		return
	except TypeError:
		return

# NAME: process_page
# DESCRIPTION: Runs method 'automated_control()' on every Robot inside the
# 'pagetable' specified by 'page_row' and 'page_col'.
# REQUIREMENTS: 'pagetable' must be an object of type PageTable. 'page_row' and
#   'page_col' must be integers. All objects inside of the page must be Robot
#   objects.
# ALTERS: 'pagetable' may be altered by the Robot 'automated_control()' method.
# RETURNS: Nothing
def process_page(pagetable, page_row, page_col):
	try:
		for robot in pagetable.get_page(page_row, page_col):
			robot.automated_control()
		return
	except TypeError:
		return
		

################################################################################
#############################  INITIALIZATION ##################################
################################################################################


#Initialize pygame and the display
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
screen_height = displayInfo.current_h

screen = None
if config.FULLSCREEN:
	screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF, config.BIT_RESOLUTION)
else:
	screen = pygame.display.set_mode((576, 432), 0, config.BIT_RESOLUTION)

#Load the main menu world
world = World(screen)
world.load_world("data/world0.txt")

#Initialize the World class
World.init_class()

#Initialize Robot class
Robot.init_class(world)

#Initialize Laser class
Laser.init_class(world)

#Initialize Typewriter class and instantiate object
Typewriter.init_class(world)
typewriter = Typewriter(world)

#Initialize checkered surface for blit upon the transition from the
#main menu to the cutscene. This is to be the same size as the screen.
checker_width = int(floor(144 * world.scale_x))
checker_height = int(floor(144 * world.scale_y))
checker = pygame.Surface((checker_width, checker_height))
checker.fill((0,0,0))
displayInfo = pygame.display.Info()
checker_s = screen.copy()
checker_s.fill((255, 255, 255))

#Create page table instance
pagetable = PageTable()
pagetable.load_blank(world)

#Initialize the camera
world.camera_x = 0
world.camera_y = 0

#Initialize Title of Game
title_surface = world.scale(pygame.image.load("Images/HUD/title.png"))
title_frame = (60 * world.scale_x, 100 * world.scale_y)

#Initialize the "Press Button" blinking boxes for the menus
press_btn_box_surface = world.scale(pygame.image.load("Images/HUD/pressButton.png"))
press_btn_box_frame = (int(floor(200 * world.scale_x)), int(floor(200 * world.scale_y)))

press_btn2_box_surface = world.scale(pygame.image.load("Images/HUD/pressButton2.png"))
press_btn2_fill_black = press_btn2_box_surface.copy()
press_btn2_fill_black.fill((0,0,0))
press_btn2_box_frame = (int(floor(140 * world.scale_x)), int(floor(310 * world.scale_y)))

#Initialize health bar

health_bar_outer_top = int(floor(5 * world.scale_y))
health_bar_outer_left = int(floor(429 * world.scale_x))
health_bar_outer_width = int(floor(143 * world.scale_x))
health_bar_outer_height = int(floor(21 * world.scale_y))

health_bar_inner_top = int(floor(10 * world.scale_y))
health_bar_inner_left = int(floor(434 * world.scale_x))
health_bar_inner_width = int(floor(133 * world.scale_x))
health_bar_inner_widths = []
cnt = 0
while cnt < 100:
	health_bar_inner_widths.append(int(floor((cnt / 100) * health_bar_inner_width)))
	cnt += 1
health_bar_inner_height = int(floor(11 * world.scale_y))

health_bar_outer_rect = pygame.Rect(health_bar_outer_left, health_bar_outer_top, health_bar_outer_width, health_bar_outer_height)
health_bar_inner_rect = pygame.Rect(health_bar_inner_left, health_bar_inner_top, health_bar_inner_width, health_bar_inner_height)
health_bar_surface = pygame.Surface((health_bar_outer_width, health_bar_outer_height))
pygame.draw.rect(health_bar_surface, (0,0,0), pygame.Rect(0,0,health_bar_outer_width,health_bar_outer_height))

#Initialize your robot
#your_robot = Robot(world, pagetable, 0, 4, 11)

#Game state
game_state = 0 #main menu

#Main loop
running = True

while True:

#####################################################
#####################################################
#####################################################
################  MAP TEST MODE #####################
#####################################################
#####################################################
#####################################################

	while config.MODE_MAP_TEST == 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_state = 2

		#Pan ability with arrow keys in map test mode
		keys = pygame.key.get_pressed()
		if config.MODE_MAP_TEST == 1:
			if keys[pygame.K_ESCAPE]:
				game_state = 2
				break
			if keys[pygame.K_RIGHT]:
				world.pan(8,0)
			if keys[pygame.K_LEFT]:
				world.pan(-8,0)
			if keys[pygame.K_UP]:
				world.pan(0,-8)
			if keys[pygame.K_DOWN]:
				world.pan(0,8)
					
		world.render_full(False)
		render_page(pagetable, 0, 0)
		render_page(pagetable, 0, 1)
		pygame.display.flip()
		clock.tick(30)

#####################################################
#####################################################
#####################################################
#################    MAIN MENU    ###################
#####################################################
#####################################################
#####################################################
	menu_scroll_state = 0
	menu_proceed_state = 0
	checker_counter = 0
	blink_counter = 0
	blink_state = 0
	level = 0
	
	if game_state == 0:
		pygame.mixer.music.load("Audio/WarpSpeed.wav")
		pygame.mixer.music.play(-1)
		
		#Generate all robots
		load_robots(world, pagetable, "data/robots0.txt")
		
		while game_state == 0:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_state = 2

			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				game_state = 2
				break
			if keys[pygame.K_SPACE]:
				menu_proceed_state = 1
				world.points = 0

			blink_counter = blink_counter + 1
			if blink_state:
				if blink_counter == 15:
					blink_state = 0
					blink_counter = 0
			else:
				if blink_counter == 4:
					blink_state = 1
					blink_counter = 0

			if menu_scroll_state == 0:
				world.camera_x = world.camera_x + 2
				if world.camera_x == 2500:
					menu_scroll_state = 1
			elif menu_scroll_state == 1:
				world.camera_y = world.camera_y + 2
				if world.camera_y == 1000:
					menu_scroll_state = 2
			elif menu_scroll_state == 2:
				world.camera_x = world.camera_x - 2
				if world.camera_x == 0:
					menu_scroll_state = 3
			elif menu_scroll_state == 3:
				world.camera_y = world.camera_y - 2
				if world.camera_y == 0:
					menu_scroll_state = 0
						
			clock.tick(30)
			world.render_full(False)
			render_page(pagetable, 0, 0)
			render_page(pagetable, 0, 1)
			screen.blit(title_surface, title_frame)
			if blink_state:
				screen.blit(press_btn_box_surface, press_btn_box_frame)
			if menu_proceed_state:
				if checker_counter < 12:
					checker_s.blit(checker, (checker_counter % 4 * checker_width, floor(checker_counter / 4) * checker_height))
					checker_counter = checker_counter + 1
				else:
					game_state = 1
				screen.blit(checker_s, (0,0))
			pygame.display.flip()

#####################################################
#####################################################
#####################################################
#############    CUTSCENE SCREEN    #################
#####################################################
#####################################################
#####################################################
	
	if game_state == 1:
		pygame.mixer.music.stop()
		#pygame.mixer.music.unload()
		pygame.mixer.music.load("Audio/IncomingMessage.mp3")
		pygame.mixer.music.play(-1)
		
		screen.fill((0,0,0))
		typewriter.set_cursor(Typewriter.letter_width,Typewriter.letter_width)
		
		level = level + 1
		
		message_file = open("data/messages/" + str(level) + ".txt")
		fps = 14
		
		char_buffer = ""
		
		eof = False
		
		while game_state == 1:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_state = 2
			
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				game_state = 2
				break
			if keys[pygame.K_SPACE]:
				fps = 750
			else:
				fps = 14
				
			if keys[pygame.K_s]:
				game_state = 4
				break
			
			
			if len(char_buffer) == 0 and eof == False:
				end_marker = False
				while not end_marker:
					char = message_file.read(1)
					if char != '':
						if char == ' ' or char == '\n':
							if typewriter.can_fit(char_buffer):
								if char == '\n':
									char_buffer = char_buffer + char
								elif typewriter.can_fit(char_buffer + ' '):
									char_buffer = char_buffer + char
							else:
								char_buffer = '\n' + char_buffer + char
							end_marker = True
						else:
							char_buffer = char_buffer + char
					else:
						eof = True
						end_marker = True
						
			typewriter.type(char_buffer[0])
			if len(char_buffer) > 0:
				char_buffer = char_buffer[1:]
			if eof and len(char_buffer) == 0:
				game_state = 3
				
			clock.tick(fps)
			pygame.display.flip()

#####################################################
#####################################################
#####################################################
##############    EXIT OPERATION    #################
#####################################################
#####################################################
#####################################################

	if game_state == 2:
		pygame.display.quit()
		pygame.quit()
		sys.exit()
		
#####################################################
#####################################################
#####################################################
#############    SPACE TO PROCEED    ################
#####################################################
#####################################################
#####################################################

	if game_state == 3:
		blink_state = 0
		blink_counter = 0
		space_ready = 1
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			space_ready = 0
			
		while game_state == 3:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_state = 2
			
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				game_state = 2
				break
				
			if keys[pygame.K_SPACE]:
				if space_ready == 1:
					game_state = 4
					break
			else:
				space_ready = 1
				
			if blink_state == 0:
				screen.blit(press_btn2_box_surface, press_btn2_box_frame)
			else:
				screen.blit(press_btn2_fill_black, press_btn2_box_frame)
				
			blink_counter = blink_counter + 1
			if blink_state == 0:
				if blink_counter == 10:
					blink_state = 1
					blink_counter = 0
			else:
				if blink_counter == 5:
					blink_state = 0
					blink_counter = 0
				
			clock.tick(30)
			pygame.display.flip()
			
#####################################################
#####################################################
#####################################################
##############    MAIN OPERATION    #################
#####################################################
#####################################################
#####################################################

	if game_state == 4:
	
		pygame.mixer.music.stop()
		pygame.mixer.music.load("Audio/RampantNoiseEqualized.mp3")
		pygame.mixer.music.play(-1)
		
		world.load_world("data/world" + str(level) + ".txt")
		pagetable.load_blank(world)
		your_robot = load_robots(world, pagetable, "data/robots" + str(level) + ".txt")
		#print("YOUR ROBOT ID: " + str(hex(id(your_robot))))
		your_robot.ai = False
		your_robot.health = 99
		fire_cooldown = 0
		points = 0
		
		
		world.focus_camera(your_robot)
		world.render_full(True)
		
		while game_state == 4:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_state = 2
			
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				game_state = 2
				break
				
			#Control of your_robot
			if keys[pygame.K_RIGHT]:
				your_robot.try_move_right()
			if keys[pygame.K_DOWN]:
				your_robot.try_move_down()
			if keys[pygame.K_LEFT]:
				your_robot.try_move_left()
			if keys[pygame.K_UP]:
				your_robot.try_move_up()
			if keys[pygame.K_SPACE]:
				if not fire_cooldown:
					your_robot.fire()
					fire_cooldown = 5
					
			if fire_cooldown > 0:
				fire_cooldown = fire_cooldown - 1
				
			
			your_robot.calc_page()
			#Process pages around your_robot
			process_page(pagetable, your_robot.page_row-1, your_robot.page_col-1)
			process_page(pagetable, your_robot.page_row, your_robot.page_col-1)
			process_page(pagetable, your_robot.page_row+1, your_robot.page_col-1)
			process_page(pagetable, your_robot.page_row-1, your_robot.page_col)
			process_page(pagetable, your_robot.page_row, your_robot.page_col)
			process_page(pagetable, your_robot.page_row+1, your_robot.page_col)
			process_page(pagetable, your_robot.page_row-1, your_robot.page_col+1)
			process_page(pagetable, your_robot.page_row, your_robot.page_col+1)
			process_page(pagetable, your_robot.page_row+1, your_robot.page_col+1)
			
			#Render the background
			
			world.focus_camera(your_robot)
			world.render_partial()
			#print(world.bgnd_tiles)
			
			#Render lasers
			Laser.process_all_lasers()
			
			#Render pages around your_robot
			render_page(pagetable, your_robot.page_row-1, your_robot.page_col-1)
			render_page(pagetable, your_robot.page_row, your_robot.page_col-1)
			render_page(pagetable, your_robot.page_row+1, your_robot.page_col-1)
			render_page(pagetable, your_robot.page_row-1, your_robot.page_col)
			render_page(pagetable, your_robot.page_row, your_robot.page_col)
			render_page(pagetable, your_robot.page_row+1, your_robot.page_col)
			render_page(pagetable, your_robot.page_row-1, your_robot.page_col+1)
			render_page(pagetable, your_robot.page_row, your_robot.page_col+1)
			render_page(pagetable, your_robot.page_row+1, your_robot.page_col+1)
			
			#Render the health bar
			health_bar_inner_rect.width = health_bar_inner_widths[your_robot.health]
			pygame.draw.rect(screen, (0,0,0), health_bar_outer_rect)
			pygame.draw.rect(screen, (72,212,51), health_bar_inner_rect)
			
			#Render the points
			typewriter.set_cursor(0,0)
			typewriter.type_number(str(world.points))
			
			if your_robot.diminish == 2:
				#You lost!
				game_state = 5
				break
			
			clock.tick_busy_loop(60)
			pygame.display.flip()
			
			
#####################################################
#####################################################
#####################################################
##############    YOU LOST FLASH    #################
#####################################################
#####################################################
#####################################################

	if game_state == 5:
		screen_save_image = screen.copy()
		flash_state = 20
		while game_state == 5:
			if flash_state < 7:
				if flash_state % 2 == 0:
					screen.blit(screen_save_image, (0,0))
					#flash_state 
				else:
					screen.fill((255,255,255))
			flash_state = flash_state - 1
			if flash_state == 0:
				game_state = 0
			pygame.display.flip()
			clock.tick_busy_loop(4)