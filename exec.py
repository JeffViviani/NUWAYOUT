import sys
sys.path.insert(1, 'modules/')

import pygame
import config
from filestream import *
from world import *
from robot import *
from pagetable import *

#####################################################
#####################################################
#####################################################
##################  FUNCTIONS #######################
#####################################################
#####################################################
#####################################################

def load_enemies(world, pagetable, file):
	enemy_list = file_to_1D_list(file)
	num_items = len(enemy_list)
	item = 0
	while item < num_items:
		new_robot = Robot(world, pagetable, enemy_list[item], enemy_list[item + 1], enemy_list[item + 2])
		item = item + 3
		
def render_page(pagetable, row, col):
	for robot in pagetable.get_page(row,col):
		robot.render()

#####################################################
#####################################################
#####################################################
################  INITIALIZATION ####################
#####################################################
#####################################################
#####################################################

#Initialize pygame and the display
pygame.init()
clock = pygame.time.Clock()
displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
screen_height = displayInfo.current_h
screen = None
if config.FULLSCREEN:
	screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, 8)
else:
	screen = pygame.display.set_mode((576, 432), 0, 8)

#Load the main menu world
world = World(screen)
world.load_world("data/world0.txt")

#Initialize Robot class
Robot.init_class(world)

#Create page table instance
pagetable = PageTable()
pagetable.load_blank(world)

#Generate all enemies
load_enemies(world, pagetable, "data/enemies1.txt")

#Initialize the camera
world.camera_x = 0
world.camera_y = 0

#Initialize Title of Game
title_surface = world.scale(pygame.image.load("Images/HUD/title.png"))
title_frame = (90 * world.scale_x, 100 * world.scale_y)

#Initialize the "Press Button" blinking box for the main menu
press_btn_box_surface = world.scale(pygame.image.load("Images/HUD/pressButton.png"))
press_btn_box_frame = (230 * world.scale_x, 200 * world.scale_y)

#Initialize your robot
your_robot = Robot(world, pagetable, 0, 4, 11)

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
					
		clock.tick(30)
		world.render()
		render_page(pagetable, 0, 0)
		render_page(pagetable, 0, 1)
		pygame.display.flip()

#####################################################
#####################################################
#####################################################
#################    MAIN MENU    ###################
#####################################################
#####################################################
#####################################################
	menu_scroll_state = 0
	blink_counter = 0
	blink_state = 0

	while game_state == 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_state = 2

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			game_state = 2
			break
		if keys[pygame.K_SPACE]:
			game_state = 1
			break

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
		pygame.display.flip()

#####################################################
#####################################################
#####################################################
###############    LOAD SCREEN    ###################
#####################################################
#####################################################
#####################################################

	while game_state == 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_state = 2
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			game_state = 2
			break
		break

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