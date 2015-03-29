import pygame, sys, os, copy, random, math
import animation
import bob
import camera
import chain
import constants
import enemy
import entity
import jay
import level
import staircase
import tile
import trigger

from animation import *
from bob import *
from camera import *
from chain import *
from constants import *
from enemy import *
from entity import *
from jay import *
from level import *
from staircase import *
from tile import *
from trigger import *


def main():
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.set_volume(1.0)
	pygame.mixer.music.load('assets/Early Riser.wav')
	pygame.mixer.music.play(-1)

	# LEVEL 1
	levels = read_level_file("level1.txt")
	# LEVEL 2
	#levels = read_level_file("level2.txt")
	# LEVEL 3
	#levels = read_level_file("level3.txt")

	currentLevel = 0
	level = levels[currentLevel] #levels[currentLevel]

	while True: #main game loop
		displayScreen(SCREENS['startScreen'])
		displayScreen(SCREENS['howToScreen'])
		#displayScreen(SCREENS['backgroundScreen'])

		result = run_level(level, currentLevel, levels)

		if result == 'quit':
			terminate()
		if result == 'finished':
			#displayScreen(SCREENS['endScreen'])
			displayScreen(SCREENS['creditsScreen'])
			main()
		if result == 'dead':
			#displayScreen(SCREENS['deathScreen'])
			level.resetLevel()
		if result == 'restart':
			#print("resetlevel")
			level.resetLevel()

def displayScreen(image):
	image_rect = image.get_rect()
	image_rect.topleft = (0, 0)

	SCREEN.fill((0,0,0))
	SCREEN.blit(image, image_rect)

	while True: #enables quit capability during screens
		CLOCK.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return 1
				return 1
		pygame.display.update()

def run_level(level, levelNum, levels):
	bob = level.bob
	jay = level.jay
	chain = level.chain
	triggers = level.triggers
	entities = level.entities
	backgroundEntities = level.backgroundEntities
	camera = level.camera
	enemies = level.enemies

	while True:
		CLOCK.tick(FPS)

		key_presses = pygame.event.get(pygame.KEYDOWN)
		key_states = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()

		if key_states[pygame.K_r]:
			return 'restart'

		if key_states[pygame.K_ESCAPE]:
			return 'quit'
		
		jay.update(key_presses, key_states, level)
		#print("jay completed", jay.completed)
		#print("jay dead", jay.dead)
		if jay.dead:
			jay.dead = False
			bob.dead = False
			return 'restart'
		bob.update(key_presses, key_states, level)
		#print("bob completed", bob.completed)
		#print("bob dead", bob.dead)
		if bob.dead:
			jay.dead = False
			bob.dead = False
			return 'restart'


		if key_states[pygame.K_k]:
			if levelNum + 1 == len(levels):	
				# jay.completed = False
				# bob.completed = False			
				return 'finished'
			levelNum += 1
			level = levels[levelNum]
			run_level(level, levelNum, levels)

		# if the current level has been completed by both jay and bob
		if (jay.completed and bob.completed) and not (jay.dead or bob.dead):
			# if this is the last level
			if levelNum + 1 == len(levels):	
				# jay.completed = False
				# bob.completed = False			
				return 'finished'
			levelNum += 1
			level = levels[levelNum]
			run_level(level, levelNum, levels)

		chain.update(jay, bob, level)
		
		# Fix the camera onto the 'chain'!!!
		camera.update(chain)
		# camera.update(bob)
		# camera.update(jay)

		# draw the background
		for y in range(26):
			for x in range(20):
				SCREEN.blit(IMAGES['BackGroundWall'], (x * TILESIZE, y * TILESIZE))

		for entity in backgroundEntities:
			entity.update()
			if entity.image.get_rect().colliderect(SCREEN.get_rect()):
				SCREEN.blit(entity.image, camera.apply(entity))

		for entity in triggers:
			SCREEN.blit(entity.image, camera.apply(entity))

		for enemy in enemies:
			enemy.update(level)

		for entity in entities:
			if entity.image.get_rect().colliderect(SCREEN.get_rect()):
				SCREEN.blit(entity.image, camera.apply(entity))
				SCREEN.blit(bob.image, camera.apply(bob))
				SCREEN.blit(jay.image, camera.apply(jay))
				#pygame.draw.line(SCREEN, (0,0,255), bob.rect.center, jay.rect.center, 5)
				SCREEN.blit(chain.image, camera.apply(chain))

		pygame.display.update()

def read_level_file(fileName):
	assert os.path.exists(fileName), 'Cannot find the level file: %s' % (fileName)
	mapFile = open(fileName, 'r')

	# Each level must end with a blank line
	content = mapFile.readlines() + ['\r\n']
	mapFile.close()

	levels = [] # Will contain a list of level objects.
	levelNum = 0
	mapBlueprintText = [] # contains the lines for a single level's map.
	mapGrid = [] # the map grid double array made from the data in mapBlueprintText.

	# Process each line in the level text to create the map grid
	for lineNum in range(len(content)):
		# Process each line that was in the level file.
		line = content[lineNum].rstrip('\r\n')

		if line != '':
			# This line is part of the map.
			mapBlueprintText.append(line)
		elif line == '' and len(mapBlueprintText) > 0:
			# A blank line indicates the end of a level's map in the file.
			# Convert the text in mapBlueprintText into a level object.

			# Find the longest row in the map.
			maxWidth = -1
			for i in range(len(mapBlueprintText)):
				if len(mapBlueprintText[i]) > maxWidth:
					maxWidth = len(mapBlueprintText[i])

			# Add spaces to the ends of the shorter rows. This
			# ensures the map will be rectangular.
			for i in range(len(mapBlueprintText)):
				mapBlueprintText[i] += ' ' * (maxWidth - len(mapBlueprintText[i]))

			# Convert mapBlueprintText to a map object.
			for x in range(len(mapBlueprintText[0])):
				mapGrid.append([])

			for y in range(len(mapBlueprintText)):
				for x in range(maxWidth):
				    mapGrid[x].append(mapBlueprintText[y][x])

			bob = None
			bobX = None
			bobY = None

			jay = None
			jayX = None
			jayY = None

			chain = None
			chainX = None
			chainY = None

			camera = Camera(complex_camera, maxWidth*TILESIZE, LEVEL_HEIGHT)

			triggers = []
			collidables = []
			entities = pygame.sprite.Group()
			backgroundEntities = pygame.sprite.Group()
			enemies = pygame.sprite.Group()

			# Loops through the levels file and creates objects that are in the level
			for x in range(maxWidth):
				for y in range(len(mapGrid[x])):

					# Entities

					if mapGrid[x][y] in ('J'):
						# 'J' is the player Jay
						jayX = getPixelCoord(x)
						jayY = getPixelCoord(y)
						jay = Jay(jayX, jayY)
						entities.add(jay)

					if mapGrid[x][y] in ('B'):
						# 'B' is the player Bob
						bobX = getPixelCoord(x)
						bobY = getPixelCoord(y)
						bob = Bob(getPixelCoord(x), getPixelCoord(y))
						entities.add(bob)

					if mapGrid[x][y] in ('h'):
						# 'h' is a chain object, must be placed after Bob and Jay objects in text file
						chain = Chain(jay, bob)
						entities.add(chain)

					if mapGrid[x][y] in ('1'):
						# 'p' is the Prisoner entities (initDirection = "right")
						enemy_prisoner1 = Enemy(getPixelCoord(x), getPixelCoord(y), 3, 3, "right")
						#collidables.append(enemy_prisoner_l)
						entities.add(enemy_prisoner1)
						enemies.add(enemy_prisoner1)

					if mapGrid[x][y] in ('2'):
						# 'p' is the Prisoner entities (initDirection = "right")
						enemy_prisoner2 = Enemy(getPixelCoord(x), getPixelCoord(y), 4, 4, "right")
						#collidables.append(enemy_prisoner_l)
						entities.add(enemy_prisoner2)
						enemies.add(enemy_prisoner2)

					if mapGrid[x][y] in ('3'):
						# 'p' is the Prisoner entities (initDirection = "right")
						enemy_prisoner3 = Enemy(getPixelCoord(x), getPixelCoord(y), 5, 5, "right")
						#collidables.append(enemy_prisoner_l)
						entities.add(enemy_prisoner3)
						enemies.add(enemy_prisoner3)

					if mapGrid[x][y] in ('4'):
						# 'p' is the Prisoner entities (initDirection = "right")
						enemy_prisoner4 = Enemy(getPixelCoord(x), getPixelCoord(y), 3, 3, "left")
						#collidables.append(enemy_prisoner_l)
						entities.add(enemy_prisoner4)
						enemies.add(enemy_prisoner4)

					if mapGrid[x][y] in ('5'):
						# 'p' is the Prisoner entities (initDirection = "right")
						enemy_prisoner5 = Enemy(getPixelCoord(x), getPixelCoord(y), 4, 4, "left")
						#collidables.append(enemy_prisoner_l)
						entities.add(enemy_prisoner5)
						enemies.add(enemy_prisoner5)

					if mapGrid[x][y] in ('6'):
						# 'p' is the Prisoner entities (initDirection = "right")
						enemy_prisoner6 = Enemy(getPixelCoord(x), getPixelCoord(y), 5, 5, "left")
						#collidables.append(enemy_prisoner_l)
						entities.add(enemy_prisoner6)
						enemies.add(enemy_prisoner6)

					if mapGrid[x][y] in ('S'):
						# 'S' is the staircase/checkpoint/end of level
						staircase = Staircase(getPixelCoord(x), getPixelCoord(y), IMAGES['stairs_bot'])
						triggers.append(staircase)

					if mapGrid[x][y] in ('X'):
						# 'X' is the top of the stairs
						upperStaircase = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['stairs_top'], 'staircase')
						backgroundEntities.add(upperStaircase)

					if mapGrid[x][y] in ('E'):
						# 'E' is the final exit, only changes visually from staircase
						exitDoor = Staircase(getPixelCoord(x), getPixelCoord(y), IMAGES['endDoor'])
						triggers.append(exitDoor)

					if mapGrid[x][y] in ('='):
						# '=' is debris with platform behavior (drop through)
						debrisPlatform = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['rubble'], 'platform')
						collidables.append(debrisPlatform)
						entities.add(debrisPlatform)

					if mapGrid[x][y] in ('D'):
						# 'D' is the debris tile
						debrisTile = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['rubble'], 'debris')
						collidables.append(debrisTile)
						entities.add(debrisTile)

					if mapGrid[x][y] in ('W'):
						# 'W' is a collidable wall tile
						wallTile = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['wall'], 'wall')
						collidables.append(wallTile)
						entities.add(wallTile)

					if mapGrid[x][y] in ('_'):
						# '_' is the pitfall tile
						pitfallTile = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['blanktile'], "death")
						collidables.append(pitfallTile)
						entities.add(pitfallTile)			

					if mapGrid[x][y] in ('C'):
					# 	# 'C' is the ceiling tile
						ceilingTile = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['ceiling'], 'ceiling')
						collidables.append(ceilingTile)
						entities.add(ceilingTile)

					if mapGrid[x][y] in ('F'):
						# 'F' is the floor tile
						floorTile = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['floor'], 'floor')
						collidables.append(floorTile)
						entities.add(floorTile)

					# Background Tiles

					if mapGrid[x][y] in ('w'):
						# 'w' is the wire tile
						wireTile = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['wire'], 'wire')
						backgroundEntities.add(wireTile)

					if mapGrid[x][y] in ('s'):
						# 's' is the lower staircase background entity
						bg_staircase_lower = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['downstairs_bot'], 'staircase')
						backgroundEntities.add(bg_staircase_lower)

					if mapGrid[x][y] in ('x'):
						# 'x' is the upper staircase background entity
						bg_staircase_upper = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['downstairs_top'], 'staircase')
						backgroundEntities.add(bg_staircase_upper)

					if mapGrid[x][y] in ('d'):
						# 'd' is background rubble
						bg_rubble = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['deco_rubble'], 'deco_rubble')
						backgroundEntities.add(bg_rubble)

					if mapGrid[x][y] in ('['):
						cell1q1 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cell_1BJ'], 'cell_1BJ')
						backgroundEntities.add(cell1q1)

					if mapGrid[x][y] in (']'):
						cell1q2 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cell_2BJ'], 'cell_2BJ')
						backgroundEntities.add(cell1q2)

					if mapGrid[x][y] in ('{'):
						cell1q3 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cell_3BJ'], 'cell_3BJ')
						backgroundEntities.add(cell1q3)

					if mapGrid[x][y] in ('}'):
						cell1q4 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cell_4BJ'], 'cell_4BJ')
						backgroundEntities.add(cell1q4)

					if mapGrid[x][y] in ('!'):
						cell2q1 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cell_1Blindman'], 'cell_1Blindman')
						backgroundEntities.add(cell2q1)

					if mapGrid[x][y] in ('|'):
						cell2q2 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cell_2Blindman'], 'cell_2Blindman')
						backgroundEntities.add(cell2q2)

					if mapGrid[x][y] in (':'):
						cell2q3 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cell_3Blindman'], 'cell_3Blindman')
						backgroundEntities.add(cell2q3)

					if mapGrid[x][y] in (';'):
						cell2q4 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cell_4Blindman'], 'cell_4Blindman')
						backgroundEntities.add(cell2q4)

					if mapGrid[x][y] in ('A'):
						arrow = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['arrow'], 'arrow')
						backgroundEntities.add(arrow)


			assert jay != None, "Level %s line %s in file %s is missing a 'J' for Jay." % (levelNum, lineNum, fileName)
			assert bob != None, "Level %s line %s in file %s is missing a 'B' for Bob." % (levelNum, lineNum, fileName)
			assert chain != None, "Level %s line %s in file %s is missing a 'h' for Chain." % (levelNum, lineNum, fileName)

			reset = {'bob': copy.deepcopy(bob),
				'jay': copy.deepcopy(jay),
				'chain': copy.deepcopy(chain),
				'triggers':copy.copy(triggers),
				'entities': copy.copy(entities),
				'enemies': copy.copy(enemies),
				'backgroundEntities': copy.copy(backgroundEntities),
				'collidables': copy.copy(collidables)}

			level = Level(mapGrid, bob, jay, chain, enemies, triggers, entities, backgroundEntities, collidables, camera, reset)
			levels.append(level)

			mapBlueprintText = []
			mapGrid = []
			gameObjs = {}
			levelNum += 1

	return levels

def getPixelCoord(gridCoord):
	pixelCoord = gridCoord * TILESIZE
	return pixelCoord

def terminate():
	pygame.quit()
	sys.exit()

main()
