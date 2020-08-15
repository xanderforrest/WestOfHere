import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
)
from utilities.consts import *
from user_config import *
import math
from utilities.animation import Animation
from utilities.soundsystem import SoundSystem
import time
import random
from utilities.base_entities import Entity, Human
stero = SoundSystem()


class Target(Entity):
    def __init__(self, location):
        super(Target, self).__init__()
        self.name = "target"
        self.class_ref = Target

        self.surf = TILE_BARREL.convert()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=location
        )
        self.hit_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "richochet.wav"))

    def on_hit(self):
        stero.play_sound(self.hit_sound)
        self.kill()


class Bullet(Entity):
    def __init__(self, start_pos, end_pos, owner_id=None):
        super(Bullet, self).__init__()
        self.name = "bullet"
        self.class_ref = Bullet

        self.owner = owner_id
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

        dif_x = int(self.current_point[0] - self.last_point[0])
        for x in range(1, abs(dif_x)):
            y_add = x * self.gradient

            test_coords = (self.last_point[0] + x, self.last_point[1] + y_add)
            self.rect.center = test_coords
            for e in GS.entities:
                if self.rect.colliderect(e.rect):
                    if e.id != self.owner and e.id != self.id:
                        e.on_hit()
                        self.kill()
        self.rect.center = self.current_point

        collisions = GS.GameMap.get_collisions(self.rect, GS.Camera.offset)
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


class Tumbleweed(Human):
    def __init__(self, position=None, direction="left"):
        super(Tumbleweed, self).__init__()
        self.name = "tumbleweed"
        self.class_ref = Tumbleweed

        self.animation_count = 0
        self.roll_angle = 10
        self.current_angle = 0
        self.surf = TUMBLEWEED_IMG
        if position:
            self.rect = self.surf.get_rect(
                center=position
            )
        else:
            self.rect = self.surf.get_rect(
                center=(SCREEN_WIDTH, SCREEN_HEIGHT/2)
            )

        self.v = [0, 0]
        self.acceleration = 10
        self.gravity = 10
        self.max_v = [50, 200]
        self.direction = direction

    def update(self, GS, keys_pressed):
        if self.direction == "right":
            self.v[0] += self.acceleration
        else:
            self.v[0] -= self.acceleration

        self.v[1] += self.gravity
        self.update_movement(GS)

        self.animation_count += 1
        if self.animation_count == 5:
            self.animation_count = 0
            self.update_animation()

        return GS

    def update_animation(self): # TODO add offset cam to tumbleweed and target
        new_image = pygame.transform.rotate(TUMBLEWEED_IMG, self.current_angle)
        self.surf = new_image

        self.current_angle += self.roll_angle
        if self.current_angle >= 360:
            self.current_angle = 0


class Player(Human):
    def __init__(self):
        super(Player, self).__init__()
        self.name = "player"
        self.class_ref = Player
        self.health = 100
        self.mount = None

        self.gun_draw = False

        self.gunshot_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "gunshot.wav"))
        self.Animation_GunDraw = Animation("gun_draw_spritesheet.png", [0, 6])
        self.Animation_Idle = Animation(CLINT_SPRITESHEET, [0, 4])
        self.Animation_Walk = Animation(CLINT_SPRITESHEET, [4, 10])

        self.surf = self.Animation_Idle.get_frame(position=0, direction=self.direction)
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, GS, keys_pressed):
        self.idle = True
        if not self.gun_draw:
            if keys_pressed[MOVE_LEFT]:
                self.v[0] -= self.acceleration
                self.update_direction("left")
                self.idle = False
            if keys_pressed[MOVE_RIGHT]:
                self.v[0] += self.acceleration
                self.update_direction("right")
                self.idle = False
            if keys_pressed[JUMP]:
                self.trigger_jump()
        if not keys_pressed[MOVE_RIGHT] and not keys_pressed[MOVE_LEFT]:
            self.v[0] = 0

        # update the gamestate with changes made
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
        spos = self.rect.center
        epos = pygame.mouse.get_pos()

        if epos[0] > spos[0]:
            self.update_direction("right")
        else:
            self.update_direction("left")

        stero.play_sound(self.gunshot_sound)

        bullet = Bullet(spos, epos, owner_id=self.id)
        self.spawned_entities.append(bullet)

    def trigger_gunfire(self):
        self.gun_draw = True

    def on_hit(self):
        self.health -= 5
        print(self.health)
        if self.health <= 0:
            self.kill()


class Bandit(Human):
    def __init__(self, start_pos=(0, 0), goal=None, hostile=True):
        super(Bandit, self).__init__()
        self.name = "bandit"
        self.class_ref = Bandit
        self.goal = goal
        self.hostile = hostile

        self.Animation_Idle = Animation("bandit-spritesheet.png", [0, 4])
        self.Animation_Walk = Animation("bandit-spritesheet.png", [4, 10])
        self.Animation_GunDraw = Animation("bandit_gun_draw.png", [0, 6])

        self.gun_draw = False
        self.gun_target = (0, 0)
        self.draw_speed = random.randint(0, 6)
        self.c_draw = 0

        self.gunshot_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "gunshot.wav"))

        self.last_shot = int(time.time())
        self.gun_cooldown = random.randint(0, 2)
        self.accuracy = random.randint(-20, 20)

        self.direction = "left"
        self.surf = self.Animation_Idle.get_frame(position=0, direction=self.direction)
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=start_pos
        )

    def update(self, GS, keys_pressed):
        self.idle = True
        # TODO insert movement logic

        if not self.gun_draw:
            if self.goal:  # will probably be updated to use a rect/target object
                if self.rect.center[0] > self.goal[0]:
                    self.v[0] -= self.acceleration
                    self.update_direction("left")
                    self.idle = False
                else:
                    self.v[0] += self.acceleration
                    self.update_direction("right")
                    self.idle = False

        if self.hostile:
            target = GS.player.rect.center
            if int(time.time())-self.last_shot >= 3:
                self.gun_target = target
                self.trigger_gunfire()
                self.last_shot = int(time.time())

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

    def update_animation(self):  # TODO swap frame increment and display so that the first frame is displayed
        if not self.gun_draw:
            if self.idle:
                self.Animation_Idle.increment_frame()
                self.surf = self.Animation_Idle.get_frame(direction=self.direction)
            else:
                self.Animation_Walk.increment_frame()
                self.surf = self.Animation_Walk.get_frame(direction=self.direction)
        else:
            if self.Animation_GunDraw.finished:
                self.c_draw += 1
                if self.c_draw <= self.draw_speed:
                    self.surf = self.Animation_GunDraw.get_frame(position=self.Animation_GunDraw.held_frame,
                                                                 direction=self.direction)
                else:
                    self.c_draw = 0
                    self.fire_gun()
                    self.gun_draw = False
                    self.Animation_GunDraw.increment_frame()
            else:
                self.Animation_GunDraw.increment_frame()
                self.surf = self.Animation_GunDraw.get_frame(direction=self.direction)
        self.surf.set_colorkey((255, 255, 255))

    def on_hit(self):
        self.kill()

    def trigger_gunfire(self):
        self.gun_draw = True
        self.v = [0, 0]

    def fire_gun(self):
        spos = self.rect.center
        epos = self.gun_target

        epos = (epos[0]+self.accuracy, epos[1]+self.accuracy)

        if epos[0] > spos[0]:
            self.update_direction("right")
        else:
            self.update_direction("left")

        stero.play_sound(self.gunshot_sound)

        bullet = Bullet(spos, epos, owner_id=self.id)
        self.spawned_entities.append(bullet)


class Horse(Entity):
    def __init__(self, spawn_point=(10, 10)):
        super(Horse, self).__init__()

        self.direction = "right"
        self.idle = True

        self.v = [0, 0]
        self.acceleration = 20
        self.gravity = 10
        self.max_v = [100, 200]

        self.jumping = False
        self.on_tile = False
        self.jump_velocity = [-42, 0]
        self.jump_start = None
        self.max_jump_height = 36

        self.animation_count = 0
        self.Animation_Run = Animation("horse-spritesheet.png", [0, 20], size=[48, 32])
        self.surf = self.Animation_Run.get_frame(position=0, direction=self.direction)

        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=spawn_point
        )

    def update(self, GS, keys_pressed):
        self.idle = True

        # consider gravity
        self.v[1] += self.gravity

        self.update_movement(GS)

        self.animation_count += 1
        if self.animation_count == 2:
            self.animation_count = 0
            self.update_animation()

        return GS

    def update_animation(self):  # TODO swap frame increment and display so that the first frame is displayed
        self.Animation_Run.increment_frame()
        self.surf = self.Animation_Run.get_frame(direction=self.direction)
        self.surf.set_colorkey((0, 0, 0))

    def update_movement(self, GS):
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


named_entities = {
    "bandit": Bandit,
    "player": Player,
    "tumbleweed": Tumbleweed,
    "bullet": Bullet,
    "target": Target,
    "horse": Horse
}
