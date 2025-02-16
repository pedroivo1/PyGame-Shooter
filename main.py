import pygame
from src import Game


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    game = Game.Game()
    game.run()
