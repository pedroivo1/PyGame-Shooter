from pydantic import BaseModel

class MovementConfig(BaseModel):
    x_velocity: float
    y_velocity: float
    direction: int

class HealthConfig(BaseModel):
    health: int
    start_health: int

class StateConfig(BaseModel):
    soldier_alive: bool
    running_left: bool
    running_right: bool
    jumped: bool
    in_air: bool
    flip_image: bool

class AmmoConfig(BaseModel):
    shot: bool
    shot_cooldown: int
    shot_time: int
    ammo: int
    start_ammo: int

class AnimationConfig(BaseModel):
    animation_cooldown: int
    animation_timer: int
    animation_index: int
    animation_action: str
    animations_map: dict

class SoldierConfig(BaseModel):
    movement: MovementConfig
    health: HealthConfig
    state: StateConfig
    ammo: AmmoConfig
    animation: AnimationConfig

class GrenadeConfig(BaseModel):
    threw_grenade: bool
    threw_grenade_cooldown: int
    threw_grenade_time: int
    number_of_grenades: int
