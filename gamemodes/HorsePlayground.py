import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Tumbleweed, Bandit, Horse
from utilities.utilities import GameState, Camera
from utilities.GameMap import GameMap
from utilities.consts import *
from utilities.GUI import file_loader
import os


class HorsePlayground:  # TODO redo sound handling so sound settings can be changed
    def __init__(self, screen, global_config, GS=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.global_config = global_config
        self.GS = GameState()

        self.GS.player = Player()
        self.GS.Camera = Camera(self.GS.player)
        self.GS.entities.add(self.GS.player)

        self.GS.GameMap = None
        self.first_start = True

        self.soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))

    def resume(self, gamemap=None):
        if self.first_start and not gamemap:
            map_file = "para" # hardcoded in filename temporarily
            if not map_file:
                self.pause()
            else:
                self.GS.GameMap = GameMap(map_file)
                self.first_start = False

                if gamemap:
                    map_file = gamemap
                    self.GS.GameMap = GameMap(map_file)
                    self.first_start = False

                if self.GS.GameMap.player_location:
                    self.GS.player.rect.topleft = self.GS.GameMap.player_location
                else:
                    self.GS.player.rect.topleft = (10, 10)

                self.GS.running = True
                self.mainloop()

                return self.global_config

    def pause(self):
        pygame.mixer.pause()
        self.GS.running = False
        return self.global_config

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.global_config.next_game = "mainmenu"
                self.pause()
            if event.key == K_UP:
                self.GS.debug = False if self.GS.debug else True
        elif event.type == QUIT:
            self.global_config.game_running = False
            self.GS.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.GS.player.trigger_gunfire()
            else:
                target = Horse(spawn_point=pygame.mouse.get_pos())
                self.GS.entities.add(target)

    def mainloop(self):
        # pygame.mixer.Channel(0).play(self.soundtrack, loops=-1)
        while self.GS.running:
            self.GS.dt = self.GS.clock.tick(60) / 1000

            if self.GS.debug:
                fps_value = int(self.GS.clock.get_fps())
                self.GS.GameMap.render(self.screen, self.GS.Camera.offset, self.GS.debug,
                                       fps=fps_value, inf_background=True)
            else:
                self.GS.GameMap.render(self.screen, self.GS.Camera.offset, self.GS.debug, inf_background=True)


            self.GS.curs_pos = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)
            self.screen.blit(CURSOR_IMG,
                             (self.GS.curs_pos[0] - 3,
                              self.GS.curs_pos[1] - 3))

            for event in pygame.event.get():
                self.handle_event(event)

            for entity in self.GS.entities:
                self.GS = entity.update(self.GS, pygame.key.get_pressed())

            for entity in self.GS.entities:
                self.screen.blit(entity.surf, entity.rect)

            if self.GS.player.mount:  # horrible, temporary fix.
                self.screen.blit(CLINT_LEG, self.GS.player.rect)

            self.GS = self.GS.Camera.update(self.GS)
            pygame.display.flip()
