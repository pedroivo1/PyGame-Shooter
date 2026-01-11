#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from abc import ABC, abstractmethod
from .settings import *
from .entities import Player, Enemy

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

        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player(game, 200, 200, 300, 'green', 20)
        self.player_group.add(self.player)

        self.enemy_group = pygame.sprite.Group()
        enemy1 = Enemy(game, 500, 350, 300, 'red')
        self.enemy_group.add(enemy1)

    def update(self, dt, actions):
        self.player_group.update(dt, actions)
        self.player.bullet_group.update(dt)
        
        self.enemy_group.update(dt)

        hits = pygame.sprite.groupcollide(self.enemy_group, self.player.bullet_group, False, True)
        for enemy in hits:
            enemy.take_damage(25)

    def draw(self, surface):
        surface.fill((144, 201, 120))
        pygame.draw.line(surface, (255, 0, 0), (0, 300), (800, 300))
        self.player_group.draw(surface)
        self.player.bullet_group.draw(surface)
        self.enemy_group.draw(surface)
