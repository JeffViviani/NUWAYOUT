#
# FILE: scaler.py
# PART OF: Part of the NUWAYOUT arcade game.
# DESCRIPTION: Class for handling the robots.
#

#LOad required modules
import pygame
from random import random
from scaler import *
from lasers import *

#Initialize music commented out since already done in main.py
#pygame.mixer.init()
class Robot:
	game_over = None
	sound_good = None
	sound_bad = None
	spawn_lines = [None]*5
	death_lines = [None]*1
	registry = []
	image_widths = [None]*12
	image_surfaces = [None]*12
		
	def __init__(self,screen,background,color,door_manager):
		self.alive = True
		self.screen = screen
		self.background = background
		self.color = color
		self.door_manager = door_manager
		self.grid_x = None
		self.grid_y = None
		self.pos_x = None
		self.pos_y = None
		self.dir = None
		self.in_motion = False
		self.width = None
		self.image_file = None
		self.image = None
		self.rect = None
		self.destination_x = None
		self.destination_y = None
		self.move_next_frame = False
		self.last_fire_time = 0
		Robot.registry.append(self)
		grid_found = False
		#If intended to auto-generate
		if self.color == 0:
			self.sound = Robot.sound_good
			self.fire_delay = 100
			self.grid_x = 13
			self.grid_y = 9
			self.dir = 1
		else:
			self.sound = Robot.sound_bad
			self.fire_delay = 200
			spawn_location = int(round(random() * 3))
			if spawn_location == 0:
				grids_to_check = [[25,9],[25,8],[25,10],[25,7],[25,11]]
				self.dir = 2
			elif spawn_location == 1:
				grids_to_check = [[13,18],[14,18],[12,18],[15,18],[11,18]]
				self.dir = 3
			elif spawn_location == 2:
				grids_to_check = [[0,9],[0,10],[0,8],[0,11],[0,7]]
				self.dir = 0
			elif spawn_location == 3:
				grids_to_check = [[13,0],[12,0],[14,0],[11,0],[15,0]]
				self.dir = 1
			for g in grids_to_check:
				if not self.grid_occupied(g[0],g[1]):
					grid_found = True
					self.grid_x = g[0]
					self.grid_y = g[1]
					break
			if grid_found:
				self.door_manager.doors[spawn_location].open()
				if random() < 0.3:
					Robot.spawn_lines[int(round(random()*4.0))].play()
			else:
				self.alive = False
		if self.alive:
			coordinates = self.grid_to_coordinates()
			self.pos_x = coordinates[0]
			self.pos_y = coordinates[1]
			self.update_image()
			self.position_rect()
			self.draw()
	@classmethod
	def init_scaled_surfaces(cls):
		cls.image_surfaces[0] = scl.scale(pygame.image.load("Images/Robots/blue_right.png")).convert()
		cls.image_widths[0] = 16
		cls.image_surfaces[1] = scl.scale(pygame.image.load("Images/Robots/blue_front.png")).convert()
		cls.image_widths[1] = 16
		cls.image_surfaces[2] = scl.scale(pygame.image.load("Images/Robots/blue_left.png")).convert()
		cls.image_widths[2] = 18
		cls.image_surfaces[3] = scl.scale(pygame.image.load("Images/Robots/blue_back.png")).convert()
		cls.image_widths[3] = 18
		cls.image_surfaces[4] = scl.scale(pygame.image.load("Images/Robots/orange_right.png")).convert()
		cls.image_widths[4] = 16
		cls.image_surfaces[5] = scl.scale(pygame.image.load("Images/Robots/orange_front.png")).convert()
		cls.image_widths[5] = 16
		cls.image_surfaces[6] = scl.scale(pygame.image.load("Images/Robots/orange_left.png")).convert()
		cls.image_widths[6] = 18
		cls.image_surfaces[7] = scl.scale(pygame.image.load("Images/Robots/orange_back.png")).convert()
		cls.image_widths[7] = 18
		cls.image_surfaces[8] = scl.scale(pygame.image.load("Images/Robots/red_right.png")).convert()
		cls.image_widths[8] = 16
		cls.image_surfaces[9] = scl.scale(pygame.image.load("Images/Robots/red_front.png")).convert()
		cls.image_widths[9] = 16
		cls.image_surfaces[10] = scl.scale(pygame.image.load("Images/Robots/red_left.png")).convert()
		cls.image_widths[10] = 18
		cls.image_surfaces[11] = scl.scale(pygame.image.load("Images/Robots/red_back.png")).convert()
		cls.image_widths[11] = 18
	@classmethod
	def init_sounds(cls):
		cls.spawn_lines[0] = pygame.mixer.Sound("Audio/Robot Lines/Spawn/0.wav")
		cls.spawn_lines[1] = pygame.mixer.Sound("Audio/Robot Lines/Spawn/1.wav")
		cls.spawn_lines[2] = pygame.mixer.Sound("Audio/Robot Lines/Spawn/2.wav")
		cls.spawn_lines[3] = pygame.mixer.Sound("Audio/Robot Lines/Spawn/3.wav")
		cls.spawn_lines[4] = pygame.mixer.Sound("Audio/Robot Lines/Spawn/4.wav")
		cls.death_lines[0] = pygame.mixer.Sound("Audio/Robot Lines/Death/1.wav")
		cls.sound_good = pygame.mixer.Sound("Audio/Good_Laser.wav")
		cls.sound_bad = pygame.mixer.Sound("Audio/Bad_Laser.wav")
			
	def calc_destination(self):
		coordinates = self.grid_to_coordinates()
		self.destination_x = coordinates[0]
		self.destination_y = coordinates[1]
	def try_move(self):
		if self.dir == 0 and self.grid_x < 25:
			if not self.grid_occupied(self.grid_x + 1,self.grid_y):
				self.grid_x += 1; self.in_motion = True; self.calc_destination();
		elif self.dir == 1 and self.grid_y < 18:
			if not self.grid_occupied(self.grid_x,self.grid_y + 1):
				self.grid_y += 1; self.in_motion = True; self.calc_destination();
		elif self.dir == 2 and self.grid_x > 0:
			if not self.grid_occupied(self.grid_x - 1,self.grid_y):
				self.grid_x -= 1; self.in_motion = True; self.calc_destination();
		elif self.dir == 3 and self.grid_y > 0:
			if not self.grid_occupied(self.grid_x,self.grid_y - 1):
				self.grid_y -= 1; self.in_motion = True; self.calc_destination();
		return self.in_motion
	def change_dir(self,new_dir):
		different_dir = new_dir != self.dir
		if different_dir:
			self.dir = new_dir
			self.vanish_from(self.background)
			self.update_image()
			self.draw()
		return different_dir
	def ai(self):
		if not self.in_motion:
			if self.color == 1:
				x = random()
				if x < 0.006:
					self.try_move()
				elif x < 0.015:
					self.change_dir(int(round(random() * 3)))
				elif x < 0.020:
					self.fire()
			elif self.color == 2:
				to_fire = False
				if self.move_next_frame:
					self.try_move()
					if not self.in_motion:
						to_fire = True
					self.move_next_frame = False
				else:
					self.hunt_blue()
				if not to_fire:
					x = random()
					if x < 0.15:
						to_fire = True
				if to_fire:
					self.fire()
	def move(self):
		if self.in_motion:
			self.vanish_from(self.background)
			if self.dir == 0 and self.pos_x < self.destination_x:
				self.pos_x += 2
			elif self.dir == 1 and self.pos_y < self.destination_y:
				self.pos_y += 2
			elif self.dir == 2 and self.pos_x > self.destination_x:
				self.pos_x -= 2
			elif self.dir == 3 and self.pos_y > self.destination_y:
				self.pos_y -= 2
			if self.pos_x == self.destination_x and self.pos_y == self.destination_y:
				self.in_motion = False
			self.position_rect()
			self.draw()
	def hunt_blue(self):
		your_robot = Robot.registry[0]
		motion_orientation = 0
		if self.grid_x == your_robot.grid_x:
			motion_orientation = 2
		elif self.grid_y == your_robot.grid_y:
			motion_orientation = 1
		if motion_orientation == 0:
			x = round(random())
			if x == 0:
				motion_orientation = 1
			else:
				motion_orientation = 2
		if motion_orientation == 1:
			if your_robot.grid_x < self.grid_x:
				self.change_dir(2); self.move_next_frame = True;
			else:
				self.change_dir(0); self.move_next_frame = True;
		else:
			if your_robot.grid_y < self.grid_y:
				self.change_dir(3); self.move_next_frame = True;
			else:
				self.change_dir(1); self.move_next_frame = True;
	def update_image(self):
		_list_index = self.color * 4 + self.dir
		self.image = Robot.image_surfaces[_list_index]
		self.rect = self.image.get_rect()
		self.width = Robot.image_widths[_list_index]
		self.position_rect()
	def position_rect(self):
		self.rect.left = (self.pos_x + ((20 - self.width) / 2)) * scl.scale_x
		self.rect.top = self.pos_y * scl.scale_y
	def vanish_from(self, clean_image):
		self.screen.blit(clean_image,self.rect,self.rect)
	def draw(self):
		self.screen.blit(self.image,self.rect)
	def grid_to_coordinates(self):
		return [self.grid_x * 20 + 28, self.grid_y * 20 + 26]
	def fire(self):
		time_mil = pygame.time.get_ticks()
		if time_mil > self.last_fire_time + self.fire_delay:
			if self.dir == 0:
				laser_grid_x = self.grid_x + 1; laser_grid_y = self.grid_y;
			elif self.dir == 1:
				laser_grid_x = self.grid_x; laser_grid_y = self.grid_y + 1;
			elif self.dir == 2:
				laser_grid_x = self.grid_x - 1; laser_grid_y = self.grid_y;
			elif self.dir == 3:
				laser_grid_x = self.grid_x; laser_grid_y = self.grid_y - 1;
			Laser(self.screen, self.background, laser_grid_x, laser_grid_y, self.dir, self.sound)
			self.last_fire_time = time_mil
	def grid_occupied(self,grid_x,grid_y):
		occupied = False
		for r in Robot.registry:
			if grid_x == r.grid_x and grid_y == r.grid_y:
				occupied = True
				break
		return occupied

class Laser:
	registry = []
	image_vertical = None
	image_horizontal = None
	
	@classmethod
	def init_scaled_surfaces(cls):
		cls.image_vertical = scl.scale(pygame.image.load("Images/Projectiles/laser_vertical.png")).convert()
		cls.image_horizontal = scl.scale(pygame.image.load("Images/Projectiles/laser_horizontal.png")).convert()
	def __init__(self,screen,background,grid_x,grid_y,dir,sound):
		Laser.registry.append(self)
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.sound = sound
		self.alive = True
		self.pos_x = None
		self.pos_y = None
		self.screen = screen
		self.background = background
		self.dir = dir
		if self.dir % 2 == 0:
			self.image = Laser.image_horizontal
			self.width = 10 * scl.scale_x
			self.height = 6 * scl.scale_y
		else:
			self.image = Laser.image_vertical
			self.width = 6 * scl.scale_x
			self.height = 10 * scl.scale_y
		self.grid_to_coordinates()
		self.rect = pygame.Rect(self.pos_x,self.pos_y,self.width,self.height)
		self.sound.play()
		self.draw()
	def move(self):
		self.vanish_from(self.background)
		if self.dir == 0:
			self.rect.left += 6 * scl.scale_x
			if self.rect.left >= self.screen.get_width() - 28 - self.width:
				self.delete()
		elif self.dir == 1:
			self.rect.top += 6 * scl.scale_y
			if self.rect.top >= self.screen.get_height() - 25 - self.height:
				self.delete()
		elif self.dir == 2:
			self.rect.left -= 6 * scl.scale_x
			if self.rect.left <= 27 + self.width:
				self.delete()
		elif self.dir == 3:
			self.rect.top -= 6 * scl.scale_y
			if self.rect.top <= 25 + self.height:
				self.delete()
		if self.alive and not self.check_contact():
			self.draw()
	def vanish_from(self, clean_image):
		self.screen.blit(clean_image,self.rect,self.rect)
	def draw(self):
		self.screen.blit(self.image,self.rect)
	def grid_to_coordinates(self):
		self.pos_x = (self.grid_x * 20 + 28 + ((20 - self.width) / 2)) * scl.scale_x
		self.pos_y = (self.grid_y * 20 + 26 + ((20 - self.height) / 2)) * scl.scale_y
	def delete(self):
		self.alive = False
		self.vanish_from(self.background)
		Laser.registry.remove(self)
	def check_contact(self):
		made_contact = False
		for r in Robot.registry:
			if self.rect.colliderect(r.rect):
				self.vanish_from(self.background)
				Laser.registry.remove(self)
				r.vanish_from(r.background)
				Robot.registry.remove(r)
				made_contact = True
				if r.color == 0:
					Robot.game_over = True
				break
		return made_contact
