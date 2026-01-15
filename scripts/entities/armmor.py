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
        
        # Correção do Bug: Vida útil da bala em segundos
        self.life_time = 2.0 

    def update(self, dt):
        self.rect.x += (self.direction * self.speed) * dt
        
        # Mata a bala por tempo, não por posição
        self.life_time -= dt
        if self.life_time <= 0:
            self.kill()


class Grenade(pygame.sprite.Sprite):
    # ... (Manter a classe Grenade igual à anterior) ...
    # Se certifique de usar a versão que eu mandei no passo anterior, 
    # com a colisão do obstacle_group!
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

    def update(self, dt, obstacle_group):
        self.timer -= dt
        if self.timer < 0:
            Explosion(self.game, self.rect.centerx, self.rect.centery, self.player.explosion_group)
            self.kill()
            return

        # Movimento X
        self.rect.x += (self.direction * self.speed) * dt
        for tile in obstacle_group:
            if tile.rect.colliderect(self.rect):
                if self.direction == 1: self.rect.right = tile.rect.left
                else: self.rect.left = tile.rect.right
                self.direction *= -1
                self.speed *= GRENADE_BOUNCE

        # Movimento Y
        self.velocity_y += GRAVITY * dt
        dy = self.velocity_y * dt
        self.rect.y += dy 

        for tile in obstacle_group:
            if tile.rect.colliderect(self.rect):
                if dy > 0: 
                    self.rect.bottom = tile.rect.top
                    self.velocity_y = -self.velocity_y * GRENADE_BOUNCE
                    self.speed *= 0.8
                    if abs(self.velocity_y) < 100: self.velocity_y = 0
                elif dy < 0: 
                    self.rect.top = tile.rect.bottom
                    self.velocity_y = 0

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