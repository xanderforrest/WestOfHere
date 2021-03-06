from pygame.constants import QUIT, K_ESCAPE

from utilities.consts import *


def file_loader(screen, filename="?"):
    title = FONT.render("Enter world name: ", True, (0, 0, 0))
    filename_input = TextInput(32, 64, filename)
    filename_input.active = True
    while True:
        screen.fill((0, 255, 255))
        screen.blit(CRATE_BORDER, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return None
                filename_input.update(event)
                if event.key == pygame.K_RETURN:
                    return filename_input.text
            elif event.type == QUIT:
                return None
        screen.blit(title, (32, 16))
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

    def refresh(self):
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


class Interacter(pygame.sprite.Sprite):
    def __init__(self, size, position, on_interact=None, name="default"):
        super(Interacter, self).__init__()
        self.rect = pygame.Rect(position, size)
        self._on_interact = on_interact
        self.name = name

    def on_interact(self):
        if self._on_interact:
            self._on_interact(self.name)


class TickBox(pygame.sprite.Sprite):
    def __init__(self, position, on_interact=None, name="TickBox"):
        super(TickBox, self).__init__()
        self.ticked = False
        self.name = name
        self.surf = UNTICKED_BOX
        self.rect = self.surf.get_rect(
            topleft=position
        )
        self._on_interact = on_interact

    def on_click(self):
        if self.ticked:
            self.ticked = False
            self.surf = UNTICKED_BOX
        else:
            self.ticked = True
            self.surf = TICKED_BOX

        if self._on_interact:
            self._on_interact()
