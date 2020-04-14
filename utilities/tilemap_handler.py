import pygame
import os
from utilities.consts import *
import json


class Layer:
    def __init__(self, layer_json):
        self.tile_jsons = layer_json

    def get_tile_by_coords(self, coords):
        print(self.tile_jsons)
        for tile in self.tile_jsons:
            if tile["coords"] == coords:
                return tile
        return None


class TileMapHandler:
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

    @staticmethod
    def load_tile_from_json(tile_json):
        return Tile(tile_json["image"], tile_json["interactable"], tile_json["category"])

    def load_map(self, filename):
        with open(os.path.join(MAPS_DIRECTORY, filename), "r") as f:
            json_data = json.load(f)

        tile_map = self.empty_map()  # change this to take the dimensions from the backgrounds layer in save file
        layers = json_data["layers"]
        layer_objects = [Layer(layers[layer]) for layer in layers]

        for x in range(0, len(tile_map)):
            for y in range(0, len(tile_map[x])):
                for layer in layer_objects:  # iterate over all layers in order, only load the topmost layer
                    tile_data = layer.get_tile_by_coords([x, y])
                    if tile_data:
                        tile_map[x][y] = self.load_tile_from_json(tile_data)

        return tile_map

    @staticmethod
    def get_layer_tiles(map):
        tiles = []
        for x in range(0, len(map)):  # loads map
            for y in range(0, len(map[x])):
                tile = map[x][y]
                if tile.image:
                    try:
                        tile_json = tile.get_json_save_data()
                        tile_json["coords"] = [x, y]
                        print(tile_json)
                        tiles.append(tile_json)
                    except:
                        pass
        return tiles


class Tile:
    def __init__(self, image_path, interactable=False, category="none", rect=None):
        self.image_path = image_path  # TODO make this universal so maps can work with changed directories
        print(self.image_path)
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
