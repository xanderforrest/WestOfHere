import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Tumbleweed, Bandit, Bullet
from utilities.utilities import GameState, Camera
from utilities.GameMap import GameMap
from utilities.consts import *
from utilities.GUI import file_loader
import os
import random
import time


class TypistPlayer(Player):
    def __init__(self, goal):
        super(TypistPlayer, self).__init__()
        self.goal = goal
        self.gunfire_target = None

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
            self.update_animation(GS)

        return GS

    def update_animation(self, GS):
        if not self.gun_draw:
            if self.idle:
                self.Animation_Idle.increment_frame()
                self.surf = self.Animation_Idle.get_frame(direction=self.direction)
            else:
                self.Animation_Walk.increment_frame()
                self.surf = self.Animation_Walk.get_frame(direction=self.direction)
        else:
            if GS.CurrentEnemy:
                percent_done = GS.CurrentEnemy.DuelText.percent_complete
                if int(self.Animation_GunDraw.current_frame/len(self.Animation_GunDraw.frames)*100) < percent_done:
                    if self.Animation_GunDraw.current_frame == len(self.Animation_GunDraw.frames)-1:
                        if percent_done == 100:
                            self.Animation_GunDraw.increment_frame()
                    else:
                        self.Animation_GunDraw.increment_frame()
            if self.Animation_GunDraw.finished:
                self.fire_gun()
                self.gun_draw = False
            self.surf = self.Animation_GunDraw.get_frame(direction=self.direction)
        self.surf.set_colorkey((255, 255, 255))

    def fire_gun(self):
        spos = self.rect.center
        epos = self.gunfire_target

        if epos[0] > spos[0]:
            self.update_direction("right")
        else:
            self.update_direction("left")

        pygame.mixer.Channel(1).play(self.gunshot_sound)

        bullet = Bullet(spos, epos, owner_id=self.id)
        self.spawned_entities.append(bullet)

    def trigger_gunfire(self, target):
        self.gunfire_target = target
        self.gun_draw = True


class TypistEnemy(Bandit):
    def __init__(self, pos):
        super(TypistEnemy, self).__init__(start_pos=pos)
        self.hostile = False
        self.DuelText = DuelText()
        self.dead = False

    def update(self, GS, keys_pressed):
        self.idle = True

        for entity in self.spawned_entities:
            GS.entities.add(entity)
        self.spawned_entities = []

        # consider gravity
        self.v[1] += self.gravity

        player_location = GS.player.rect.center
        if player_location[0] > self.rect.center[0]:
            self.update_direction("right")
        else:
            self.update_direction("left")
        self.update_movement(GS)

        self.animation_count += 1
        if self.animation_count == 5:
            self.animation_count = 0
            self.update_animation()

        return GS

    def on_hit(self):
        self.dead = True
        self.kill()


class DuelText:
    def __init__(self, pos=(20, 100), text=None):
        if text:
            self.text = text
        else:
            self.text = self.get_text()
        self.typed_text = ""
        self.completed = False

        self.start_time = None
        self.end_time = None
        self.wpm = 0
        self.percent_complete = 0

        self.STD_COLOUR = (255, 255, 255)
        self.ALT_COLOUR = (255, 0, 0)

        self.rect = pygame.Rect(pos, FONT.size(self.text))
        self.background_surf = FONT_SMALL.render(self.text, True, self.STD_COLOUR)
        self.surf = self.background_surf

    @staticmethod
    def get_text():
        with open(os.path.join(GAME_DATA_DIRECTORY, "typeduelclean.txt")) as f:
            return random.choice(f.read().splitlines())

    def get_wpm(self):
        dif = self.end_time - self.start_time
        wps = len(self.text.split()) / dif
        self.wpm = wps * 60

    def update(self, event):  # update on key press
        if self.typed_text == self.text:
            self.completed = True
            self.percent_complete = 100
            self.get_wpm()
            return

        if event.type == KEYDOWN:
            character = event.unicode
            if self.text[len(self.typed_text)] == character:
                if self.typed_text == "":
                    self.start_time = time.time()
                # the len should give the index of the next character
                # so we can check if the person has typed correctly
                self.typed_text += character

                if self.typed_text == self.text:
                    self.end_time = time.time()

        self.percent_complete = int(len(self.typed_text)/len(self.text) * 100)
        self.refresh()

    def refresh(self):
        top_surf = FONT_SMALL.render(self.typed_text.replace(" ", "-"), True, self.ALT_COLOUR)
        self.surf.blit(top_surf, (0, 0))


class TypeDuel:
    def __init__(self, screen, global_config, GS=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.global_config = global_config
        self.GS = GameState()

        self.GS.player = TypistPlayer((380, 0))
        self.GS.Camera = Camera(self.GS.player)
        self.GS.entities.add(self.GS.player)

        self.GS.CurrentEnemy = None
        self.SPAWN_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_ENEMY, 1500)

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
        if self.GS.CurrentEnemy:
            self.GS.CurrentEnemy.DuelText.update(event)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.global_config.next_game = "mainmenu"
                self.pause()
            if event.key == K_UP:
                self.GS.debug = False if self.GS.debug else True
        elif event.type == QUIT:
            self.global_config.game_running = False
            self.GS.running = False
        elif event.type == self.SPAWN_ENEMY:
            if not self.GS.CurrentEnemy:
                self.GS.CurrentEnemy = TypistEnemy((random.randint(300, 600), 192))
                self.GS.entities.add(self.GS.CurrentEnemy)

    def mainloop(self):
        wpms = []
        pygame.mixer.Channel(0).play(self.soundtrack, loops=-1)
        while self.GS.running:
            self.GS.dt = self.GS.clock.tick(60) / 1000

            self.GS.GameMap.render(self.screen, self.GS.Camera.offset, self.GS.debug)

            if wpms:
                avg = sum(wpms) // len(wpms)
                last = int(wpms[-1])
                display_text = f"Avg: {avg} | Last: {last}"
                self.screen.blit(FONT_SMALL.render(display_text, True, (255, 255, 255)), (0, 0))

            self.GS.curs_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                self.handle_event(event)

            for entity in self.GS.entities:
                self.GS = entity.update(self.GS, pygame.key.get_pressed())

            for entity in self.GS.entities:
                self.screen.blit(entity.surf, entity.rect)

            if self.GS.CurrentEnemy:
                percent = self.GS.CurrentEnemy.DuelText.percent_complete
                if percent > 0:
                    self.GS.player.trigger_gunfire(self.GS.CurrentEnemy.rect.center)
                if self.GS.CurrentEnemy.DuelText.completed:
                    wpms.append(self.GS.CurrentEnemy.DuelText.wpm)
                    self.GS.CurrentEnemy = None
                else:
                    self.screen.blit(self.GS.CurrentEnemy.DuelText.surf, self.GS.CurrentEnemy.DuelText.rect)

            self.GS = self.GS.Camera.update(self.GS)
            pygame.display.flip()
