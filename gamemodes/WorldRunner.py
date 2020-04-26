import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Tumbleweed
from utilities.utilities import GameState
from utilities.GameMap import GameMap
from utilities.consts import *
import os


class WorldRunner:  # TODO redo sound handling so sound settings can be changed
    def __init__(self, global_config, GS=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.global_config = global_config
        self.GS = GameState()

        self.GS.player = Player()
        self.GS.entities.add(self.GS.player)

        self.GameMap = GameMap(filename="testbutagain.json")

        self.soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))

    def resume(self):
        self.GS.running = True
        self.mainloop()

    def pause(self):
        pygame.mixer.pause()
        self.GS.running = False

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.pause()
            if event.key == K_UP:
                self.GS.debug = False if self.GS.debug else True
                # this will become "interact" key for entering doors
        elif event.type == QUIT:
            self.global_config.game_running = False
            self.GS.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.GS.player.trigger_gunfire()
            else:
                target = Tumbleweed(pygame.mouse.get_pos())
                # GS.destroyables.add(target)
                # GS.animated.add(target)
                self.GS.entities.add(target)

    def mainloop(self):
        pygame.mixer.Channel(0).play(self.soundtrack, loops=-1)
        while self.GS.running:
            self.GS.dt = self.GS.clock.tick(60) / 1000
            self.screen.fill((255, 255, 255))

            self.GameMap.render(self.screen, (0, 0))

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

            pygame.display.flip()
