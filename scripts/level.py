#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from .state import State
from .settings import *
from .entities import Soldier

class Level(State):
    def __init__(self, game):
        super().__init__(game)
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Soldier(game, 200, 200, 300)
        self.player_group.add(self.player)

    def update(self, dt, actions):
        self.player_group.update(dt, actions)
        self.player.bullet_group.update(dt)

    def draw(self, surface):
        surface.fill((144, 201, 120))
        pygame.draw.line(surface, (255, 0, 0), (0, 300), (800, 300))
        self.player_group.draw(surface)
        self.player.bullet_group.draw(surface)
