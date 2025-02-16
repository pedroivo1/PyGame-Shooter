import pygame
from abc import ABC, abstractmethod
from . import Bullet
from . import Grenade
from . import HealthBar
from ..settings import Game_settings
from ..settings import Soldier_settings
from .. import default_imports

class Soldier(pygame.sprite.Sprite, ABC):
    def __init__(self, x: int, y: int, config: Game_settings.Settings, assets: dict, color: str) -> None:
        super().__init__()

        self.config = config
        self.assets = assets
        self.soldier_settings = Soldier_settings.SoldierConfig(**(default_imports.soldier_settings))
        self.soldier_settings.animation.animations_map = self.assets['animations'][color]


        self.image = self.soldier_settings.animation.animations_map[self.soldier_settings.animation.animation_action][self.soldier_settings.animation.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.health_bar = HealthBar.HealthBar(self)


    def action_update(self, new_action: str) -> None:
        self.soldier_settings.animation.animation_action = new_action
        self.soldier_settings.animation.animation_index = 0
        self.soldier_settings.animation.animation_timer = pygame.time.get_ticks()


    def animation_update(self) -> None:
        self.image = self.soldier_settings.animation.animations_map[self.soldier_settings.animation.animation_action][self.soldier_settings.animation.animation_index]
        if self.animation_timer():
            self.soldier_settings.animation.animation_timer = pygame.time.get_ticks()
            self.soldier_settings.animation.animation_index = (self.soldier_settings.animation.animation_index + 1) % len(self.soldier_settings.animation.animations_map[self.soldier_settings.animation.animation_action])
            self.death_animation_control()


    def animation_timer(self) -> bool:
        return pygame.time.get_ticks() - self.soldier_settings.animation.animation_timer > self.config.screen.animation_cooldown


    def death_animation_control(self) -> None:
        if self.soldier_settings.animation.animation_action == 'death':
            if self.soldier_settings.animation.animation_index == 7:
                self.soldier_settings.animation.animation_index = 6


    def draw(self, screen: pygame.Surface) -> None:
        self.health_bar.draw(screen)
        screen.blit(pygame.transform.flip(self.image, self.soldier_settings.state.flip_image, False), self.rect)


    def is_soldier_alive(self) -> None:
        if self.soldier_settings.health.health <= 0:
            self.soldier_settings.health.health = 0
            self.soldier_settings.movement.x_velocity = 0
            if self.soldier_settings.state.soldier_alive:
                self.soldier_settings.state.soldier_alive = False
                self.action_update('death')


    def move(self, dt: int) -> None:
        dx = 0
        dy = 0

        if self.soldier_settings.state.running_left:
            dx = -self.soldier_settings.movement.x_velocity * dt
            self.soldier_settings.state.flip_image = True
            self.soldier_settings.movement.direction = -1
        elif self.soldier_settings.state.running_right:
            dx = +self.soldier_settings.movement.x_velocity * dt
            self.soldier_settings.state.flip_image = False
            self.soldier_settings.movement.direction = 1

        self.soldier_settings.movement.y_velocity = self.soldier_settings.movement.y_velocity + self.config.physics.gravity*dt
        if self.soldier_settings.state.jumped:
            self.soldier_settings.movement.y_velocity -= 11
            self.soldier_settings.state.jumped = False
            self.soldier_settings.state.in_air = True


        dy += self.soldier_settings.movement.y_velocity * dt / self.config.physics.GC

        if self.rect.bottom + dy > 300:
            self.soldier_settings.movement.y_velocity = 0
            dy = 300 - self.rect.bottom
            if self.soldier_settings.state.in_air:
                if self.soldier_settings.state.running_left or self.soldier_settings.state.running_right:
                    self.action_update('run')
                else:
                    self.action_update('idle')
            self.soldier_settings.state.in_air = False

        self.rect.x += dx
        self.rect.y += dy


    def apply_gravity(self, dt: int) -> None:
        self.soldier_settings.movement.y_velocity += self.config.physic.gravity
        if self.rect.bottom + self.soldier_settings.movement.y_velocity > 300:
            self.soldier_settings.movement.y_velocity = 0
            self.rect.bottom = 300
            if self.soldier_settings.state.in_air:
                if self.soldier_settings.state.running_left or self.soldier_settings.state.running_right:
                    self.action_update('run')
                else:
                    self.action_update('idle')
            self.soldier_settings.state.in_air = False


    def jump(self) -> None:
        if not self.soldier_settings.state.in_air:
            self.soldier_settings.movement.y_velocity = -11
            self.soldier_settings.state.in_air = True


    def shoot(self, bullets: pygame.sprite.Group) -> None:
        if self.soldier_settings.ammo.shot and self.soldier_settings.ammo.ammo and pygame.time.get_ticks() - self.soldier_settings.ammo.shot_time > self.soldier_settings.ammo.shot_cooldown:
            self.soldier_settings.ammo.shot_time = pygame.time.get_ticks()
            bullet = Bullet.Bullet(
                self.rect.centerx + self.rect.size[0] * 0.7 * self.soldier_settings.movement.direction,
                self.rect.centery,
                self.soldier_settings.movement.direction,
                self.assets['images']['bullet'],
                self.config
            )
            bullets.add(bullet)
            self.soldier_settings.ammo.ammo -= 1

    @abstractmethod
    def update(self, dt: int, bullets: pygame.sprite.Group, grenades: pygame.sprite.Group) -> None:
        self.is_soldier_alive()
        self.health_bar.update(self)
        if self.soldier_settings.state.soldier_alive:
            self.shoot(bullets)
            self.move(dt)

        self.animation_update()



class Player(Soldier):
    def __init__(self, x: int, y: int, config: Game_settings.Settings, assets: dict, color: str) -> None:
        super().__init__(x, y, config, assets, color)
        self.grenade_config = Soldier_settings.GrenadeConfig(**(default_imports.grenade_config))


    def throw_grenade(self, grenades: pygame.sprite.Group, explosion_group: pygame.sprite.Group) -> None:
        if self.grenade_config.threw_grenade and self.grenade_config.number_of_grenades and pygame.time.get_ticks() - self.grenade_config.threw_grenade_time > self.grenade_config.threw_grenade_cooldown:
            self.grenade_config.threw_grenade_time = pygame.time.get_ticks()
            grenade = Grenade.Grenade(self.rect.centerx + (0.5 * self.rect.size[0] * self.soldier_settings.movement.direction), self.rect.top, self.soldier_settings.movement.direction, self.assets['images']['grenade'], self.assets['animations']['explosion'], explosion_group, self.config)
            grenades.add(grenade)
            self.grenade_config.number_of_grenades -= 1


    def update(self, dt: int, bullet_group: pygame.sprite.Group, grenade_group: pygame.sprite.Group, explosion_group:pygame.sprite.Group) -> None:
        super().update(dt, bullet_group, grenade_group)
        if self.soldier_settings.state.soldier_alive:
            self.throw_grenade(grenade_group, explosion_group)



class Enemy(Soldier):
    def __init__(self, x: int, y: int, config: Game_settings.Settings, assets: dict, color: str) -> None:
        super().__init__(x, y, config, assets, color)


    def update(self, dt: int, bullets: pygame.sprite.Group, grenades: pygame.sprite.Group) -> None:
        super().update(dt, bullets, grenades)
