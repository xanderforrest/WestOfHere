import pygame
import os
from utilities.consts import *


class Animation:
    def __init__(self, sprite_sheet, positions, size=[16, 32]):
        self.sprite_sheet = pygame.image.load(os.path.join(ASSETS_DIRECTORY, SPRITESHEET_DIRECTORY, sprite_sheet))
        self.size = size
        self.frames = []
        self.frame_count = 0
        self.current_frame = 0
        self.held_frame = positions[1]-1
        self.finished = False

        self.load_frames(positions)

    def load_frames(self, positions):
        for i in range(positions[0], positions[1]):
            sprite_crop = pygame.Surface(self.size).convert()
            sprite_crop.blit(self.sprite_sheet, (0, 0), ((i*self.size[0]), 0, self.size[0], self.size[1]))

            self.frames.append([sprite_crop, pygame.transform.flip(sprite_crop, True, False)])
        self.frame_count = len(self.frames)-1

    def get_frame(self, position=None, direction="right"):
        if not position:
            position = self.current_frame

        if direction == "right":
            return self.frames[position][0]
        else:
            return self.frames[position][1]

    def increment_frame(self):
        self.current_frame += 1
        if self.current_frame > self.frame_count:
            self.finished = True
            self.current_frame = 0
        else:
            self.finished = False
