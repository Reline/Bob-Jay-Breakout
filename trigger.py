import pygame
import constants
import entity

from constants import *
from entity import *

class Trigger(Entity):
	def __init__(self, x, y, image, type):
		Entity.__init__(self, type)
		self.posX = x
		self.posY = y
		self.activated = False
		self.image = image
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def set(self, activated):
		self.activated = activated