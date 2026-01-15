import pygame
from ..settings import *
from ..utils import AnimationManager


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction, group):
        super().__init__(group)
        self.game = game
        self.speed = 650
        self.image = game.assets['bullet']
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction

    def update(self, dt):
        self.rect.x += (self.direction * self.speed) * dt
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction, player):
        super().__init__(player.grenade_group)
        self.game = game
        self.player = player
        
        self.timer = GRENADE_TIMER
        self.velocity_y = -550
        self.speed = GRENADE_SPEED
        self.direction = direction
        
        self.image = game.assets['grenade']
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.timer -= dt
        if self.timer < 0:
            Explosion(self.game, self.rect.centerx, self.rect.centery, self.player.explosion_group)
            self.kill()
            return

        self.rect.x += (self.direction * self.speed) * dt
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction *= -1
            self.speed *= GRENADE_BOUNCE
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction *= -1 
            self.speed *= GRENADE_BOUNCE

        self.velocity_y += GRAVITY * dt
        dy = self.velocity_y * dt
        
        if self.rect.bottom + dy > FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.velocity_y = -(self.velocity_y * GRENADE_BOUNCE)
            self.speed *= 0.8
        else:
            self.rect.y += dy 

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, x, y, group):
        super().__init__(group)
        self.game = game
        self.hit_list = []
        self.damage = 80

        self.animations = {'explosion': game.assets['explosion']}
        self.anim_manager = AnimationManager(self.animations, frame_duration=0.07, action='explosion')
        
        self.image = self.anim_manager.get_image()
        self.rect = self.image.get_rect(center=(x, y))
        self.game.sfx['grenade'].play()

    def update(self, dt):
        finished = self.anim_manager.update(dt, loop=False)
        self.image = self.anim_manager.get_image()
        if finished:
            self.kill()
