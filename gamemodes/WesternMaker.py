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
from utilities.utilities import GameState, get_available_assets, num_from_keypress
from utilities.GameMap import GameMap, Tile
from utilities.consts import *
from utilities.GUI import TextInput, Button, ImageButton
import os


class WesternMaker:
    def __init__(self, screen, global_config):
        self.screen = screen
        self.global_config = global_config
        self.running = False
        self.debug = False
        self.potential_objects = get_available_assets("assets")
        self.selected_object = Tile(["assets", "dirt.png"], interactable=True)
        for i, obj in enumerate(self.potential_objects):
            print(f"{i} - {obj[0]}")

        self.GameMap = GameMap()
        self.x_offset = 0

        self.gui_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "western-maker-gui.png"))
        self.screen = None
        self.buttons = []
        self.filename_input = TextInput(200, 400, "filename.json")

        for i, block in enumerate(self.potential_objects):
            print(i)
            x = i + 1
            tile_image = pygame.transform.scale(pygame.image.load(os.path.join(*self.potential_objects[i][1])), (64, 64))
            print(self.potential_objects[i][1])
            button = ImageButton((x * 64, 20 * 16), tile_image, image_path=self.potential_objects[i][1])
            self.buttons.append(button)

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

    def mainloop(self):
        while self.running:
            self.screen.fill((0, 255, 255))
            self.GameMap.render(self.screen, (self.x_offset, 0), debug=self.debug)

            # gui stuff
            #self.screen.blit(self.gui_image, (0, 18*16))
            for x in range(0, 50):
                self.screen.blit(TILE_CRATE, (x*16, 18*16))
                self.screen.blit(TILE_CRATE, (x*16, 26*16))
            for y in range(18, 27):
                self.screen.blit(TILE_CRATE, (0, y*16))
                self.screen.blit(TILE_CRATE, (49*16, y*16))

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
                        self.global_config.next_game = "worldrunner"
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
                            print(button.image_path)
                            if pygame.mouse.get_pressed()[0]:
                                self.selected_object = Tile(button.image_path, category="none")
                                print("not interactable block")
                            else:
                                self.selected_object = Tile(button.image_path, category="none", interactable=True)
                                print("making blockinteractable")
            pygame.display.flip()


def load(screen, global_config):
    return WesternMaker(screen, global_config)
