from math import floor
from copy import copy
import pygame
from filestream import *

GAME_NATIVE_W = 576
GAME_NATIVE_H = 432

class World:
	def __init__(self, screen):
		self.screen = screen
		self.camera_x = None
		self.camera_y = None
		self.bgnd_tiles = []
		self.occupancy = []
		displayInfo = pygame.display.Info()
		self.scale_x = displayInfo.current_w / GAME_NATIVE_W
		self.scale_y = displayInfo.current_h / GAME_NATIVE_H
		self.tile_surfaces = []
		self.tile_surfaces.append(self.scale(pygame.image.load("Images/Tiles/tile0.png")))
		self.tile_surfaces.append(self.scale(pygame.image.load("Images/Tiles/tile1.png")))
		self.tile_surfaces.append(self.scale(pygame.image.load("Images/Tiles/tile2.png")))
		self.tile_surfaces.append(self.scale(pygame.image.load("Images/Tiles/tile3.png")))
		self.tile_pixel_w = 20 * self.scale_x
		self.tile_pixel_h = 20 * self.scale_y
		
		
	def load_world(self, file):
		self.bgnd_tiles = file_to_2D_list(file)
		self.occupancy = copy(self.bgnd_tiles)
		zero_list(self.occupancy)
		
	def scale(self, surface):
		current_w = surface.get_width()
		current_h = surface.get_height()
		return pygame.transform.scale(surface,(int(floor(current_w * self.scale_x)), int(floor(current_h * self.scale_y))))

	def render(self):
		#Begin one tile to the left
		frame = pygame.Rect(0, 0 - self.camera_y % self.tile_pixel_h, self.tile_pixel_w, self.tile_pixel_h)
		tile_x_pos_init = int(floor(self.camera_x / self.tile_pixel_w))
		tile_y_pos_init = int(floor(self.camera_y / self.tile_pixel_h))
		tile_x_pos_max = tile_x_pos_init + 33
		tile_y_pos_max = tile_y_pos_init + 27
		row_ref = None
		tile_y_pos = tile_y_pos_init
		while tile_y_pos < tile_y_pos_max:
			if tile_y_pos >= len(self.bgnd_tiles) or tile_y_pos < 0:
				tile_x_pos = tile_x_pos_init
				frame.left = 0 - (self.camera_x % self.tile_pixel_w)
				tile_to_blit = self.tile_surfaces[3]
				while tile_x_pos < tile_x_pos_max:
					self.screen.blit(tile_to_blit, frame)
					frame = frame.move(self.tile_pixel_w, 0)
					tile_x_pos = tile_x_pos + 1
			else:
				row_ref = self.bgnd_tiles[tile_y_pos]
				tile_x_pos = tile_x_pos_init
				frame.left = 0 - (self.camera_x % self.tile_pixel_w)
				while tile_x_pos < tile_x_pos_max:
					tile_to_blit = None
					if tile_x_pos >= len(row_ref) or tile_x_pos < 0:
						tile_to_blit = self.tile_surfaces[3]
					else:
						tile_to_blit = self.tile_surfaces[row_ref[tile_x_pos]]
					self.screen.blit(tile_to_blit, frame)
					frame = frame.move(self.tile_pixel_w, 0)
					tile_x_pos = tile_x_pos + 1
			frame = frame.move(0, self.tile_pixel_h)
			tile_y_pos = tile_y_pos + 1
			
	def pan(self, x_shift, y_shift):
		self.camera_x = self.camera_x + x_shift;
		self.camera_y = self.camera_y + y_shift

def zero_list(lst):
	for i in lst:
		if isinstance(i, list):
			zero_list(i)
		else:
			i = 0