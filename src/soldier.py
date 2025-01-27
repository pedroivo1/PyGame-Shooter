import pygame
import inspect
import os
from pathlib import Path
from src import Bullet

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, image_folder, ammo):
        super().__init__()

        self.speed = 0.3
        self.direction = 1
        self.y_velocity = 0
        self.gravity = 0.75
        self.ammo = ammo
        self.start_ammo = ammo
        self.health = 100
        self.start_health = self.health

        self.soldier_alive = True
        self.running_left = False
        self.running_right = False
        self.shooting = False
        self.shooting_cooldown = 250
        self.shooting_time = pygame.time.get_ticks()
        self.jumped = False
        self.in_air = False
        self.flip_image = False

        self.animation_cooldown = 100
        self.animation_time = pygame.time.get_ticks()
        self.animation_index = 0
        self.animation_action = "idle"
        self.animation_dict = {}
        self.animation_import(scale, image_folder)

        self.image = self.animation_dict[self.animation_action][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def animation_import(self, scale, image_folder):
        caller_file = Path(inspect.stack()[1].filename).resolve()
        caller_dir = caller_file.parent
        for action in os.listdir(caller_dir.parent / image_folder):
            self.animation_dict[action] = []
            for frame in os.listdir(caller_dir.parent / image_folder / action):
                image_path = (caller_dir.parent / image_folder / action / frame).resolve()
                img = pygame.image.load(str(image_path)).convert_alpha()
                self.animation_dict[action].append(pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale)))


    def action_update(self, new_action):
        self.animation_action = new_action
        self.animation_index = 0
        self.animation_time = pygame.time.get_ticks()


    def animation_update(self):
        self.image = self.animation_dict[self.animation_action][self.animation_index]
        if pygame.time.get_ticks() - self.animation_time > self.animation_cooldown:
            self.animation_time = pygame.time.get_ticks()
            self.animation_index = (self.animation_index + 1) % len(self.animation_dict[self.animation_action])
            if self.animation_action == 'death':
                if self.animation_index == 7:
                    self.animation_index = 6


    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip_image, False), self.rect)


    def is_soldier_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            if self.soldier_alive:
                self.soldier_alive = False
                self.action_update('death')

    def move(self, dt):
        dx = 0
        dy = 0

        if self.running_left:
            dx = -self.speed * dt
            self.flip_image = True
            self.direction = -1
        elif self.running_right:
            dx = +self.speed * dt
            self.flip_image = False
            self.direction = 1

        self.y_velocity += self.gravity
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


    def shoot(self, bullets):
        if self.shooting and self.ammo:
            if pygame.time.get_ticks() - self.shooting_time > self.shooting_cooldown:
                self.shooting_time = pygame.time.get_ticks()
                bullet = Bullet.Bullet(
                    self.rect.centerx + self.rect.size[0] * 0.6 * self.direction,
                    self.rect.centery,
                    self.direction
                )
                bullets.add(bullet)
                self.ammo -= 1


    def update(self, dt, bullets):
        self.is_soldier_alive()
        if self.soldier_alive:
            self.shoot(bullets)
            self.move(dt)
        self.animation_update()



class Player(Soldier):
    def __init__(self, x, y, scale, ammo):
        super().__init__(x, y, scale, "img/player", ammo)



class Enemy(Soldier):
    def __init__(self, x, y, scale, ammo):
        super().__init__(x, y, scale, "img/enemy", ammo)
