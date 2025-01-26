import pygame
from pathlib import Path
import inspect

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, image_folder):
        pygame.sprite.Sprite.__init__(self)

        self.speed = speed
        self.direction = 1
        self.flip = False

        # Get the path to the caller directory
        caller_file = Path(inspect.stack()[1].filename).resolve()
        caller_dir = caller_file.parent

        # Fix image path by navigating to the correct folder
        image_path = (caller_dir.parent / image_folder / "Idle/0.png").resolve()

        img = pygame.image.load(str(image_path))
        self.img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

        self.moving_left = False
        self.moving_right = False
        self.jump = False


    def move(self, dt):
        dx = 0
        dy = 0

        if self.moving_left:
            dx = -self.speed * dt
            self.flip = True
            self.direction = -1
        elif self.moving_right:
            dx = +self.speed * dt
            self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)


class Player(Soldier):
    def __init__(self, x, y, scale, speed):
        super().__init__(x, y, scale, speed, "img/player")


class Enemy(Soldier):
    def __init__(self, x, y, scale, speed):
        super().__init__(x, y, scale, speed, "img/enemy")
