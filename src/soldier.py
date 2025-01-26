import pygame
from pathlib import Path
import inspect

class Soldier:
    def __init__(self, x, y, scale):
        caller_file = Path(inspect.stack()[1].filename).resolve()
        caller_dir = caller_file.parent
        image_path = (caller_dir / "img/player/Idle/0.png").resolve()

        img = pygame.image.load(str(image_path))
        self.img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height()*scale))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.img, self.rect)
