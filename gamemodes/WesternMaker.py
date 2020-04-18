import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_6,
K_7
)
from entities import Player, Tumbleweed
from utilities.utilities import GameState, Button, get_available_assets, num_from_keypress
from utilities.tilemap_handler import TileMapHandler, Tile
from utilities.consts import *
import os


class WesternMaker:
    def __init__(self, screen, global_config):
        self.screen = screen
        self.global_config = global_config
        self.running = True
        self.debug = False
        self.potential_objects = get_available_assets("assets")
        self.selected_object = Tile(["assets", "dirt.png"], interactable=True)
        for i, obj in enumerate(self.potential_objects):
            print(f"{i} - {obj[0]}")

        self.tile_map = TileMapHandler().empty_map()
        print(self.tile_map)
        self.cursor_img = pygame.image.load(os.path.join(ASSETS_DIRECTORY, CURSOR_IMG))

        self.font = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 32)
        self.title_font = pygame.font.Font(os.path.join(ASSETS_DIRECTORY, "fonts", "arcade-font.ttf"), 60)

        self.mainloop()

    def place_object(self):
        pos = pygame.mouse.get_pos()
        tile_x = pos[0] // 16
        tile_y = pos[1] // 16

        try:
            self.tile_map[tile_x][tile_y] = self.selected_object
        except IndexError:
            self.tile_map = TileMapHandler().extend_map(self.tile_map, (tile_x, tile_y))
            self.place_object()

    def mainloop(self):
        while self.running:
            self.screen.fill((0, 255, 255))
            for x in range(0, len(self.tile_map)):  # loads map
                for y in range(0, len(self.tile_map[x])):
                    tile = self.tile_map[x][y]
                    if tile.image:
                        self.screen.blit(tile.image, (x * 16, y * 16))
                        if tile.interactable:  # TODO move this into the tile class
                            tile.rect = pygame.Rect(x * 16, y * 16, 16, 16)

            if self.debug:
                # render blocks
                for y in range(18):
                    for x in range(50):
                        rect = pygame.Rect(x * 16, y * 16, 16, 16)
                        pygame.draw.rect(self.screen, (0, 0, 255), rect, 1)

            curs_pos = pygame.mouse.get_pos()
            # self.screen.blit(self.title_font.render("West of Here", 1, (255, 255, 255)), (46, 60))

            # render in where the selected tile would be placed
            self.screen.blit(self.selected_object.image, ((curs_pos[0]//16)*16, (curs_pos[1]//16)*16))

            # render a cursor
            pygame.mouse.set_visible(False)
            self.screen.blit(self.cursor_img,
                             (curs_pos[0] - 3,
                              curs_pos[1] - 3))  # offset to make mouse pointer line up with cursor centre

            # EVENT HANDLING
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_UP:
                        self.debug = False if self.debug else True
                        # this will become "interact" key for entering doors
                    if event.key == K_6:
                        self.selected_object = Tile(["assets", "buildings", "general-shop.png"], category="building")
                    elif event.key == K_7:
                        self.screen = pygame.display.set_mode((800, 600))
                    else:
                        obj_num = num_from_keypress(event.key)
                        if obj_num:
                            if obj_num < len(self.potential_objects):
                                new_selected_path = self.potential_objects[obj_num][1]
                                self.selected_object = Tile([new_selected_path], category="none")
                elif event.type == QUIT:
                    self.global_config.game_running = False
                    self.running = False

            if pygame.mouse.get_pressed()[0]:
                self.place_object()

            pygame.display.flip()


def load(screen, global_config):
    return WesternMaker(screen, global_config)
