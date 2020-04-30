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
from utilities.utilities import GameState, num_from_keypress
from utilities.GameMap import GameMap, Tile
from utilities.consts import *
from utilities.GUI import TextInput, Button, ImageButton, Interacter
from gamemodes.WorldRunner import WorldRunner
import os


class WesternMaker:
    def __init__(self, screen, global_config):
        self.screen = screen
        self.global_config = global_config
        self.running = False
        self.debug = False
        self.selected_object = Tile(["assets", "dirt.png"], interactable=True)

        self.GameMap = GameMap()
        self.x_offset = 0

        self.gui_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "gui.png"))
        self.save_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "save-button.png"))
        self.play_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "play-button.png"))
        self.screen = None

        # TODO unhardcode this

        self.buttons = []
        self.filename_input = TextInput(16, 24*16, "filename")

        self.save_button = ImageButton((19*16, 24*16), self.save_button_image, on_click=self.save_map)
        self.buttons.append(self.save_button)

        self.play_button = ImageButton((24*16, 24*16), self.play_button_image, on_click=self.quickplay)
        self.buttons.append(self.play_button)

        self.grass_button = ImageButton((16, 19*16), TILE_GRASS, image_path=[ASSETS_DIRECTORY, "grass.png"])
        self.buttons.append(self.grass_button)

        self.dirt_variant_button = ImageButton((16, 20*16), TILE_DIRT_VARIANT, image_path=[ASSETS_DIRECTORY, "dirt-variant.png"])
        self.buttons.append(self.dirt_variant_button)

        self.dirt_button = ImageButton((16, 21*16), TILE_DIRT, image_path=[ASSETS_DIRECTORY, "dirt.png"])
        self.buttons.append(self.dirt_button)

        self.barrel_button = ImageButton((32, 19*16), TILE_BARREL, image_path=[ASSETS_DIRECTORY, "barrel.png"])
        self.buttons.append(self.barrel_button)

        self.crate_button = ImageButton((32, 20*16), TILE_CRATE, image_path=[ASSETS_DIRECTORY, "crate.png"])
        self.buttons.append(self.crate_button)

        self.general_store = Interacter((4 * 16, 3 * 16), (7 * 16, 19 * 16), on_interact=self.building_select,
                                        name="general-shop.png")
        self.gun_store = Interacter((4 * 16, 3 * 16), (11 * 16, 19 * 16), on_interact=self.building_select,
                                        name="gun-shop.png")
        self.saloon = Interacter((3 * 16, 3 * 16), (15 * 16, 19 * 16), on_interact=self.building_select,
                                        name="saloon.png")
        self.side_store = Interacter((4 * 16, 3 * 16), (18 * 16, 19 * 16), on_interact=self.building_select,
                                        name="side-shop.png")
        self.interactors = [self.general_store, self.gun_store, self.saloon, self.side_store]

    def resume(self):
        self.screen = pygame.display.set_mode((800, 432))
        self.running = True
        self.mainloop()
        return self.global_config

    def pause(self):
        pygame.mixer.pause()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = False

    def place_object(self):
        pos = pygame.mouse.get_pos()
        tile_x = (pos[0]+self.x_offset) // 16
        tile_y = pos[1] // 16
        print(f"{tile_x}, {tile_y}")

        try:  # TODO rewrite to handle this in gamemap
            self.GameMap.tile_map[tile_x][tile_y] = self.selected_object
        except IndexError:
            self.GameMap.extend_map([tile_x, tile_y])
            self.GameMap.tile_map[tile_x][tile_y] = self.selected_object

    def save_map(self):
        name = self.filename_input.text
        self.GameMap.save_map(name)
        self.global_config.default_world = name

    def quickplay(self):
        self.GameMap.save_map("tempmap.json")
        WorldRunner(self.screen, self.global_config).resume(gamemap="tempmap.json")
        self.screen = pygame.display.set_mode((800, 432))
        pygame.mixer.pause()

    def building_select(self, name):
        fp = [ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, name]
        self.selected_object = Tile(fp, category="building")

    def mainloop(self):
        while self.running:
            self.screen.fill((0, 255, 255))
            self.GameMap.render(self.screen, (self.x_offset, 0), debug=self.debug)

            # gui stuff
            self.screen.blit(self.gui_image, (0, 18*16))

            for button in self.buttons:
                self.screen.blit(button.surf, button.rect)

            self.screen.blit(self.filename_input.text_surface, self.filename_input.rect)

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
                    self.filename_input.update(event)

                    if event.key == K_ESCAPE:
                        self.global_config.next_game = "mainmenu"
                        self.pause()
                    if event.key == K_UP:
                        self.debug = False if self.debug else True
                        # this will become "interact" key for entering doors
                    if event.key == K_6:
                        self.selected_object = Tile(["assets", "buildings", "general-shop.png"], category="building")
                    if event.key == K_7:
                        self.GameMap.player_location = curs_posx + self.x_offset
                    else:
                        obj_num = num_from_keypress(event.key)
                        if obj_num:
                            if obj_num == 1:
                                name = self.filename_input.text
                                self.GameMap.save_map(name)
                                self.global_config.default_world = name
                            elif obj_num == 2:
                                pygame.image.save(self.screen, "testsc.png")
                elif event.type == QUIT:
                    self.global_config.game_running = False
                    self.pause()

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.x_offset -= 4
            if keys[K_RIGHT]:
                self.x_offset += 4


            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                if curs_pos[1] < 288:
                    self.place_object()
                else:
                    if self.filename_input.rect.collidepoint(curs_pos):
                        self.filename_input.active = True
                    else:
                        self.filename_input.active = False
                    for button in self.buttons:
                        if button.rect.collidepoint(curs_pos):
                            if button.image_path:
                                if pygame.mouse.get_pressed()[0]:
                                    self.selected_object = Tile(button.image_path, surf=button.surf, category="none")
                                    print("not interactable block")
                                else:
                                    self.selected_object = Tile(button.image_path, surf=button.surf, category="none", interactable=True)
                                    print("making blockinteractable")
                            else:
                                button.on_click()
                    for interacter in self.interactors:
                        if interacter.rect.collidepoint(curs_pos):
                            interacter.on_interact()

            pygame.display.flip()


def load(screen, global_config):
    return WesternMaker(screen, global_config)
