import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Bandit
from utilities.utilities import GameState, Camera
from utilities.GameMap import GameMap
from utilities.consts import *
import random
import os


class TreasureProtect:  # TODO redo sound handling so sound settings can be changed
    def __init__(self, screen, global_config, GS=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
        self.global_config = global_config
        self.GS = GameState()

        self.GS.player = Player()
        self.GS.Camera = Camera(self.GS.player)
        self.GS.entities.add(self.GS.player)

        self.goal = (14*16, 18*16)
        self.SPAWN_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_ENEMY, 750)

        self.GS.GameMap = GameMap("treasure.json")
        self.first_start = True

        self.soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))

    def resume(self):
        self.GS.running = True
        self.mainloop()
        return self.global_config

    def pause(self):
        pygame.mixer.pause()
        self.GS.running = False

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.global_config.next_game = "mainmenu"
                self.pause()
            if event.key == K_UP:
                self.GS.debug = False if self.GS.debug else True
                # this will become "interact" key for entering doors
            if event.key == pygame.K_2:
                pygame.image.save(self.screen, "testsc.png")
        elif event.type == QUIT:
            self.global_config.game_running = False
            self.GS.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.GS.player.trigger_gunfire()
        elif event.type == self.SPAWN_ENEMY:
            if random.randint(0, 1) == 1:
                pos = (SCREEN_WIDTH - 20 - self.GS.Camera.offset[0], SCREEN_HEIGHT - 60 - self.GS.Camera.offset[0])
                if random.randint(0, 5) == 5:
                    pos = (16, 16)
                entity = Bandit(pos, goal=self.goal, hostile=True)
                self.GS.entities.add(entity)

    def mainloop(self):
        pygame.mixer.Channel(0).play(self.soundtrack, loops=-1)
        while self.GS.running:
            self.GS.dt = self.GS.clock.tick(60) / 1000
            self.screen.blit(TREASURE_SKY, (0, 0))

            self.GS.GameMap.render(self.screen, self.GS.Camera.offset, self.GS.debug)

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

            self.GS = self.GS.Camera.update(self.GS)
            pygame.display.flip()
