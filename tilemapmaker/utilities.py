from PIL import Image
import pygame
import os
import platform

IMAGE_DIRECTORY = "images"
SPLITTER_DIRECTORY = "splitters"


class SpriteSheet(object):
	""" Class used to grab images out of a sprite sheet. """
	# This points to our sprite sheet image
	sprite_sheet = None

	def __init__(self, file_name):
		""" Constructor. Pass in the file name of the sprite sheet. """

		# Load the sprite sheet.
		self.sprite_sheet = pygame.image.load(file_name).convert()

	def get_image(self, x, y, width, height):
		""" Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

		# Create a new blank image
		image = pygame.Surface([width, height]).convert()

		# Copy the sprite from the large sheet onto the smaller image
		image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

		# Assuming black works as the transparent color
		image.set_colorkey(constants.BLACK)

		# Return the image
		return image

class TileLoader:
	def __init__(self):
		self.tiles = []
		self.blocks = []
		self.load_tiles()

	def load_tiles(self):
		for filename in os.listdir(IMAGE_DIRECTORY):
			filename = os.path.join(IMAGE_DIRECTORY, filename)
			if filename.endswith(".png"):
				im = Image.open(filename)
				new_tile = Tile(filename, filename.strip(".png"))
				self.tiles.append(new_tile)
		for filename in os.listdir(os.path.join(IMAGE_DIRECTORY, SPLITTER_DIRECTORY)):
			filename = os.path.join(IMAGE_DIRECTORY, SPLITTER_DIRECTORY, filename)
			if filename.endswith(".png"):
				self.handle_large(filename)

	def handle_large(self, image_path):
		im = Image.open(image_path)
		name = image_path.split("\\")[-1].strip(".png") if platform.system() == "Windows" else image_path.split("/")[-1].strip(".png")

		x, y = im.size

		if (x % 16) != 0 or (y % 16) != 0:
			return

		x_chunks = x // 16
		y_chunks = y // 16
		block_size = (x_chunks, y_chunks)
		print(block_size)

		block = []
		for i in range(0, (x_chunks)):
			row = []
			for j in range(0, y_chunks):
				# print(f"Processing {i}, {j}")
				sx = i*16
				ex = (i+1) * 16
				sy = j*16
				ey = (j+1) * 16

				box = (sy, sx, ey, ex)
				tile_image = im.crop(box)

				save_location = os.path.join(image_path.strip(name+".png"), "output", f"{name}{i}{j}.png")
				tile_image.save(save_location)

				name = f"{name}{i}{j}.png"
				tile = Tile(save_location, name)
				row.append(tile)

				self.tiles.append(tile)
			block.append(row)

		self.blocks.append(block)

class Block:
	def __init__(self, block_matrix):
		self.matrix = block_matrix
		self.x, self.y = (len(block_matrix[0]), len(block_matrix))


class Tile: # rect must be initiated when loaded into real game
	def __init__(self, image_path, name):
		self.name = name
		self.image = pygame.image.load(image_path)
		# self.x, self.y = image.size



TileLoader().load_tiles()
