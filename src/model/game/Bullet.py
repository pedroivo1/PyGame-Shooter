import pygame
from src.model.settings import game_settings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, image: pygame.Surface, confg: game_settings.Settings) -> None:
        super().__init__()
        
        self.confg = confg

        self.x_velocity = 10

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction


    def update(self) -> None:
        if self.rect.right < 0 or self.rect.left > self.confg.screen.width:
            self.kill()
        self.rect.x += self.x_velocity * self.direction
