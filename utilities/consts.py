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
# ASSETS VARIABLES
ASSETS_DIRECTORY = "assets"

DIRT_IMG = "dirt.png"
GRASS_IMG = "grass.png"

SPRITESHEET_DIRECTORY = "spritesheets"
CLINT_SPRITESHEET = "clint-spritesheet.png"

SOUNDS_DIRECTORY = "sounds"
BUILDINGS_DIRECTORY = "buildings"

CRATE_BORDER = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "crateborder.png"))

# Fonts
FONT = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 32)
FONT_TITLE = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 60)

# Tiles
TILE_DIRT = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt.png"))
TILE_DIRT_VARIANT = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "dirt-variant.png"))
TILE_GRASS = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "grass.png"))
TILE_CRATE = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "crate.png"))
TILE_BARREL = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "barrel.png"))

# Other
CURSOR_IMG = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "cursor.png"))
TUMBLEWEED_IMG = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "tumbleweed.png"))