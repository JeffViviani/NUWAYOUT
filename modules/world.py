from math import floor
from copy import deepcopy
import pygame
from filestream import *

GAME_NATIVE_W = 576.0
GAME_NATIVE_H = 432.0

PRINT_WIDTH = 30
PRINT_HEIGHT = 23

class World:
	def __init__(self, screen):
		self.screen = screen
		self.camera_x = None
		self.camera_y = None
		self.bgnd_tiles = []
		self.bgnd_tiles_width = None
		self.bgnd_tiles_height = None
		self.occupancy = []
		self.displayInfo = pygame.display.Info()
		self.scale_x = self.displayInfo.current_w / GAME_NATIVE_W
		self.scale_y = self.displayInfo.current_h / GAME_NATIVE_H
		self.last_tile_x_init = None
		self.last_tile_y_init = None
		self.tile_surfaces = [None] * 100
		self.tile_surfaces[0] = self.scale(pygame.image.load("Images/Tiles/tile0.png"))
		self.tile_surfaces[1] = self.scale(pygame.image.load("Images/Tiles/tile1.png"))
		self.tile_surfaces[50] = self.scale(pygame.image.load("Images/Tiles/tile50.png"))
		self.tile_surfaces[51] = self.scale(pygame.image.load("Images/Tiles/tile51.png"))
		self.tile_pixel_w = int(floor(20 * self.scale_x))
		self.tile_pixel_h = int(floor(20 * self.scale_y))
		self.camera_focus_offset_x = int(floor(0 - self.tile_pixel_w * 13.5))
		self.camera_focus_offset_y = int(floor(0 - self.tile_pixel_h * 10.5))
		self.frame = pygame.Rect(0, 0, self.tile_pixel_w, self.tile_pixel_h)
		self.render_panel = pygame.Surface((self.tile_pixel_w * PRINT_WIDTH, self.tile_pixel_h * PRINT_HEIGHT))
		self.render_panel_temp = self.render_panel.copy()
		
	def load_world(self, file):
		self.bgnd_tiles, self.bgnd_tiles_width, self.bgnd_tiles_height = file_to_fake_2D_list_ints(file)
		#print(len(self.bgnd_tiles))
		self.occupancy = deepcopy(self.bgnd_tiles)
		list_consolidate(self.occupancy, 1, 0, 9)
		zero_list(self.occupancy)
		
	def scale(self, surface):
		current_w = surface.get_width()
		current_h = surface.get_height()
		return pygame.transform.scale(surface,(int(floor(current_w * self.scale_x)), int(floor(current_h * self.scale_y))))
		
	def focus_camera(self, robot):
		self.camera_x = robot.x + self.camera_focus_offset_x
		self.camera_y = robot.y + self.camera_focus_offset_y
		
	def render_partial(self):
		tile_y_pos_init = int(floor(self.camera_y / self.tile_pixel_h))
		tile_x_pos_init = int(floor(self.camera_x / self.tile_pixel_w))
		if tile_x_pos_init > self.last_tile_x_pos_init:
			self.last_tile_x_pos_init = tile_x_pos_init
			#Shift the render_pane one tile to the left
			self.render_panel_temp.blit(self.render_panel, (0 - self.tile_pixel_w, 0))
			self.render_panel.blit(self.render_panel_temp, (0,0))
			#Render the new rightmost column
			index = self.bgnd_tiles_width * tile_y_pos_init + tile_x_pos_init + PRINT_WIDTH - 1
			frame = self.frame
			frame.left = self.tile_pixel_w * (PRINT_WIDTH - 1)
			frame.top = 0
			
			cnt = 0
			while(cnt < PRINT_HEIGHT):
				tile_to_blit = None
				if index > 0 and index < len(self.bgnd_tiles):
					tile_to_blit = self.tile_surfaces[self.bgnd_tiles[index]]
				else:
					tile_to_blit = self.tile_surfaces[3]
				self.render_panel.blit(tile_to_blit, frame)
				cnt = cnt + 1
				index = index + self.bgnd_tiles_width
				frame.top = frame.top + self.tile_pixel_h
		elif tile_x_pos_init < self.last_tile_x_pos_init:
			self.last_tile_x_pos_init = tile_x_pos_init
			#Shift the render_pane one tile to the right
			self.render_panel_temp.blit(self.render_panel, (self.tile_pixel_w, 0))
			self.render_panel.blit(self.render_panel_temp, (0,0))
			#Render the new leftmost column
			index = self.bgnd_tiles_width * tile_y_pos_init + tile_x_pos_init
			frame = self.frame
			frame.left = 0
			frame.top = 0
			
			cnt = 0
			while(cnt < PRINT_HEIGHT):
				tile_to_blit = None
				if index > 0 and index < len(self.bgnd_tiles):
					tile_to_blit = self.tile_surfaces[self.bgnd_tiles[index]]
				else:
					tile_to_blit = self.tile_surfaces[3]
				self.render_panel.blit(tile_to_blit, frame)
				cnt = cnt + 1
				index = index + self.bgnd_tiles_width
				frame.top = frame.top + self.tile_pixel_h
			
		elif tile_y_pos_init > self.last_tile_y_pos_init:
			self.last_tile_y_pos_init = tile_y_pos_init
			#Shift the render_pane one tile up
			self.render_panel_temp.blit(self.render_panel, (0, 0 - self.tile_pixel_h))
			self.render_panel.blit(self.render_panel_temp, (0,0))
			#Render the new leftmost column
			index = self.bgnd_tiles_width * (tile_y_pos_init + PRINT_HEIGHT - 1) + tile_x_pos_init
			frame = self.frame
			frame.left = 0
			frame.top = self.tile_pixel_h * (PRINT_HEIGHT - 1)
			
			cnt = 0
			while(cnt < PRINT_WIDTH):
				tile_to_blit = None
				if index > 0 and index < len(self.bgnd_tiles):
					tile_to_blit = self.tile_surfaces[self.bgnd_tiles[index]]
				else:
					tile_to_blit = self.tile_surfaces[3]
				self.render_panel.blit(tile_to_blit, frame)
				cnt = cnt + 1
				index = index + 1
				frame.left = frame.left + self.tile_pixel_w
		elif tile_y_pos_init < self.last_tile_y_pos_init:
			self.last_tile_y_pos_init = tile_y_pos_init
			#Shift the render_pane one tile down
			self.render_panel_temp.blit(self.render_panel, (0, self.tile_pixel_h))
			self.render_panel.blit(self.render_panel_temp, (0,0))
			#Render the new topmost column
			index = self.bgnd_tiles_width * (tile_y_pos_init) + tile_x_pos_init
			frame = self.frame
			frame.left = 0
			frame.top = 0
			
			cnt = 0
			while(cnt < PRINT_WIDTH):
				tile_to_blit = None
				if index > 0 and index < len(self.bgnd_tiles):
					tile_to_blit = self.tile_surfaces[self.bgnd_tiles[index]]
				else:
					tile_to_blit = self.tile_surfaces[3]
				self.render_panel.blit(tile_to_blit, frame)
				cnt = cnt + 1
				index = index + 1
				frame.left = frame.left + self.tile_pixel_w
		self.screen.blit(self.render_panel, (0 - self.camera_x % self.tile_pixel_w, 0 - self.camera_y % self.tile_pixel_h))

	def render_full(self):
		#Begin one tile to the left
		dark_tile = self.tile_surfaces[50]
		#frame = self.frame
		#frame_left_init = 0 - (self.camera_x % self.tile_pixel_w)
		#frame.left = frame_left_init
		#frame.top = 0 - self.camera_y % self.tile_pixel_h
		frame = self.frame
		frame_left_init = 0
		frame.left = frame_left_init
		frame.top = 0
		
		tile_y_pos_init = int(floor(self.camera_y / self.tile_pixel_h))
		tile_x_pos_init = int(floor(self.camera_x / self.tile_pixel_w))
		self.last_tile_x_pos_init = tile_x_pos_init
		self.last_tile_y_pos_init = tile_y_pos_init
		#print(len(self.bgnd_tiles))
		
		arr_index_init = 0
		arr_jump_size = 0
		
		shadow_jump_index = None
		shadow_jump_amnt = None
		shadow_end = None
		shadow_index = 0
		
		newline_index = PRINT_WIDTH
		end_index = PRINT_WIDTH * PRINT_HEIGHT
		
		if tile_y_pos_init < 0:
			
			#Camera view contains region above the top of the map.
			shadow_index = 0
			
			if tile_x_pos_init < 0:
			
				# Beyond top-left corner of map. In this circumstance, there has to be
				# a shadow for the area beyond the borders of the map. EVentually, once the
				# shadow reaches the physical map, it has to jump. To exemplify this, consider
				# the visual below which represents a camera than encapsulated a 7x7 tile
				# grid. "X"s represent tiles outside the map, and "O"s represent tiles inside
				# the map.
				
				# X X X X X X X
				# X X X X X X X
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				
				# The shadow needs configured such that it will be present for all of the
				# "X"s and absent for all of the "O"s. The tile below that is marked "J"
				# is the tile at which the shadow needs to jump:
				
				# X X X X X X X
				# X X X X X X X
				# X J O O O O O
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				
				# The 'shadow_jump_index' variable is to be calculated as the index of J
				# for the given hard-coded tile dimensions of the world camera view. In the
				# above example, 'tile_x_pos' would be -2, and 'tile_y_pos' would also be -2.
				# This is known because the to-left corner value in the aboce is 2 offset
				# on both axes from the top-left corner of the physical world.
				
				# The process of rendering is iterative, and there is an index that counts from
				# 0 upward for each consecutive tile. The count goes like so:
				
				# 0 1 2 3 4 5 6
				# 7 8 9 .......
				# .............
				
				# In the above example, the 'J' would be at index 15.
				
				# The dimensions of the actual camera are 34 tiles WIDE and 28 tiles HIGH.
				# With this knowledge, the formulas below are derived:
				
				shadow_jump_index = PRINT_WIDTH * (0 - tile_y_pos_init) - 1 - tile_x_pos_init
				shadow_jump_amnt = PRINT_WIDTH + tile_x_pos_init + 1
				arr_jump_size = self.bgnd_tiles_width - PRINT_WIDTH - tile_x_pos_init + 1
				#shadow_end = -1
				
			elif tile_x_pos_init < self.bgnd_tiles_width - PRINT_WIDTH:
			
				# Situation is as follows:
				
				# X X X X X X X
				# X X X X X X X
				# O O O O O O O
				# O O O O O O O
				# O O O O O O O
				# O O O O O O O
				# O O O O O O O
				
				# In this case, once the shadow reaches the final 'X', there is
				# no more need of the shadow.
				
				arr_index_init = tile_x_pos_init
				shadow_jump_index = PRINT_WIDTH * (0 - tile_y_pos_init) - 1
				shadow_jump_amnt = 0
				arr_jump_size = self.bgnd_tiles_width - PRINT_WIDTH
				
			else:
			
				# Situation is as follows:
				
				# X X X X X X X
				# X X X X X X X
				# O O O O O X X
				# O O O O O X X
				# O O O O O X X
				# O O O O O X X
				# O O O O O X X
			
				shadow_jump_index = PRINT_WIDTH * (0 - tile_y_pos_init) + tile_x_pos_init + PRINT_WIDTH
				shadow_jump_amnt = PRINT_WIDTH + 1 - tile_x_pos_init + PRINT_WIDTH - self.bgnd_tiles_width
				arr_jump_size = self.bgnd_tiles_width + self.bgnd_tiles_width - tile_x_pos_init + PRINT_WIDTH
				
		elif tile_y_pos_init < self.bgnd_tiles_height - PRINT_HEIGHT:
			
			if tile_x_pos_init < 0:
			
				# Situation is as follows:
				
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				# X X O O O O O
				
				arr_index_init = tile_y_pos_init * self.bgnd_tiles_width
				shadow_jump_index = 0 - tile_x_pos_init - 1
				shadow_jump_amnt = PRINT_WIDTH + tile_x_pos_init + 1
				arr_jump_size = self.bgnd_tiles_width - PRINT_WIDTH - tile_x_pos_init
				
			elif tile_x_pos_init < self.bgnd_tiles_width - PRINT_WIDTH:
			
				# Situation is as follows:
				
				# O O O O O O O
				# O O O O O O O
				# O O O O O O O
				# O O O O O O O
				# O O O O O O O
				# O O O O O O O
				# O O O O O O O
				
				shadow_index = -1
				arr_index_init = tile_y_pos_init * self.bgnd_tiles_width + tile_x_pos_init
				arr_jump_size = self.bgnd_tiles_width - PRINT_WIDTH
					
		index = 0
		arr_index = arr_index_init
		#print("START")
		while True:
			#print("Index: " + str(index))
			if index == shadow_index:
				#print("SHADOW!")
				tile_to_blit = dark_tile
				if shadow_index == shadow_jump_index:
					#print("SHADOW JUMPS! By value " + str(shadow_jump_amnt))
					shadow_jump_index = shadow_index + PRINT_WIDTH
					shadow_index = shadow_index + shadow_jump_amnt
				else:
					shadow_index = shadow_index + 1
			else:
				#print("Print tile at array index " + str(arr_index))
				tile_to_blit = self.tile_surfaces[self.bgnd_tiles[arr_index]]
				arr_index = arr_index + 1
			self.render_panel.blit(tile_to_blit, frame)
			frame = frame.move(self.tile_pixel_w, 0)
			index = index + 1
			if index == newline_index:
				if newline_index == end_index:
					break
				#print("NEWLINE")
				if(arr_index > arr_index_init):
					#print("arr_index jumps by 1 plus " + str(arr_jump_size))
					arr_index = arr_index + arr_jump_size
				newline_index = newline_index + PRINT_WIDTH
				frame.left = frame_left_init
				frame.top = frame.top + self.tile_pixel_h
		self.screen.blit(self.render_panel, (0 - self.camera_x % self.tile_pixel_w, 0 - self.camera_y % self.tile_pixel_h))
			
	def pan(self, x_shift, y_shift):
		self.camera_x = self.camera_x + x_shift
		self.camera_y = self.camera_y + y_shift

def zero_list(lst):
	for i in lst:
		if isinstance(i, list):
			zero_list(i)
		else:
			i = 0
