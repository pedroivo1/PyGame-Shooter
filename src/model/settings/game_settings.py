from pydantic import BaseModel

class ScreenSettings(BaseModel):
    width: int
    height: int
    fps: int
    scale: float
    title: str
    animation_cooldown: int
    tile_size: float

class PhysicSettings(BaseModel):
    gravity: float
    GC: float

class Settings(BaseModel):
    screen: ScreenSettings
    physic: PhysicSettings
