import pygame
import constants

from constants import *

class Camera(object):
	def __init__(self, camera_func, width, height):
		self.camera_func = camera_func
		self.state = pygame.Rect(0, 0, width, height)

	def apply(self, target):
		return target.rect.move(self.state.topleft)

	def update(self, target):
		self.state = self.camera_func(self.state, target.rect)

def complex_camera(camera, target_rect):
	left, top, _, _ = target_rect
	_, _, width, height = camera
	left, top, _, _ = -left+(WIDTH/2), -target_rect.bottom-TILESIZE+height, width, height

	left = min(0, left) # stop scrolling at the left edge
	left = max(-(camera.width-WIDTH), left) # stop scrolling at the right edge
	top = max(-(camera.height), top) # stop scrolling at the bottom
	top = min(0, top) # stop scrolling at the top

	return pygame.Rect(left, top, width, height)