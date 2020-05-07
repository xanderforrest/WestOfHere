import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from utilities.GameMap import GameMap
from utilities.GUI import Button
from utilities.consts import *


class MainMenu:
    def __init__(self, screen, global_config):
        self.screen = screen
        self.global_config = global_config
        self.running = True
        self.first_start = True

        self.buttons = []
        self.start_button = Button("play", self.start_game)
        self.buttons.append(self.start_button)
        self.settings_button = Button("create", self.start_maker)
        self.buttons.append(self.settings_button)
        self.play_treasure = Button("treasure protect", self.start_treasure)
        self.buttons.append(self.play_treasure)
        self.selected_button = None

        self.GameMap = GameMap("menu_town.json")

    def resume(self):
        self.running = True
        self.mainloop()
        return self.global_config

    def pause(self):
        pygame.mixer.pause()
        self.running = False

    def start_maker(self):
        self.global_config.next_game = "westernmaker"
        self.pause()

    def start_game(self):
        self.global_config.next_game = "worldrunner"
        self.pause()

    def start_treasure(self):
        self.global_config.next_game = "treasureprotect"
        self.pause()

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
        elif event.type == QUIT:
            self.global_config.game_running = False
            self.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.selected_button:
                    self.selected_button.on_hit()

    def mainloop(self):
        while self.running:
            self.GameMap.render(self.screen)

            pygame.mouse.set_visible(False)
            curs_pos = pygame.mouse.get_pos()
            self.screen.blit(CURSOR_IMG,
                             (curs_pos[0] - 3,
                              curs_pos[1] - 3))  # offset to make mouse pointer line up with cursor centre

            for button in self.buttons:
                if button.rect.collidepoint(curs_pos):
                    button.update_highlight("on")
                    self.selected_button = button
                    break
                else:
                    button.update_highlight("off")
                    self.selected_button = None

            # menu rendering
            self.screen.blit(FONT_TITLE.render("West of Here", 1, (255, 255, 255)), (46, 60))
            self.start_button.rect.center = (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.08))
            self.screen.blit(self.start_button.button_surface, self.start_button.rect)
            self.settings_button.rect.center = (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.08))
            self.screen.blit(self.settings_button.button_surface, self.settings_button.rect)
            self.play_treasure.rect.center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT*0.1)
            self.screen.blit(self.play_treasure.button_surface, self.play_treasure.rect)

            # EVENT HANDLING
            for event in pygame.event.get():
                self.handle_event(event)

            pygame.display.flip()
