import pygame
from ..settings import default_imports

class HealthBar():
    def __init__(self, soldier) -> None:
        super().__init__()
        self.x = soldier.rect.topleft[0]
        self.y = soldier.rect.top + 5
        self.width = int(soldier.rect.width)
        self.height = 4
        self.health = soldier.soldier_settings.health.health
        self.start_health = soldier.soldier_settings.health.start_health


    def update(self, soldier) -> None:
        self.x = soldier.rect.topleft[0]
        self.y = soldier.rect.topleft[1] - 5
        self.health = soldier.soldier_settings.health.health


    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, default_imports.colors['black'], (self.x-1, self.y-1, self.width+2, self.height+2))
        pygame.draw.rect(screen, default_imports.colors['red'], (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, default_imports.colors['green'], (self.x, self.y, self.width * (self.health/self.start_health), self.height))
