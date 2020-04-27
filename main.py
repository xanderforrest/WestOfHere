import pygame
pygame.init()
from pygame.locals import (
    KEYDOWN,
    QUIT,
)
from gamemodes.WorldRunner import WorldRunner
from gamemodes.WesternMaker import WesternMaker
from utilities.utilities import GlobalSettings
from utilities.consts import *

pygame.display.set_icon(pygame.image.load(os.path.join(ASSETS_DIRECTORY, WINDOW_ICON)))
pygame.display.set_caption(WINDOW_TITLE)
pygame.event.set_allowed([KEYDOWN, QUIT, pygame.MOUSEBUTTONUP])
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(None)

global_config = GlobalSettings()

games = {"worldrunner": WorldRunner, "westernmaker": WesternMaker}
global_config.next_game = "westernmaker"

while global_config.game_running:
    current_game = games[global_config.next_game]
    global_config = current_game(screen, global_config).resume()
