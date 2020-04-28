import pygame
from utilities.consts import *


def file_loader(screen, filename="?"):
    filename_input = TextInput(0, 0, filename)
    filename_input.colour = (255, 0, 0)
    filename_input.active = True
    while True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                filename_input.update(event)
                if event.key == pygame.K_RETURN:
                    return filename_input.text

        screen.blit(filename_input.text_surface, filename_input.rect)
        pygame.display.flip()


class TextInput:
    def __init__(self, x, y, text="input here"):
        self.rect = pygame.Rect((x, y), FONT.size(text))
        self.colour = (255, 255, 255)
        self.text = text
        self.text_surface = FONT.render(self.text, True, self.colour)
        self.active = False

    def update(self, event):
        if self.active:
            if event.key == pygame.K_RETURN:
                print(self.text)
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.text_surface = FONT.render(self.text, True, self.colour)


class Button:
    def __init__(self, text, action=None):
        self.text = text
        self.mode = "off"
        self.action = action

        self.button_surface = self.draw_button()
        self.rect = self.button_surface.get_rect()

    def draw_button(self, text_colour=(255, 255, 255)):
        text_surf = FONT.render(self.text, 1, text_colour)
        size = FONT.size(self.text)

        self.border_size = 4
        border_offset = 4

        box_size = (size[0]+border_offset*2, size[1]+border_offset*2)
        self.button_surface = pygame.Surface(box_size, pygame.SRCALPHA)
        self.button_surface.blit(text_surf, (border_offset, border_offset))
        rect = pygame.Rect((0, 0), box_size)
        pygame.draw.rect(self.button_surface, (255, 255, 255), rect, self.border_size)

        return self.button_surface

    def update_highlight(self, mode):
        if self.mode != mode:
            if mode == "on":
                self.button_surface = self.draw_button((211, 211, 211))
                self.mode = "on"
            else:
                self.mode = "off"
                self.button_surface = self.draw_button()

    def on_hit(self):
        if self.action:
            self.action()


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, position, image, image_path=None, on_click=None):
        super(ImageButton, self).__init__()
        self.name = "ImageButton"

        self.surf = image
        self.rect = self.surf.get_rect(
            topleft=position
        )
        self.image_path = image_path
        self.on_click = on_click

    def on_click(self):
        if self.on_click:
            self.on_click()
