from math import ceiling
import world
PAGETABLE_N = 30

class PageTable:
	def __init__(self):
		self.table = []
		
	def load_blank(self, world):
		num_indices = ceiling(len(world.bgnd_tiles) / PAGETABLE_N)
		num_sub_indices = ceiling(len(world.bgnd_tiles[0]) / PAGETABLE_N)
		self.table = []
		index = 0
		while index < num_indices:
			self.table.append([])
			sub_index = 0
			while sub_index < num_sub_indices:
				self.table[index].append([])
				sub_index = sub_index + 1
			index = index + 1
			
	def get_page(row, col):
		return self.table[row][col]
		
	def set_page(row, col, lst = []):
		self.table[row][col] = lst
		
	def remove_obj(row, col, index):
		del self.table[row][col][index]
		
	def add_obj(row, col, obj):
		self.table[row][col].append(obj)