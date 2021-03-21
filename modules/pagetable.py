from math import ceil
import world
PAGETABLE_N = 30
ONETHIRD_PAGETABLE_N = PAGETABLE_N / 3

class PageTable:
	def __init__(self):
		self.table = []
		self.num_indices = None
		self.num_sub_indices = None
		
	# Takes an object 'obj' and used its member variables to compile a list of pointers to pages
	# that are nearby to the coordinate ('tile_x','tile_y'). If the coordinate is in the center of
	# the page, then the list will only include the page itself that the coordinate is within. If
	# the tile is within one-third a page from any edge, those pages can be included, too.
	#
	# ASSUMPTIONS:
	# -'obj' has member variables 'tile_x', 'tile_y', 'page_row', and 'page_col'.
	#
	def assemble_nearby_pages(self, obj, lst):
		x_mod = obj.tile_x % PAGETABLE_N
		y_mod = obj.tile_y % PAGETABLE_N
		if x_mod >= PAGETABLE_N - ONETHIRD_PAGETABLE_N:
			if y_mod >= PAGETABLE_N - ONETHIRD_PAGETABLE_N:
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row + 1, obj.page_col + 1))
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row + 1, obj.page_col))
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row, obj.page_col + 1))
			elif y_mod <= ONETHIRD_PAGETABLE_N:
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row - 1, obj.page_col + 1))
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row - 1, obj.page_col))
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row, obj.page_col + 1))
			else:
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row, obj.page_col + 1))
		elif x_mod <= ONETHIRD_PAGETABLE_N:
			if y_mod >= PAGETABLE_N - ONETHIRD_PAGETABLE_N:
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row + 1, obj.page_col - 1))
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row, obj.page_col - 1))
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row + 1, obj.page_col))
			elif y_mod <= ONETHIRD_PAGETABLE_N:
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row - 1, obj.page_col - 1))
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row, obj.page_col - 1))
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row - 1, obj.page_col))
			else:
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row, obj.page_col - 1))
		else:
			if y_mod >= PAGETABLE_N - ONETHIRD_PAGETABLE_N:
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row + 1, obj.page_col))
			elif y_mod <= ONETHIRD_PAGETABLE_N:
				lst.append(obj.pagetable.get_page_lstexc(obj.page_row - 1, obj.page_col))
		
	# Loads a blank pagetable for the respective 'world'.
	#
	# ASSUMPTIONS:
	# Every row in 'world.bgnd_tiles' has the same number of columns.
	#
	def load_blank(self, world):
		self.num_indices = int(ceil(len(world.bgnd_tiles) / float(PAGETABLE_N)))
		self.num_sub_indices = int(ceil(len(world.bgnd_tiles[0]) / float(PAGETABLE_N)))
		self.table = []
		index = 0
		while index < self.num_indices:
			self.table.append([])
			sub_index = 0
			while sub_index < self.num_sub_indices:
				self.table[index].append([])
				sub_index = sub_index + 1
			index = index + 1
	
	def get_num_rows(self):
		return self.num_indices
		
	def get_num_cols(self):
		return self.num_sub_indices
			
			
	def get_page(self, row, col):
		try:
			if row >= 0 and col >= 0:
				return self.table[row][col]
			else:
				return None
		except IndexError:
			return None
			
	def get_page_lstexc(self, row, col):
		try:
			if row >= 0 and col >= 0:
				return self.table[row][col]
			else:
				return []
		except IndexError:
			return []
		
	def set_page(self, row, col, lst = []):
		self.table[row][col] = lst
		
	def remove_obj_by_indices(self, row, col, index):
		del self.table[row][col][index]
	
	def remove_obj_by_ref(self, pageref, obj_to_del):
		index = 0
		num_indices = len(pageref)
		while index < num_indices:
			if pageref[index] == obj_to_del:
				del pageref[index]
				break
			index = index + 1
		
	def add_obj(self, row, col, obj):
		page_array = self.table[row][col]
		page_array.append(obj)
		return page_array