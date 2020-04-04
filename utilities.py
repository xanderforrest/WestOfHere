from PIL import Image

class TileLoader:
	def __init__(self):
		pass

	def load_map(self):
		im = Image.open("TILEMAP.bmp")
		tilemap = []

		width, height = im.size
		imable = im.load()
		for y in range(height):
			row = []
			for x in range(width):
				row.append(imable[x, y])
			tilemap.append(row)

		return tilemap
