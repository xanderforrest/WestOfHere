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


class TestWorld:  # TODO redo sound handling so sound settings can be changed
    def __init__(self, screen, global_config):
        self.screen = screen
        self.global_config = global_config
        self.GS = GameState()

        self.GS.player = Player()
        self.GS.entities.add(self.GS.player)

        self.GameMap = GameMap(filename=str(input("Worldname: ")+".json"))

        self.soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))
        pygame.mixer.Channel(0).play(self.soundtrack, loops=-1)

        self.mainloop()

    def mainloop(self):
        while self.GS.running:
            # update game clock
            self.GS.dt = self.GS.clock.tick(60) / 1000
            self.screen.fill((255, 255, 255))

            self.GameMap.render(self.screen, self.GS)

            self.GS.curs_pos = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)
            self.screen.blit(CURSOR_IMG,
                             (self.GS.curs_pos[0] - 3,
                              self.GS.curs_pos[1] - 3))

            # EVENT HANDLING
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mixer.pause()
                        self.GS.running = False
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

            # ENTITY UPDATES
            for entity in self.GS.entities:
                self.GS = entity.update(self.GS, pygame.key.get_pressed())

            for entity in self.GS.entities:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
