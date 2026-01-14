import pygame
import random
from abc import ABC
from ..settings import *
from ..utils import AnimationManager


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, game, item_type, x, y, group):
        super().__init__(group)
        self.item_type = item_type
        self.image = game.assets[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.rect.height)

    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'health_box':
                player.health += 25
                if player.health > player.max_health:
                    player.health = 300
                
            elif self.item_type == 'ammo_box':
                player.ammo += 5
            elif self.item_type == 'grenade_box':
                player.grenade += 2
            self.kill()
