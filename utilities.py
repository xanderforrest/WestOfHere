import pygame
import os
from consts import *
import math
import random


def get_collisions(rect, tile_map):
    collisions = []

    cx, cy = [rect.center[0] // 16, rect.center[1] // 16]  # get the tile the rect is currently in
    tiles = []

    subetc = {}
    for i in range(-2, 3):
        if i == -3:
            subetc[i] = [0, -1, 1]
        if i == -2:
            subetc[i] = [0]
        elif i == -1:
            subetc[i] = [-1, 0, 1]
        elif i == 0:
            subetc[i] = [-2, -1, 0, 1, 2]
        elif i == 1:
            subetc[i] = [-1, 0, 1]
        elif i == 2:
            subetc[i] = [0]

    for yval in subetc:
        for xval in subetc[yval]:
            try:
                tiles.append(tile_map[cx + xval][cy + yval])
            except IndexError as e:
                pass
            # print("Entity gone out of range.")

    for tile in tiles:
        if tile.rect:
            if rect.colliderect(tile.rect):
                collisions.append(tile)
    return collisions


class GlobalSettings:
    def __init__(self):
        self.game_running = True
        self.sound_on = True


class GameState:
    def __init__(self):
        self.tile_map = []

        self.entities = pygame.sprite.Group()
        self.destroyables = pygame.sprite.Group()
        self.animated = pygame.sprite.Group()
        self.player = None

        self.clock = pygame.time.Clock()
        self.dt = None
        self.animation_count = 0

        self.running = True
        self.debug = False


class Button:
    def __init__(self, text):
        self.text = text
        self.font = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 32)

        self.button_surface = self.draw_button()
        self.rect = self.button_surface.get_rect()

    def draw_button(self):
        text_surf = self.font.render(self.text, 1, (255, 255, 255))
        size = self.font.size(self.text)

        border_size = 4
        border_offset = 4

        box_size = (size[0]+border_offset*2, size[1]+border_offset*2)
        self.button_surface = pygame.Surface(box_size)
        self.button_surface.blit(text_surf, (border_offset, border_offset))
        rect = pygame.Rect((0, 0), box_size)
        pygame.draw.rect(self.button_surface, (255, 255, 255), rect, 1)

        return self.button_surface

    def on_press(self):
        pass


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
        map[20][9] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, "saloon.png")))
        map[26][10] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, "gun-shop.png")))
        map[33][11] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, "side-shop.png")))
        map[37][10] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, "general-shop.png")))

        map[12][14] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "crate.png")))
        map[12][13] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "crate.png")))
        map[13][14] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "crate.png")))
        map[14][13] = Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "cactus.png")))
        return map

    def load_floor(self):
        map = []
        for x in range(0, 50):
            row = []
            for y in range(0, 18):
                if y >= 15:
                    if y == 15:
                        row.append(Tile(
                            pygame.image.load(os.path.join(ASSETS_DIRECTORY, "grass.png")), True, category="floor"))
                    else:
                        if random.randint(0, 5) == 3:
                            row.append(Tile(
                                pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt-variant.png")), True,
                                category="floor"))
                        else:
                            row.append(
                                Tile(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt.png")), True,
                                     category="floor"))
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
    def __init__(self, image, interactable=False, category="none", rect=None):
        self.image = image
        self.interactable = interactable
        self.category = category
        self.rect = rect

    def get_block_coords(self):
        return f"({self.rect.center[0] // 16}, {self.rect.center[1] // 16})"
