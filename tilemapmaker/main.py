import pygame
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
from utilities import TileLoader

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 288

pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.display.set_caption("West of Here")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

tile_map = TileLoader().load_map()
tile_rects = []
animation_count = 0

dirt_img = pygame.image.load("dirt.png")
grass_img = pygame.image.load("grass.png")

running = True
while running:
    # ANIMATION HANDLING
    dt = clock.tick(60)
    animation_count += 1
    if animation_count == 10:
        animation_count = 0

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

    pygame.display.flip()
