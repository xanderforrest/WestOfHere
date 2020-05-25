import pygame
import uuid
import math


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        self.id = "ENTITY" + str(uuid.uuid4())

    def serialise(self):
        pass

    def update(self, GS, keys_pressed):
        return GS

    def update_animation(self):
        pass

    def on_hit(self):
        pass


class Human(Entity):
    def __init__(self):
        super(Human, self).__init__()
        self.rect = None
        self.surf = None

        self.direction = "right"
        self.idle = True

        self.v = [0, 0]
        self.acceleration = 10
        self.gravity = 10
        self.max_v = [50, 200]

        self.jumping = False
        self.on_tile = False
        self.jump_velocity = [-30, 0]
        self.jump_start = None
        self.max_jump_height = 24

        self.animation_count = 0
        self.spawned_entities = []

    def update_movement(self, GS): # TODO update all of this to just use gamestate
        dt = GS.dt
        if self.jumping and (self.jump_start[1] - self.rect.center[1]) >= self.max_jump_height:
            self.jumping = False
            self.v[1] = 0

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

        self.on_tile = False
        if x != 0:
            self.rect.move_ip(x, 0)
            collisions = GS.GameMap.get_collisions(self.rect, GS.Camera.offset)
            for collide in collisions:
                if x < 0:  # colliding with the right of a tile
                    self.rect.left = collide.rect.right
                else:  # colliding with the left of a tile
                    self.rect.right = collide.rect.left
        if y != 0:
            self.rect.move_ip(0, y)
            collisions = GS.GameMap.get_collisions(self.rect, GS.Camera.offset)
            for collide in collisions:
                if y > 0:  # standing on top of a tile
                    self.v[1] = 0
                    self.rect.bottom = collide.rect.top
                    self.on_tile = True
                else:  # hitting bottom of tile
                    self.rect.top = collide.rect.bottom

    def update_direction(self, direction="right"):
        if self.direction != direction:
            self.direction = direction
            self.surf = pygame.transform.flip(self.surf, True, False)  # horizontal flip: true, vertical: false

    def trigger_jump(self):
        if self.on_tile:
            self.jumping = True
            self.v[1] = 0
            self.jump_start = self.rect.center
