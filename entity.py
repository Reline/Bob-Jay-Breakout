import pygame

class Entity(pygame.sprite.Sprite):
	def __init__(self, type):
		pygame.sprite.Sprite.__init__(self)
		self.type = type