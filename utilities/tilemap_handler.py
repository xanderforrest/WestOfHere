import pygame
import os
from utilities.consts import *
import json


class Layer:
    def __init__(self, layer_json):
        self.tile_jsons = layer_json

    def get_tile_by_coords(self, coords):
        for tile in self.tile_jsons:
            if tile["coords"] == coords:
                return tile
        return None


class TileMapHandler:
    def __init__(self):
        pass

    @staticmethod
    def empty_map(size=(50, 18)):
        map = []
        for x in range(0, size[0]):
            row = []
            for y in range(0, size[1]):
                row.append(Tile(None))
            map.append(row)
        return map

    def extend_map(self, tile_map, xy):
        x, y = xy
        cur_x = len(tile_map)
        cur_y = len(tile_map[0])
        print(f"Proposed {x}, {y}")
        print(f"Current {cur_x}, {cur_y}")

        if x+2 > cur_x:
            new_base_x = x + 2
        else:
            new_base_x = cur_x
        if y+2 > cur_y:
            new_base_y = y+2
        else:
            new_base_y = cur_y

        print(f"Creating new map of {new_base_x}, {new_base_y}")
        base_map = self.empty_map((new_base_x, new_base_y))
        for x in range(0, len(tile_map)):
            for y in range(0, len(tile_map[x])):
                if tile_map[x][y].image:
                    base_map[x][y] = tile_map[x][y]

        return base_map


    @staticmethod
    def load_tile_from_json(tile_json):
        return Tile(tile_json["image"], tile_json["interactable"], tile_json["category"])

    def save_map(self, filename, tile_map):
        json_data = {}
        json_data["layers"] = {}
        # layering hasnt been introduced to tilemaker so one layer is assumed
        json_data["layers"]["general"] = []

        tiles = self.get_layer_tiles(tile_map)
        json_data["layers"]["general"] = tiles

        with open(os.path.join(MAPS_DIRECTORY, filename), "w") as f:
            json.dump(json_data, f, indent=4)

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
                        tiles.append(tile_json)
                    except:
                        pass
        return tiles


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
