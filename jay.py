import pygame
import animation
import constants
import entity
import trigger

from constants import *
from animation import *
from trigger import *
from entity import *

class Jay(animatedEntity):
	def __init__(self, x, y):
		animatedEntity.__init__(self, IMAGES['jay_idle'], 5, IMAGES['jay_walk'], 8, "jay")

		self.deltaX = 1
		self.deltaY = 0
		self.onGround = False
		self.isCrouching = False
		self.speed = 9
		self.slackLeft = True
		self.slackRight = True
		self.slackTop = True
		self.slackBot = True

		self.dead = False
		self.completed = False

		self.image = self.idleSprite[0]
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)

	def update(self, keyPresses, keyStates, level):
		if self.idleSprite != None:
			currentIdleFrame = getFrame(pygame.time.get_ticks(), self.idleFPS, self.idleFrameCount)
		if self.movingSprite != None:
			currentMovingFrame = getFrame(pygame.time.get_ticks(), self.movingFPS, self.movingFrameCount)

		# If player presses UP
		if keyStates[pygame.K_UP] and self.slackTop:
			if self.onGround:
				self.deltaY -= 10
				self.onGround = False

		# If player presses DOWN
		if keyStates[pygame.K_DOWN] and self.slackBot:
			self.isCrouching = True
			#self.deltaY += 5
		else:
			self.isCrouching = False

		# If player moves LEFT
		if keyStates[pygame.K_LEFT] and self.slackLeft:
			self.deltaX = -self.speed

			if self.deltaY == 0:
				self.image = pygame.transform.flip(self.movingSprite[currentMovingFrame], True, False)

			self.rect.left += self.deltaX
			self.collide(self.deltaX, 0, level)

		# If player moves RIGHT
		if keyStates[pygame.K_RIGHT] and self.slackRight:
			self.deltaX = self.speed

			if self.deltaY == 0:
				self.image = pygame.transform.flip(self.movingSprite[currentMovingFrame], False, False)
			
			self.rect.left += self.deltaX
			self.collide(self.deltaX, 0, level)

		#If player is airborne
		if not self.onGround:
			self.deltaY += .6

			if self.deltaY > 30:
				self.deltaY = 30

		# If NOT pressing LEFT or RIGHT / Used for idle
		if not (keyStates[pygame.K_a] or keyStates[pygame.K_d]):
			if self.onGround:
				if self.deltaX > 0:
					self.image = pygame.transform.flip(self.idleSprite[currentIdleFrame], False, False)
				else:
					self.image = pygame.transform.flip(self.idleSprite[currentIdleFrame], True, False)

		# If FALLING or JUMPING
		if self.deltaY < -1.6 or self.deltaY > 1.6:
			if self.deltaX > 0:
				self.image = pygame.transform.flip(IMAGES['jay_jump'], False, False)
			else:
				self.image = pygame.transform.flip(IMAGES['jay_jump'], True, False)

		self.rect.top += self.deltaY
		self.onGround = False
		self.collide(0, self.deltaY, level)

	def setSlack(self, slackLeft, slackRight, slackTop, slackBot):
		self.slackLeft = slackLeft
		self.slackRight = slackRight
		self.slackTop = slackTop
		self.slackBot = slackBot
	
	def collide(self, deltaX, deltaY, level):
		for entity in level.collidables:
			if pygame.sprite.collide_rect(self, entity):

				if entity.type == 'death':
					self.completed = False
					self.dead = True
					#level.resetLevel()
					# Start players back at last checkpoint (beginning of level)

				if deltaX > 0: self.rect.right = entity.rect.left
				if deltaX < 0: self.rect.left = entity.rect.right
				if deltaY > 0:
					if entity.type == 'platform' and self.isCrouching:
						pass
					else:
						self.rect.bottom = entity.rect.top
						self.onGround = True
						self.deltaY = 0

				if deltaY < 0:
					self.rect.top = entity.rect.bottom
					self.deltaY = 0

		for entity in level.entities:
			if entity.type == "bob":
				if entity.dead == True:
					self.dead = True
				if entity.completed == True:
					self.completed = True

			if pygame.sprite.collide_rect(self, entity):
				if self.rect.bottom > entity.rect.top and entity.type == "bob":
					if self.rect.center[0] <= entity.rect.center[0] + 16 and self.rect.center[0] >= entity.rect.center[0] - 16 and self.rect.center[1] < entity.rect.center[1]:
						self.onBob = True
						self.rect.bottom = entity.rect.top
						self.onGround = True
						self.deltaY = 0

						for item in level.collidables:
							if pygame.sprite.collide_rect(self, item):
								self.deltaY -= 13
				

		for trigger in level.triggers:
			if pygame.sprite.collide_rect(self, trigger):
				if trigger.type == 'staircase':
					if trigger.activated == False:
						trigger.nextLevel(self)
						#trigger.setCheckpoint(self)
						#go to next level

						#What do these do???
						#self.altarcoordinatex = trigger.rect.left
						#self.altarcoordinatey = trigger.rect.top

		for enemy in level.enemies:
			if pygame.sprite.collide_rect(self, enemy):
				if enemy.type == "death":
					self.dead = True
					#level.resetLevel()