import pygame
import json
from utilities.consts import *


class Tile:
    def __init__(self, image_path, interactable=False, category="none", rect=None):
        self.image_path = image_path  # TODO make this universal so maps can work with changed directories
        if self.image_path:
            self.image = pygame.image.load(os.path.join(*image_path))
        else:
            self.image = None
        self.interactable = interactable
        self.category = category
        self.rect = rect

    def get_block_coords(self):
        return f"({self.rect.center[0] // 16}, {self.rect.center[1] // 16})"

    def get_json_save_data(self):
        if not self.image:
            return None

        return {"image": self.image_path, "interactable": self.interactable, "category": self.category}


class Layer:
    def __init__(self, layers_data, layer_name):
        self.layer_data = layers_data[layer_name]
        self.name = layer_name

    def get_tile(self, xy):
        for tile in self.layer_data:
            if tile["coords"] == xy:
                return tile
        return None


class GameMap:
    def __init__(self, filename=None):
        self.tile_map = []
        self.map_size = (50, 18)
        self.player_location = None
        self.layers = []

        if filename:
            self.load_map(filename)
        else:
            self.tile_map = self.empty_map()

    @staticmethod
    def empty_map(size=(50, 18)):
        tile_map = []
        for x in range(0, size[0]):
            row = []
            for y in range(0, size[1]):
                row.append(Tile(None))
            tile_map.append(row)
        return tile_map

    @staticmethod
    def empty_save_data():
        map_data = {}
        map_data["layers"] = {}
        map_data["entities"] = {}
        map_data["meta"] = {}

        return map_data

    @staticmethod
    def get_tiles(layer_data):
        tiles = []
        for x in range(0, len(layer_data)):  # loads map
            for y in range(0, len(layer_data[x])):
                tile = layer_data[x][y]
                if tile.image:
                    tile_json = tile.get_json_save_data()
                    tile_json["coords"] = [x, y]
                    tiles.append(tile_json)
        return tiles

    @staticmethod
    def load_tile(tile_data):
        return Tile(tile_data["image"], tile_data["interactable"], tile_data["category"])

    def load_map(self, filename):
        with open(os.path.join(MAPS_DIRECTORY, filename), "r") as f:
            map_data = json.load(f)

        base_map = self.empty_map()
        self.layers = [Layer(map_data["layers"], layer) for layer in map_data["layers"]]

        width, height = map_data["meta"]["size"]
        for x in range(width):
            for y in range(height):
                for layer in self.layers:
                    tile_data = layer.get_tile([x, y])
                    if tile_data:
                        base_map[x][y] = self.load_tile(tile_data)

        self.player_location = map_data["entities"]["player"]["location"]

    def save_map(self, filename, player_location=None):
        map_data = self.empty_save_data()
        for layer in self.layers:
            map_data["layers"][layer.name] = self.get_tiles(layer.layer_data)

        # TODO REMOVE THIS AND INTRODUCE LAYERING IN GAME MODES PROPERLY
        map_data["layers"]["BASE"] = self.get_tiles(self.tile_map)

        if player_location:
            map_data["entities"]["player"] = player_location

        map_data["meta"]["size"] = self.map_size

        with open(os.path.join(MAPS_DIRECTORY, filename), "w") as f:
            json.dump(map_data, f, indent=4)

    def extend_map(self, xy):
        x, y = xy
        cur_x = len(self.tile_map)
        cur_y = len(self.tile_map[0])

        if x+1 > cur_x:
            new_base_x = x + 1
        else:
            new_base_x = cur_x
        if y+1 > cur_y:
            new_base_y = y+1
        else:
            new_base_y = cur_y

        base_map = self.empty_map((new_base_x, new_base_y))
        for x in range(0, len(self.tile_map)):
            for y in range(0, len(self.tile_map[x])):
                if self.tile_map[x][y].image:
                    base_map[x][y] = self.tile_map[x][y]

        self.map_size = (new_base_x, new_base_y)
        self.tile_map = base_map

    def render(self, screen, GS):
        x_offset, y_offset = GS.offset
        for x in range(0, len(self.tile_map)):  # loads map
            for y in range(0, len(self.tile_map[x])):
                tile = self.tile_map[x][y]
                if tile.image:
                    screen.blit(tile.image, ((x * 16) - x_offset, y * 16))
                    if tile.interactable:
                        tile.rect = pygame.Rect((x * 16) - x_offset, y * 16, 16, 16)

        if GS.debug:
            for y in range(0, len(self.tile_map[0])):
                for x in range(0, len(self.tile_map)):
                    rect = pygame.Rect((x*16)-x_offset, (y*16)-y_offset, 16, 16)
                    pygame.draw.rect(screen, (0, 0, 255), rect, 1)
            fps = str(int(GS.clock.get_fps()))
            screen.blit(FONT.render(fps, 1, (255, 255, 255)), (0, 0))

        return screen
