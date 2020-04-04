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

        self.sprite_sheet = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "clint-spritesheet.png"))

        self.idle_imgs = []
        for i in range(0, 4):
            idle_image = pygame.Surface([16, 32]).convert()
            idle_image.blit(self.sprite_sheet, (0, 0), ((i*16), 0, 16, 32))
            self.idle_imgs.append(idle_image)

        self.running_imgs = []
        for i in range(4, 10):
            running_image = pygame.Surface([16, 32]).convert()
            running_image.blit(self.sprite_sheet, (0, 0), ((i*16), 0, 16, 32))
            self.running_imgs.append(running_image)
        self.rect = self.surf.get_rect()

        self.speed = 0.1
        self.jump = False

        self.standing = True
        self.on_object = False
        self.direction = "right"
        self.jump_count = 0

        self.idle_level = 0
        self.running_level = 0

    def update_animation(self):
        if self.standing:
            self.idle_level += 1
            if self.idle_level > 3:
                self.idle_level = 0

            if self.direction == "right":
                self.surf = self.idle_imgs[self.idle_level]
            else:
                self.surf = pygame.transform.flip(self.idle_imgs[self.idle_level], True, False)
        else:
            self.running_level += 1
            if self.running_level > 5:
                self.running_level = 0
            if self.direction == "right":
                self.surf = self.running_imgs[self.running_level]
            else:
                self.surf = pygame.transform.flip(self.running_imgs[self.running_level], True, False)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)




    def trigger_jump(self, tile_rects):
        print("Jump triggered")
        if self.on_object:
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
        self.on_object = False
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
                    self.rect.bottom = collide.top
                    self.on_object = True
                else: # hitting bottom of tile
                    self.rect.top = collide.bottom

    def update_direction(self, direction="right"):
        if self.direction != direction:
            self.direction = direction
            self.surf = pygame.transform.flip(self.surf, True, False)

    def update(self, dt, pressed_keys, tile_rects):
        #print(f"Pos X: {self.rect.left} \nPos Y {self.rect.top}")
        speed = self.speed * dt
        self.standing = True
        if pressed_keys[K_LEFT]:
            self.move([-speed, 0], tile_rects)
            self.update_direction("left")
            self.standing = False
        if pressed_keys[K_RIGHT]:
            self.standing = False
            self.update_direction("right")
            self.move([speed, 0], tile_rects)
        if not (pressed_keys[K_RIGHT] or pressed_keys[K_LEFT]):
            self.standing = True
            self.running_level = 0
        #if pressed_keys[K_DOWN]:
        #    self.move([0, speed], tile_rects)
        # print(f"Is the player standing? {self.standing}")
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
