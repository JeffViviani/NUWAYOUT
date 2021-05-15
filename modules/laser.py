from math import floor
from world import *
import robot
import pygame

class Laser:
	image_surfaces_horizontal = [None]*7
	image_surfaces_vertical = [None]*7
	laser_sound = None
	registry = []

	def __init__(self, world, robot):
		self.world = world
		self.direction = robot.direction
		self.disperse = False
		self.x_offset = 0
		self.y_offset = 0
		if self.direction == 0:
			self.tile_x_init = robot.tile_x + 1
			self.tile_y_init = robot.tile_y
			self.disperse_tile = self.tile_x_init + 27
			self.y_offset = Laser.half_tile_height
		elif self.direction == 1:
			self.tile_x_init = robot.tile_x
			self.tile_y_init = robot.tile_y + 1
			self.disperse_tile = self.tile_y_init + 27
			self.x_offset = Laser.half_tile_width
		elif self.direction == 2:
			self.tile_x_init = robot.tile_x - 1
			self.tile_y_init = robot.tile_y
			self.disperse_tile = self.tile_x_init - 27
			self.y_offset = Laser.half_tile_height
		elif self.direction == 3:
			self.tile_x_init = robot.tile_x
			self.tile_y_init = robot.tile_y - 1
			self.disperse_tile = self.tile_y_init - 27
			self.x_offset = Laser.half_tile_width
		self.tile_x = self.tile_x_init
		self.tile_y = self.tile_y_init
		self.position_x_by_tile(self.tile_x)
		self.position_y_by_tile(self.tile_y)
		Laser.registry.append(self)
		pygame.mixer.Sound.play(Laser.laser_sound)
		
	@classmethod
	def init_class(cls, world):
		cls.image_surfaces_horizontal[0] = world.scale(pygame.image.load("Images/Lasers/Horizontal/1.png"))
		cls.image_surfaces_horizontal[1] = world.scale(pygame.image.load("Images/Lasers/Horizontal/2.png"))
		cls.image_surfaces_horizontal[2] = world.scale(pygame.image.load("Images/Lasers/Horizontal/3.png"))
		cls.image_surfaces_horizontal[3] = world.scale(pygame.image.load("Images/Lasers/Horizontal/4.png"))
		cls.image_surfaces_horizontal[4] = world.scale(pygame.image.load("Images/Lasers/Horizontal/5.png"))
		cls.image_surfaces_horizontal[5] = world.scale(pygame.image.load("Images/Lasers/Horizontal/6.png"))
		cls.image_surfaces_horizontal[6] = world.scale(pygame.image.load("Images/Lasers/Horizontal/7.png"))
		cls.image_surfaces_vertical[0] = world.scale(pygame.image.load("Images/Lasers/Vertical/1.png"))
		cls.image_surfaces_vertical[1] = world.scale(pygame.image.load("Images/Lasers/Vertical/2.png"))
		cls.image_surfaces_vertical[2] = world.scale(pygame.image.load("Images/Lasers/Vertical/3.png"))
		cls.image_surfaces_vertical[3] = world.scale(pygame.image.load("Images/Lasers/Vertical/4.png"))
		cls.image_surfaces_vertical[4] = world.scale(pygame.image.load("Images/Lasers/Vertical/5.png"))
		cls.image_surfaces_vertical[5] = world.scale(pygame.image.load("Images/Lasers/Vertical/6.png"))
		cls.image_surfaces_vertical[6] = world.scale(pygame.image.load("Images/Lasers/Vertical/7.png"))
		cls.segment_width = int(floor(20 * world.scale_x))
		cls.segment_height = int(floor(20 * world.scale_y))
		cls.half_tile_width = world.tile_pixel_w // 2
		cls.half_tile_height = world.tile_pixel_h // 2
		cls.laser_sound = pygame.mixer.Sound("Audio/Good_Laser.wav")
		
	@classmethod
	def process_all_lasers(cls):
		lsr_index = 0
		num_lasers = len(Laser.registry)
		while lsr_index < num_lasers:
			lsr = Laser.registry[lsr_index]
			if not lsr.disperse:
				lsr.automated_control()
				lsr_index = lsr_index + 1
			else:
				del Laser.registry[lsr_index]
				num_lasers = num_lasers - 1
		
	def automated_control(self):
	
		if self.direction == 0:
			if self.tile_x >= self.disperse_tile:
				self.disperse = True
				return
			old_tile = self.tile_x
			tile_max_extend = self.tile_x + 3
			index = self.tile_y * self.world.bgnd_tiles_width + self.tile_x
			if tile_max_extend > self.world.bgnd_tiles_height:
				self.disperse = True
				tile_max_extend = self.world.bgnd_tiles_height
			while self.tile_x < tile_max_extend:
				tile_value = self.world.occupancy[index]
				if isinstance(tile_value, robot.Robot):
					tile_value.get_shot()
					self.disperse = True
					break
				elif tile_value == 9:
					self.disperse = True
					break
				self.tile_x = self.tile_x + 1
				index = index + 1
			self.position_x_by_tile(old_tile)
			costume = self.tile_x - old_tile - 1
			if costume >= 0:
				self.render_horizontal(costume)
			return
			
		if self.direction == 1:
			if self.tile_y >= self.disperse_tile:
				self.disperse = True
				return
			old_tile = self.tile_y
			tile_max_extend = self.tile_y + 3
			num_rows = self.world.bgnd_tiles_width
			index = self.tile_y * self.world.bgnd_tiles_width + self.tile_x
			if tile_max_extend > num_rows:
				self.disperse = True
				tile_max_extend = num_rows
			while self.tile_y < tile_max_extend:
				tile_value = self.world.occupancy[index]
				if isinstance(tile_value, robot.Robot):
					tile_value.get_shot()
					self.disperse = True
					break
				elif tile_value == 9:
					self.disperse = True
					break
				self.tile_y = self.tile_y + 1
				index = index + self.world.bgnd_tiles_width
			self.position_y_by_tile(old_tile)
			costume = self.tile_y - old_tile - 1
			if costume >= 0:
				self.render_vertical(costume)
			return
			
		if self.direction == 2:
			if self.tile_x <= self.disperse_tile:
				self.disperse = True
				return
			old_tile = self.tile_x
			tile_max_extend = self.tile_x - 3
			index = self.tile_y * self.world.bgnd_tiles_width + self.tile_x
			if tile_max_extend < 0:
				self.disperse = True
				tile_max_extend = 0
			while self.tile_x >= tile_max_extend:
				tile_value = self.world.occupancy[index]
				if isinstance(tile_value, robot.Robot):
					tile_value.get_shot()
					self.disperse = True
					break
				elif tile_value == 9:
					self.disperse = True
					break
				self.tile_x = self.tile_x - 1
				index = index - 1
			self.position_x_by_tile(self.tile_x + 1)
			costume = old_tile - self.tile_x - 1
			if costume >= 0:
				self.render_horizontal(costume)
			return
			
		if self.direction == 3:
			if self.tile_y <= self.disperse_tile:
				self.disperse = True
				return
			old_tile = self.tile_y
			tile_max_extend = self.tile_y - 3
			index = self.tile_y * self.world.bgnd_tiles_width + self.tile_x
			if tile_max_extend < 0:
				self.disperse = True
				tile_max_extend = 0
			while self.tile_y >= tile_max_extend:
				tile_value = self.world.occupancy[index]
				if isinstance(tile_value, robot.Robot):
					tile_value.get_shot()
					self.disperse = True
					break
				elif tile_value == 9:
					self.disperse = True
					break
				self.tile_y = self.tile_y - 1
				index = index - self.world.bgnd_tiles_width
			self.position_y_by_tile(self.tile_y + 1)
			costume = old_tile - self.tile_y - 1
			if costume >= 0:
				self.render_vertical(costume)
			return
			
	def position_x_by_tile(self, tile_x):
		self.x = tile_x * self.world.tile_pixel_w + self.x_offset
	
	def position_y_by_tile(self, tile_y):
		self.y = tile_y * self.world.tile_pixel_h + self.y_offset
			
				
	def render_horizontal(self, breadth):
		self.world.screen.blit(Laser.image_surfaces_horizontal[breadth], (self.x - self.world.camera_x, self.y - self.world.camera_y))
		
	def render_vertical(self, breadth):
		self.world.screen.blit(Laser.image_surfaces_vertical[breadth], (self.x - self.world.camera_x, self.y - self.world.camera_y))
		