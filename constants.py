import pygame

#constants
FPS = 60
SCALE = 1
TILESIZE = 64 #* SCALE
WIDTH = 1280
HEIGHT = 640


LEVEL_HEIGHT = 704

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

def scale(image):
	rect = image.get_rect()
	_, _, width, height = rect 
	return pygame.transform.scale(image, (width*SCALE, height*SCALE))

IMAGES = {
	#'barber': scale(pygame.image.load("assets/barber.png").convert_alpha()),
	'bob_idle': scale(pygame.image.load("assets/Bob_idle.png").convert_alpha()),
	'bob_walk': scale(pygame.image.load("assets/Bob_walk.png").convert_alpha()),
	'bob_jump': scale(pygame.image.load("assets/Bob_jump.png").convert_alpha()),
	'jay_idle': scale(pygame.image.load("assets/Jay_idle.png").convert_alpha()),
	'jay_walk': scale(pygame.image.load("assets/Jay_walk.png").convert_alpha()),
	'jay_jump': scale(pygame.image.load("assets/Jay_jump.png").convert_alpha()),
	'floor': scale(pygame.image.load("assets/Floor.png").convert_alpha()),
	'ceiling': scale(pygame.image.load("assets/Ceiling.png").convert_alpha()),
	'wall': scale(pygame.image.load("assets/Wall.png").convert_alpha()),
	'BackGroundWall': scale(pygame.image.load("assets/BackGroundWall.png").convert_alpha()),
	'Twall': scale(pygame.image.load("assets/T-Wall.png").convert_alpha()),
	'wire': scale(pygame.image.load("assets/Wire.png").convert_alpha()),
	'enemy_prisoner': scale(pygame.image.load("assets/Prisoner.png").convert_alpha()),
	'enemy_prisoner_walk': scale(pygame.image.load("assets/Prisoner_walk.png").convert_alpha()),
	'blanktile': scale(pygame.image.load("assets/Blank.png").convert_alpha()),
	'chain': scale(pygame.image.load("assets/Chain.png").convert_alpha()),
	'blacktile': scale(pygame.image.load("assets/BackGroundWall.png").convert_alpha()),
	'rubble': scale(pygame.image.load("assets/rubble.png").convert_alpha()),
	'deco_rubble': scale(pygame.image.load("assets/DecoRubble.png").convert_alpha()),
	'arrow': scale(pygame.image.load("assets/arrow.png").convert_alpha()),
	'stairs_bot': scale(pygame.image.load("assets/Stairs_b.png").convert_alpha()),
	'stairs_top': scale(pygame.image.load("assets/Stairs_A.png").convert_alpha()),
	'cell_1BJ': scale(pygame.image.load("assets/cell_1BJ.png").convert_alpha()),
	'cell_1Blindman': scale(pygame.image.load("assets/cell_1Blindman.png").convert_alpha()),
	'cell_2BJ': scale(pygame.image.load("assets/cell_2BJ.png").convert_alpha()),
	'cell_2Blindman': scale(pygame.image.load("assets/cell_2Blindman.png").convert_alpha()),
	'cell_3BJ': scale(pygame.image.load("assets/cell_3BJ.png").convert_alpha()),
	'cell_3Blindman': scale(pygame.image.load("assets/cell_3Blindman.png").convert_alpha()),
	'cell_4BJ': scale(pygame.image.load("assets/cell_4BJ.png").convert_alpha()),
	'cell_4Blindman': scale(pygame.image.load("assets/cell_4Blindman.png").convert_alpha()),
	'downstairs_top': scale(pygame.image.load("assets/DownStairs_A.png").convert_alpha()),
	'downstairs_bot': scale(pygame.image.load("assets/DownStairs_b.png").convert_alpha()),
	'endDoor': scale(pygame.image.load("assets/endgamedoor.png").convert_alpha())
}

SCREENS = {
	'startScreen': pygame.image.load("assets/StartScreen.png").convert_alpha(),
	'creditsScreen': pygame.image.load("assets/Credits.png").convert_alpha(),
	'howToScreen': pygame.image.load("assets/HowToPlay.png").convert_alpha(),
	'endScreen': pygame.image.load("assets/EndScreen.png").convert_alpha()
	}

SCREENS_INTRO = [
	SCREENS['startScreen']
]

SCREENS_HELP = [
	
]

SCREENS_COMPLETED = [
	SCREENS['creditsScreen']
]