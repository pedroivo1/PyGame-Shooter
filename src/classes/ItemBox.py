import pygame
from ..settings import Game_settings
from . import Soldier
from abc import ABC, abstractmethod


class ItemBox(pygame.sprite.Sprite, ABC):
    def __init__(self, x: int, y: int, image: pygame.Surface, config: Game_settings.Settings) -> None:
        super().__init__()

        self.config = config

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + self.config.screen.tile_size // 2, y + (self.config.screen.tile_size - self.image.get_height()))


    def update(self, player: Soldier.Player):
        if pygame.sprite.collide_rect(self, player):
            self.kill()
            self.action(player)


    @abstractmethod
    def action(self):
        pass



class HealthBox(ItemBox):
    def __init__(self, x: int, y: int, image: pygame.Surface, config: Game_settings.Settings) -> None:
        super().__init__(x, y, image, config)


    def action(self, player: Soldier.Player):
        super().action()
        if player.soldier_settings.health.health < 75:
            player.soldier_settings.health.health += 25
        else:
            player.soldier_settings.health.health = 100




class GrenadeBox(ItemBox):
    def __init__(self, x: int, y: int, image: pygame.Surface, config: Game_settings.Settings) -> None:
        super().__init__(x, y, image, config)


    def action(self, player: Soldier.Player):
        super().action()
        player.grenade_config.number_of_grenades += 2



class BulletBox(ItemBox):
    def __init__(self, x: int, y: int, image: pygame.Surface, config: Game_settings.Settings) -> None:
        super().__init__(x, y, image, config)


    def action(self, player: Soldier.Player):
        super().action()
        player.soldier_settings.ammo.ammo += 10
