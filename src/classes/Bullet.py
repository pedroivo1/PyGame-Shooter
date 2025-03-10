import pygame
from ..settings import screen

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, image: pygame.Surface, screen_settings: screen.ScreenSettings) -> None:
        super().__init__()

        self.screen_settings = screen_settings

        self.x_velocity = 0.8
        self.direction = direction

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, dt: int) -> None:
        if self.rect.right < 0 or self.rect.left > self.screen_settings.width:
            self.kill()
        self.rect.x += self.x_velocity * self.direction * dt
