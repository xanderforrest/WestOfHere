import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_6,
K_7,
K_LEFT,
K_RIGHT
)
from entities import Player, Tumbleweed
from utilities.utilities import GameState, Button, get_available_assets, num_from_keypress, ImageButton
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
        self.x_offset = 0

        self.gui_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "western-maker-gui.png"))
        self.screen = pygame.display.set_mode((800, 432))
        self.buttons = []

        for i, block in enumerate(self.potential_objects):
            print(i)
            x = i + 1
            tile_image = pygame.transform.scale(pygame.image.load(os.path.join(*self.potential_objects[i][1])), (64, 64))
            print(self.potential_objects[i][1])
            button = ImageButton((x * 64, 20 * 16), tile_image, image_path=self.potential_objects[i][1])
            self.buttons.append(button)

        self.mainloop()

    def place_object(self):
        pos = pygame.mouse.get_pos()
        tile_x = (pos[0]+self.x_offset) // 16
        tile_y = pos[1] // 16
        print(f"{tile_x}, {tile_y}")

        try:
            self.tile_map[tile_x][tile_y] = self.selected_object
        except IndexError:
            self.tile_map = TileMapHandler().extend_map(self.tile_map, (tile_x, tile_y))
            print(f"New map size {len(self.tile_map)}")
            self.tile_map[tile_x][tile_y] = self.selected_object

    def mainloop(self):
        while self.running:
            self.screen.fill((0, 255, 255))
            for x in range(0, len(self.tile_map)):  # loads map
                for y in range(0, len(self.tile_map[x])):
                    tile = self.tile_map[x][y]
                    if tile.image:
                        self.screen.blit(tile.image, ((x * 16)-self.x_offset, y * 16))
                        if tile.interactable:  # TODO move this into the tile class
                            tile.rect = pygame.Rect((x * 16)-self.x_offset, y * 16, 16, 16)

            if self.debug:
                # render blocks
                for y in range(18):  # this is here to show where the game is actually affected
                    for x in range(len(self.tile_map)):
                        rect = pygame.Rect((x * 16), y * 16, 16, 16)
                        pygame.draw.rect(self.screen, (0, 0, 255), rect, 1)

            # gui stuff
            self.screen.blit(self.gui_image, (0, 18*16))
            for x in range(0, 50):
                self.screen.blit(TILE_CRATE, (x*16, 18*16))

            for button in self.buttons:
                self.screen.blit(button.surf, button.rect)

            curs_posx, curs_posy = pygame.mouse.get_pos()
            curs_pos = (curs_posx, curs_posy)
            # self.screen.blit(self.title_font.render("West of Here", 1, (255, 255, 255)), (46, 60))

            # render in where the selected tile would be placed
            if curs_pos[1] < 288:  # don't want it interefering with the gui
                tile_x = ((curs_posx+self.x_offset)//16)
                self.screen.blit(self.selected_object.image, ((tile_x*16)-self.x_offset, (curs_pos[1]//16)*16))

            # render a cursor
            pygame.mouse.set_visible(False)
            self.screen.blit(CURSOR_IMG,
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
                    if event.key == K_LEFT:
                        self.x_offset -= 4
                    if event.key == K_RIGHT:
                        self.x_offset += 4
                    if event.key == K_6:
                        self.selected_object = Tile(["assets", "buildings", "general-shop.png"], category="building")
                    else:
                        obj_num = num_from_keypress(event.key)
                        if obj_num:
                            if obj_num == 1:
                                TileMapHandler().save_map("testsave.json", self.tile_map)
                elif event.type == QUIT:
                    self.global_config.game_running = False
                    self.running = False

            if pygame.mouse.get_pressed()[0]:
                if curs_pos[1] < 288:
                    self.place_object()
                else:
                    for button in self.buttons:
                        if button.rect.collidepoint(curs_pos):
                            print(button.image_path)
                            self.selected_object = Tile(button.image_path, category="none")

            pygame.display.flip()


def load(screen, global_config):
    return WesternMaker(screen, global_config)
