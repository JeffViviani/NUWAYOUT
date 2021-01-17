from world import *
from math import floor
import pygame

class Typewriter:
	charbank = {}
	letter_width = None
	letter_height = None
	
	def __init__(self, world):
		self.world = world
	
	@classmethod
	def init_class(cls, world):
		cls.charbank[' '] = world.scale(pygame.image.load("Images/font/space.png"))
		cls.charbank[','] = world.scale(pygame.image.load("Images/font/comma.png"))
		cls.charbank['.'] = world.scale(pygame.image.load("Images/font/period.png"))
		cls.charbank['A'] = world.scale(pygame.image.load("Images/font/A.png"))
		cls.charbank['B'] = world.scale(pygame.image.load("Images/font/B.png"))
		cls.charbank['C'] = world.scale(pygame.image.load("Images/font/C.png"))
		cls.charbank['D'] = world.scale(pygame.image.load("Images/font/D.png"))
		cls.charbank['E'] = world.scale(pygame.image.load("Images/font/E.png"))
		cls.charbank['F'] = world.scale(pygame.image.load("Images/font/F.png"))
		cls.charbank['G'] = world.scale(pygame.image.load("Images/font/G.png"))
		cls.charbank['H'] = world.scale(pygame.image.load("Images/font/H.png"))
		cls.charbank['I'] = world.scale(pygame.image.load("Images/font/I.png"))
		cls.charbank['J'] = world.scale(pygame.image.load("Images/font/J.png"))
		cls.charbank['K'] = world.scale(pygame.image.load("Images/font/K.png"))
		cls.charbank['L'] = world.scale(pygame.image.load("Images/font/L.png"))
		cls.charbank['M'] = world.scale(pygame.image.load("Images/font/M.png"))
		cls.charbank['N'] = world.scale(pygame.image.load("Images/font/N.png"))
		cls.charbank['O'] = world.scale(pygame.image.load("Images/font/O.png"))
		cls.charbank['P'] = world.scale(pygame.image.load("Images/font/P.png"))
		cls.charbank['Q'] = world.scale(pygame.image.load("Images/font/Q.png"))
		cls.charbank['R'] = world.scale(pygame.image.load("Images/font/R.png"))
		cls.charbank['S'] = world.scale(pygame.image.load("Images/font/S.png"))
		cls.charbank['T'] = world.scale(pygame.image.load("Images/font/T.png"))
		cls.charbank['U'] = world.scale(pygame.image.load("Images/font/U.png"))
		cls.charbank['V'] = world.scale(pygame.image.load("Images/font/V.png"))
		cls.charbank['W'] = world.scale(pygame.image.load("Images/font/W.png"))
		cls.charbank['X'] = world.scale(pygame.image.load("Images/font/X.png"))
		cls.charbank['Y'] = world.scale(pygame.image.load("Images/font/Y.png"))
		cls.charbank['Z'] = world.scale(pygame.image.load("Images/font/Z.png"))
		cls.letter_width = int(floor(5 * world.scale_x))
		cls.letter_height = int(floor(9 * world.scale_y))
		cls.letter_spacing = int(floor(world.scale_x))
		
	def set_cursor(self, x, y):
		self.cursor_x = x
		self.cursor_y = y
	
	def newline(self):
		self.cursor_x = Typewriter.letter_width
		self.cursor_y = self.cursor_y + Typewriter.letter_height + Typewriter.letter_spacing * 2
	
	def print(self, char):
		if char == '\r':
			return
		if char == '\n':
			self.newline()
			return
		self.world.screen.blit(Typewriter.charbank[char],(self.cursor_x, self.cursor_y))
		if self.cursor_x + Typewriter.letter_width + Typewriter.letter_width > self.world.displayInfo.current_w:
			self.newline()
		else:
			self.cursor_x = self.cursor_x + Typewriter.letter_width + Typewriter.letter_spacing