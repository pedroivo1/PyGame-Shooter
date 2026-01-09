import pygame

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        img = pygame.image.load('img/player/Idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGTH = int(SCREEN_WIDTH *0.8)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
    pygame.display.set_caption('Shooter')

    player = Soldier(200, 200, 3)

    run = True
    while run:

        player.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
