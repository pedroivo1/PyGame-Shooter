from src import utils
import pygame

width, height = utils.get_screen_size()

config_data = {
    'screen': {
        'width': int(width*0.9),
        'height': int(height*0.9),
        'fps': 200,
        'scale': 2,
        'title': 'Shooter',
        'animation_cooldown': 100,
        'tile_size': 16
    },
    'physics': {
        'gravity': 0.05,
        'GC': 13.0
    }
}

soldier_settings = {
    "movement": {"x_velocity": 0.3, "y_velocity": 0, "direction": 1},
    "health": {"health": 100, "start_health": 100},
    "state": {
        "soldier_alive": True,
        "running_left": False,
        "running_right": False,
        "jumped": False,
        "in_air": False,
        "flip_image": False,
    },
    "ammo": {
        "shot": False,
        "shot_cooldown": 250,
        "shot_time": pygame.time.get_ticks(),
        "ammo": 20,
        "start_ammo": 20,
    },
    "animation": {
        "animation_timer": pygame.time.get_ticks(),
        "animation_index": 0,
        "animation_action": "idle",
        "animations_map": {},
    },
}

grenade_config = {
    "threw_grenade": False,
    "threw_grenade_cooldown": 400,
    "threw_grenade_time": pygame.time.get_ticks(),
    "number_of_grenades": 5,
}

colors = {
    'bg': (144, 201, 120),
    'red': (210, 60, 40),
    'green': (60, 210, 40),
    'gray': (60, 60, 60),
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}
