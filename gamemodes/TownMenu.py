import pygame
import pygame.gfxdraw
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from entities import Player, Tumbleweed
from utilities.utilities import GameState, Button
from utilities.tilemap_handler import TileMapHandler, Tile
from utilities.consts import *
import os


class TownMenu:  # TODO redo sound handling so sound settings can be changed
    def __init__(self, screen, global_config):
        self.screen = screen
        self.global_config = global_config
        self.GS = GameState()

        self.GS.player = Player()
        self.GS.entities.add(self.GS.player)

        self.GS.tile_map = TileMapHandler().load_map("menu_town.json")

        self.soundtrack = pygame.mixer.Sound(os.path.join(ASSETS_DIRECTORY, SOUNDS_DIRECTORY, "soundtrack.wav"))
        pygame.mixer.Channel(0).play(self.soundtrack, loops=-1)

        self.mainloop()

    def mainloop(self):
        while self.GS.running:
            # update game clock
            self.GS.dt = self.GS.clock.tick(60) / 1000

            for x in range(0, len(self.GS.tile_map)):  # loads map
                for y in range(0, len(self.GS.tile_map[x])):
                    tile = self.GS.tile_map[x][y]
                    if tile.image:
                        self.screen.blit(tile.image, (x * 16, y * 16))
                        if tile.interactable:  # TODO move this into the tile class
                            tile.rect = pygame.Rect(x * 16, y * 16, 16, 16)

            if self.GS.debug:
                # render blocks
                for y in range(18):
                    for x in range(50):
                        rect = pygame.Rect(x * 16, y * 16, 16, 16)
                        pygame.draw.rect(self.screen, (0, 0, 255), rect, 1)

                # render fps
                fps = str(int(self.GS.clock.get_fps()))
                self.screen.blit(FONT.render(fps, 1, (255, 255, 255)), (0, 0))

            self.screen.blit(FONT_TITLE.render("West of Here", 1, (255, 255, 255)), (46, 60))

            # render a cursor
            pygame.mouse.set_visible(False)
            curs_pos = pygame.mouse.get_pos()
            self.screen.blit(CURSOR_IMG,
                             (curs_pos[0] - 3,
                              curs_pos[1] - 3))  # offset to make mouse pointer line up with cursor centre

            # EVENT HANDLING
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mixer.pause()
                        self.GS.running = False
                    if event.key == K_UP:
                        self.GS.debug = False if self.GS.debug else True
                        # this will become "interact" key for entering doors
                elif event.type == QUIT:
                    self.global_config.game_running = False
                    self.GS.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.GS.player.trigger_gunfire()
                    else:
                        target = Tumbleweed(pygame.mouse.get_pos())
                        # GS.destroyables.add(target)
                        # GS.animated.add(target)
                        self.GS.entities.add(target)

            # ENTITY UPDATES
            for entity in self.GS.entities:
                self.GS = entity.update(self.GS, pygame.key.get_pressed())

            for entity in self.GS.entities:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()