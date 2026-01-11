#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pygame
from pathlib import Path

# --- CONFIGURAÇÃO DE CAMINHOS ---
# 1. __file__ é o utils.py
# 2. .parent é a pasta 'scripts'
# 3. .parent.parent é a raiz do projeto (onde está o main.py)
ROOT_DIR = Path(__file__).parent.parent 

BASE_IMG_PATH = ROOT_DIR / 'data' / 'images'
BASE_SND_PATH = ROOT_DIR / 'data' / 'audios'
BASE_LVL_PATH = ROOT_DIR / 'data' / 'levels'

def load_image(path: str, scale: float = 1.0):
    full_path = BASE_IMG_PATH / path
    try:
        img = pygame.image.load(full_path).convert_alpha()
        if scale != 1.0:
            new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
            img = pygame.transform.scale(img, new_size)
        return img
    except FileNotFoundError:
        print(f"ERRO: Imagem não encontrada: {full_path}")
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))
        return surf

def load_images(path: str, scale: float = 1.0):
    folder_path = BASE_IMG_PATH / path
    images = []
    
    if not folder_path.exists():
        print(f"ERRO: Pasta não encontrada: {folder_path}")
        return []

    for file_path in sorted(folder_path.glob('*.png')):
        try:
            img = pygame.image.load(file_path).convert_alpha()
            if scale != 1.0:
                new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
                img = pygame.transform.scale(img, new_size)
            images.append(img)
        except Exception as e:
            print(f"Erro ao carregar {file_path.name}: {e}")

    return images

def load_sound(path: str, volume: float = 1.0):
    full_path = BASE_SND_PATH / path
    try:
        sound = pygame.mixer.Sound(full_path)
        sound.set_volume(volume)
        return sound
    except FileNotFoundError:
        print(f"ERRO: Audio não encontrado: {full_path}")
        return None


class AnimationManager:
    def __init__(self, animations: dict, frame_duration: float = 0.12):
        self.animations = animations 
        self.frame_duration = frame_duration 
        self.action = 'idle'
        self.frame = 0
        self.timer = 0

    def update(self, dt: float, loop: bool = True):
        finished = False
        self.timer += dt
        
        if self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            
            next_frame = self.frame + 1
            
            if next_frame >= len(self.animations[self.action]):
                if loop:
                    self.frame = 0
                else:
                    self.frame = len(self.animations[self.action]) - 1 # Sem loop: TRAVA no último
                    
                finished = True
            else:
                self.frame = next_frame

        return finished

    def set_action(self, action: str):
        if action != self.action:
            self.action = action
            self.frame = 0
            self.timer = 0

    def get_image(self):
        return self.animations[self.action][self.frame]
