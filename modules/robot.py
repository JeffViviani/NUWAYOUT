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
		self.base_costume = (type - 1) * 4
		self.costume = self.base_costume
		self.tile_x = tile_x_init
		self.x = tile_x_init * self.world.tile_pixel_w
		self.tile_y = tile_y_init
		self.y = tile_y_init * self.world.tile_pixel_h
		world.occupancy[self.tile_y][self.tile_x] = self.type
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
		#neutral
		self.control_state = 0
		self.movement_progress = 0
		self.dest_x = None
		self.dest_y = None
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
		cls.step_size_x = int(floor(world.tile_pixel_w / 4))
		cls.step_size_y = int(floor(world.tile_pixel_h / 4))
		
	#should be called once per frame
	def automated_control(self):
		#If in process of moving rightward
		if self.control_state == 1:
			self.movement_progress = self.movement_progress + 1
			if self.movement_progress == 4:
				self.x = self.dest_x
				self.control_state = 0
			else:
				self.x = self.x + Robot.step_size_x
			return
		if self.control_state == 2:
			self.movement_progress = self.movement_progress + 1
			if self.movement_progress == 4:
				self.y = self.dest_y
				self.control_state = 0
			else:
				self.y = self.y + Robot.step_size_y
			return
		if self.control_state == 3:
			self.movement_progress = self.movement_progress + 1
			if self.movement_progress == 4:
				self.x = self.dest_x
				self.control_state = 0
			else:
				self.x = self.x - Robot.step_size_x
			return
		if self.control_state == 4:
			self.movement_progress = self.movement_progress + 1
			if self.movement_progress == 4:
				self.y = self.dest_y
				self.control_state = 0
			else:
				self.y = self.y - Robot.step_size_y
			return
		

	def calc_page(self):
		self.page_row = int(floor(self.tile_y / PAGETABLE_N))
		self.page_col = int(floor(self.tile_x / PAGETABLE_N))

	def calc_page_row(self):
		self.page_row = int(floor(self.tile_y / PAGETABLE_N))

	def calc_page_col(self):
		self.page_col = int(floor(self.tile_x / PAGETABLE_N))
	
	def leave_page(self):
		index = 0
		my_page = self.pagetable.get_page(self.page_row,self.page_col)
		num_indices = len(my_page)
		while index < num_indices:
			if my_page[index] == self:
				self.pagetable.remove_obj(self.page_row,self.page_col,index)
				break
			index = index + 1

	def join_page(self):
		self.pagetable[self.page_row][self.page_col].append(self)
		
	def render(self):
		self.world.screen.blit(Robot.image_surfaces[self.costume], (self.x - self.world.camera_x, self.y - self.world.camera_y))
	
	#If capable, initiate rightward movement
	def try_move_right(self):
		if self.control_state == 0:
			#If free to move
			try:
				if self.world.occupancy[self.tile_y][self.tile_x + 1] == 0:
					self.world.occupancy[self.tile_y][self.tile_x] = 0
					self.tile_x = self.tile_x + 1
					self.dest_x = self.x + self.world.tile_pixel_w
					self.world.occupancy[self.tile_y][self.tile_x] = self.type
					self.control_state = 1
					self.movement_progress = 0
					self.costume = self.base_costume + 0
					self.validate_page_col()
			except IndexError:
				return
				
	#If capable, initiate downward movement
	def try_move_down(self):
		if self.control_state == 0:
			#If free to move
			try:
				if self.world.occupancy[self.tile_y + 1][self.tile_x] == 0:
					self.world.occupancy[self.tile_y][self.tile_x] = 0
					self.tile_y = self.tile_y + 1
					self.dest_y = self.y + self.world.tile_pixel_h
					self.world.occupancy[self.tile_y][self.tile_x] = self.type
					self.control_state = 2
					self.movement_progress = 0
					self.costume = self.base_costume + 1
					self.validate_page_row()
					
			except IndexError:
				return
				
	#If capable, initiate leftward movement
	def try_move_left(self):
		if self.control_state == 0:
			#If free to move
			try:
				if self.world.occupancy[self.tile_y][self.tile_x - 1] == 0:
					self.world.occupancy[self.tile_y][self.tile_x] = 0
					self.tile_x = self.tile_x - 1
					self.dest_x = self.x - self.world.tile_pixel_w
					self.world.occupancy[self.tile_y][self.tile_x] = self.type
					self.control_state = 3
					self.movement_progress = 0
					self.costume = self.base_costume + 2
					self.validate_page_col()
					
			except IndexError:
				return
				
	#If capable, initiate upward movement
	def try_move_up(self):
		if self.control_state == 0:
			#If free to move
			try:
				if self.world.occupancy[self.tile_y - 1][self.tile_x] == 0:
					self.world.occupancy[self.tile_y][self.tile_x] = 0
					self.tile_y = self.tile_y - 1
					self.dest_y = self.y - self.world.tile_pixel_h
					self.world.occupancy[self.tile_y][self.tile_x] = self.type
					self.control_state = 4
					self.movement_progress = 0
					self.costume = self.base_costume + 3
					self.validate_page_row()
			except IndexError:
				return
	
	#Checks if its page row is correct, and if not, changes it.
	def validate_page_row(self):
		previous_page_row = self.page_row
		self.calc_page_row()
		if self.page_row != previous_page_row:
			self.leave_page()
			self.join_page()
	
	#Checks if its page column is correct, and if not, changes it.
	def validate_page_col(self):
		previous_page_col = self.page_col
		self.calc_page_col()
		if self.page_col != previous_page_col:
			self.leave_page()
			self.join_page()