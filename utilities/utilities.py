import pygame
import os
from utilities.consts import *
import random
from utilities import soundsystem


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
        self.SoundSystem = soundsystem.SoundSystem()


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
        self.button_surface = pygame.Surface(box_size, pygame.SRCALPHA)
        self.button_surface.blit(text_surf, (border_offset, border_offset))
        rect = pygame.Rect((0, 0), box_size)
        pygame.draw.rect(self.button_surface, (255, 255, 255), rect, border_size)

        return self.button_surface

    def on_press(self):
        pass