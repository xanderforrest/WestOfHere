import pygame
import os
from consts import *


def get_collisions(rect, tiles):
	collisions = []
	for tile in tiles:
		if rect.colliderect(tile.rect):
			collisions.append(tile)
	return collisions


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
				if y >= 15:
					if y == 15:
						row.append(Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt.png")), True))
					else:
						row.append(Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt.png"))))
				else:
					row.append(Tile(None))
			map.append(row)
		return map

	def load_map(self):
		background_map = self.load_background()
		building_map = self.load_buildings()
		floor_map = self.load_floor()

		final_map = self.empty_map()
		for x in range(0, len(final_map)):  # builds the final map with layering, because who needs parallax?
			for y in range(0, len(final_map[x])):
				final_map[x][y] = background_map[x][y] if background_map[x][y].image else Tile(None)
				final_map[x][y] = building_map[x][y] if building_map[x][y].image else final_map[x][y]
				final_map[x][y] = floor_map[x][y] if floor_map[x][y].image else final_map[x][y]
		return final_map


class Tile:
	def __init__(self, image, interactable=False, category="floor", rect=None):
		self.image = image
		self.interactable = interactable
		self.category = category
		self.rect = rect
