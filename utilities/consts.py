import os
import pygame
pygame.init()

# GAME SETTINGS
WINDOW_TITLE = "West of Here"
WINDOW_ICON = "icon.png"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 288
# 50 x 18 blocks per screen

MAPS_DIRECTORY = "maps"
GUI_DIRECTORY = "gui"
GAME_DATA_DIRECTORY = "gamedata"
# ASSETS VARIABLES
ASSETS_DIRECTORY = "assets"

DIRT_IMG = "dirt.png"
GRASS_IMG = "grass.png"

SPRITESHEET_DIRECTORY = "spritesheets"
CLINT_SPRITESHEET = "clint-spritesheet.png"
CLINT_LEG = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "clint-leg.png"))

SOUNDS_DIRECTORY = "sounds"
BUILDINGS_DIRECTORY = "buildings"

WESTERN_MAKER_GUI = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "gui.png"))
CRATE_BORDER = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "crateborder.png"))
TREASURE_SKY = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "treasurebackground.png"))
UNTICKED_BOX = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "unticked.png"))
TICKED_BOX = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "ticked.png"))

# Fonts
FONT_SMALL = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 16)
FONT = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 32)
FONT_TITLE = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 60)

# Tiles
TILE_DIRT = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt.png"))
TILE_DIRT_VARIANT = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt-variant.png"))
TILE_GRASS = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "grass.png"))
TILE_CRATE = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "crate.png"))
TILE_BARREL = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "barrel.png"))

BG2 = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "background", "BG2.png"))
FG2 = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "background", "FG2.png"))
SKY2 = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "background", "Sky2.png"))
CLOUD2 = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "background", "Cloud2.png"))


# Other
CURSOR_IMG = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "cursor.png"))
TUMBLEWEED_IMG = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "tumbleweed.png"))