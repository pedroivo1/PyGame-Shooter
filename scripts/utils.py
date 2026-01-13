#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent
BASE_IMG_PATH = ROOT_DIR / 'data' / 'images'
BASE_SND_PATH = ROOT_DIR / 'data' / 'audios'


def load_image(path: str | Path, scale: float = 1.0) -> pygame.Surface:
    full_path = BASE_IMG_PATH / path
    try:
        img = pygame.image.load(full_path).convert_alpha()
        if scale != 1.0:
            new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
            img = pygame.transform.scale(img, new_size)
        return img
    except FileNotFoundError:
        logger.error(f"File not found: {full_path}")
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))
        return surf


def load_images(path: str, scale: float = 1.0) -> list[pygame.Surface]:
    folder_path = BASE_IMG_PATH / path
    if not folder_path.exists():
        logger.error(f"Folder not found: {folder_path}")
        return []

    images = []
    for file_path in sorted(folder_path.glob('*.png')):
        rel_path = file_path.relative_to(BASE_IMG_PATH)
        images.append(load_image(rel_path, scale))
    return images


def load_sound(path: str, volume: float = 1.0) -> pygame.mixer.Sound | None:
    full_path = BASE_SND_PATH / path
    try:
        sound = pygame.mixer.Sound(full_path)
        sound.set_volume(volume)
        return sound
    except FileNotFoundError:
        logger.error(f"Audio file not found: {full_path}")
        return None


class AnimationManager:
    def __init__(self, animations: dict, frame_duration: float = 0.12, action='idle'):
        self.animations = animations 
        self.frame_duration = frame_duration 
        self.action = action
        self.frame = 0
        self.timer = 0.0

    def update(self, dt: float, loop: bool = True) -> bool:
        finished = False
        self.timer += dt

        if self.timer >= self.frame_duration:
            self.timer %= self.frame_duration
            next_frame = self.frame + 1
            
            if next_frame >= len(self.animations[self.action]):
                if loop:
                    self.frame = 0
                else:
                    self.frame = len(self.animations[self.action]) - 1
                    finished = True
            else:
                self.frame = next_frame

        return finished

    def set_action(self, action: str):
        if action != self.action:
            self.action = action
            self.frame = 0
            self.timer = 0

    def get_image(self) -> pygame.Surface:
        return self.animations[self.action][self.frame]
