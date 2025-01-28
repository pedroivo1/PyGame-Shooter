import pygame
from src.model.settings import game_settings

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, image: pygame.Surface, confg: game_settings.Settings) -> None:
        super().__init__()

        self.confg = confg
        
        self.x_velocity = 9
        self.y_velocity = -9

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction


    def update(self) -> None:
        dx = 0
        dy = 0

        dx += self.x_velocity * self.direction
        if self.rect.left + dx < 0:
            self.direction *= -1
            self.x_velocity *= 0.5
            dx = 0 - self.rect.left
        if self.rect.right + dx > self.confg.screen.width:
            self.direction *= -1
            self.x_velocity *= 0.5
            dx = self.confg.screen.width - self.rect.right
        self.rect.x += dx

        self.y_velocity += self.confg.physic.gravity
        dy = self.y_velocity
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.y_velocity = -self.y_velocity * 0.3
            self.x_velocity = self.x_velocity * 0.5
        self.rect.y += dy
