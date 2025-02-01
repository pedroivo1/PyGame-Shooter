import pygame
from src.model.settings import game_settings
from src.model.game import Explosion

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, image: pygame.Surface, explosion_animation: list[pygame.Surface], explosion_group:pygame.sprite.Group, confg: game_settings.Settings) -> None:
        super().__init__()

        self.confg = confg

        self.x_velocity = 0.7
        self.y_velocity = -8
        self.direction = direction

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.explosion_group = explosion_group
        self.explosion_animation = explosion_animation
        self.creation_time = pygame.time.get_ticks()
        self.explosion_time = 3000


    def update(self, dt: int) -> None:
        dx = self.x_moviment(dt)
        self.rect.x += dx

        dy = self.y_moviment()
        self.rect.y += dy

        self.timer()


    def x_moviment(self, dt: int) -> int:
        dx = self.x_velocity * self.direction * dt
        if self.rect.left + dx < 0:
            self.direction *= -1
            self.x_velocity *= 0.5
            dx = 0 - self.rect.left
        if self.rect.right + dx > self.confg.screen.width:
            self.direction *= -1
            self.x_velocity *= 0.5
            dx = self.confg.screen.width - self.rect.right

        return dx


    def y_moviment(self) -> int:
        self.y_velocity += self.confg.physic.gravity
        dy = self.y_velocity
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.y_velocity = -self.y_velocity * 0.5
            self.x_velocity = self.x_velocity * 0.79

        return dy


    def timer(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time >= self.explosion_time:
            self.explode()


    def explode(self) -> None:
        self.kill()
        self.explosion_group.add(Explosion.Explosion(self.rect.x, self.rect.y, self.explosion_animation, self.confg))
