import pygame
import os

BG = (144, 201, 120)
RED = (230, 20, 10)
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        super().__init__()
        self.alive_ = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.on_air = True
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        animations_types = ['Idle', 'Run', 'Jump']
        for animation in animations_types:
            temp_list = []
            frames_n = len(os.listdir(f'img/{self.char_type}/{animation}')) 
            for i in range(frames_n):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = img.get_rect()
        self.rect.center = (x, y)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.freme_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self):
        ANIMATION_COOLDWON = 100
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDWON:
            self.index += 1
            self.update_time = pygame.time.get_ticks()
            self.image = self.animation_list[self.action][self.index % len(self.animation_list[self.action])]

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx += self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.on_air:
            self.vel_y = -11
            self.jump = False
            self.on_air = True

        if self.vel_y > 10:
            self.vel_y = 10
        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.on_air = False

        self.rect.x += dx
        self.rect.y += dy

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGTH = int(SCREEN_WIDTH *0.8)

    clock = pygame.time.Clock()
    FPS = 60

    GRAVITY = 0.75

    moving_left = False
    moving_right = False

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
    pygame.display.set_caption('Shooter')

    player = Soldier('player', 200, 200, 3, 5)

    run = True
    while run:
        clock.tick(FPS)

        draw_bg()
        player.update_animation()
        player.draw()
        player.move(moving_left, moving_right)

        if player.alive_:
            if player.on_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w:
                    player.jump = True
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False

        pygame.display.update()

    pygame.quit()
