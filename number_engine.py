#
# AUTHOR: JEFFREY VIVIANI
# PART OF: Part of the NUWAYOUT arcade game.
# DESCRIPTION: Module and class for rendering numbers to then display.
#
from scaler import *
import pygame

class NumberEngine:
	screen = None;
	background_surface = None
	erase_rect = None
	fixed_char_spacing = None
	surface_width = None
	symbols_surfaces = {}
	symbols_rects = {}
	@classmethod
	def init_class(cls, screen, background_surface):
		cls.fixed_char_spacing = 20 * scl.scale_x
		cls.screen = screen
		cls.background_surface = background_surface
		cls.symbols_surfaces['0'] = scl.scale(pygame.image.load("Images/Numbers/0.png")).convert_alpha()
		cls.symbols_surfaces['1'] = scl.scale(pygame.image.load("Images/Numbers/1.png")).convert_alpha()
		cls.symbols_surfaces['2'] = scl.scale(pygame.image.load("Images/Numbers/2.png")).convert_alpha()
		cls.symbols_surfaces['3'] = scl.scale(pygame.image.load("Images/Numbers/3.png")).convert_alpha()
		cls.symbols_surfaces['4'] = scl.scale(pygame.image.load("Images/Numbers/4.png")).convert_alpha()
		cls.symbols_surfaces['5'] = scl.scale(pygame.image.load("Images/Numbers/5.png")).convert_alpha()
		cls.symbols_surfaces['6'] = scl.scale(pygame.image.load("Images/Numbers/6.png")).convert_alpha()
		cls.symbols_surfaces['7'] = scl.scale(pygame.image.load("Images/Numbers/7.png")).convert_alpha()
		cls.symbols_surfaces['8'] = scl.scale(pygame.image.load("Images/Numbers/8.png")).convert_alpha()
		cls.symbols_surfaces['9'] = scl.scale(pygame.image.load("Images/Numbers/9.png")).convert_alpha()
		cls.symbols_surfaces['.'] = scl.scale(pygame.image.load("Images/Numbers/decimal.png")).convert_alpha()
		
		
		cls.symbols_rects['0'] = cls.symbols_surfaces['0'].get_rect()
		cls.symbols_rects['1'] = cls.symbols_surfaces['1'].get_rect()
		cls.symbols_rects['2'] = cls.symbols_surfaces['2'].get_rect()
		cls.symbols_rects['3'] = cls.symbols_surfaces['3'].get_rect()
		cls.symbols_rects['4'] = cls.symbols_surfaces['4'].get_rect()
		cls.symbols_rects['5'] = cls.symbols_surfaces['5'].get_rect()
		cls.symbols_rects['6'] = cls.symbols_surfaces['6'].get_rect()
		cls.symbols_rects['7'] = cls.symbols_surfaces['7'].get_rect()
		cls.symbols_rects['8'] = cls.symbols_surfaces['8'].get_rect()
		cls.symbols_rects['9'] = cls.symbols_surfaces['9'].get_rect()
		cls.symbols_rects['.'] = cls.symbols_surfaces['.'].get_rect()
		
		cls.surface_width = cls.symbols_rects['0'].width
		cls.surface_height = cls.symbols_rects['0'].height
		
		cls.erase_rect = cls.symbols_rects['0']
	def __init__(self) :
		pass
	def print_right_justify(self, num, x, y):
		num = str(round(num, 1))
		num_chars = len(num)
		ch_index = num_chars
		while ch_index > 0:
			ch_index -= 1
			ch_order = num_chars - ch_index
			ch = num[ch_index]
			NumberEngine.erase_rect.left = x * scl.scale_x - NumberEngine.fixed_char_spacing * ch_order
			NumberEngine.erase_rect.top = y * scl.scale_y
			#Erase previous surface
			NumberEngine.screen.blit(NumberEngine.background_surface, NumberEngine.erase_rect, NumberEngine.erase_rect)
			NumberEngine.screen.blit(NumberEngine.symbols_surfaces[ch], NumberEngine.erase_rect)
