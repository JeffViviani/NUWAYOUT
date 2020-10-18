#AUTHOR: JEFFREY VIVIANI
#DATE CREATED: 12/15/2019
#LAST MODIFIED: 12/18/2019
#NUWAYOUT BASE CODE

#Import modules
from math import exp
from random import random
import sys, pygame, config
from robots import *
from scaler import *
from doors import *

#Initialize pygame
pygame.mixer.init()
pygame.joystick.init()
pygame.init()

#Initialize clock
clock = pygame.time.Clock()

#Acquire information on the current display
displayInfo = pygame.display.Info()
screen_width = displayInfo.current_w
screen_height = displayInfo.current_h

#Initialize the scaler
scl.set_scalers(screen_width, screen_height)

#Initialize the robot surfaces
Robot.init_scaled_surfaces()
Robot.init_sounds()

#Initialize the laser surfaces
Laser.init_scaled_surfaces()

#Initialize the door surfaces
Door.init_scaled_surfaces()

#Initialize the full screen display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, 8)
	
#Initialize the background
background = scl.scale(pygame.image.load("Images/Background/background.png"))
background_rect = background.get_rect()

#Initialize the "Press Button" surface
press_button = scl.scale(pygame.image.load("Images/HUD/pressButton.png"))
press_button_rect = press_button.get_rect()
press_button_rect.left = 187 * scl.scale_x; press_button_rect.top = 200 * scl.scale_y;

#Initialize the title surface
title = scl.scale(pygame.image.load("Images/HUD/title.jpeg"))
title_rect = title.get_rect()
title_rect.left = 58 * scl.scale_x
title_rect.top = 100 * scl.scale_y

#Initialize the text renderer
myfont = pygame.font.SysFont('impact', 25)
text_rect = pygame.Rect(0,0,20 * scl.scale_x,20 * scl.scale_y)

#Blit the initialized surfaces to the screen
screen.blit(background,background_rect)
screen.blit(press_button,press_button_rect)
state = 0
flash = 0
i = 4
delay_time = 0
showing_space = True
clear_last_number = False
fire = False
last_fire_time = 0
door_times = 10

if config.MUSIC:
	#Play music
	pygame.mixer.music.load("Audio/Hyperloop-Deluxe.mp3")
	pygame.mixer.music.play(-1)
if pygame.joystick.get_count() == 1:
	my_joystick = pygame.joystick.Joystick(0)
	my_joystick.init()
if my_joystick.get_init():
	running = True
	while running:
		#Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				elif event.key == pygame.K_SPACE:
					pass
			elif event.type == pygame.JOYBUTTONDOWN:
				if state == 0:
					state = 1
					screen.blit(background,background_rect)
					flash = 0
					i = 4
					next_number = True;
				elif state == 2:
					fire = True
		clock.tick(75) #60FPS
		
		if Robot.game_over == True:
			Robot.game_over = None
			state = 0
			x = len(Robot.registry); i = 0;
			while i < x:
				i += 1
				Robot.Registry.pop(0)
			x = len(Laser.registry); i = 0;
			while i < x:
				i += 1
				Laser.registry.pop(0)
			screen.blit(background,background_rect)
		if state == 0:
			flash = flash + 1
			if flash > 29:
				flash = 0
				showing_space = not showing_space
			screen.blit(title, title_rect)
			if showing_space:
				screen.blit(press_button,press_button_rect)
			else:
				screen.blit(background,press_button_rect,press_button_rect)
		elif state == 1:
			flash += 1
			if next_number:
				i -= 1
				if clear_last_number:
					screen.blit(background,countdown_rect,countdown_rect)
					clear_last_number = False
				if i > 0:
					countdown = scl.scale(pygame.image.load("Images/HUD/big" + str(i) + ".png"))
					countdown_rect = countdown.get_rect()
					countdown_rect.left = 185 * scl.scale_x
					countdown_rect.top = 55 * scl.scale_y
					screen.blit(countdown,countdown_rect)
					next_number = False
				else:
					Robot.game_over = False
					your_robot = Robot(screen,background,0,None)
					time_start = pygame.time.get_ticks()
					generation_time = pygame.time.get_ticks() + 1000
					door_manager_1 = DoorManager(screen,background)
					timer = -1
					state = 2
			flash += 1
			if flash > 59:
				next_number = True
				clear_last_number = True
				flash = 0
		elif state == 2:
			#Joystick Operation for your robot
			vertical_joy_axis = my_joystick.get_axis(1)
			horizontal_joy_axis = my_joystick.get_axis(0)
			if not your_robot.in_motion:
				if vertical_joy_axis > 0.9:
					your_robot.change_dir(1); your_robot.try_move();
				elif vertical_joy_axis < -0.9:
					your_robot.change_dir(3); your_robot.try_move();
				elif horizontal_joy_axis > 0.9:
					your_robot.change_dir(0); your_robot.try_move();
				elif horizontal_joy_axis < -0.9:
					your_robot.change_dir(2); your_robot.try_move();
			#Control Logic for robot generation
			time_mil = pygame.time.get_ticks()
			time_decisec_from_start = floor((time_mil - time_start) / 100)
			if time_mil > generation_time:
				x = random()
				prob_orange = 0.5 * exp((time_start - time_mil)*0.000001) + 0.5
				if x < prob_orange:
					color = 1
				else:
					color = 2
				Robot(screen,background,color,door_manager_1)
				delay_time = exp(-0.00001*(time_mil - time_start)) * 5000 + 200
				delay_time = delay_time + delay_time * (random() * 0.4 - 0.2)
				generation_time = delay_time + time_mil
			#Every frame, work on robot motion
			for rob in Robot.registry:
				rob.ai()
				rob.move()
			for las in Laser.registry:
				las.move()
			#Laser firing
			if fire and time_mil > last_fire_time + 100:
				your_robot.fire()
				last_fire_time = time_mil
				fire = False
			#Door management
			door_times -= 1
			if not door_times:
				door_manager_1.operate_doors()
				door_times = 10
			#Manage the timer
			if time_decisec_from_start != timer:
				timer = time_decisec_from_start
				screen.blit(background,text_rect,text_rect)
				textsurface = scl.scale(myfont.render(str(timer/10), False, (0, 0, 0)))
				text_rect = textsurface.get_rect()
				text_rect.left = screen_width - (28 * scl.scale_x) - text_rect.width
				text_rect.top = 3 * scl.scale_y
				screen.blit(textsurface,text_rect)
		#Refresh the display
		pygame.display.flip()
	sys.exit()


