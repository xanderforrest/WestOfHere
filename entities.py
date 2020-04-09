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
from utilities import get_collisions
import math
from animation import Animation


class Target(pygame.sprite.Sprite):
    def __init__(self, location):
        super(Target, self).__init__()
        self.name = "target"
        self.surf = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "barrel.png")).convert()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=location
        )
        self.hit_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "richochet.wav"))

    def update(self, GS, keys_pressed):
        return GS

    def on_hit(self):
        pygame.mixer.Channel(0).play(self.hit_sound)
        self.kill()
    # TODO spin animation


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos):
        super(Bullet, self).__init__()
        self.name = "bullet"
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.surf = pygame.Surface((5, 5))
        self.v = self.calc_initial_velocity()
        self.speed = 30
        self.v = [self.v[0] * self.speed, self.v[1] * self.speed]
        self.rect = self.surf.get_rect(
            center=start_pos
        )
        try:
            self.gradient = (end_pos[1] - start_pos[1]) // (end_pos[0] - start_pos[0])
        except ZeroDivisionError:
            self.gradient = 0
        self.last_point = self.rect.center
        self.current_point = self.rect.center

    def update(self, GS, keys_pressed):
        self.rect.move_ip(self.v[0], self.v[1])
        self.current_point = self.rect.center

        if self.rect.left < 0:  # LEFT BORDER
            self.kill()
        if self.rect.right > SCREEN_WIDTH:  # RIGHT BORDER
            self.kill()
        if self.rect.top <= 0:  # TOP BORDER
            self.kill()
        if self.rect.bottom >= SCREEN_HEIGHT:  # BOTTOM BORDER
            self.kill()

        # this block of code checks the gap left by each frame for possible collisions
        # TODO fix this not working with collisions to the left of you, probably involving checking which point
        # has a larger x value so that the subtraction doesn't mess up
        dif_x = int(self.current_point[0] - self.last_point[0])
        for x in range(1, dif_x):
            y_add = x * self.gradient

            test_coords = (self.last_point[0] + x, self.last_point[1] + y_add)
            self.rect.center = test_coords
            for e in GS.destroyables:
                if self.rect.colliderect(e.rect):
                    self.kill()
                    e.on_hit()
        self.rect.center = self.current_point

        collisions = get_collisions(self.rect, GS.tile_map)
        if collisions:  # for now we're only concerned if the bullet hits the floor
            self.kill()

        self.last_point = self.current_point
        return GS

    def calc_initial_velocity(self):
        sp = self.start_pos
        ep = self.end_pos
        # these variables need a short name so these lines aren't massive
        # minimising dependencies by not using numpy vector operations here

        nv = [ep[0] - sp[0], ep[1] - sp[1]]
        magnitude = math.sqrt(abs(nv[0] ** 2 + nv[1] ** 2))
        direction_vector = [nv[0] / magnitude, nv[1] / magnitude]

        return direction_vector


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.name = "player"

        self.idle = True
        self.gun_draw = False

        self.gunshot_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "gunshot.wav"))
        self.Animation_GunDraw = Animation("gun_draw_spritesheet.png", [0, 6])
        self.Animation_Idle = Animation(CLINT_SPRITESHEET, [0, 4])
        self.Animation_Walk = Animation(CLINT_SPRITESHEET, [4, 10])

        self.direction = "right"

        self.surf = self.Animation_Idle.get_frame(position=0, direction=self.direction)
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.v = [0, 0]
        self.acceleration = 10
        self.gravity = 10
        self.max_v = [50, 200]

        self.spawned_entities = []

    def update(self, GS, keys_pressed):
        self.idle = True
        if keys_pressed[K_LEFT]:
            self.v[0] -= self.acceleration
            self.update_direction("left")
            self.idle = False
        if keys_pressed[K_RIGHT]:
            self.v[0] += self.acceleration
            self.update_direction("right")
            self.idle = False
        if not keys_pressed[K_RIGHT] and not keys_pressed[K_LEFT]:
            self.v[0] = 0

        # update the gamestate with changes made
        for entity in self.spawned_entities:
            GS.entities.add(entity)
        self.spawned_entities = []

        # consider gravity
        self.v[1] += self.gravity

        self.update_movement(GS.dt, GS.tile_map)
        return GS

    def update_movement(self, dt, tile_map):

        if self.v[0] > self.max_v[0]:
            self.v[0] = self.max_v[0]
        elif self.v[0] < -self.max_v[0]:
            self.v[0] = -self.max_v[0]
        if self.v[1] > self.max_v[1]:
            self.v[1] = self.max_v[1]
        elif self.v[1] < -self.max_v[1]:
            self.v[1] = -self.max_v[1]

        if self.v[0] < 0:
            x = -math.ceil((self.v[0] * -1) * dt)
        else:
            x = math.ceil(self.v[0] * dt)
        y = math.ceil(self.v[1] * dt)

        # cx, cy = [self.rect.center[0] // 16, self.rect.center[1] // 16]  # get the tile the rect is currently in
        # print(f"The player is currently in block ({cx}, {cy})")
        # print(f"The x velocity is {self.v[0]}\nThe applied x velocity is {x}")

        if x != 0:
            self.rect.move_ip(x, 0)
            collisions = get_collisions(self.rect, tile_map)
            for collide in collisions:
                if x < 0:  # colliding with the right of a tile
                    self.rect.left = collide.rect.right
                else:  # colliding with the left of a tile
                    self.rect.right = collide.rect.left
        if y != 0:
            self.rect.move_ip(0, y)
            collisions = get_collisions(self.rect, tile_map)
            for collide in collisions:
                if y > 0:  # standing on top of a tile
                    self.v[1] = 0
                    self.rect.bottom = collide.rect.top
                else:  # hitting bottom of tile
                    self.rect.top = collide.rect.bottom

    def update_direction(self, direction="right"):
        if self.direction != direction:
            self.direction = direction
            self.surf = pygame.transform.flip(self.surf, True, False)  # horizontal flip: true, vertical: false

    def update_animation(self):  # TODO swap frame increment and display so that the first frame is displayed
        if not self.gun_draw:
            if self.idle:
                self.Animation_Idle.increment_frame()
                self.surf = self.Animation_Idle.get_frame(direction=self.direction)
            else:
                self.Animation_Walk.increment_frame()
                self.surf = self.Animation_Walk.get_frame(direction=self.direction)
        else:
            self.Animation_GunDraw.increment_frame()
            if self.Animation_GunDraw.finished:
                self.fire_gun()
                self.gun_draw = False
            self.surf = self.Animation_GunDraw.get_frame(direction=self.direction)
        self.surf.set_colorkey((255, 255, 255))

    def fire_gun(self):
        # TODO start gun draw animation
        pygame.mixer.Channel(1).play(self.gunshot_sound)

        spos = self.rect.center
        epos = pygame.mouse.get_pos()

        bullet = Bullet(spos, epos)
        self.spawned_entities.append(bullet)

    def trigger_gunfire(self):
        self.gun_draw = True


class Bandit(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super(Bandit, self).__init__()
        self.name = "bandit"

        self.sprite_sheet = pygame.image.load(os.path.join(ASSETS_DIRECTORY, "bandit-spritesheet.png"))
        self.idle_images = []
        self.idle_level = 0
        self.running_images = []
        self.running_level = 0
        self.idle = True

        self.gunshot_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "gunshot.wav"))

        for i in range(0, 10):
            sprite_crop = pygame.Surface([16, 32]).convert()
            sprite_crop.blit(self.sprite_sheet, (0, 0), ((i * 16), 0, 16, 32))

            if i < 4:
                if i == 0:
                    self.surf = sprite_crop
                    self.surf.set_colorkey((255, 255, 255))
                self.idle_images.append([sprite_crop, pygame.transform.flip(sprite_crop, True, False)])
            else:
                self.running_images.append([sprite_crop, pygame.transform.flip(sprite_crop, True, False)])

        self.direction = "left"
        self.rect = self.surf.get_rect(
            center=start_pos
        )
        self.v = [0, 0]
        self.acceleration = 10
        self.gravity = 10
        self.max_v = [50, 200]

    def update(self, GS, keys_pressed):
        self.idle = True
        # TODO insert movement logic

        # consider gravity
        self.v[1] += self.gravity

        self.update_movement(GS.dt, GS.tile_map)
        return GS

    def update_movement(self, dt, tile_map):
        if self.v[0] > self.max_v[0]:
            self.v[0] = self.max_v[0]
        elif self.v[0] < -self.max_v[0]:
            self.v[0] = -self.max_v[0]
        if self.v[1] > self.max_v[1]:
            self.v[1] = self.max_v[1]
        elif self.v[1] < -self.max_v[1]:
            self.v[1] = -self.max_v[1]

        if self.v[0] < 0:
            x = -math.ceil((self.v[0] * -1) * dt)
        else:
            x = math.ceil(self.v[0] * dt)
        y = math.ceil(self.v[1] * dt)

        # cx, cy = [self.rect.center[0] // 16, self.rect.center[1] // 16]  # get the tile the rect is currently in
        # print(f"The player is currently in block ({cx}, {cy})")
        # print(f"The x velocity is {self.v[0]}\nThe applied x velocity is {x}")

        if x != 0:
            self.rect.move_ip(x, 0)
            collisions = get_collisions(self.rect, tile_map)
            for collide in collisions:
                if x < 0:  # colliding with the right of a tile
                    self.rect.left = collide.rect.right
                else:  # colliding with the left of a tile
                    self.rect.right = collide.rect.left
        if y != 0:
            self.rect.move_ip(0, y)
            collisions = get_collisions(self.rect, tile_map)
            for collide in collisions:
                if y > 0:  # standing on top of a tile
                    self.v[1] = 0
                    self.rect.bottom = collide.rect.top
                else:  # hitting bottom of tile
                    self.rect.top = collide.rect.bottom

    def update_animation(self):
        if self.idle:
            self.idle_level += 1
            self.idle_level = 0 if self.idle_level > 3 else self.idle_level

            if self.direction == "right":
                self.surf = self.idle_images[self.idle_level][0]
            else:
                self.surf = self.idle_images[self.idle_level][1]
        else:
            self.running_level += 1
            self.running_level = 0 if self.running_level > 5 else self.running_level

            if self.direction == "right":
                self.surf = self.running_images[self.running_level][0]
            else:
                self.surf = self.running_images[self.running_level][1]
        self.surf.set_colorkey((255, 255, 255))

    def on_hit(self):
        self.kill()
