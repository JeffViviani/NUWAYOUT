import pygame
from scaler import *

class DoorManager:
	def __init__(self, screen, background):
		self.screen = screen
		self.background = background
		self.doors = [Door(screen,background,1,0), Door(screen,background,0,1),Door(screen,background,1,2),Door(screen,background,0,3)]
		for d in self.doors:
			d.draw()
	def operate_doors(self):
		for d in self.doors:
			d.open_close_motion()
	def refresh_doors(self):
		for d in self.doors:
			d.refresh()
class Door:
	image_surfaces = [None]*6
	grid_x = [26, 11, -1, 11]
	grid_y = [7, 19, 7, -1]
	def __init__(self,screen,background,orientation,id):
		self.screen = screen
		self.background = background
		self.orientation = orientation
		self.id = id
		self.state = 0
		self.open_close = None
		self.update_image()
		self.rect = self.image.get_rect() #rect doesn't ever change for doors, unlike robots and lasers
		self.grid_x = Door.grid_x[self.id]
		self.grid_y = Door.grid_y[self.id]
		coordinates = self.grid_to_coordinates()
		self.rect.left = coordinates[0]
		self.rect.top = coordinates[1]
		
	@classmethod
	def init_scaled_surfaces(cls):
		cls.image_surfaces[0] = scl.scale(pygame.image.load("Images/Doors/Horizontal/s0.png")).convert_alpha()
		cls.image_surfaces[1] = scl.scale(pygame.image.load("Images/Doors/Horizontal/s1.png")).convert_alpha()
		cls.image_surfaces[2] = scl.scale(pygame.image.load("Images/Doors/Horizontal/s2.png")).convert_alpha()
		cls.image_surfaces[3] = scl.scale(pygame.image.load("Images/Doors/Vertical/s0.png")).convert_alpha()
		cls.image_surfaces[4] = scl.scale(pygame.image.load("Images/Doors/Vertical/s1.png")).convert_alpha()
		cls.image_surfaces[5] = scl.scale(pygame.image.load("Images/Doors/Vertical/s2.png")).convert_alpha()
		
		#cls.image_surfaces[0].set_colorkey((255,255,255), pygame.RLEACCEL)
		#cls.image_surfaces[1].set_colorkey((255,255,255), pygame.RLEACCEL)
		#cls.image_surfaces[2].set_colorkey((255,255,255), pygame.RLEACCEL)
		#cls.image_surfaces[3].set_colorkey((255,255,255), pygame.RLEACCEL)
		#cls.image_surfaces[4].set_colorkey((255,255,255), pygame.RLEACCEL)
		#cls.image_surfaces[5].set_colorkey((255,255,255), pygame.RLEACCEL)

	def update_image(self):
		_surface_index = self.orientation * 3 + self.state
		self.image = Door.image_surfaces[_surface_index]
	def vanish(self):
		self.screen.blit(self.background,self.rect,self.rect)
	def draw(self):
		self.screen.blit(self.image,self.rect)
	def grid_to_coordinates(self):
		return [(self.grid_x * 20 + 28) * scl.scale_x, (self.grid_y * 20 + 26) * scl.scale_y]
	def open(self):
		if self.open_close == None:
			self.open_close = "Open"
	def refresh(self):
		self.vanish()
		self.update_image()
		self.draw()
	def open_close_motion(self):
		if self.open_close != None:
			if self.open_close == "Open":
				self.state += 1
				if self.state == 2:
					self.open_close = "Close"
			else:
				self.state -= 1
				if self.state == 0:
					self.open_close = None
