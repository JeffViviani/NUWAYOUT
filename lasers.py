import pygame, scaler
from robots import *

class Laser:
	registry = []
	image_vertical = None
	image_horizontal = None
	
	@classmethod
	def init_scaled_surfaces(cls):
		cls.image_vertical = scl.scale(pygame.image.load("Images/Projectiles/laser_vertical.png"))
		cls.image_horizontal = scl.scale(pygame.image.load("Images/Projectiles/laser_horizontal.png"))
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
			self.width = 10
			self.height = 6
		else:
			self.image = Laser.image_vertical
			self.width = 6
			self.height = 10
		self.grid_to_coordinates()
		self.rect = pygame.Rect(self.pos_x,self.pos_y,self.width,self.height)
		self.sound.play()
		self.draw()
	def move(self):
		self.vanish_from(self.background)
		if self.dir == 0:
			self.rect.left += 6
			if self.rect.left >= self.screen.get_width() - 28 - self.width:
				self.delete()
		elif self.dir == 1:
			self.rect.top += 6
			if self.rect.top >= self.screen.get_height() - 25 - self.height:
				self.delete()
		elif self.dir == 2:
			self.rect.left -= 6
			if self.rect.left <= 27 + self.width:
				self.delete()
		elif self.dir == 3:
			self.rect.top -= 6
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
