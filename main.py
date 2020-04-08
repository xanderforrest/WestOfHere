import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Target, Bandit
from utilities import TileLoader, GameState
from consts import *
import os

pygame.init()
pygame.display.set_icon(pygame.image.load(os.path.join(ASSETS_DIRECTORY, WINDOW_ICON)))
pygame.display.set_caption(WINDOW_TITLE)

# trying to increase performance
pygame.event.set_allowed([KEYDOWN, QUIT, pygame.MOUSEBUTTONUP])
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(None)

GS = GameState()

clint = Player()
GS.entities.add(clint)
GS.animated.add(clint)

GS.tile_map = TileLoader().load_map()

cursor_img = pygame.image.load(os.path.join(ASSETS_DIRECTORY, CURSOR_IMG))
soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))
pygame.mixer.Channel(0).play(soundtrack, loops=-1)
font = pygame.font.SysFont("Arial", 32)


while GS.running:
    # ANIMATION HANDLING
    GS.dt = GS.clock.tick(60) / 1000
    GS.animation_count += 1
    if GS.animation_count == 5:
        GS.animation_count = 0
        for e in GS.animated:
            e.update_animation()

    for x in range(0, len(GS.tile_map)):  # loads map
        for y in range(0, len(GS.tile_map[x])):
            tile = GS.tile_map[x][y]
            if tile.image:
                screen.blit(tile.image, (x * 16, y * 16))
                if tile.interactable:  # TODO move this into the tile class
                    tile.rect = pygame.Rect(x * 16, y * 16, 16, 16)

    if GS.debug:
        # render blocks
        for y in range(18):
            for x in range(50):
                rect = pygame.Rect(x * 16, y * 16, 16, 16)
                pygame.draw.rect(screen, (0, 0, 255), rect, 1)

        # render fps
        fps = str(int(GS.clock.get_fps()))
        screen.blit(font.render(fps, 1, (255, 255, 255)), (0, 0))

    # render a cursor
    pygame.mouse.set_visible(False)
    curs_pos = pygame.mouse.get_pos()
    screen.blit(cursor_img,
                (curs_pos[0] - 3, curs_pos[1] - 3))  # offset to make mouse pointer line up with cursor centre

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                GS.running = False
            if event.key == K_UP:
                GS.debug = False if GS.debug else True
                # this will become "interact" key for entering doors
        elif event.type == QUIT:
            GS.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                bullet = clint.fire_gun()
                GS.entities.add(bullet)
            else:
                # target = Target(pygame.mouse.get_pos())
                target = Bandit(pygame.mouse.get_pos())
                GS.destroyables.add(target)
                GS.animated.add(target)
                GS.entities.add(target)

    # ENTITY UPDATES
    for entity in GS.entities:
        GS = entity.update(GS, pygame.key.get_pressed())

    for entity in GS.entities:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
