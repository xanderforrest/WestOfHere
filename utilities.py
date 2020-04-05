import pygame
import os
from consts import *


class TileLoader:
	def __init__(self):
		pass

	@staticmethod
	def empty_map():
		map = []
		for x in range(0, 50):
			row = []
			for y in range(0, 18):
				row.append(Tile(None))
			map.append(row)
		return map

	def load_background(self):
		map = self.empty_map()
		map[0][0] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "mountains.png")))
		return map

	def load_buildings(self):
		map = self.empty_map()
		map[20][9] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "buildings", "saloon.png")))
		return map

	def load_floor(self):
		map = []
		for x in range(0, 50):
			row = []
			for y in range(0, 18):
				if y >= 14:
					row.append(Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt.png")), True))
				else:
					row.append(Tile(None))
			map.append(row)
		return map

	def load_map(self):
		background_map = self.load_background()
		building_map = self.load_buildings()
		floor_map = self.load_floor()

		final_map = self.empty_map()
		for x in range(0, len(final_map)): # builds the final map with layering, because who needs parallax?
			for y in range(0, len(final_map[x])):
				print(background_map[x][y])
				final_map[x][y] = background_map[x][y] if background_map[x][y].image else Tile(None)
				final_map[x][y] = building_map[x][y] if building_map[x][y].image else final_map[x][y]
				final_map[x][y] = floor_map[x][y] if floor_map[x][y].image else final_map[x][y]
		return final_map


class Tile:
	def __init__(self, image, interactable=False):
		self.image = image
		self.interactable = interactable
