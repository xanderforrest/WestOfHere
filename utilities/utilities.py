import pygame
import os
import pygame.locals
from utilities.consts import *
import random
from utilities import soundsystem


def get_collisions(rect, tile_map, offset=[0, 0]):  # TODO update this to use new GameMap system instead of hacky solutions
    collisions = []

    cx, cy = [(rect.center[0]+offset[0]) // 16, (rect.center[1]+offset[1]) // 16]  # get the tile the rect is currently in
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


def num_from_keypress(key):
    name_string = pygame.key.name(key)
    try:
        to_return = int(name_string)
    except ValueError:
        to_return = None
    return to_return


class Camera:
    def __init__(self, target):
        self.target = target
        self.offset = [0, 0]

    def update(self, GS):
        updated = False
        dif = 0
        if self.target.rect.center[0] > SCREEN_WIDTH//2:
            dif = (self.target.rect.center[0] - SCREEN_WIDTH//2)
            self.offset[0] = self.offset[0] + dif
            updated = True
        if updated:
            for entity in GS.entities:
                entity.rect.move_ip((-1 * dif, 0))

        return GS


class GlobalSettings:
    def __init__(self):
        self.game_running = True
        self.SoundSystem = soundsystem.SoundSystem()
        self.next_game = ""
        self.default_world = "menu_town.json"


class GameState:
    def __init__(self):
        self.GameMap = None

        self.entities = pygame.sprite.Group()
        self.player = None
        self.curs_pos = (0, 0)

        self.clock = pygame.time.Clock()
        self.dt = None
        self.animation_count = 0
        self.offset = [0, 0]

        self.running = True
        self.debug = False
