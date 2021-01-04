import pygame
from world import *
from pagetable import *
from math import floor

class Robot:
	image_widths = [None]*12
	image_surfaces = [None]*12
	id_counter = 0
	def __init__(self, world, pagetable, type, tile_x_init, tile_y_init):
		self.world = world
		self.pagetable = pagetable
		self.type = type
		self.base_costume = type * 4
		self.costume = self.base_costume
		self.tile_x = tile_x_init
		self.x = tile_x_init * self.world.tile_pixel_w
		self.tile_y = tile_y_init
		self.y = tile_y_init * self.world.tile_pixel_h
		self.calc_page()
		self.page_row = None
		self.page_col = None
		self.calc_page_row()
		self.calc_page_col()
		self.direction = 0
		self.pos_offset = 0
		self.frame = (0, 0)
		self.pagetable.add_obj(self.page_row, self.page_col, self)
		self.id = Robot.id_counter
		Robot.id_counter = Robot.id_counter + 1
		
	
	@classmethod
	def init_class(cls, world):
		cls.image_surfaces[0] = world.scale(pygame.image.load("Images/Robots/blue_right.png"))
		cls.image_widths[0] = 16 * world.scale_x
		cls.image_surfaces[1] = world.scale(pygame.image.load("Images/Robots/blue_front.png"))
		cls.image_widths[1] = 16 * world.scale_x
		cls.image_surfaces[2] = world.scale(pygame.image.load("Images/Robots/blue_left.png"))
		cls.image_widths[2] = 18 * world.scale_x
		cls.image_surfaces[3] = world.scale(pygame.image.load("Images/Robots/blue_back.png"))
		cls.image_widths[3] = 18 * world.scale_x
		cls.image_surfaces[4] = world.scale(pygame.image.load("Images/Robots/orange_right.png"))
		cls.image_widths[4] = 16 * world.scale_x
		cls.image_surfaces[5] = world.scale(pygame.image.load("Images/Robots/orange_front.png"))
		cls.image_widths[5] = 16 * world.scale_x
		cls.image_surfaces[6] = world.scale(pygame.image.load("Images/Robots/orange_left.png"))
		cls.image_widths[6] = 18 * world.scale_x
		cls.image_surfaces[7] = world.scale(pygame.image.load("Images/Robots/orange_back.png"))
		cls.image_widths[7] = 18 * world.scale_x
		cls.image_surfaces[8] = world.scale(pygame.image.load("Images/Robots/red_right.png"))
		cls.image_widths[8] = 16 * world.scale_x
		cls.image_surfaces[9] = world.scale(pygame.image.load("Images/Robots/red_front.png"))
		cls.image_widths[9] = 16 * world.scale_x
		cls.image_surfaces[10] = world.scale(pygame.image.load("Images/Robots/red_left.png"))
		cls.image_widths[10] = 18 * world.scale_x
		cls.image_surfaces[11] = world.scale(pygame.image.load("Images/Robots/red_back.png"))
		cls.image_widths[11] = 18 * world.scale_x

	def calc_page(self):
		self.page_row = int(floor(self.tile_y / PAGETABLE_N))
		self.page_col = int(floor(self.tile_x / PAGETABLE_N))

	def calc_page_row(self):
		self.page_row = int(floor(self.tile_y / PAGETABLE_N))

	def calc_page_col(self):
		self.page_col = int(floor(self.tile_x / PAGETABLE_N))
		
	def render(self):
		self.world.screen.blit(Robot.image_surfaces[self.costume], (self.x - self.world.camera_x, self.y - self.world.camera_y))
	
	def leave_page(self):
		index = 0
		my_page = self.pagetable[self.page_row][self.page_col]
		num_indices = len(my_page)
		while index < num_indices:
			if my_page[index] == self:
				del self.pagetable[self.page_row][self.page_col][index]
				break

	def join_page(self):
		self.pagetable[self.page_row][self.page_col].append(self)