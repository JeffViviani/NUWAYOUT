# Pathfinder class utilized by the robots. Used a custom search algorithm inspired
# by A* and Dijkstra's algorithms. A "path" is sent as represented as a raw list
# of integers denoting RIGHT, DOWN, LEFT, and UP as instructions for the receiver
# of the path (e.g. a robot) to follow over a period of time. It contains the
# following members:
#
# nodeQueue - A priority queue consisting of all the nodes that are part of the search algorithm.
class Pathfinder:
	def __init__(self, world):
		self.world = world
		self.nodeQueue = OrderedList()
	
	#A* search algorithm
	def find_path(self, tile_x_orig, tile_y_orig, tile_x_dest, tile_y_dest, max_dist):
		self.tile_x_orig = tile_x_orig
		self.tile_y_orig = tile_y_orig
		self.tile_x_dest = tile_x_dest
		self.tile_y_dest = tile_y_dest
		#if tile_x_orig == tile_x_dest and tile_y_orig == tile_y_dest:
			#print("PATH MATCH ALREADY")
		#print("Go from (" + str(tile_x_orig) + "," + str(tile_y_orig) + ") to (" + str(tile_x_dest) + "," + str(tile_y_dest) + ")")
		self.off_tile_x_dest = self.tile_x_dest - self.tile_x_orig
		self.off_tile_y_dest = self.tile_y_dest - self.tile_y_orig
		self.max_dist = max_dist
		tile_queue = OrderedList()
		double_max_dist = max_dist + max_dist
		#Generate the open list. The size is determined by `max_dist`.
		self.node_arr = [[None for i in range(double_max_dist + 1 )] for j in range(double_max_dist + 1)]
		#Generate the starting node
		nxtup = PathNode(None, None, self)
		tile_queue.add(nxtup)
		
		self.final_node = None
		
		calculated_path = []
		#Generate successors to starting tile and continue process until destination is reached
		
		while not tile_queue.empty():
			nxtup = tile_queue.pop()
			if nxtup.valid:
				tile_queue.add(nxtup.sprout_right())
				tile_queue.add(nxtup.sprout_down())
				tile_queue.add(nxtup.sprout_left())
				tile_queue.add(nxtup.sprout_up())
			if self.final_node != None:
				#Backtrack from the final node to calculate the path
				node = self.final_node
				while node.previousNode != None:
					calculated_path.insert(0, node.direction)
					node = node.previousNode
				break
		#print(calculated_path)
		#if tile_x_orig == tile_x_dest and tile_y_orig == tile_y_dest:
			#print(calculated_path)
		return calculated_path
		
		
# Represents a single node in a path. It contains the following members:
#
# lastNode - A pointer to the node from which this node came. This is useful for
#     performing backtracking once a complete path from source to destination is
#     found.
class PathNode:
	def __init__(self, previousNode, direction, path=None):
		self.valid = False
		if previousNode == None:
			self.previousNode = None
			self.direction = None
			self.path = path
			self.path.node_arr[0][0] = self
			#
			# self.off_tile_x - Represents the x offset from the starting tile.
			# self.off_tile_y - Represents the y offset from the starting tile.
			#
			self.off_tile_x = 0
			self.off_tile_y = 0
			self.g = 0
			self.calc_f()
			self.valid = True
		else:
			self.previousNode = previousNode
			self.direction = direction
			self.path = self.previousNode.path
			if self.direction == 0:
				self.off_tile_x = previousNode.off_tile_x + 1
				self.off_tile_y = previousNode.off_tile_y
			elif self.direction == 1:
				self.off_tile_x = previousNode.off_tile_x
				self.off_tile_y = previousNode.off_tile_y + 1
			elif self.direction == 2:
				self.off_tile_x = previousNode.off_tile_x - 1
				self.off_tile_y = previousNode.off_tile_y
			elif self.direction == 3:
				self.off_tile_x = previousNode.off_tile_x
				self.off_tile_y = previousNode.off_tile_y - 1
			tmp = self.path.max_dist
			if abs(self.off_tile_x) <= tmp and abs(self.off_tile_y) <= tmp:
				curHolder = self.path.node_arr[self.off_tile_y][self.off_tile_x]
				self.g = previousNode.g + 1
				self.calc_f()
				if curHolder == None or self.f < curHolder.f:
					if curHolder != None:
						curHolder.valid = False
					self.valid = True
					self.path.node_arr[self.off_tile_y][self.off_tile_x] = self
					if self.off_tile_x == self.path.off_tile_x_dest and self.off_tile_y == self.path.off_tile_y_dest:
						self.path.final_node = self
					
			
	def calc_f(self):
		self.f = self.g + abs(self.path.off_tile_x_dest - self.off_tile_x) + abs(self.path.off_tile_y_dest - self.off_tile_y)
			
	def sprout_right(self):
		tentative_x_off = self.off_tile_x + 1
		tentative_y_off = self.off_tile_y
		try:
			if self.path.world.occupancy[self.path.tile_y_orig + tentative_y_off][self.path.tile_x_orig + tentative_x_off] == 0 or (tentative_x_off == self.path.off_tile_x_dest and tentative_y_off == self.path.off_tile_y_dest):
				return PathNode(self, 0)
			else:
				return None
		except IndexError:
			return None
		
	def sprout_down(self):
		tentative_x_off = self.off_tile_x
		tentative_y_off = self.off_tile_y + 1
		try:
			if self.path.world.occupancy[self.path.tile_y_orig + tentative_y_off][self.path.tile_x_orig + tentative_x_off] == 0 or (tentative_x_off == self.path.off_tile_x_dest and tentative_y_off == self.path.off_tile_y_dest):
				return PathNode(self, 1)
			else:
				return None
		except IndexError:
			return None
		
	def sprout_left(self):
		tentative_x_off = self.off_tile_x - 1
		tentative_y_off = self.off_tile_y
		try:
			if self.path.world.occupancy[self.path.tile_y_orig + tentative_y_off][self.path.tile_x_orig + tentative_x_off] == 0 or (tentative_x_off == self.path.off_tile_x_dest and tentative_y_off == self.path.off_tile_y_dest):
				return PathNode(self, 2)
			else:
				return None
		except IndexError:
			return None
	
	def sprout_up(self):
		tentative_x_off = self.off_tile_x
		tentative_y_off = self.off_tile_y - 1
		try:
			if self.path.world.occupancy[self.path.tile_y_orig + tentative_y_off][self.path.tile_x_orig + tentative_x_off] == 0 or (tentative_x_off == self.path.off_tile_x_dest and tentative_y_off == self.path.off_tile_y_dest):
				return PathNode(self, 3)
			else:
				return None
		except IndexError:
			return None

#Class that acts as a custom implemented priority queue, with the priority favoring the node
#with the lowest f value. Actual implementation is done with a simple list.
class OrderedList:
	#index 0 is a value that is half of 0, index 1 is a value that is half of 1, etc.
	#Because division in hardware is inefficient, this is a more efficient process.
	half_size = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 23,
	                24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31]

	def __init__(self):
		#The highest element (rightmost) in a list is in the front of the virtual queue. This is more efficient for popping than
		#using the left.
		self.lst = []
		self.size = 0
	
	def add(self, node):
		if node != None:
			if node.valid == True:
				f = node.f
				half_size = self.size // 2#OrderedList.half_size[self.size]
				span = self.size
				index = half_size
				while span > 0:
					span = span // 2#OrderedList.half_size[span]
					if f >= self.lst[index].f:
						index = index - (span // 2)#OrderedList.half_size[span]
					else:
						index = index + (span // 2)#OrderedList.half_size[span]
				self.lst.insert(index, node)
				self.size = self.size + 1
	
	def pop(self):
		self.size = self.size - 1
		return self.lst.pop(self.size)
		
	def empty(self):
		return (self.size == 0)