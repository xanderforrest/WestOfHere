import pygame
import os
from utilities.consts import *
import random
import json


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

    def load_background(self):
        map = self.empty_map()
        map[0][0] = Tile([ASSETS_DIRECTORY, "mountains.png"])
        return map

    def load_buildings(self):
        map = self.empty_map()
        map[20][9] = Tile([ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, "saloon.png"])
        map[26][10] = Tile([ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, "gun-shop.png"])
        map[33][11] = Tile([ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, "side-shop.png"])
        map[37][10] = Tile([ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, "general-shop.png"])

        map[12][14] = Tile([ASSETS_DIRECTORY, "crate.png"])
        map[12][13] = Tile([ASSETS_DIRECTORY, "crate.png"])
        map[13][14] = Tile([ASSETS_DIRECTORY, "crate.png"])
        map[14][13] = Tile([ASSETS_DIRECTORY, "cactus.png"])
        return map

    def load_floor(self):
        map = []
        for x in range(0, 50):
            row = []
            for y in range(0, 18):
                if y >= 15:
                    if y == 15:
                        row.append(Tile([ASSETS_DIRECTORY, "dirt.png"], True, category="floor"))
                    else:
                        if random.randint(0, 5) == 3:
                            row.append(Tile([ASSETS_DIRECTORY, "dirt-variant.png"], True, category="floor"))
                        else:
                            row.append(Tile([ASSETS_DIRECTORY, "dirt.png"], True, category="floor"))
                else:
                    row.append(Tile(None))
            map.append(row)
        return map

    def get_layer_tiles(self, map):
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

    def gen_save_file(self):
        #background_tiles = [Tile([ASSETS_DIRECTORY, "mountains.png"])]
        #background_tiles[0]["coords"] = [0, 0]
        buildings_layer = self.load_buildings()
        buildings_tiles = self.get_layer_tiles(buildings_layer)
        floor_layer = self.load_floor()
        floor_tiles = self.get_layer_tiles(floor_layer)

        save_json = {"layers": {}}
        #ave_json["layers"]["background"] = background_tiles
        save_json["layers"]["buildings"] = buildings_tiles
        save_json["layers"]["floor"] = floor_tiles

        with open("test_save.json", "w") as f:
            json.dump(save_json, f, indent=4)


class Tile:
    def __init__(self, image_path, interactable=False, category="none", rect=None):
        self.image_path = image_path  # TODO make this universal so maps can work with changed directories
        print(self.image_path)
        if self.image_path:
            #current_path = os.path.dirname(__file__)
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

TileMapHandler().gen_save_file()
