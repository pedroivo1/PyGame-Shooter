import pygame
import sys
from src import soldier


class Game():
    def __init__(self):
        screen_width = 800
        screen_height = int(screen_width * 0.8)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Shooter')

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.player = soldier.Player(200, 200, 2, 0.3)
        self.enemy = soldier.Enemy(500, 200, 2, 0.3)


    def event_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\033[92mGame ended clean.\033[0m\n")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("\033[92mGame ended clean.\033[0m\n")
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_a:
                    self.player.moving_left = True
                elif event.key == pygame.K_d:
                    self.player.moving_right = True
                elif event.key == pygame.K_w:
                    self.player.jump = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.moving_left = False
                elif event.key == pygame.K_d:
                    self.player.moving_right = False
                elif event.key == pygame.K_w:
                    self.player.jump = False


    def draw_background(self):
        self.screen.fill((60, 60, 60))


    def screen_update(self):
        self.draw_background()

        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        pygame.display.update()


    def run(self):

        while True:
            dt = self.clock.tick(self.fps)
            self.event_update()
            self.player.move(dt)
            self.screen_update()


if __name__ == '__main__':
    pygame.init()

    game = Game()
    game.run()
