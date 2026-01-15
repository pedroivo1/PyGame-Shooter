#!/usr/bin/env python3
# Author: https://github.com/pedroivo1

import pygame
from ..settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tile_type):
        super().__init__()
        self.image = game.assets['tiles'][tile_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class ExitTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tile_type):
        super().__init__()
        self.image = game.assets['tiles'][tile_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
