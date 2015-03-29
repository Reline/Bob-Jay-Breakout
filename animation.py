import pygame
import constants
import entity

from constants import *
from entity import *

class animatedEntity(Entity):
	def __init__(self, idleImage, idleFPS, movingImage, movingFPS, type):
		Entity.__init__(self, type)

		if idleImage != None:
			self.idleSprite = get_sprite_sheet((TILESIZE, TILESIZE), idleImage, TILESIZE)
			self.idleFrameCount = len(self.idleSprite)
		else:
			self.idleSprite = None

		if movingImage != None:
			self.movingSprite = get_sprite_sheet((TILESIZE, TILESIZE), movingImage, TILESIZE)
			self.movingFrameCount = len(self.movingSprite)		
		else:
			self.movingSprite = None

		self.idleFPS = idleFPS
		self.movingFPS = movingFPS

class animatedTile(Entity):
	def __init__(self, x, y, idleImage, idleFPS, imageHeight, type):
		entity.__init__(self, type)

		self.idleSprite = get_sprite_sheet((TILESIZE, TILESIZE), idleImage, imageHeight)
		self.frameCount = len(idleSprite)
		self.idleFPS = idleFPS

		self.x = x
		self.y = y
		self.idleImage = idleImage
		self.idleFPS = idleFPS
		self.imageHeight = imageHeight

	def getUpdate(self):
		currentFrame = getFrame(pygame.time.get_ticks, self.idleFPS, self.framecount)
		self.image = self.idleSprite[currentFrame]


def get_sprite_sheet(size,image, image_height, pos=(0,0)):

	#Initial Values
	len_sprt_x,len_sprt_y = size #sprite size
	sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet

	sheet = image.convert_alpha() #Load the sheet
	sheet_rect = sheet.get_rect()
	sprites = []

	for i in range(0,sheet_rect.height,image_height):#rows
		sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
		sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
		sprites.append(sprite)
		sprt_rect_y += len_sprt_y
		sprt_rect_x = 0

	return sprites

def getFrame(millis, frames_per_second, framecount, start_millis=0):
	# Manual division cause *uck logic
	# millis_per_frame = 1000/ frames_per_second
	temp = 0
	millis_per_frame = 0
	while (temp < 1000):
		temp += frames_per_second
		millis_per_frame += 1
	if (temp > 1000):
		millis_per_frame -= 1
		
	elapsed_millis = millis - start_millis

	# Again...
	#total_frames = elapsed_millis / millis_per_frame
	total_frames = 0
	temp = 0
	while (temp < elapsed_millis):
		temp += millis_per_frame
		total_frames += 1
	if (temp > elapsed_millis):
		total_frames -= 1

	return total_frames % framecount