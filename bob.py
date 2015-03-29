import pygame
import animation
import entity
import constants
import trigger

from animation import *
from entity import *
from constants import *
from trigger import *

class Bob(animatedEntity):
	def __init__(self, x, y):
		animatedEntity.__init__(self, IMAGES['bob_idle'], 6, IMAGES['bob_walk'], 8, "bob")

		self.deltaX = 1
		self.deltaY = 0
		self.onGround = False
		self.isCrouching = False
		self.speed = 6
		self.slackRight = True
		self.slackLeft = True
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

		# If player presses W
		if keyStates[pygame.K_w] and self.slackTop:
			if self.onGround:
				self.deltaY -= 14
				self.onGround = False

		# If player presses S
		if keyStates[pygame.K_s] and self.slackBot:
			self.isCrouching = True
			#self.deltaY += 5
		else:
			self.isCrouching = False

		# If player moves a
		if keyStates[pygame.K_a] and self.slackLeft:
			self.deltaX = -self.speed

			if self.deltaY == 0:
				self.image = pygame.transform.flip(self.movingSprite[currentMovingFrame], True, False)

			self.rect.left += self.deltaX
			self.collide(self.deltaX, 0, level)

		# If player moves d
		if keyStates[pygame.K_d] and self.slackRight:
			self.deltaX = self.speed

			if self.deltaY == 0:
				self.image = pygame.transform.flip(self.movingSprite[currentMovingFrame], False, False)
			
			self.rect.left += self.deltaX
			self.collide(self.deltaX, 0, level)

		# If player is airborne
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
				self.image = pygame.transform.flip(IMAGES['bob_jump'], False, False)
			else:
				self.image = pygame.transform.flip(IMAGES['bob_jump'], True, False)

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
			if entity.type == "jay":
				if entity.dead == True:
					print("jay is dead??")
					self.dead = True
				if entity.completed == True:
					self.completed = True

		for trigger in level.triggers:
			if pygame.sprite.collide_rect(self, trigger):
				if trigger.type == 'staircase':
					print("bob collided with staircase trigger object")
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