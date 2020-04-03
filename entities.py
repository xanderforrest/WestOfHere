import pygame
import os
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from consts import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "clint.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # self.idle_imgs = []
        # for i in range(0, 40):
        #   print(i)
        #    self.idle_imgs.append(pygame.image.load(os.path.join("idle", f"clint{i}.png")).convert())
        self.rect = self.surf.get_rect()
        self.speed = 0.1
        self.jump = True
        self.standing = False
        self.jump_count = 0
        self.idle_level = 0

    def update_animation(self):
        self.idle_level += 1
        if self.idle_level > 39:
            self.idle_level = 0

        # self.surf = self.idle_imgs[self.idle_level]
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)


    def trigger_jump(self, tile_rects):
        print("Jump triggered")
        if self.standing:
            self.jump = True
            self.jump_count = 0
        # self.move([0, -0.8], tile_rects)

    def get_collisions(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def move(self, xy, tile_rects):
        x, y = xy
        self.standing = False
        if x != 0:
            self.rect.move_ip(x, 0)
            collisions = self.get_collisions(tile_rects)
            if not collisions:
                return
            for collide in collisions:
                if x < 0: # colliding with the right of a tile
                    self.rect.left = collide.right
                else: # colliding with the left of a tile
                    self.rect.right = collide.left
        if y != 0 and y <= 14:
            self.rect.move_ip(0, y)
            collisions = self.get_collisions(tile_rects)
            if not collisions:
                return
            for collide in collisions:
                if y > 0: # standing on top of a tile
                    self.standing = True
                    self.rect.bottom = collide.top
                else: # hitting bottom of tile
                    self.rect.top = collide.bottom

    def update(self, dt, pressed_keys, tile_rects):
        #print(f"Pos X: {self.rect.left} \nPos Y {self.rect.top}")
        speed = self.speed * dt

        if pressed_keys[K_LEFT]:
            self.move([-speed, 0], tile_rects)
        if pressed_keys[K_RIGHT]:
            self.move([speed, 0], tile_rects)
        #if pressed_keys[K_DOWN]:
        #    self.move([0, speed], tile_rects)

        # gravity
        if not self.jump:
            self.move([0, 0.2*dt], tile_rects)
        else:
            self.jump_count += 1
            self.move([0, -0.25*dt], tile_rects)
            if self.jump_count == 5:
                self.jump = False
                self.jump_count = 0

        # screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
