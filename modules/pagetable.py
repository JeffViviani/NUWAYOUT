from math import ceil
import world
PAGETABLE_N = 30

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
			return self.table[row][col]
		except IndexError:
			return None
		
	def set_page(self, row, col, lst = []):
		self.table[row][col] = lst
		
	def remove_obj(self, row, col, index):
		del self.table[row][col][index]
		
	def add_obj(self, row, col, obj):
		self.table[row][col].append(obj)