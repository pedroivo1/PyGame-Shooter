import pygame
from ..settings import screen

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, animation: list[pygame.Surface], screen_settings: screen.ScreenSettings) -> None:
        super().__init__()

        self.screen_settings = screen_settings

        self.animation = animation
        self.frame_index = 0
        self.image = animation[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_check = pygame.time.get_ticks()
        self.explosion_time = 150

    def update(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_check >= self.screen_settings.animation_cooldown:
            self.last_check = pygame.time.get_ticks()
            self.frame_index += 1
            try:
                self.image = self.animation[self.frame_index]
            except IndexError:
                self.kill()
