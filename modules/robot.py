import pygame
import random
from world import *
from laser import *
from pagetable import *
from pathfinder import *
from math import floor

class Robot:
	image_widths = [None]*15
	image_surfaces = [None]*15
	id_counter = 0
	def __init__(self, world, pagetable, type, personality, tile_x_init, tile_y_init):
		self.ai = True
		self.world = world
		self.pagetable = pagetable
		self.type = type
		self.base_costume = (type - 1) * 5
		self.costume = self.base_costume
		self.target = None
		self.path = None
		self.personality = personality
		if self.personality == 0:
			self.preferred_dist = random.randint(3,6)
		self.tile_x = tile_x_init
		self.x = tile_x_init * self.world.tile_pixel_w
		self.tile_y = tile_y_init
		self.y = tile_y_init * self.world.tile_pixel_h
		world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = self
		self.my_page = None
		self.calc_page()
		self.direction = 0
		self.pos_offset = 0
		self.frame = (0, 0)
		self.join_page()
		self.health = 10
		self.just_got_shot = False
		self.flicker_counter = 0
		self.flicker_state = 0
		self.id = Robot.id_counter
		self.control_state = 0
		self.movement_progress = 0
		self.dest_x = None
		self.dest_y = None
		self.diminish = 0
		self.tick = 0
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
		cls.image_surfaces[4] = world.scale(pygame.image.load("Images/Robots/blue_bits.png"))
		cls.image_widths[4] = 20 * world.scale_x
		
		cls.image_surfaces[5] = world.scale(pygame.image.load("Images/Robots/orange_right.png"))
		cls.image_widths[5] = 16 * world.scale_x
		cls.image_surfaces[6] = world.scale(pygame.image.load("Images/Robots/orange_front.png"))
		cls.image_widths[6] = 16 * world.scale_x
		cls.image_surfaces[7] = world.scale(pygame.image.load("Images/Robots/orange_left.png"))
		cls.image_widths[7] = 18 * world.scale_x
		cls.image_surfaces[8] = world.scale(pygame.image.load("Images/Robots/orange_back.png"))
		cls.image_widths[8] = 18 * world.scale_x
		cls.image_surfaces[9] = world.scale(pygame.image.load("Images/Robots/orange_bits.png"))
		cls.image_widths[9] = 20 * world.scale_x
		
		cls.image_surfaces[10] = world.scale(pygame.image.load("Images/Robots/red_right.png"))
		cls.image_widths[10] = 16 * world.scale_x
		cls.image_surfaces[11] = world.scale(pygame.image.load("Images/Robots/red_front.png"))
		cls.image_widths[11] = 16 * world.scale_x
		cls.image_surfaces[12] = world.scale(pygame.image.load("Images/Robots/red_left.png"))
		cls.image_widths[12] = 18 * world.scale_x
		cls.image_surfaces[13] = world.scale(pygame.image.load("Images/Robots/red_back.png"))
		cls.image_widths[13] = 18 * world.scale_x
		cls.image_surfaces[14] = world.scale(pygame.image.load("Images/Robots/red_bits.png"))
		cls.image_widths[14] = 20 * world.scale_x
		
		cls.step_size_x = int(floor(world.tile_pixel_w / 4))
		cls.step_size_y = int(floor(world.tile_pixel_h / 4))
		
	#should be called once per frame
	def automated_control(self):
		if self.diminish:
			if self.diminish == 1:
				self.costume = self.base_costume + 4
				self.diminish = 2
				return
			elif self.diminish == 2:
				self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = 0
				self.leave_page()
				return
		if self.flicker_counter > 0:
			self.flicker_counter = self.flicker_counter - 1
			if self.flicker_state == 0:
				self.flicker_state = 1
			else:
				self.flicker_state = 0
				
		# If a computer controlled robot
		#
		# ROBOT AI FUNCTIONALITY FULL DESCRIPTION
		# The AI for the robots is state oriented. There are higher order states and lower order
		# states for each of the higher order states. They are designed to represent similar
		# behavior to that of a real thought process.
		#
		# BASIC PERSONALITY
		# This is just the typical robot that tries to attack when it sees an enemy at mid-range. It will
		# not go to any extremes of the other personalities but is well-rounded.
		#
		# AGGRESSIVE PERSONALITY
		# These robots are more likely to charge head-on at their opponents. They will be less prudent
		# when weilding their weapons, so they certainly risk accidentally shooting a teammate.
		#
		# When choosing a target, an aggressive robot does not choose the most convenient opponent. It
		# may lock onto one specific opponent for no undersdtandable reason other than it feels like
		# going after that one. If one opponent has been particularly successful or appears to be quite
		# strong, it may be more likely to target that one.
		#
		# Of course, if anything gets too close to an aggressive robot, it is bound to take its eyes off
		# its target to target the nearby opponent.
		#
		# STEALTH PERSONALITY
		# These robots will usually try to attack from a distance or work their away around to try to get
		# an opponent from behind or the side. They can still handle close encounters but are more skillful
		# at range. When choosing a target, it is fairly random. How they go about hunting that target is discreetly.
		#
		# NERVOUS PERSONALITY
		# These robots are likely to run away when they encounter danger until they find a group of allies that
		# they can cluster to. They are less likely to even choose a target but are rather focuses on
		# self-preservation.
		#
		# WATCHGUARD PERSONALITY
		# These robots are most interesting in guarding an ear, particularly the area around which they spawn.
		# They may move a bit here and there but mostly hang out in one area.
		#
		# TRIBAL PERSONALITY
		# These robots seek out allies to hang out with. They may follow another robot as following a leader.
		# They may also go after the very robot who the followee is going after to double team.
		#
		# The personalities are permanent. For each personality then there are higher order states and lower
		# order states.
		if self.control_state == 0:
			if self.ai:
				personality = self.personality
				
				#BASIC PERSONALITY
				if personality == 0:
					#NO TARGET STATE
					if self.target == None:
						self.target = self.find_target(1, 0)
						self.tick = 0
					#HAS A TARGET STATE
					else:
						#Empty path currently
						if self.path == None:
							self.tick = self.tick - 1
							if self.tick == -1:
								if random.randint(0,2) == 0:
									self.tick = random.randint(10,40)
									if self.target_in_sight():
											self.fire()
								else:
									self.tick = 0
							if self.tick == 0:
								#Hunt down robot
								pfind = Pathfinder(self.world)
								x_off = self.target.tile_x - self.tile_x
								y_off = self.target.tile_y - self.tile_y
								if abs(x_off) > abs(y_off):
									if x_off < 0:
										self.path = pfind.find_path(self.tile_x, self.tile_y, self.target.tile_x + self.preferred_dist, self.target.tile_y, 20)
									else:
										self.path = pfind.find_path(self.tile_x, self.tile_y, self.target.tile_x - self.preferred_dist, self.target.tile_y, 20)
								else:
									if y_off < 0:
										self.path = pfind.find_path(self.tile_x, self.tile_y, self.target.tile_x, self.target.tile_y + self.preferred_dist, 20)
									else:
										self.path = pfind.find_path(self.tile_x, self.tile_y, self.target.tile_x, self.target.tile_y - self.preferred_dist, 20)
								#print("Path Found:")
								#print(self.path)
								self.path_index = 0
								self.path_index_end = len(self.path)
								self.reconsider_index = random.randint(2,6)
								if self.path_index_end == 0:
									self.path = None
									
							#Face general direction of robot
							off_x = self.tile_x - self.target.tile_x
							off_y = self.tile_y - self.target.tile_y
							if abs(off_x) >= abs(off_y):
								if off_x > 0:
									self.direction = 2
									self.costume = self.base_costume + 2
								else:
									self.direction = 0
									self.costume = self.base_costume + 0
							else:
								if off_y > 0:
									self.direction = 3
									self.costume = self.base_costume + 3
								else:
									self.direction = 1
									self.costume = self.base_costume + 1
						else:
							#Follow path:
							#print("Path index:")
							#print(self.path_index)
							if self.control_state == 0:
								self.try_move_dir(self.path[self.path_index])
								if self.control_state != 0:
									self.path_index = self.path_index + 1
									if self.path_index == self.reconsider_index or self.path_index == self.path_index_end:
										self.path = None
								else:
									self.path = None
							
			
			
				#Basic looking in different directions
				#if random.randint(0,50) == 0:
					#new_dir = random.randint(0,3)
					#self.direction = new_dir
					#self.costume = self.base_costume + new_dir
				
		#If in process of moving
		if self.control_state == 1:
			self.movement_progress = self.movement_progress + 1
			if self.movement_progress == 4:
				self.x = self.dest_x
				self.control_state = 0
			else:
				self.x = self.x + Robot.step_size_x
			return
		elif self.control_state == 2:
			self.movement_progress = self.movement_progress + 1
			if self.movement_progress == 4:
				self.y = self.dest_y
				self.control_state = 0
			else:
				self.y = self.y + Robot.step_size_y
			return
		elif self.control_state == 3:
			self.movement_progress = self.movement_progress + 1
			if self.movement_progress == 4:
				self.x = self.dest_x
				self.control_state = 0
			else:
				self.x = self.x - Robot.step_size_x
			return
		elif self.control_state == 4:
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
		
	def find_target(self, type, criteria):
		#Scan your page and any nearby pages for a potential target of type 'type'.
		pages_to_check = []
		self.pagetable.assemble_nearby_pages(self, pages_to_check)
		#Iterate over all robots in the pages and pick one based on the criteria
		#NEAREST
		if criteria == 0:
			pTarget = None #pTarget is potential target
			min_distance = 100
			for page in pages_to_check:
				for obj in page:
					if obj.type == type:
						distance = abs(self.tile_x - obj.tile_x) + abs(self.tile_y - obj.tile_y)
						if distance < min_distance:
							min_distance = distance
							pTarget = obj
			return pTarget
	
	def fire(self):
		Laser(self.world, self)
		
	def join_page(self):
		self.my_page = self.pagetable.add_obj(self.page_row,self.page_col,self)
	
	def leave_page(self):
		self.pagetable.remove_obj_by_ref(self.my_page, self)
			
	def get_shot(self):
		self.health = self.health - 1
		if self.health == 0:
			self.diminish = 1
		self.flicker_counter = 4
		self.flicker_state = 0
		
	def render(self):
		if self.flicker_state == 0:
			self.world.screen.blit(Robot.image_surfaces[self.costume], (self.x - self.world.camera_x, self.y - self.world.camera_y))
			
	def point_right(self):
		self.direction = 0
		self.costume = self.base_costume + 0
		
	def point_down(self):
		self.direction = 1
		self.costume = self.base_costume + 1
		
	def point_left(self):
		self.direction = 2
		self.costume = self.base_costume + 2
		
	def point_up(self):
		self.direction = 3
		self.costume = self.base_costume + 3
		
	def try_move_dir(self, dir):
		if dir == 0:
			self.try_move_right()
		elif dir == 1:
			self.try_move_down()
		elif dir == 2:
			self.try_move_left()
		elif dir == 3:
			self.try_move_up()
	
	#If capable, initiate rightward movement
	def try_move_right(self):
		if self.control_state == 0:
			#Point in direction
			self.point_right()
			#If free to move
			try:
				if self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x + 1] == 0:
					self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = 0
					self.tile_x = self.tile_x + 1
					self.dest_x = self.x + self.world.tile_pixel_w
					self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = self
					self.control_state = 1
					self.movement_progress = 0
					self.validate_page_col()
			except IndexError:
				return
				
	#If capable, initiate downward movement
	def try_move_down(self):
		if self.control_state == 0:
			#Point in direction
			self.point_down()
			#If free to move
			try:
				if self.world.occupancy[(self.tile_y + 1) * self.world.bgnd_tiles_width + self.tile_x] == 0:
					self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = 0
					self.tile_y = self.tile_y + 1
					self.dest_y = self.y + self.world.tile_pixel_h
					self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = self
					self.control_state = 2
					self.movement_progress = 0
					self.validate_page_row()
					
			except IndexError:
				return
				
	#If capable, initiate leftward movement
	def try_move_left(self):
		if self.control_state == 0:
			#Point in direction
			self.point_left()
			#If free to move
			try:
				if self.tile_x >= 1 and self.world.occupancy[(self.tile_y * self.world.bgnd_tiles_width) + self.tile_x - 1] == 0:
					self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = 0
					self.tile_x = self.tile_x - 1
					self.dest_x = self.x - self.world.tile_pixel_w
					self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = self
					self.control_state = 3
					self.movement_progress = 0
					self.validate_page_col()
					
			except IndexError:
				return
				
	#If capable, initiate upward movement
	def try_move_up(self):
		if self.control_state == 0:
			#Point in direction
			self.point_up()
			#If free to move
			try:
				if self.tile_y >= 1 and self.world.occupancy[(self.tile_y - 1)*self.world.bgnd_tiles_width + self.tile_x] == 0:
					self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = 0
					self.tile_y = self.tile_y - 1
					self.dest_y = self.y - self.world.tile_pixel_h
					self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + self.tile_x] = self
					self.control_state = 4
					self.movement_progress = 0
					self.validate_page_row()
			except IndexError:
				return
	
	#Checks if its page row is correct, and if not, changes it.
	def validate_page_row(self):
		old_page_row = self.page_row
		self.calc_page_row()
		if self.page_row != old_page_row:
			self.leave_page()
			self.join_page()
	
	#Checks if its page column is correct, and if not, changes it.
	def validate_page_col(self):
		old_page_col = self.page_col
		self.calc_page_col()
		if self.page_col != old_page_col:
			self.leave_page()
			self.join_page()
	
#Precondition: Must have a target
	def target_in_sight(self):
		if self.direction == 0:
			if self.target.tile_y == self.tile_y and self.target.tile_x > self.tile_x:
				tile_x_check = self.tile_x
				end = self.target.tile_x - 1
				while tile_x_check < end:
					tile_x_check = tile_x_check + 1
					if self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + tile_x_check] != 0:
						return False
				if tile_x_check == end:
					return True
		elif self.direction == 1:
			if self.target.tile_x == self.tile_x and self.target.tile_y > self.tile_y:
				tile_y_check = self.tile_y
				end = self.target.tile_y - 1
				while tile_y_check < end:
					tile_y_check = tile_y_check + 1
					if self.world.occupancy[tile_y_check * self.world.bgnd_tiles_width + self.tile_x] != 0:
						return False
				if tile_y_check == end:
					return True
		elif self.direction == 2:
			if self.target.tile_y == self.tile_y and self.target.tile_x < self.tile_x:
				tile_x_check = self.tile_x
				end = self.target.tile_x + 1
				while tile_x_check > end:
					tile_x_check = tile_x_check - 1
					if self.world.occupancy[self.tile_y * self.world.bgnd_tiles_width + tile_x_check] != 0:
						return False
				if tile_x_check == end:
					return True
		elif self.direction == 3:
			if self.target.tile_x == self.tile_x and self.target.tile_y < self.tile_y:
				tile_y_check = self.tile_y
				end = self.target.tile_y + 1
				while tile_y_check > end:
					tile_y_check = tile_y_check - 1
					if self.world.occupancy[tile_y_check * self.world.bgnd_tiles_width + self.tile_x] != 0:
						return False
				if tile_y_check == end:
					return True
		return False