import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
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

entities = pygame.sprite.Group()
clint = Player()
entities.add(clint)
clock = pygame.time.Clock()
tile_rects = []

cursor_img = pygame.image.load(os.path.join(ASSETS_DIRECTORY, CURSOR_IMG))
tile_map = TileLoader().load_map()

animation_count = 0
running = True

while running:
    # ANIMATION HANDLING
    dt = clock.tick(60)
    animation_count += 1
    if animation_count == 5:
        animation_count = 0
        clint.update_animation()

    for x in range(0, len(tile_map)):  # loads map
        for y in range(0, len(tile_map[x])):
            tile = tile_map[x][y]
            if tile.image:
                screen.blit(tile.image, (x*16, y*16))
                if tile.interactable:
                    tile.rect = pygame.Rect(x * 16, y * 16, 16, 16)
                    tile_rects.append(tile)

    # render a cursor
    pygame.mouse.set_visible(False)
    curs_pos = pygame.mouse.get_pos()
    screen.blit(cursor_img, (curs_pos[0]-3, curs_pos[1]-3))  # offset to make mouse pointer line up with cursor centre

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_UP:
                pass  # this will become "interact" key for entering doors
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            bullet = clint.on_gun_fired()
            entities.add(bullet)

    # ENTITY UPDATES
    entities.update(dt, pygame.key.get_pressed(), tile_rects)

    for entity in entities:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
