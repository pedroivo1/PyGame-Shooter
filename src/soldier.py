import pygame
import inspect
import os
from pathlib import Path

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, image_folder):
        super().__init__()

        self.live = True
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.y_velocity = 0
        self.gravity = 0.75

        self.runing_left = False
        self.runing_right = False
        self.jumped = False
        self.in_air = False

        self.animation_changed = False
        self.animation_time = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.animation_index = 0
        self.animation_action = "idle"
        self.animation_dict = {}
        self.animation_import(scale, image_folder)

        self.img = self.animation_dict[self.animation_action][self.animation_index]
        self.rect = self.img.get_rect()
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


    def move(self, dt):
        dx = 0
        dy = 0

        if self.runing_left:
            dx = -self.speed * dt
            self.flip = True
            self.direction = -1
        elif self.runing_right:
            dx = +self.speed * dt
            self.flip = False
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
                if self.runing_left or self.runing_right:
                    self.action_update('run')
                else:
                    self.action_update('idle')
            self.in_air = False


        self.rect.x += dx
        self.rect.y += dy


    def animation_update(self):
        self.img = self.animation_dict[self.animation_action][self.animation_index]
        if pygame.time.get_ticks()-self.animation_time > self.animation_cooldown:
            self.animation_time = pygame.time.get_ticks()
            self.animation_index = (self.animation_index+1) % len(self.animation_dict[self.animation_action])


    def action_update(self, new_action):
            self.animation_action = new_action
            self.animation_index = 0
            self.animation_time = pygame.time.get_ticks()


    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)



class Player(Soldier):
    def __init__(self, x, y, scale, speed):
        super().__init__(x, y, scale, speed, "img/player")



class Enemy(Soldier):
    def __init__(self, x, y, scale, speed):
        super().__init__(x, y, scale, speed, "img/enemy")
