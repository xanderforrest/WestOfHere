import pygame
from utilities.consts import *
from utilities.GameMap import GameMap, Tile
from utilities.GUI import TextInput, ImageButton, Interacter, Button


class WesternMakerGUI:
    def __init__(self):
        self.gui_surf = WESTERN_MAKER_GUI
        self.selected_object = None

        self.buttons = []
        self.interactors = []

        self.filename_input = TextInput(16, 6*16, "filename")

        self.save_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "save-button.png"))
        self.play_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "play-button.png"))
        self.load_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "load-button.png"))
        self.new_button_image = pygame.image.load(os.path.join(ASSETS_DIRECTORY, GUI_DIRECTORY, "new-button.png"))

        self.setup_buttons()

    def setup_buttons(self):
        self.save_button = ImageButton((19 * 16, 24 * 16), self.save_button_image, on_click=self.save_map)
        self.buttons.append(self.save_button)

        self.play_button = ImageButton((24 * 16, 24 * 16), self.play_button_image, on_click=self.quickplay)
        self.buttons.append(self.play_button)

        self.load_button = ImageButton((24 * 16, 22 * 16), self.load_button_image, on_click=self.load_map)
        self.buttons.append(self.load_button)

        self.newlayer_button = ImageButton((24 * 16, 22 * 16), self.new_button_image, on_click=self.new_layer)
        self.buttons.append(self.newlayer_button)

        self.grass_button = ImageButton((16, 19 * 16), TILE_GRASS, image_path=[ASSETS_DIRECTORY, "grass.png"])
        self.buttons.append(self.grass_button)

        self.dirt_variant_button = ImageButton((16, 20 * 16), TILE_DIRT_VARIANT,
                                               image_path=[ASSETS_DIRECTORY, "dirt-variant.png"])
        self.buttons.append(self.dirt_variant_button)

        self.dirt_button = ImageButton((16, 21 * 16), TILE_DIRT, image_path=[ASSETS_DIRECTORY, "dirt.png"])
        self.buttons.append(self.dirt_button)

        self.barrel_button = ImageButton((32, 19 * 16), TILE_BARREL, image_path=[ASSETS_DIRECTORY, "barrel.png"])
        self.buttons.append(self.barrel_button)

        self.crate_button = ImageButton((32, 20 * 16), TILE_CRATE, image_path=[ASSETS_DIRECTORY, "crate.png"])
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

    def render_gui(self):
        for button in self.buttons:
            self.gui_surf.blit(button.surf, button.rect)

        self.gui_surf.blit(self.filename_input.text_surface, self.filename_input.rect)

    def on_click_gui(self):
        curs_pos = pygame.mouse.get_pos()
        if self.filename_input.rect.collidepoint(curs_pos):
            self.filename_input.active = True
        else:
            self.filename_input.active = False

        for button in self.buttons:
            if button.rect.collidepoint(curs_pos):
                self.selected_object = Tile(button.image_path, surf=button.surf, category="none")

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

        self.render_gui()
        self.GameMap = GameMap()

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
            if event.key == pygame.K_ESCAPE:
                self.global_config.next_game = "mainmenu"
                self.pause()
        elif event.type == pygame.QUIT:
            self.global_config.game_running = False
            self.running = False

    def on_click_screen(self):
        pass

    def mainloop(self):
        while self.running:
            self.GameMap.render(self.screen, self.offset)
            self.screen.blit(self.gui_surf, (0, SCREEN_HEIGHT))

            curs_pos = pygame.mouse.get_pos()
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


