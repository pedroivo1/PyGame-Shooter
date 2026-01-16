#!/usr/bin/env python3
# Author: https://github.com/pedroivo1

# Screen
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "My Pygame Framework"
TILE_SIZE = 40

# Colors
BG_COLOR = (30, 30, 30)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (220, 220, 220)
D_GRAY = (60, 60, 60)

# BACKGROUND
BACKGROUND_LAYERS = ['sky_cloud.png', 'mountain.png', 'pine1.png', 'pine2.png']
PARALLAX_SPEEDS = [0.2, 0.4, 0.6, 0.8]
BACKGROUND_Y_POSITIONS = [0, 100, 250, 280]

# Physics
GRAVITY = 2600
JUMP_FORCE = -700
FLOOR_Y = 300

# Gameplay
GRENADE_TIMER = 1.2
GRENADE_SPEED = 480
GRENADE_BOUNCE = 0.4

# Font
FONT_NAME = 'Futura'
FONT_SIZE = 32

# Game Infos
DEBUG = False
MAX_LEVELS = 10
ROWS = 16
MAX_COLS = 150
