import pygame
import bob
import jay
import chain

from bob import *
from jay import *
from chain import *

class Level():
	def __init__(self, mapGrid, bob, jay, chain, enemies, triggers, entities, backgroundEntities, collidables, camera, reset):
		self.bob = bob
		self.jay = jay
		self.chain = chain
		self.triggers = triggers
		self.enemies = enemies
		self.entities = entities
		self.backgroundEntities = backgroundEntities
		self.collidables = collidables
		self.camera = camera
		self.reset = reset
		self.finish = False

	def resetLevel(self):
		self.finish = False

		self.bob = Bob(self.reset['bob'].rect.left, self.reset['bob'].rect.top)
		self.jay = Jay(self.reset['jay'].rect.left, self.reset['bob'].rect.top)
		self.chain = Chain(self.reset['chain'].rect.left, self.reset['chain'].rect.top)

		self.enemies = pygame.sprite.Group
		self.entities = []
		self.collidables = []
		self.enemies = []

		self.entities.append(self.bob)
		self.entities.append(self.jay)
		self.entities.append(self.chain)

		for trigger in self.reset['triggers']:
			trigger.set(False)

		for collidable in self.reset['collidables']:
			self.entities.append(collidable)
			self.collidables.append(collidable)

		for enemy in self.reset['enemies']:
			self.entities.append(enemy)
			self.enemies.append(enemy)

		self.backgroundEntities = pygame.sprite.Group()
		for bg_entity in self.reset['backgroundEntities'].sprites():
			self.backgroundEntities.add(bg_entity)
