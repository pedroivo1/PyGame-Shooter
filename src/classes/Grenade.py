import pygame
from ..settings import Game_settings
from . import Explosion
from . import Soldier

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, image: pygame.Surface, explosion_animation: list[pygame.Surface], explosion_group: pygame.sprite.Group, config: Game_settings.Settings) -> None:
        super().__init__()

        self.config = config

        self.x_velocity = 0.7
        self.y_velocity = -8
        self.direction = direction

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.explosion_group = explosion_group
        self.explosion_animation = explosion_animation
        self.creation_time = pygame.time.get_ticks()
        self.explosion_time = 1000


    def update(self, dt: int, soldier_group: Soldier) -> None:
        dx = self.x_movement(dt)
        self.rect.x += dx

        dy = self.y_movement(dt)
        self.rect.y += dy

        self.timer(soldier_group)


    def x_movement(self, dt: int) -> int:
        dx = self.x_velocity * self.direction * dt
        if self.rect.left + dx < 0:
            self.direction *= -1
            self.x_velocity *= 0.5
            dx = 0 - self.rect.left
        if self.rect.right + dx > self.config.screen.width:
            self.direction *= -1
            self.x_velocity *= 0.5
            dx = self.config.screen.width - self.rect.right

        return dx


    def y_movement(self, dt: int) -> int:
        self.y_velocity += self.config.physics.gravity * dt
        dy = self.y_velocity * dt / self.config.physics.GC
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.y_velocity = -self.y_velocity * 0.5
            self.x_velocity = self.x_velocity * 0.79

        return dy


    def timer(self, soldier_group: Soldier) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time >= self.explosion_time:
            self.explode(soldier_group)


    def explode(self, soldier_group: Soldier) -> None:
        self.kill()
        self.explosion_group.add(Explosion.Explosion(self.rect.x, self.rect.y, self.explosion_animation, self.config))

        collided_soldiers = pygame.sprite.spritecollide(self, soldier_group, False)
        for soldier in collided_soldiers:
            soldier.soldier_settings.health.health -= 50
