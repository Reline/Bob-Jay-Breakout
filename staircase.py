import pygame
import constants
import trigger

from constants import *
from trigger import *

class Staircase(Trigger):
	def __init__(self, x, y, image):
		Trigger.__init__(self, x, y, image, 'staircase')

		self.bob_activated = False
		self.jay_activated = False

	def nextLevel(self, jay_or_bob):
		jay_or_bob.completed = True

		if jay_or_bob.type == 'jay':
			self.jay_activated = True
		if jay_or_bob.type == 'bob':
			self.bob_activated = True
			
		if self.bob_activated and self.jay_activated:
			self.activated = True