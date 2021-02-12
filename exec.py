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

#####################################################
#####################################################
#####################################################
##################  FUNCTIONS #######################
#####################################################
#####################################################
#####################################################

def load_robots(world, pagetable, file):
	enemy_list = file_to_1D_list(file)
	num_items = len(enemy_list)
	item = 0
	first = 0
	firstRef = None
	while item < num_items:
		new_robot = Robot(world, pagetable, enemy_list[item], enemy_list[item + 1], enemy_list[item + 2])
		item = item + 3
		if first == 0:
			first = 1
			firstRef = new_robot
	return firstRef
		
def render_page(pagetable, row, col):
	try:
		for robot in pagetable.get_page(row,col):
			robot.render()
		return
	except TypeError:
		return
		
def process_page(pagetable, row, col):
	try:
		for robot in pagetable.get_page(row,col):
			robot.automated_control()
		return
	except TypeError:
		return
		
#####################################################
#####################################################
#####################################################
################  INITIALIZATION ####################
#####################################################
#####################################################
#####################################################

#Initialize pygame and the display
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
screen_height = displayInfo.current_h
screen = None
if config.FULLSCREEN:
	screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF, 8)
else:
	screen = pygame.display.set_mode((576, 432), 0, 8)

#Load the main menu world
world = World(screen)
world.load_world("data/world0.txt")

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
					
		world.render()
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
		pygame.mixer.music.load("Audio/Hyperloop-Deluxe.mp3")
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
			world.render()
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
		pygame.mixer.music.load("Audio/Space.mp2")
		pygame.mixer.music.play(-1)
		
		world.load_world("data/world" + str(level) + ".txt")
		pagetable.load_blank(world)
		your_robot = load_robots(world, pagetable, "data/robots" + str(level) + ".txt")
		your_robot.ai = False
		fire_cooldown = 0
		
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
			world.render()
			
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
			
			pygame.display.flip()
			clock.tick_busy_loop(30)
			
