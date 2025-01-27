import pygame
import inspect
from pathlib import Path

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.speed = 10

        caller_file = Path(inspect.stack()[1].filename).resolve()
        caller_dir = caller_file.parent.parent
        self.image = pygame.image.load(caller_dir / 'img/icons/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction


    def update(self):
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
        self.rect.x += self.speed * self.direction
