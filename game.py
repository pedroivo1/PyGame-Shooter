import pygame
import sys
from src import soldier


class Game():
    def __init__(self):
        screen_width = 800
        screen_height = int(screen_width * 0.8)

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Shooter')

        self.player = soldier.Soldier(200, 200, 2)
        self.player2 = soldier.Soldier(400, 200, 2)


    def event_update(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


    def screen_update(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        self.player2.draw(self.screen)
        pygame.display.update()


    def run(self):
        
        while True:
            self.event_update()
            self.screen_update()



if __name__ == '__main__':
    pygame.init()

    game = Game()
    game.run()
