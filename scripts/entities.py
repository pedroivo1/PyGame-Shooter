import pygame
import random
from abc import ABC
from .settings import *
from .utils import AnimationManager


class Soldier(pygame.sprite.Sprite, ABC):
    def __init__(self, game, x, y, speed, color, ammo):
        super().__init__()
        self.game = game
        self.speed = speed
        self.ammo = ammo
        self.health = 100
        self.max_health = 100
        self.alive_ = True
        
        self.health_bar = HealthBar(40, 8, self.max_health, 2)

        self.shoot_cooldown = 0.0
        self.shoot_delay = 0.35
        self.death_timer = 0.0

        self.bullet_group = pygame.sprite.Group()

        self.animations = {
            'idle': game.assets[f'{color}_idle'],
            'run':  game.assets[f'{color}_run'],
            'jump': game.assets[f'{color}_jump'],
            'death': game.assets[f'{color}_death']
        }
        self.anim_manager = AnimationManager(self.animations)
        self.image = self.anim_manager.get_image()
        self.rect = self.image.get_rect(center=(x, y))

        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.direction = 1
        self.pressed_jump = False

    def move(self, dt, actions):
        dx = 0
        dy = 0
        
        if actions['left']:
            dx = -self.speed * dt
            self.facing_right = False
            self.direction = -1
        elif actions['right']:
            dx = self.speed * dt
            self.facing_right = True
            self.direction = 1

        if actions['jump'] and self.on_ground and not self.pressed_jump:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False
            self.pressed_jump = True
            self.game.sfx['jump'].play()
        
        if not actions['jump']:
            self.pressed_jump = False

        self.velocity_y += GRAVITY * dt
        dy += self.velocity_y * dt

        if self.rect.bottom + dy > FLOOR_Y:
            dy = FLOOR_Y - self.rect.bottom
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
        self.image = pygame.transform.flip(self.anim_manager.get_image(), not self.facing_right, False)

        if not self.alive_ and self.anim_manager.frame == len(self.anim_manager.animations['death']) - 1:
            self.death_timer += dt
            if self.death_timer > 2.0: 
                self.kill()

    def shoot(self, dt, actions):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        if actions.get('shoot') and self.shoot_cooldown <= 0 and self.ammo > 0:
            self.ammo -= 1
            self.shoot_cooldown = self.shoot_delay
            
            offset_x = self.rect.width * self.direction * 0.6
            Bullet(self.game, self.rect.centerx + offset_x, self.rect.centery, self.direction, self.bullet_group)
            self.game.sfx['shot'].play()

    def take_damage(self, amount):
        if not self.alive_: return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive_ = False

    def draw_ui(self, surface):
        if self.alive_:
            bar_x = self.rect.x + (self.rect.width // 2) - (self.health_bar.width // 2)
            bar_y = self.rect.y - 15 
            self.health_bar.draw(surface, self.health, bar_x, bar_y)


class Player(Soldier):
    def __init__(self, game, x, y, speed, color, ammo, grenade):
        super().__init__(game, x, y, speed, color, ammo)
        self.grenade_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.grenade = grenade
        self.grenade_cooldown = 0.0

        self.health_bar = HealthBar(200, 20, self.max_health, 3)
        self.max_health = 300

    def update(self, dt, actions):
        if self.alive_:
            self.move(dt, actions)
            self.shoot(dt, actions)
            self.throw_grenade(dt, actions)
        self.animate(dt, actions)

    def draw_ui(self, surface):
        self.health_bar.draw(surface, self.health, 10, 10)

    def throw_grenade(self, dt, actions):
        if self.grenade_cooldown > 0:
            self.grenade_cooldown -= dt

        if (actions.get('grenade') and 
            self.grenade_cooldown <= 0 and 
            self.grenade > 0 and 
            self.game.actions['relesed_q']):
            
            self.game.actions['relesed_q'] = False
            self.grenade_cooldown = 0.35
            self.grenade -= 1
            
            offset_x = self.rect.width * self.direction * 0.4
            offset_y = -self.rect.height * 0.35
            
            Grenade(self.game, 
                    self.rect.centerx + offset_x, 
                    self.rect.centery + offset_y, 
                    self.direction, 
                    self)

class Enemy(Soldier):
    def __init__(self, game, x, y, speed, color):
        super().__init__(game, x, y, speed, color, -1)
        self.move_counter = 0 
        self.idling = False
        self.idling_counter = 0
        self.t = 1
        
    def update(self, dt):
        ai_actions = {'left': False, 'right': False, 'jump': False, 'shoot': False}
        if self.alive_:
            self.ai(dt, ai_actions)
            self.move(dt, ai_actions)
            self.shoot(dt, ai_actions)
        self.animate(dt, ai_actions)

    def ai(self, dt, ai_actions):
        if not self.idling:
            if self.facing_right:
                ai_actions['right'] = True
            else:
                ai_actions['left'] = True

            self.move_counter += dt
            if self.move_counter > self.t:
                self.t = random.uniform(0.5, 3)
                self.idling = True
                self.idling_counter = 0
                self.move_counter = 0
        else:
            self.idling_counter += dt
            if self.idling_counter > self.t:
                self.t = random.uniform(0.5, 3)
                self.idling = False
                self.facing_right = not self.facing_right


class HealthBar:
    def __init__(self, width, height, max_health, border):
        self.width = width
        self.height = height
        self.max_health = max_health
        self.border = border

    def draw(self, surface, current_health, x, y):
        health_to_draw = max(0, current_health)
        
        green_width = 0
        yellow_width = 0
        black_width = 0

        if health_to_draw <= self.max_health:
            ratio = health_to_draw / self.max_health
            green_width = int(self.width * ratio)
        elif health_to_draw <= self.max_health * 2:
            green_width = self.width
            extra_health = health_to_draw - self.max_health
            ratio_extra = extra_health / self.max_health 
            yellow_width = int(self.width * ratio_extra)
        else:
            green_width = self.width
            yellow_width = self.width
            black_health = health_to_draw - (self.max_health * 2)
            ratio_black = black_health / self.max_health
            black_width = int(self.width * ratio_black)
            black_width = min(black_width, self.width)

        border_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(surface, RED, border_rect)
        
        if green_width > 0:
            fill_rect = pygame.Rect(x, y, green_width, self.height)
            pygame.draw.rect(surface, GREEN, fill_rect)

        if yellow_width > 0:
            yellow_rect = pygame.Rect(x, y, yellow_width, self.height)
            pygame.draw.rect(surface, YELLOW, yellow_rect)

        if black_width > 0:
            black_rect = pygame.Rect(x, y, black_width, self.height)
            pygame.draw.rect(surface, GRAY, black_rect)
        
        pygame.draw.rect(surface, BLACK, border_rect, self.border)


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, game, item_type, x, y, group):
        super().__init__(group)
        self.item_type = item_type
        self.image = game.assets[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.rect.height)

    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'health_box':
                player.health += 25
                if player.health > player.max_health:
                    player.health = 300
                
            elif self.item_type == 'ammo_box':
                player.ammo += 5
            elif self.item_type == 'grenade_box':
                player.grenade += 2
            self.kill()

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
