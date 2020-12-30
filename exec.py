import sys
sys.path.insert(1, 'modules/')

import pygame
import config
from filestream import *
from world import *
from robot import *
from pagetable import *

def load_enemies(world, pagetable, file):
	enemy_list = file_to_1D_list(file)
	num_items = len(enemy_list)
	item = 0
	print num_items
	while item < num_items:
		new_robot = Robot(world, pagetable, enemy_list[item], enemy_list[item + 1], enemy_list[item + 2])
		item = item + 3
		
def render_page(pagetable, row, col):
	for robot in pagetable.get_page(row,col):
		robot.render()

clock = pygame.time.Clock()

#Initialize pygame and the display
pygame.init()
displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
print screen_width
screen_height = displayInfo.current_h
screen = None
if config.FULLSCREEN:
	screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, 8)
else:
	screen = pygame.display.set_mode((576, 432), 0, 8)

#Load the world
world = World(screen)
world.load_world("data/world1.txt")

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

#Main loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#Pan ability with arrow keys in map test mode
	keys = pygame.key.get_pressed()
	if config.MODE_MAP_TEST == 1:
		if keys[pygame.K_ESCAPE]:
			running = False
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
	pygame.display.flip()
sys.exit()