from PIL import Image
import pygame
import os
import platform

IMAGE_DIRECTORY = "images"
SPLITTER_DIRECTORY = "splitters"


class TileLoader:
	def __init__(self):
		self.tiles = []
		self.load_tiles()

	def load_tiles(self):
		for filename in os.listdir(IMAGE_DIRECTORY):
			filename = os.path.join(IMAGE_DIRECTORY, filename)
			if filename.endswith(".png"):
				im = Image.open(filename)
				new_tile = Tile(filename, im.size)
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

		new_matrix = []
		for i in range(0, (x_chunks)):
			row = []
			for j in range(0, y_chunks):
				# print(f"Processing {i}, {j}")
				sx = i*16
				ex = (i+1) * 16
				sy = j*16
				ey = (j+1) * 16

				box = (sy, sx, ey, ex)
				new_image = im.crop(box)

				save_location = os.path.join(image_path.strip(name+".png"), "output", f"{name}{i}{j}.png")

				new_image.save(save_location)
				row.append(new_image)

				tile = Tile(save_location, new_image.size, piece=True, folder=os.path.join(IMAGE_DIRECTORY, SPLITTER_DIRECTORY, "output"), block_size=block_size)
				self.tiles.append(tile)
			new_matrix.append(row)


class Tile: # rect must be initiated when loaded into real game
	def __init__(self, image_path, size, piece=False, folder=None, block_size=None):
		self.name = image_path.split("\\")[-1].strip(".png")
		self.image = pygame.image.load(image_path)
		self.x, self.y = size
		self.size = size
		self.piece = piece
		print(f"{self.name}")
		print(f"Am I a piece of a block?: {self.piece}")

	def get_block_details(self):
		if not self.piece:
			return


TileLoader().load_tiles()
