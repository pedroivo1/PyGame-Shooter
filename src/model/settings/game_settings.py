from pydantic import BaseModel

class ScreenSettings(BaseModel):
    width: int
    height: int
    fps: int
    scale: float
    title: str
    animation_cooldown: int

class PhysicSettings(BaseModel):
    gravity: float

class Settings(BaseModel):
    screen: ScreenSettings
    physic: PhysicSettings
