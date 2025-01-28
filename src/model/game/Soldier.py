import pygame
from src.model.game import Bullet
from src.model.game import Grenade
from src.model.data import settings

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, ammo: int, config: settings.Settings, assets: dict, color: str):
        super().__init__()

        self.config = config
        self.assets = assets

        self.x_velocity = 0.3
        self.y_velocity = 0
        self.direction = 1
        self.ammo = ammo
        self.start_ammo = ammo
        self.health = 100
        self.start_health = self.health

        self.soldier_alive = True
        self.running_left = False
        self.running_right = False

        self.shot = False
        self.shot_cooldown = 250
        self.shot_time = pygame.time.get_ticks()
        self.threw_grenade = False
        self.threw_grenade_cooldown = 400
        self.threw_grenade_time = pygame.time.get_ticks()
        self.grenades_number = 5

        self.jumped = False
        self.in_air = False
        self.flip_image = False

        self.animation_cooldown = 100
        self.animation_time = pygame.time.get_ticks()
        self.animation_index = 0
        self.animation_action = "idle"
        self.animation_dict = self.assets['animations'][color]

        self.image = self.animation_dict[self.animation_action][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def action_update(self, new_action: str) -> None:
        self.animation_action = new_action
        self.animation_index = 0
        self.animation_time = pygame.time.get_ticks()


    def animation_update(self) -> None:
        self.image = self.animation_dict[self.animation_action][self.animation_index]
        if pygame.time.get_ticks() - self.animation_time > self.animation_cooldown:
            self.animation_time = pygame.time.get_ticks()
            self.animation_index = (self.animation_index + 1) % len(self.animation_dict[self.animation_action])
            if self.animation_action == 'death':
                if self.animation_index == 7:
                    self.animation_index = 6


    def draw(self, screen) -> None:
        screen.blit(pygame.transform.flip(self.image, self.flip_image, False), self.rect)


    def is_soldier_alive(self) -> None:
        if self.health <= 0:
            self.health = 0
            self.x_velocity = 0
            if self.soldier_alive:
                self.soldier_alive = False
                self.action_update('death')


    def move(self, dt: int) -> None:
        dx = 0
        dy = 0

        if self.running_left:
            dx = -self.x_velocity * dt
            self.flip_image = True
            self.direction = -1
        elif self.running_right:
            dx = +self.x_velocity * dt
            self.flip_image = False
            self.direction = 1

        self.y_velocity += self.config.physic.gravity
        if self.jumped:
            self.y_velocity -= 11
            self.jumped = False
            self.in_air = True

        dy += self.y_velocity

        if self.rect.bottom + dy > 300:
            self.y_velocity = 0
            dy = 300 - self.rect.bottom
            if self.in_air:
                if self.running_left or self.running_right:
                    self.action_update('run')
                else:
                    self.action_update('idle')
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy


    def apply_gravity(self, dt: int) -> None:
        self.y_velocity += self.config.physic.gravity * dt
        if self.rect.bottom + self.y_velocity > 300:
            self.y_velocity = 0
            self.rect.bottom = 300
            if self.in_air:
                if self.running_left or self.running_right:
                    self.action_update('run')
                else:
                    self.action_update('idle')
            self.in_air = False


    def jump(self) -> None:
        if not self.in_air:
            self.y_velocity = -11
            self.in_air = True


    def shoot(self, bullets) -> None:
        if self.shot and self.ammo and pygame.time.get_ticks() - self.shot_time > self.shot_cooldown:
            self.shot_time = pygame.time.get_ticks()
            bullet = Bullet.Bullet(
                self.rect.centerx + self.rect.size[0] * 0.7 * self.direction,
                self.rect.centery,
                self.direction,
                self.assets['images']['bullet'],
                self.config
            )
            bullets.add(bullet)
            self.ammo -= 1


    def throw_grenade(self, grenades: pygame.sprite.Group) -> None:
        if self.threw_grenade and self.grenades_number and pygame.time.get_ticks() - self.threw_grenade_time > self.threw_grenade_cooldown:
            self.threw_grenade_time = pygame.time.get_ticks()
            grenade = Grenade.Grenade(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction), self.rect.top, self.direction, self.assets['images']['grenade'], self.config)
            grenades.add(grenade)
            self.grenades_number -= 1


    def update(self, dt: int, bullets: pygame.sprite.Group, grenades: pygame.sprite.Group) -> None:
        self.is_soldier_alive()
        if self.soldier_alive:
            self.shoot(bullets)
            self.throw_grenade(grenades)
            self.move(dt)
        self.animation_update()



class Green_soldier(Soldier):
    def __init__(self, x: int, y: int, ammo: int, config: settings.Settings, assets: dict) -> None:
        super().__init__(x, y, ammo, config, assets, 'green')



class Red_soldier(Soldier):
    def __init__(self, x: int, y: int, ammo: int, config: settings.Settings, assets: dict) -> None:
        super().__init__(x, y, ammo, config, assets, 'red')
