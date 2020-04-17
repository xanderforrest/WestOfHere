import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Tumbleweed
from utilities.utilities import GameState, Button
from utilities.tilemap_handler import TileMapHandler, Tile
from utilities.consts import *
import os


class MainMenu:
    def __init__(self, screen, global_config):
        self.screen = screen
        self.global_config = global_config
        self.running = True

        self.buttons = []
        self.start_button = Button("play", self.play_game)
        self.buttons.append(self.start_button)
        self.settings_button = Button("config")
        self.buttons.append(self.settings_button)

        self.tile_map = TileMapHandler().load_map("menu_town.json")
        self.cursor_img = pygame.image.load(os.path.join(ASSETS_DIRECTORY, CURSOR_IMG))
        self.font = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 32)
        self.title_font = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 60)

        self.mainloop()

    def play_game(self):
        self.running = False  # kill this game state after this loop

    def mainloop(self):
        while self.running:
            selected_button = None

            for x in range(0, len(self.tile_map)):  # loads map
                for y in range(0, len(self.tile_map[x])):
                    tile = self.tile_map[x][y]
                    if tile.image:
                        self.screen.blit(tile.image, (x * 16, y * 16))
                        if tile.interactable:  # TODO move this into the tile class
                            tile.rect = pygame.Rect(x * 16, y * 16, 16, 16)

            # render a cursor
            pygame.mouse.set_visible(False)
            curs_pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor_img,
                             (curs_pos[0] - 3,
                              curs_pos[1] - 3))  # offset to make mouse pointer line up with cursor centre

            for button in self.buttons:
                if button.rect.collidepoint(curs_pos):
                    button.update_highlight("on")
                    selected_button = button
                    break
                else:
                    button.update_highlight("off")
                    selected_button = None

            # menu rendering
            self.screen.blit(self.title_font.render("West of Here", 1, (255, 255, 255)), (46, 60))
            self.start_button.rect.center = (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.08))
            self.screen.blit(self.start_button.button_surface, self.start_button.rect)
            self.settings_button.rect.center = (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.08))
            self.screen.blit(self.settings_button.button_surface, self.settings_button.rect)

            # EVENT HANDLING
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                elif event.type == QUIT:
                    self.global_config.game_running = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # is the mouse currently colliding with a button?
                        if selected_button:
                            print("pressing button")
                            selected_button.on_hit()

            pygame.display.flip()
