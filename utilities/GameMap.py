import pygame
import json
from utilities.consts import *
from utilities.utilities import get_collisions, get_entity_by_name
import uuid


def empty_map(size=(50, 18)):
    if size[0] == 0 and size[1] == 0:
        return [[Tile(None)]]
    tile_map = []
    for x in range(0, size[0]):
        row = []
        for y in range(0, size[1]):
            row.append(Tile(None))
        tile_map.append(row)
    return tile_map


def load_tile(tile_data):
    return Tile(tile_data["image"], tile_data["interactable"], tile_data["category"])


class Tile:
    def __init__(self, image_path, interactable=False, category="none", rect=None, surf=None):
        self.id = "TILE" + str(uuid.uuid4())
        self.image_path = image_path  # TODO make this universal so maps can work with changed directories
        if self.image_path:
            self.image = pygame.image.load(os.path.join(*image_path))
            self.rect = self.image.get_rect()
        elif surf:
            self.image = surf
            self.rect = self.image.get_rect()
        else:
            self.image = None
            self.rect = rect
        self.interactable = interactable
        self.category = category

    def get_block_coords(self):
        return f"({self.rect.center[0] // 16}, {self.rect.center[1] // 16})"

    def get_json_save_data(self):
        if not self.image:
            return None

        return {"image": self.image_path, "interactable": self.interactable, "category": self.category}


class Layer:
    def __init__(self, layers_data, layer_name):
        self.tile_map = [[]]
        self.layer_data = layers_data[layer_name]
        self.name = layer_name
        self.size = self.get_size()
        self.tile_map = self.gen_tile_map()

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

        base_map = empty_map((new_base_x, new_base_y))
        for x in range(0, len(self.tile_map)):
            for y in range(0, len(self.tile_map[x])):
                if self.tile_map[x][y].image:
                    base_map[x][y] = self.tile_map[x][y]

        self.size = [new_base_x, new_base_y]
        self.tile_map = base_map

    def gen_tile_map(self):
        base = empty_map(self.size)

        for tile in self.layer_data:
            x, y = tile["coords"]
            try:
                base[x][y] = load_tile(tile)
            except IndexError:
                self.extend_map([x, y])

        return base

    def get_size(self):
        lx = 50
        ly = 18
        for tile in self.layer_data:

            x, y = tile["coords"]

            if x > lx:
                lx = x
            if y > ly:
                ly = y
        return [lx+1, ly+1]

    def get_tile(self, xy):
        for tile in self.layer_data:
            if tile["coords"] == xy:
                return tile
        return None

    def add_tile(self, pos, tile):
        x, y = pos
        try:
            self.tile_map[x][y] = tile
        except IndexError:
            self.extend_map(pos)
            self.add_tile(pos, tile)

    def get_layer_data(self):
        tiles = []
        for x in range(0, len(self.tile_map)):  # loads map
            for y in range(0, len(self.tile_map[x])):
                tile = self.tile_map[x][y]
                if tile.image:
                    tile_json = tile.get_json_save_data()
                    tile_json["coords"] = [x, y]
                    tiles.append(tile_json)
        return tiles


class GameMap:
    def __init__(self, filename=None):
        self.player_location = None
        self.layers = []
        self.entities = []

        if filename:
            self.load_map(filename)
        else:
            self.layers.append(Layer({"BASE": []}, "BASE"))

    @staticmethod
    def empty_save_data():
        map_data = {}
        map_data["layers"] = {}
        map_data["entities"] = {}
        map_data["entities"]["other"] = []
        map_data["meta"] = {}

        return map_data

    def get_collisions(self, rect, offset):
        collisions = []
        for layer in self.layers:
            layer_collisions = get_collisions(rect, layer.tile_map, offset)
            collisions.extend(layer_collisions)
        return collisions

    def get_layer(self, layer_name):
        for pos in self.layers:
            if pos.name == layer_name:
                return pos
        return None

    def load_map(self, filename):
        with open(os.path.join(MAPS_DIRECTORY, filename), "r") as f:
            map_data = json.load(f)

        self.layers = [Layer(map_data["layers"], layer) for layer in map_data["layers"]]

        try:
            self.player_location = map_data["entities"]["player"]
        except (KeyError, TypeError):
            self.player_location = None

    def save_map(self, filename):
        map_data = self.empty_save_data()
        for layer in self.layers:
            map_data["layers"][layer.name] = layer.get_layer_data()

        map_data["entities"]["player"] = self.player_location

        for entity in self.entities:
            if entity.name != "player":  # separate behaviour
                map_data["entities"]["other"].append(entity.serialise())  # TODO make sure this is implemented

        with open(os.path.join(MAPS_DIRECTORY, filename), "w") as f:
            json.dump(map_data, f, indent=4)

    def place_tile(self, position, tile, layer_name):
        layer = self.get_layer(layer_name)
        if layer:
            layer.add_tile(position, tile)
        else:
            print(f"Layer '{layer_name}' not found")

    def add_entity(self, name, pos):
        if name == "player":
            self.player_location = pos

        instance = get_entity_by_name(name)()  # get ref and instantiate it
        instance.rect.topleft = pos

        self.entities.append(instance)

    def render(self, screen, offset=(0, 0), debug=False, fps=None, inf_background=False):
        x_offset, y_offset = offset

        offset_layers = {"sky": [16, SKY2], "bg": [16, BG2], "cloud": [2, CLOUD2], "fg": [8, FG2]}

        if inf_background:  # 850 is inf background width, there must be two blits when each half of background is on screen
            for layer in offset_layers:
                used_offset = offset[0] // offset_layers[layer][0]
                corrected_offset = ((used_offset) % 850)
                second_blit = corrected_offset + -850

                for valuee in [corrected_offset, second_blit]:
                    print(f"blitting at {valuee}")
                    screen.blit(offset_layers[layer][1],
                                 (-valuee, 0))

        for layer in self.layers:
            for x in range(0, len(layer.tile_map)):  # loads map
                for y in range(0, len(layer.tile_map[x])):
                    tile = layer.tile_map[x][y]
                    if tile.image:
                        screen.blit(tile.image, ((x * 16) - x_offset, y * 16))
                        if tile.interactable:
                            tile.rect = pygame.Rect((x * 16) - x_offset, y * 16, 16, 16)

        for entity in self.entities:
            screen.blit(entity.surf, entity.rect)

        if debug and False:  # TODO change this to use a layer or combination of layers
            for y in range(0, len(self.tile_map[0])):
                for x in range(0, len(self.tile_map)):
                    rect = pygame.Rect((x*16)-x_offset, (y*16)-y_offset, 16, 16)
                    pygame.draw.rect(screen, (0, 0, 255), rect, 1)
        if fps:
            fps = str(fps)
            screen.blit(FONT.render(fps, 1, (255, 255, 255)), (0, 0))

        return screen
