import pygame
import sys
import os
from src.model.game import Soldier
from src.model.settings import game_settings
from src import default_imports
from pathlib import Path


class Game():
    def __init__(self) -> None:
        self.config = game_settings.Settings(**(default_imports.config_data))
        self.screen = pygame.display.set_mode((self.config.screen.width, self.config.screen.height))
        pygame.display.set_caption(self.config.screen.title)

        self.clock = pygame.time.Clock()

        self.assets = {'animations': {}, 'images': {}}
        self.assets_import()

        self.player = Soldier.Player(200, 200, self.config, self.assets, 'green')
        self.enemy = Soldier.Enemy(500, 200, self.config, self.assets, 'red')
        self.bullet_group = pygame.sprite.Group()
        self.grenade_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()


    def assets_import(self) -> None:
        self.assets['images']['bullet'] = self.image_import(Path('src/assets/img/icons/bullet.png'), scale=1)
        self.assets['images']['grenade'] = self.image_import(Path('src/assets/img/icons/grenade.png'), scale=1)
        self.animations_import(Path('src/assets/img/soldier/green'))
        self.animations_import(Path('src/assets/img/soldier/red'))
        self.assets['animations']['explosion'] = self.animation_import(Path('src/assets/img/explosion'))


    def animations_import(self, image_path: Path) -> None:
        self.assets['animations'][image_path.stem] = {}
        for action in os.listdir(image_path):
            self.assets['animations'][image_path.stem][action] = self.animation_import(image_path/action)


    def animation_import(self, image_path: Path) -> list[pygame.Surface]:
        animation = []
        for frame in os.listdir(image_path):
            animation.append(self.image_import(image_path / frame, self.config.screen.scale))
        return animation

    def image_import(self, image_path: Path, scale: float) -> pygame.Surface:
        img = pygame.image.load(str(image_path)).convert_alpha()
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))


    def finesh_game(self):
        print("\033[92mThe game has closed successfully.\033[0m\n")
        pygame.quit()
        sys.exit()


    def event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finesh_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.finesh_game()

                if event.key == pygame.K_a:
                    self.player.soldier_settings.state.running_left = True
                    self.player.soldier_settings.state.running_right = False
                    if not self.player.soldier_settings.state.in_air:
                        self.player.action_update('run')
                if event.key == pygame.K_d:
                    self.player.soldier_settings.state.running_right = True
                    self.player.soldier_settings.state.running_left = False
                    if not self.player.soldier_settings.state.in_air:
                        self.player.action_update('run')
                if event.key == pygame.K_w and not self.player.soldier_settings.state.in_air:
                    self.player.soldier_settings.state.jumped = True
                    self.player.action_update('jump')
                if event.key == pygame.K_SPACE:
                    self.player.soldier_settings.ammo.shot = True
                if event.key == pygame.K_q:
                    self.player.grenade_config.threw_grenade = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.soldier_settings.state.running_left = False
                    if not self.player.soldier_settings.state.running_right:
                        self.player.action_update('idle')
                if event.key == pygame.K_d:
                    self.player.soldier_settings.state.running_right = False
                    if not self.player.soldier_settings.state.running_left:
                        self.player.action_update('idle')
                if event.key == pygame.K_SPACE:
                    self.player.soldier_settings.ammo.shot = False
                if event.key == pygame.K_q:
                    self.player.grenade_config.threw_grenade = False


    def update(self, dt: int) -> None:
        self.bullet_group.update(dt)
        self.grenade_group.update(dt)
        self.explosion_group.update()
        self.player.update(dt, self.bullet_group, self.grenade_group, self.explosion_group)
        self.enemy.update(dt, self.bullet_group, self.grenade_group)

        collided_bullets = pygame.sprite.spritecollide(self.player, self.bullet_group, False)
        for bullet in collided_bullets:
            if self.player.soldier_settings.state.soldier_alive:
                self.player.soldier_settings.health.health -= 5
                bullet.kill()

        collided_bullets = pygame.sprite.spritecollide(self.enemy, self.bullet_group, False)
        for bullet in collided_bullets:
            if self.enemy.soldier_settings.state.soldier_alive:
                self.enemy.soldier_settings.health.health -= 25
                bullet.kill()


    def draw_background(self) -> None:
        self.screen.fill(default_imports.colors['bg'])


    def screen_update(self) -> None:
        self.draw_background()
        self.bullet_group.draw(self.screen)
        self.grenade_group.draw(self.screen)
        self.explosion_group.draw(self.screen)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        pygame.display.update()


    def run(self) -> None:
        while True:
            dt = self.clock.tick(self.config.screen.fps)
            self.event_handler()
            self.update(dt)
            self.screen_update()
