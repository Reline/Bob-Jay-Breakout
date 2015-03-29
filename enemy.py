import pygame, math
import constants
import animation

from constants import *
from animation import *

class Enemy(animatedEntity):
	def __init__(self, x, y, speed, distance, initDirection):
		animatedEntity.__init__(self, IMAGES['enemy_prisoner'], 5, IMAGES['enemy_prisoner_walk'], 5, "death")

		self.speed = speed
		self.distance = distance*64
		self.initialX = x
		if initDirection == "left":
			self.speed *= -1

		self.image = self.movingSprite[0]
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def update(self, level):
		if self.movingSprite != None:
			currentMovingFrame = getFrame(pygame.time.get_ticks(), self.movingFPS, self.movingFrameCount)

		if math.fabs(self.rect.left - self.initialX) > self.distance:
			self.speed*=-1

		if self.speed < 0:
			self.image = pygame.transform.flip(self.movingSprite[currentMovingFrame], False, False)
		else:
			self.image = pygame.transform.flip(self.movingSprite[currentMovingFrame], True, False)

		self.rect.left += self.speed

		self.collide(self.speed, 0, level)

	def collide(self, deltaX, deltaY, level):
		for entity in level.collidables:
			if pygame.sprite.collide_rect(self, entity):

				if deltaX > 0: 
					self.rect.right = entity.rect.left
					self.speed*=-1
				if deltaX < 0:
				 	self.rect.left = entity.rect.right
				 	self.speed*=-1