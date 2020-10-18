#
# FILE: scaler.py
# PART OF: Part of the NUWAYOUT arcade game.
# DESCRIPTION: module for scaling images to different display resolutions.
#

#Load required modules
from __future__ import division
from math import floor
import pygame

#Constants for the native resolution of NUWAYOUT. Everything is scaled from here.
GAME_NATIVE_W = 576
GAME_NATIVE_H = 432

class Scaler:
	def __init__(self):
		self.scale_x = None
		self.scale_y = None
	def set_scalers(self, display_width, display_height):
		self.scale_x = display_width / GAME_NATIVE_W
		self.scale_y = display_height / GAME_NATIVE_H
		print "SCALE X: " + str(self.scale_x)
		print "SCALE Y: " + str(self.scale_y)
	def scale(self, surface):
		current_w = surface.get_width()
		current_h = surface.get_height()
		return pygame.transform.scale(surface,(int(floor(current_w * self.scale_x)), int(floor(current_h * self.scale_y))))

scl = Scaler()
