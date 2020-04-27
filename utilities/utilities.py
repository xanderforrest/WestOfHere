import pygame
import os
import pygame.locals
from utilities.consts import *
import random
from utilities import soundsystem
from PIL import Image


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
        if tile.interactable:
            if rect.colliderect(tile.rect):
                collisions.append(tile)
    return collisions


def get_available_assets(directory):  # this only gets tiles at the moment for simplicity
    tiles = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                file_path = os.path.join(root, file)
                image = Image.open(file_path)
                if image.size == (16, 16):
                    tiles.append([file, [root, file]])
    return tiles


def num_from_keypress(key):
    name_string = pygame.key.name(key)
    try:
        to_return = int(name_string)
    except ValueError:
        to_return = None
    return to_return


class Camera:
    def __init__(self, target):
        pass  # TODO this


class GlobalSettings:
    def __init__(self):
        self.game_running = True
        self.SoundSystem = soundsystem.SoundSystem()


class GameState:
    def __init__(self):
        self.GameMap = None

        self.entities = pygame.sprite.Group()
        self.destroyables = pygame.sprite.Group()
        self.animated = pygame.sprite.Group()
        self.player = None
        self.curs_pos = (0, 0)

        self.clock = pygame.time.Clock()
        self.dt = None
        self.animation_count = 0
        self.offset = [0, 0]

        self.running = True
        self.debug = False
