import sys
sys.path.insert(1, 'modules/')

import pygame
from world import *

clock = pygame.time.Clock()

pygame.init()
displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
screen_height = displayInfo.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, 32)
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
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
	clock.tick(60)
	wor.render()
	pygame.display.flip()
sys.exit()