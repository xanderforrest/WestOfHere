import pygame
import random
import numpy as np
import pygame.gfxdraw
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player
from utilities import TileLoader
from consts import *
import os

pygame.init()

pygame.display.set_icon(pygame.image.load(os.path.join(ASSETS_DIRECTORY, WINDOW_ICON)))
pygame.display.set_caption(WINDOW_TITLE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255))

entities = pygame.sprite.Group()
clint = Player()
entities.add(clint)
clock = pygame.time.Clock()

dirt_img = pygame.image.load(os.path.join(ASSETS_DIRECTORY, DIRT_IMG))
grass_img = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GRASS_IMG))
tile_map = TileLoader().load_map()
tile_rects = []

buildings = [[pygame.image.load(os.path.join(ASSETS_DIRECTORY, "BUILDINGS", "saloon.png")), [20, 15]]]


animation_count = 0

running = True
while running:
    # ANIMATION HANDLING
    dt = clock.tick(60)
    animation_count += 1
    if animation_count == 5:
        animation_count = 0
        clint.update_animation()

    # TILE RENDERING
    screen.fill((255, 101, 0))
    for x in range(0, 50):
        for y in range(0, 18):
            if tile_map[y][x] == 1:
                screen.blit(grass_img, (x * 16, y * 16))
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            elif tile_map[y][x] == 0:
                screen.blit(dirt_img, (x * 16, y * 16))
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            else:
                pass

    for build in buildings:
        obj = build[0]
        chunks = build[1]

        screen.blit(obj, (chunks[0]*16, (chunks[1]-6)*16))

    # EVENT HANDLING
    jumped = False
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_UP:
                clint.trigger_jump(tile_rects)
                jumped = True
        elif event.type == QUIT:
            running = False

    # ENTITY UPDATES
    if not jumped:
        entities.update(dt, pygame.key.get_pressed(), tile_rects)
    for entity in entities:
        screen.blit(entity.surf, entity.rect)
    pygame.display.flip()
