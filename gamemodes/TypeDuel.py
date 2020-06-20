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
import random


class TypistPlayer(Player):
    def __init__(self, goal):
        super(TypistPlayer, self).__init__()
        self.goal = goal

    def update(self, GS, keys_pressed):
        self.idle = True
        if self.goal:  # will probably be updated to use a rect/target object
            if not (self.rect.center[0] > self.goal[0]):
                self.v[0] += self.acceleration
                self.update_direction("right")
                self.idle = False
            else:
                self.v[0] = 0

        for entity in self.spawned_entities:
            GS.entities.add(entity)
        self.spawned_entities = []

        # consider gravity
        self.v[1] += self.gravity
        # consider jumping
        if self.jumping:
            self.v[1] += self.jump_velocity[0]

        self.update_movement(GS)
        self.animation_count += 1
        if self.animation_count == 5:
            self.animation_count = 0
            self.update_animation()

        return GS


class DuelText:
    def __init__(self, pos, text=None):
        if text:
            self.text = text
        else:
            self.text = self.get_text()
        self.typed_text = ""
        self.completed = False

        self.STD_COLOUR = (255, 255, 255)
        self.ALT_COLOUR = (255, 0, 0)

        self.rect = pygame.Rect(pos, FONT.size(self.text))
        self.background_surf = FONT_SMALL.render(self.text, True, self.STD_COLOUR)
        self.surf = self.background_surf

    @staticmethod
    def get_text():
        with open(os.path.join(GAME_DATA_DIRECTORY, "typeduelclean.txt")) as f:
            return random.choice(f.read().splitlines())

    def update(self, event): # update on key press
        if self.typed_text == self.text:
            self.completed = True
            return

        if event.type == KEYDOWN:
            character = event.unicode
            if self.text[len(self.typed_text)] == character:
                # the len should give the index of the next character
                # so we can check if the person has typed correctly
                self.typed_text += character

        self.refresh()

    def refresh(self):
        top_surf = FONT_SMALL.render(self.typed_text, True, self.ALT_COLOUR)
        self.surf.blit(top_surf, (0, 0))


class TypeDuel:
    def __init__(self, screen, global_config, GS=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.global_config = global_config
        self.GS = GameState()

        self.GS.player = TypistPlayer((250, 0))
        self.GS.Camera = Camera(self.GS.player)
        self.GS.entities.add(self.GS.player)

        self.DuelText = DuelText((100, 100))

        self.GS.GameMap = None
        self.first_start = True

        self.soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))

    def resume(self, gamemap=None):
        if self.first_start and not gamemap:
            map_file = "menu_town.json"
            self.GS.GameMap = GameMap(map_file)
            self.first_start = False

        self.GS.player.rect.topleft = (250, 192)

        self.GS.running = True
        self.mainloop()
        return self.global_config

    def pause(self):
        pygame.mixer.pause()
        self.GS.running = False

    def handle_event(self, event):
        self.DuelText.update(event)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.global_config.next_game = "mainmenu"
                self.pause()
            if event.key == K_UP:
                self.GS.debug = False if self.GS.debug else True
        elif event.type == QUIT:
            self.global_config.game_running = False
            self.GS.running = False

    def mainloop(self):
        # pygame.mixer.Channel(0).play(self.soundtrack, loops=-1)
        while self.GS.running:
            self.GS.dt = self.GS.clock.tick(60) / 1000

            self.GS.GameMap.render(self.screen, self.GS.Camera.offset, self.GS.debug)

            self.GS.curs_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                self.handle_event(event)

            for entity in self.GS.entities:
                self.GS = entity.update(self.GS, pygame.key.get_pressed())

            for entity in self.GS.entities:
                self.screen.blit(entity.surf, entity.rect)

            self.screen.blit(self.DuelText.surf, self.DuelText.rect)

            self.GS = self.GS.Camera.update(self.GS)
            pygame.display.flip()
