import pygame
import math
import constants
import bob
import jay
import entity
import animation
import camera

from constants import *
from bob import *
from jay import *
from entity import *
from animation import *
from camera import *

class Chain(animatedEntity):
	def __init__(self, jay, bob):
		animatedEntity.__init__(self, IMAGES['blanktile'], 5, IMAGES['blanktile'], 5, "chain")

		self.jay = jay
		self.bob = bob

		self.init_image = self.idleSprite[0]
		self.init_image.convert()
		self.image = self.idleSprite[0]
		self.image.convert()
		self.rect = self.image.get_rect()
		self.init_rect = self.image.get_rect()
		#self.rect.topleft = self.bob.rect.bottomright # will be tuned later

		self.length = 0
		self.slack = 160
		self.rotationAngle = 0.0

	def update(self, jay, bob, level):
		for entity in level.entities:
			if entity.type == "bob":
				self.bob = entity
				bobBot = entity.rect.bottom
				bobCenter = entity.rect.center[0]
			elif entity.type == "jay":
				self.jay = entity
				jayBot = entity.rect.bottom
				jayCenter = entity.rect.center[0]

		xDistance = abs(bobCenter - jayCenter)
		yDistance = abs(bobBot - jayBot)

		self.rotationAngle = math.sqrt(xDistance^2 + yDistance^2)

		if self.idleSprite != None:
			currentIdleFrame = getFrame(pygame.time.get_ticks(), self.idleFPS, self.idleFrameCount)
		if self.movingSprite != None:
			currentMovingFrame = getFrame(pygame.time.get_ticks(), self.movingFPS, self.movingFrameCount)

		self.rect.topleft = self.bob.rect.topright

		self.length = abs(jayCenter - bobCenter)

		if abs(bobBot - jayBot) > abs(bobCenter - jayCenter):
			self.length = abs(bobBot - jayBot)
		else:
			self.length = abs(bobCenter - jayCenter)

		if bobCenter < jayCenter: # if bob is to the left of jay
			# if bobBot < jayBot:
			# 	self.image = pygame.transform.scale(pygame.transform.rotozoom(self.init_image, self.rotationAngle, 1), (self.length, self.init_image.get_height()))
			# elif bobBot > jayBot:
			# 	self.image = pygame.transform.scale(pygame.transform.rotozoom(self.init_image, -self.rotationAngle, 1), (self.length, self.init_image.get_height()))

			self.rect.topleft = (self.bob.rect.center[0], self.bob.rect.top)

			# if self.bob.onGround == True and self.jay.onGround == True:
			# 	# stretch chain
			# 	self.image = pygame.transform.scale(self.image, (self.length, self.rect.height))
			# else:
			# 	#self.image = pygame.transform.flip(IMAGES['jumpingChain'], False, False)
			# 	# stretch chain
			# 	self.image = pygame.transform.scale(self.image, (self.length, self.rect.height))

			if self.length >= self.slack: # if the chain is stretched to its limits
				if bobBot < jayBot: # if bob is below jay
					self.bob.setSlack(False, True, True, False)
					self.jay.setSlack(True, False, False, True)

				else: # if bob is above jay
					self.bob.setSlack(False, True, False, True)
					self.jay.setSlack(True, False, True, False)
			else:
				self.bob.setSlack(True, True, True, True)
				self.jay.setSlack(True, True, True, True)

		else: # if bob is to the right of jay
		 	# if self.bob.onGround == True and self.jay.onGround == True:
		 	# 	pass
		 	# self.image = pygame.transform.scale(self.image, (self.length, self.init_image.get_height()))
		 	self.rect.topleft = (self.jay.rect.center[0], self.jay.rect.top)
		 	
		 	# if self.jay.deltaX > 0:
		 	# 	self.rect.topleft = (self.jay.rect.center[0], self.jay.rect.bottom)
		 	# else:
		 	# 	self.rect.topleft = self.jay.rect.topright

		 	if (self.length >= self.slack):
		 		if (bobBot < jayBot): # if bob is below jay
		 			self.bob.setSlack(True, False, True, False)
		 			self.jay.setSlack(False, True, False, True)
		 		else: # if bob is above jay
		 			self.bob.setSlack(True, False, False, True)
		 			self.jay.setSlack(False, True, True, False)
		 	else:
		 		self.bob.setSlack(True, True, True, True)
		 		self.jay.setSlack(True, True, True, True)