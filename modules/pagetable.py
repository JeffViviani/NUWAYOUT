from math import ceil
import world
PAGETABLE_N = 30
ONETHIRD_PAGETABLE_N = PAGETABLE_N / 3

class PageTable:
	def __init__(self):
		self.table = []
		self.num_indices = None
		self.num_sub_indices = None
		
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