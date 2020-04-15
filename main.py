import pygame
from pygame.locals import (
    KEYDOWN,
    QUIT,
)
from utilities.consts import *
from gamemodes import TownMenu, MainMenu
from utilities.utilities import GlobalSettings
import os

pygame.init()
pygame.display.set_icon(pygame.image.load(os.path.join(ASSETS_DIRECTORY, WINDOW_ICON)))
pygame.display.set_caption(WINDOW_TITLE)

pygame.event.set_allowed([KEYDOWN, QUIT, pygame.MOUSEBUTTONUP])
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(None)

global_config = GlobalSettings()

while global_config.game_running:
    MainMenu(screen, global_config)
    TownMenu(screen, global_config)
