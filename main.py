import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Target, Bandit, Tumbleweed
from utilities import TileLoader, GameState
from consts import *
from gamemodes import TownMenu
import os

pygame.init()
pygame.display.set_icon(pygame.image.load(os.path.join(ASSETS_DIRECTORY, WINDOW_ICON)))
pygame.display.set_caption(WINDOW_TITLE)

# trying to increase performance
pygame.event.set_allowed([KEYDOWN, QUIT, pygame.MOUSEBUTTONUP])
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(None)

game_running = True

while game_running:
    TownMenu(screen)
