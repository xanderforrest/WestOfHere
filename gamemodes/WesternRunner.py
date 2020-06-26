import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Tumbleweed, Bandit
from utilities.utilities import GameState, Camera
from utilities.GameMap import GameMap
from utilities.consts import *
from utilities.GUI import file_loader
import os


class Clint(Player):
    def __init__(self):
        super(Clint, self).__init__()
        self.acceleration = 15
        self.max_v = [100, 200]
        self.max_jump_height = 40
        self.jump_velocity = [-20, 0]


class WesternRunner:  # TODO redo sound handling so sound settings can be changed
    def __init__(self, screen, global_config, GS=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.global_config = global_config
        self.GS = GameState()
        self.name = "westernrunner"

        self.GS.player = Clint()
        self.GS.Camera = Camera(self.GS.player)
        self.GS.entities.add(self.GS.player)

        self.GS.GameMap = None
        self.first_start = True

        self.soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))

    def resume(self, gamemap=None):
        if self.first_start and not gamemap:
            self.GS.GameMap = GameMap("WesternRunner1", os.path.join("gamedata", self.name))
            self.first_start = False
        if gamemap:
            map_file = gamemap
            self.GS.GameMap = GameMap(map_file)
            self.first_start = False

        print(self.GS.GameMap.player_location)
        if self.GS.GameMap.player_location:
            self.GS.player.rect.topleft = self.GS.GameMap.player_location

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
        elif event.type == QUIT:
            self.global_config.game_running = False
            self.GS.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.GS.player.trigger_gunfire()
            else:
                target = Bandit(pygame.mouse.get_pos(), hostile=True)
                self.GS.entities.add(target)

    def mainloop(self):
        pygame.mixer.Channel(0).play(self.soundtrack, loops=-1)
        while self.GS.running:
            self.GS.dt = self.GS.clock.tick(60) / 1000
            self.screen.blit(pygame.image.load(os.path.join(ASSETS_DIRECTORY, "stitched-bg.png")), (-self.GS.Camera.offset[0], 0))

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
