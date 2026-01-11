import pygame
from .settings import *
from .utils import AnimationManager

class Soldier(pygame.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        super().__init__()
        self.game = game

        self.animations = {
            'idle': game.assets['player_idle'],
            'run':  game.assets['player_run'],
            'jump':  game.assets['player_jump'],
        }
        self.anim_manager = AnimationManager(self.animations)
        self.image = self.anim_manager.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = speed
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True

    def update(self, dt, actions):
        self.move(actions, dt)
        self.animate(dt, actions)

    def move(self, actions, dt):
        dx = 0
        dy = 0
        
        if actions['left']:
            dx = -self.speed * dt
            self.facing_right = False
        if actions['right']:
            dx = self.speed * dt
            self.facing_right = True
            
        if actions['jump'] and self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

        self.velocity_y += GRAVITY * dt
        dy += self.velocity_y *dt

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.velocity_y = 0
            self.on_ground = True

        self.rect.x += dx
        self.rect.y += dy

    def animate(self, dt, actions):
        if not self.on_ground:
            self.anim_manager.set_action('jump')
        elif actions['left'] or actions['right']:
            self.anim_manager.set_action('run')
        else:
            self.anim_manager.set_action('idle')

        self.anim_manager.update(dt)
        
        current_img = self.anim_manager.get_image()
        self.image = pygame.transform.flip(current_img, not self.facing_right, False)
