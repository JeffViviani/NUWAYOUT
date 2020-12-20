class Robot:
	image_widths = [None]*12
	image_surfaces = [None]*12
	def __init__(self, world, pagetable, type, tile_x_init, tile_y_init):
		self.world = world
		self.pagetable = pagetable
		self.type = type
		self.tile_x = tile_x_init
		self.tile_y = tile_y_init
		
	
	@classmethod
	def init_class(cls):
		cls.image_surfaces[0] = scl.scale(pygame.image.load("Images/Robots/blue_right.png")).convert_alpha()
		cls.image_widths[0] = 16
		cls.image_surfaces[1] = scl.scale(pygame.image.load("Images/Robots/blue_front.png")).convert_alpha()
		cls.image_widths[1] = 16
		cls.image_surfaces[2] = scl.scale(pygame.image.load("Images/Robots/blue_left.png")).convert_alpha()
		cls.image_widths[2] = 18
		cls.image_surfaces[3] = scl.scale(pygame.image.load("Images/Robots/blue_back.png")).convert_alpha()
		cls.image_widths[3] = 18
		cls.image_surfaces[4] = scl.scale(pygame.image.load("Images/Robots/orange_right.png")).convert_alpha()
		cls.image_widths[4] = 16
		cls.image_surfaces[5] = scl.scale(pygame.image.load("Images/Robots/orange_front.png")).convert_alpha()
		cls.image_widths[5] = 16
		cls.image_surfaces[6] = scl.scale(pygame.image.load("Images/Robots/orange_left.png")).convert_alpha()
		cls.image_widths[6] = 18
		cls.image_surfaces[7] = scl.scale(pygame.image.load("Images/Robots/orange_back.png")).convert_alpha()
		cls.image_widths[7] = 18
		cls.image_surfaces[8] = scl.scale(pygame.image.load("Images/Robots/red_right.png")).convert_alpha()
		cls.image_widths[8] = 16
		cls.image_surfaces[9] = scl.scale(pygame.image.load("Images/Robots/red_front.png")).convert_alpha()
		cls.image_widths[9] = 16
		cls.image_surfaces[10] = scl.scale(pygame.image.load("Images/Robots/red_left.png")).convert_alpha()
		cls.image_widths[10] = 18
		cls.image_surfaces[11] = scl.scale(pygame.image.load("Images/Robots/red_back.png")).convert_alpha()
		cls.image_widths[11] = 18
		
	