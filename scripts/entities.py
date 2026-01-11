import pygame
from .settings import *
from .utils import AnimationManager

class Soldier(pygame.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        super().__init__()
        self.game = game
        self.bullet_group = pygame.sprite.Group()
        self.shoot_cooldown = 0.35
        self.ammo = 20

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
        self.pressed_jump = False
        self.facing_right = True

    def update(self, dt, actions):
        self.move(actions, dt)
        self.animate(dt, actions)
        self.shoot(actions, dt)

    def move(self, actions, dt):
        dx = 0
        dy = 0
        
        if actions['left']:
            dx = -self.speed * dt
            self.facing_right = False
        if actions['right']:
            dx = self.speed * dt
            self.facing_right = True

        if actions['jump'] and self.on_ground and not self.pressed_jump:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False
            self.pressed_jump = True
            self.game.sfx['jump'].play()

        if not actions['jump']:
            self.pressed_jump = False

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

    def shoot(self, actions, dt):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        if actions.get('shoot') and self.shoot_cooldown <= 0 and self.ammo > 0:
            self.ammo -= 1
            self.game.actions['shoot'] = False
            direction = 1 if self.facing_right else -1
            x = self.rect.centerx + self.rect.width*direction*0.6
            y = self.rect.centery
            bullet = Bullet(self.game, x, y, direction)
            self.bullet_group.add(bullet)
            self.game.sfx['shot'].play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        super().__init__()
        self.game = game
        self.speed = 600
        self.image = game.assets['bullet']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, dt):
        self.rect.x += (self.direction * self.speed) * dt

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
