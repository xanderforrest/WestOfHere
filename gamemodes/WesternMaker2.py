import pygame
from utilities.consts import *
from utilities.GameMap import GameMap
from utilities.GUI import TextInput, ImageButton, Interacter


class WesternMakerGUI:
    def __init__(self):
        self.surf = WESTERN_MAKER_GUI

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

    def render(self):
        for button in self.buttons:
            self.surf.blit(button.surf, button.rect)

    def on_click(self):
        pass


class WesternMaker:
    def __init__(self, screen, global_config):
        self.screen = None
        self.global_config = global_config
        self.running = False
        self.offset = [0, 0]

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

    def mainloop(self):
        while self.running:
            self.GameMap.render(self.screen, self.offset)

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
                    pass  # on screen, so handle placing the objec
                else:
                    pass # in GUI, so handle whatever is going on

            pygame.display.flip()
