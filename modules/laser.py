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
		if self.direction == 0:
			self.tile_x_init = robot.tile_x + 1
			self.tile_y_init = robot.tile_y
			self.disperse_tile = self.tile_x_init + 27
		elif self.direction == 1:
			self.tile_x_init = robot.tile_x
			self.tile_y_init = robot.tile_y + 1
			self.disperse_tile = self.tile_y_init + 27
		elif self.direction == 2:
			self.tile_x_init = robot.tile_x - 1
			self.tile_y_init = robot.tile_y
			self.disperse_tile = self.tile_x_init - 27
		elif self.direction == 3:
			self.tile_x_init = robot.tile_x
			self.tile_y_init = robot.tile_y - 1
			self.disperse_tile = self.tile_y_init - 27
		self.tile_x = self.tile_x_init
		self.tile_y = self.tile_y_init
		self.position_by_tile(self.tile_x, self.tile_y)
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
		cls.laser_sound = pygame.mixer.Sound("Audio/Good_Laser.wav")
		
	@classmethod
	def process_all_lasers(cls):
		lsr_index = 0
		num_lasers = len(Laser.registry)
		while lsr_index < num_lasers:
			lsr = Laser.registry[lsr_index]
			if not lsr.disperse:
				lsr.automated_control()
			else:
				del Laser.registry[lsr_index]
				num_lasers = num_lasers - 1
			lsr_index = lsr_index + 1
		
	def automated_control(self):
		if self.direction == 0:
			if self.tile_x >= self.disperse_tile:
				self.disperse = True
				return
			tile_check = self.tile_x
			tile_max_extend = self.tile_x + 7
			while tile_check < tile_max_extend:
				tile_value = self.world.occupancy[self.tile_y][tile_check]
				if isinstance(tile_value, robot.Robot) or tile_value == 3:
					self.disperse = True
					break
					
				tile_check = tile_check + 1
			self.position_by_tile(self.tile_x, self.tile_y)
			self.render_horizontal(tile_check - self.tile_x - 1)
			self.tile_x = tile_check
			
	def position_by_tile(self, tile_x, tile_y):
		self.x = tile_x * self.world.tile_pixel_w
		self.y = tile_y * self.world.tile_pixel_h
			
				
	def render_horizontal(self, breadth):
		self.world.screen.blit(Laser.image_surfaces_horizontal[breadth], (self.x - self.world.camera_x, self.y - self.world.camera_y))
		