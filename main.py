import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Target, Bandit
from utilities import TileLoader
from consts import *
import os

pygame.init()
pygame.display.set_icon(pygame.image.load(os.path.join(ASSETS_DIRECTORY, WINDOW_ICON)))
pygame.display.set_caption(WINDOW_TITLE)

# trying to increase performance
pygame.event.set_allowed([KEYDOWN, QUIT, pygame.MOUSEBUTTONUP])
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(None)

entities = pygame.sprite.Group()
destroyables = pygame.sprite.Group()
animated = pygame.sprite.Group()
clint = Player()
entities.add(clint)
animated.add(clint)
clock = pygame.time.Clock()
tile_rects = []

cursor_img = pygame.image.load(os.path.join(ASSETS_DIRECTORY, CURSOR_IMG))
tile_map = TileLoader().load_map()
soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))
pygame.mixer.Channel(0).play(soundtrack, loops=-1)

font = pygame.font.SysFont("Arial", 32)

animation_count = 0
running = True
debug = False

while running:
    # ANIMATION HANDLING
    dt = clock.tick(60) / 1000
    animation_count += 1
    if animation_count == 5:
        animation_count = 0
        for e in animated:
            e.update_animation()

    for x in range(0, len(tile_map)):  # loads map
        for y in range(0, len(tile_map[x])):
            tile = tile_map[x][y]
            if tile.image:
                screen.blit(tile.image, (x * 16, y * 16))
                if tile.interactable:
                    tile.rect = pygame.Rect(x * 16, y * 16, 16, 16)
                    tile_rects.append(tile)

    if debug:
        # render blocks
        for y in range(18):
            for x in range(50):
                rect = pygame.Rect(x * 16, y * 16, 16, 16)
                pygame.draw.rect(screen, (0, 0, 255), rect, 1)

        # render fps
        fps = str(int(clock.get_fps()))
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
                running = False
            if event.key == K_UP:
                debug = False if debug else True
                # this will become "interact" key for entering doors
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                bullet = clint.fire_gun()
                entities.add(bullet)
            else:
                # target = Target(pygame.mouse.get_pos())
                target = Bandit(pygame.mouse.get_pos())
                destroyables.add(target)
                animated.add(target)
                entities.add(target)

    # ENTITY UPDATES
    entities.update(dt, pygame.key.get_pressed(), tile_map, destroyables)

    for entity in entities:
        screen.blit(entity.surf, entity.rect)

        if entity.name == "bullet":  # reasonably sure this could be removed, but if it isn't broke don't fix it
            for e in destroyables:
                if entity.rect.colliderect(e.rect):
                    entity.kill()
                    e.on_hit()

    pygame.display.flip()
