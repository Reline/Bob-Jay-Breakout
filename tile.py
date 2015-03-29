import pygame
import constants
import entity

from constants import *
from entity import *

class Tile(Entity):
	def __init__(self, x, y, image, type):
		Entity.__init__(self, type)

		self.image = image
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
