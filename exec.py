import sys
sys.path.insert(1, 'modules/')

import pygame
import config
from world import *
from robot import *

def load_enemies(world, pagetable, file):
	enemy_list = file_to_1D_list(file)
	index = 0
	while index < len(enemy_list):
		new_robot = Robot()
		

clock = pygame.time.Clock()

pygame.init()
displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
screen_height = displayInfo.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, 8)
wor = World(screen)
wor.load_world("data/world1.txt")
wor.camera_x = 0
wor.camera_y = 0
wor.render()
running = True
while running:
	#Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	keys = pygame.key.get_pressed()
	if config.MODE_MAP_TEST == 1:
		if keys[pygame.K_ESCAPE]:
			running = False
		if keys[pygame.K_RIGHT]:
			wor.pan(4,0)
		if keys[pygame.K_LEFT]:
			wor.pan(-4,0)
		if keys[pygame.K_UP]:
			wor.pan(0,-4)
		if keys[pygame.K_DOWN]:
			wor.pan(0,4)
				
	clock.tick(60)
	wor.render()
	pygame.display.flip()
sys.exit()