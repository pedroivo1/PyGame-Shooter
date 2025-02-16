from pydantic import BaseModel

class PhysicsSettings(BaseModel):
    gravity: float
    GC: float
