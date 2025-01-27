import pygame
import sys
from src import Soldier


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

        self.player = Soldier.Player(200, 200, 2, 23)
        self.enemy = Soldier.Enemy(500, 200, 2, 20)

        self.bullets = pygame.sprite.Group()


    def event_handler(self):
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
                    self.player.running_left = True
                    self.player.running_right = False
                    if not self.player.in_air:
                        self.player.action_update('run')
                if event.key == pygame.K_d:
                    self.player.running_right = True
                    self.player.running_left = False
                    if not self.player.in_air:
                        self.player.action_update('run')
                if event.key == pygame.K_w and not self.player.in_air:
                    self.player.jumped = True
                    self.player.action_update('jump')
                if event.key == pygame.K_SPACE:
                    self.player.shooting = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.running_left = False
                    if not self.player.running_right:
                        self.player.action_update('idle')
                if event.key == pygame.K_d:
                    self.player.running_right = False
                    if not self.player.running_left:
                        self.player.action_update('idle')
                if event.key == pygame.K_SPACE:
                    self.player.shooting = False


    def update(self, dt):
        self.bullets.update()
        self.player.update(dt, self.bullets)
        self.enemy.update(dt, self.bullets)

        collided_bullets = pygame.sprite.spritecollide(self.player, self.bullets, False)
        for bullet in collided_bullets:
            if self.player.soldier_alive:
                self.player.health -= 5
                bullet.kill()

        collided_bullets = pygame.sprite.spritecollide(self.enemy, self.bullets, False)
        for bullet in collided_bullets:
            if self.enemy.soldier_alive:
                self.enemy.health -= 25
                bullet.kill()


    def draw_background(self):
        self.screen.fill(self.colors['bg'])
        pygame.draw.line(self.screen, self.colors['red'], (0, 300), (800, 300))


    def screen_update(self):
        self.draw_background()

        self.bullets.draw(self.screen)

        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        pygame.display.update()


    def run(self):
        while True:
            dt = self.clock.tick(self.fps)
            self.event_handler()
            self.update(dt)
            self.screen_update()


if __name__ == '__main__':
    pygame.init()

    game = Game()
    game.run()
