#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: https://github.com/pedroivo1

import pygame
from abc import ABC, abstractmethod
from .settings import *
from .entities.soldier import Player, Enemy
from .entities.Items import ItemBox


class State(ABC):
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    @abstractmethod
    def update(self, dt, actions):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()


class Level(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.item_box_group = pygame.sprite.Group()
        health = ItemBox(game, 'health_box', 900, 260, self.item_box_group)
        health = ItemBox(game, 'health_box', 1100, 260, self.item_box_group)
        health = ItemBox(game, 'health_box', 1200, 260, self.item_box_group)
        health = ItemBox(game, 'health_box', 1300, 260, self.item_box_group)
        health = ItemBox(game, 'health_box', 1400, 260, self.item_box_group)
        ammo = ItemBox(game, 'ammo_box', 940, 260, self.item_box_group)
        grenade = ItemBox(game, 'grenade_box', 980, 260, self.item_box_group)

        self.player_bullet_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player(game, 200, 200, TILE_SIZE*5.8, 'blue', 20, 5, self.player_bullet_group)
        self.player_group.add(self.player)

        self.enemy_bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        enemy1 = Enemy(game, 500, 350, TILE_SIZE*4.5, 'red', self.enemy_bullet_group)
        self.enemy_group.add(enemy1)

    def update(self, dt, actions):
        self.player_group.update(dt, actions)
        self.player_bullet_group.update(dt)
        self.player.grenade_group.update(dt)
        self.player.explosion_group.update(dt)

        self.enemy_group.update(dt, self.player)
        self.enemy_bullet_group.update(dt)

        self.item_box_group.update(self.player)

        self._check_collisions()

    def _check_collisions(self):

        hits = pygame.sprite.groupcollide(self.enemy_group, self.player.bullet_group, False, True)
        for enemy in hits:
            enemy.take_damage(25)

        exp_hits = pygame.sprite.groupcollide(self.player.explosion_group, self.enemy_group, False, False)
        for explosion, enemies_hit in exp_hits.items():
            for enemy in enemies_hit:
                if enemy not in explosion.hit_list:
                    enemy.take_damage(explosion.damage)
                    explosion.hit_list.append(enemy)

        player_hit = pygame.sprite.groupcollide(self.player.explosion_group, self.player_group, False, False)
        for explosion in player_hit:
             if self.player not in explosion.hit_list:
                 self.player.take_damage(explosion.damage)
                 explosion.hit_list.append(self.player)
        
        if pygame.sprite.spritecollide(self.player, self.enemy_bullet_group, True): # type: ignore
            self.player.take_damage(5)

    def draw(self, surface):
        surface.fill((144, 201, 120))
        pygame.draw.line(surface, RED, (0, FLOOR_Y), (SCREEN_WIDTH, FLOOR_Y))

        for i in range(self.player.ammo):
            x = 10 + i*11
            surface.blit(self.game.assets['bullet'], (x, 35))

        for i in range(self.player.grenade):
            x = 10 + i*15
            surface.blit(self.game.assets['grenade'], (x, 62))

        self.player_group.draw(surface)
        self.player_bullet_group.draw(surface)
        self.player.grenade_group.draw(surface)
        self.player.explosion_group.draw(surface)

        self.enemy_group.draw(surface)
        self.enemy_bullet_group.draw(surface)
        self.item_box_group.draw(surface)

        self.player.draw_ui(surface) 

        for enemy in self.enemy_group:
            enemy.draw_ui(surface)

        if DEBUG:
            all_groups = [
                self.player_group,
                self.player.bullet_group,
                self.player.grenade_group,
                self.player.explosion_group,
                self.enemy_group,
                self.item_box_group
            ]

            for group in all_groups:
                for sprite in group:
                    pygame.draw.rect(surface, (255, 255, 255), sprite.rect, 1)
