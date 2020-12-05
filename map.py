#
# FILE: map.py
# PART OF: Part of the NUWAYOUT arcade game.
# DESCRIPTION: Class for map control and display.
#

#Global variables for the camera
global pan_x
global pan_y

#Load required modules
import pygame
from scaler import *

map1 = [[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0]]
map2 = [[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0]]
map3 = [[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0]]

map_mappings = [map1, map2, map3]

class Map:
	tiles_surfaces = [None]*2
	@classmethod
	def init_scaled_surfaces(cls):
		tiles_surfaces[0] = scl.scale(pygame.image.load("Images/Tiles/tile0.png")).convert()
		tiles_surfaces[1] = scl.scale(pygame.image.load("Images/Tiles/tile1.png")).convert()
	