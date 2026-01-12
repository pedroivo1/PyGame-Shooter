#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import time
from .settings import *
from scripts.utils import load_image, load_images, load_sound

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.state_stack = []

        self.dt = 0
        self.prev_time = time.time()
        self.actions = {"left": False, "right": False, "jump": False, "grenade": False, "relesed_q": True}
        self.scale = 2.5

        self.assets = {
            'start_btn': load_image('start_btn.png'),
            'exit_btn':  load_image('exit_btn.png'),

            'bullet': load_image('icons/bullet.png', 1.5),
            'grenade': load_image('icons/grenade.png', 1.5),

            'green_death': load_images('soldiers/green/death', self.scale),
            'green_idle': load_images('soldiers/green/idle', self.scale),
            'green_jump':  load_images('soldiers/green/jump', self.scale),
            'green_run':  load_images('soldiers/green/run', self.scale),
            'red_death': load_images('soldiers/red/death', self.scale),
            'red_idle': load_images('soldiers/red/idle', self.scale),
            'red_jump':  load_images('soldiers/red/jump', self.scale),
            'red_run':  load_images('soldiers/red/run', self.scale),
        }

        self.sfx = {
            'jump': load_sound('jump.wav', volume=0.5),
            'shot': load_sound('shot.wav', volume=0.4),
            'grenade': load_sound('grenade.wav')
        }

        try:
            pygame.mixer.music.load('data/audios/music2.mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Erro ao carregar música:", e)

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.running = False
                if event.key == pygame.K_a: self.actions['left'] = True
                if event.key == pygame.K_d: self.actions['right'] = True
                if event.key == pygame.K_w: self.actions['jump'] = True
                if event.key == pygame.K_SPACE: self.actions['shoot'] = True
                if event.key == pygame.K_q: self.actions['grenade'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: self.actions['left'] = False
                if event.key == pygame.K_d: self.actions['right'] = False
                if event.key == pygame.K_w: self.actions['jump'] = False
                if event.key == pygame.K_SPACE: self.actions['shoot'] = False
                
                if event.key == pygame.K_q: 
                    self.actions['grenade'] = False
                    self.actions['relesed_q'] = True

    def update(self):
        if self.state_stack:
            self.state_stack[-1].update(self.dt, self.actions)

    def draw(self):
        if self.state_stack:
            self.state_stack[-1].draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.get_dt()
            self.get_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
