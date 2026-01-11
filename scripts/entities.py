import pygame
from abc import ABC
from .settings import *
from .utils import AnimationManager

class Soldier(pygame.sprite.Sprite, ABC):
    def __init__(self, game, x, y, speed, color, ammo):
        super().__init__()
        self.game = game
        self.bullet_group = pygame.sprite.Group()
        self.shoot_cooldown = 0.35
        self.ammo = ammo
        self.health = 100
        self.max_health = self.health
        self.alive_ = True
        self.death_timer = 0

        self.animations = {
            'idle': game.assets[f'{color}_idle'],
            'run':  game.assets[f'{color}_run'],
            'jump': game.assets[f'{color}_jump'],
            'death': game.assets[f'{color}_death']
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

    def move(self, dt, actions):
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
        dy += self.velocity_y * dt

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.velocity_y = 0
            self.on_ground = True

        self.rect.x += dx
        self.rect.y += dy

    def animate(self, dt, actions):
        if self.alive_:
            if not self.on_ground:
                self.anim_manager.set_action('jump')
            elif actions['left'] or actions['right']:
                self.anim_manager.set_action('run')
            else:
                self.anim_manager.set_action('idle')
        else:
            self.anim_manager.set_action('death')

        self.anim_manager.update(dt, loop=self.alive_)

        if not self.alive_:
            current_frame = self.anim_manager.frame
            total_frames = len(self.anim_manager.animations['death'])
            
            if current_frame == total_frames - 1:
                self.death_timer += dt

                if self.death_timer > 2.0: 
                    self.kill()
        
        current_img = self.anim_manager.get_image()
        self.image = pygame.transform.flip(current_img, not self.facing_right, False)

    def shoot(self, dt, actions):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        if actions.get('shoot') and self.shoot_cooldown <= 0 and self.ammo != 0:
            self.ammo -= 1
            self.shoot_cooldown = 0.35

            direction = 1 if self.facing_right else -1
            x = self.rect.centerx + self.rect.width * direction * 0.6
            y = self.rect.centery
            bullet = Bullet(self.game, x, y, direction)
            self.bullet_group.add(bullet)
            self.game.sfx['shot'].play()

    def take_damage(self, amount):
        if not self.alive_: return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive_ = False
            self.anim_manager.set_action('death')


class Player(Soldier):
    def __init__(self, game, x, y, speed, color, ammo):
        super().__init__(game, x, y, speed, color, ammo)

    def update(self, dt, actions):
        if self.alive_:
            self.move(dt, actions)
            self.shoot(dt, actions)
        
        self.animate(dt, actions)


class Enemy(Soldier):
    def __init__(self, game, x, y, speed, color):
        super().__init__(game, x, y, speed, color, -1)
        
        self.move_counter = 0 
        self.idling = False
        self.idling_counter = 0

    def update(self, dt):
        
        ai_actions = {'left': False, 'right': False, 'jump': False, 'shoot': False}
        
        if self.alive_:
            # self.ai(ai_actions)
            self.move(dt, ai_actions)
            self.shoot(dt, ai_actions)

        self.animate(dt, ai_actions)

    def ai(self, ai_actions):
            
            if self.idling == False:
                if self.facing_right:
                    ai_actions['right'] = True
                else:
                    ai_actions['left'] = True
                
                self.move_counter += 1
                if self.move_counter > 100:
                    self.idling = True
                    self.idling_counter = 0
                    self.move_counter = 0
            else:
                self.idling_counter += 1
                if self.idling_counter > 50:
                    self.idling = False
                    self.facing_right = not self.facing_right


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
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
