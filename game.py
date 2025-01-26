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

        self.colors = {
            'bg': (144, 201, 120),
            'red': (210, 60, 40),
            'gray': (60, 60, 60)
        }

        self.player = soldier.Player(200, 200, 2, 0.3)
        self.enemy = soldier.Enemy(500, 200, 2, 0.3)


    def event_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\033[92mThe game has closed successfully.\033[0m\n")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("\033[92mThe game has closed successfully.\033[0m\n")
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_a:
                    self.player.runing_left = True
                    self.player.runing_right = False
                    self.player.action_update('run')
                if event.key == pygame.K_d:
                    self.player.runing_right = True
                    self.player.runing_left = False
                    self.player.action_update('run')
                if event.key == pygame.K_w and not self.player.in_air:
                    self.player.jumped = True
                    self.player.action_update('jump')

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.runing_left = False
                    if not self.player.runing_right:
                        self.player.action_update('idle')
                if event.key == pygame.K_d:
                    self.player.runing_right = False
                    if not self.player.runing_left:
                        self.player.action_update('idle')


    def draw_background(self):
        self.screen.fill(self.colors['bg'])
        pygame.draw.line(self.screen, self.colors['red'], (0, 300), (800, 300))


    def screen_update(self):
        self.draw_background()

        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        pygame.display.update()


    def run(self):

        while True:
            dt = self.clock.tick(self.fps)
            self.event_update()
            self.player.animation_update()
            self.player.move(dt)
            self.screen_update()


if __name__ == '__main__':
    pygame.init()

    game = Game()
    game.run()
