import pygame
from utilities.consts import *
from utilities.GameMap import GameMap, Tile
from utilities.GUI import TextInput, ImageButton, Interacter, Button, TickBox
from entities import Player, Bandit
from gamemodes.WorldRunner import WorldRunner


class WesternMakerGUI:
    def __init__(self):
        self.gui_surf = WESTERN_MAKER_GUI
        self.selected_object = Tile(None)

        self.buttons = []
        self.interactors = []

        self.filename_input = TextInput(16, 6 * 16, "filename")

        self.save_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "save-button.png"))
        self.play_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "play-button.png"))
        self.load_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "load-button.png"))
        self.new_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "new-button.png"))

        self.setup_buttons()

    def setup_buttons(self):
        self.save_button = ImageButton((19 * 16, 6 * 16), self.save_button_image, on_click=self.save_map)
        self.buttons.append(self.save_button)

        self.play_button = ImageButton((24 * 16, 6 * 16), self.play_button_image, on_click=self.quickplay)
        self.buttons.append(self.play_button)

        self.load_button = ImageButton((24 * 16, 4 * 16), self.load_button_image, on_click=self.load_map)
        self.buttons.append(self.load_button)

        self.newlayer_button = ImageButton((29 * 16, 6 * 16), self.new_button_image, on_click=self.new_layer)
        self.buttons.append(self.newlayer_button)

        self.grass_button = ImageButton((16, 1 * 16), TILE_GRASS, image_path=[ASSETS_DIRECTORY, "grass.png"])
        self.buttons.append(self.grass_button)

        self.dirt_variant_button = ImageButton((16, 2 * 16), TILE_DIRT_VARIANT,
                                               image_path=[ASSETS_DIRECTORY, "dirt-variant.png"])
        self.buttons.append(self.dirt_variant_button)

        self.dirt_button = ImageButton((16, 3 * 16), TILE_DIRT, image_path=[ASSETS_DIRECTORY, "dirt.png"])
        self.buttons.append(self.dirt_button)

        self.barrel_button = ImageButton((32, 1 * 16), TILE_BARREL, image_path=[ASSETS_DIRECTORY, "barrel.png"])
        self.buttons.append(self.barrel_button)

        self.crate_button = ImageButton((32, 2 * 16), TILE_CRATE, image_path=[ASSETS_DIRECTORY, "crate.png"])
        self.buttons.append(self.crate_button)

        self.interactable_check = TickBox((33 * 16, 6 * 16), on_interact=self.toggle_interactable)
        self.buttons.append(self.interactable_check)

        self.general_store = Interacter((4 * 16, 3 * 16), (7 * 16, 1 * 16), on_interact=self.building_select,
                                        name="general-shop.png")
        self.gun_store = Interacter((4 * 16, 3 * 16), (11 * 16, 1 * 16), on_interact=self.building_select,
                                    name="gun-shop.png")
        self.saloon = Interacter((3 * 16, 3 * 16), (15 * 16, 1 * 16), on_interact=self.building_select,
                                 name="saloon.png")
        self.side_store = Interacter((4 * 16, 3 * 16), (18 * 16, 1 * 16), on_interact=self.building_select,
                                     name="side-shop.png")

        self.player_select = Interacter((16, 32), (24 * 16, 1 * 16), on_interact=self.entity_select, name="player")
        self.bandit_select = Interacter((16, 32), (25 * 16, 1 * 16), on_interact=self.entity_select, name="bandit")

        self.interactors = [self.general_store, self.gun_store, self.saloon, self.side_store, self.player_select,
                            self.bandit_select]

    def get_gui_surf(self):
        self.gui_surf = pygame.Surface((800, 144))
        self.gui_surf.fill((0, 255, 255))
        self.gui_surf.blit(WESTERN_MAKER_GUI, (0, 0))

        for button in self.buttons:
            self.gui_surf.blit(button.surf, button.rect)

        self.gui_surf.blit(self.filename_input.text_surface, self.filename_input.rect)

        return self.gui_surf

    def on_click_gui(self):
        temp_cp = pygame.mouse.get_pos()
        curs_pos = (temp_cp[0], temp_cp[1] - SCREEN_HEIGHT)
        if self.filename_input.rect.collidepoint(curs_pos):
            self.filename_input.active = True
        else:
            self.filename_input.active = False

        for button in self.buttons:
            if button.rect.collidepoint(curs_pos):
                if button.name == "ImageButton":
                    if button.image_path:  # TODO move tile selects to their own object so this doesn't have to be here
                        self.selected_object = Tile(button.image_path, surf=button.surf, category="none")
                    else:
                        button.on_click()
                else:
                    button.on_click()

        for interacter in self.interactors:
            if interacter.rect.collidepoint(curs_pos):
                interacter.on_interact()

    def save_map(self):
        pass

    def quickplay(self):
        pass

    def load_map(self):
        pass

    def new_layer(self):
        pass

    def toggle_interactable(self):
        self.selected_object.interactable = self.interactable_check.ticked

    def entity_select(self, name):
        if name == "player":
            self.selected_object = Player()
        else:
            self.selected_object = Bandit()

    def building_select(self, name):
        filepath = [ASSETS_DIRECTORY, BUILDINGS_DIRECTORY, name]
        self.selected_object = Tile(filepath, category="building")


class WesternMaker(WesternMakerGUI):
    def __init__(self, screen, global_config):
        super(WesternMaker, self).__init__()
        self.screen = None
        self.global_config = global_config
        self.running = False
        self.offset = [0, 0]

        self.GameMap = GameMap()

    @staticmethod
    def get_tile_positions(coords):
        """ Returns the X and Y tile coordinates are inside of """
        return coords[0] // 16, coords[1] // 16

    def get_adjusted_mouse_pos(self):
        """ Returns the mouse position adjusted for the offset of the screen """
        real_pos = pygame.mouse.get_pos()
        adjusted = (real_pos[0] + self.offset[0], real_pos[1] + self.offset[1])
        return adjusted

    def resume(self):
        self.screen = pygame.display.set_mode((800, 432))
        self.running = True
        self.mainloop()
        return self.global_config

    def pause(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.filename_input.update(event)

            if event.key == pygame.K_ESCAPE:
                self.global_config.next_game = "mainmenu"
                self.pause()
        elif event.type == pygame.QUIT:
            self.global_config.game_running = False
            self.running = False

    def on_click_screen(self):
        curs_pos = self.get_adjusted_mouse_pos()
        tilepos = self.get_tile_positions(curs_pos)

        if "TILE" in self.selected_object.id:
            self.GameMap.place_tile(tilepos, self.selected_object, "BASE")  # replace this with layer selection later
        else:
            self.GameMap.add_entity(self.selected_object.name,
                                    self.get_adjusted_mouse_pos())  # give more options to pass stuff here

    def save_map(self):
        name = self.filename_input.text
        self.GameMap.save_map(name)
        self.global_config.default_world = name

    def quickplay(self):
        self.GameMap.save_map("tempmap.json")
        WorldRunner(self.screen, self.global_config).resume(gamemap="tempmap.json")
        self.screen = pygame.display.set_mode((800, 432))
        pygame.mixer.pause()

    def mainloop(self):
        while self.running:
            self.screen.fill((0, 255, 255))

            self.GameMap.render(self.screen, self.offset)
            gui_surf = self.get_gui_surf()

            self.screen.blit(gui_surf, (0, SCREEN_HEIGHT))

            curs_pos = pygame.mouse.get_pos()

            if curs_pos[
                1] < 288 and "TILE" in self.selected_object.id and self.selected_object.image:  # render where the tile would go if placed
                tile_x = ((curs_pos[0] + self.offset[0]) // 16)
                self.screen.blit(self.selected_object.image, ((tile_x * 16) - self.offset[0], (curs_pos[1] // 16) * 16))

            pygame.mouse.set_visible(False)
            self.screen.blit(CURSOR_IMG,
                             (curs_pos[0] - 3,
                              curs_pos[1] - 3))

            for event in pygame.event.get():
                self.handle_event(event)

            # Handle offset
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.offset[0] -= 4
            elif keys[pygame.K_RIGHT]:
                self.offset[0] += 4

            mouse_state = pygame.mouse.get_pressed()
            if mouse_state[0]:
                if curs_pos[1] < SCREEN_HEIGHT:
                    self.on_click_screen()
                else:
                    self.on_click_gui()

            pygame.display.flip()
