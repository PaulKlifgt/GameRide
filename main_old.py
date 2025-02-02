import pygame
import math, random, time


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Pursuit')
done = False

clock = pygame.time.Clock()

road_image = pygame.image.load('img/road.png')
road_width = road_image.get_width()
over_image = pygame.image.load('img/over.png')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/car_1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = screen.get_height() / 2
        self.vy = 0
    def update(self):
        self.vy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.vy = -3
        elif key[pygame.K_DOWN]:
            self.vy = 3
        if self.rect.y >= 630:
            self.rect.y = 620
        elif self.rect.y <= 0:
            self.rect.y = 10
        else:
            self.rect.y += self.vy

sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

win = False


class Musor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/mus_car.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1240
        self.rect.y = random.randint(40, 590)
        self.vx = 0
    def update(self):
        self.vx = -3
        self.rect.x += self.vx

musors = pygame.sprite.Group()

tiles = math.ceil(screen.get_width() / road_width) + 1
scroll = 0

musor = Musor()
musors.add(musor)

def spawn_musor():
    musor = Musor()
    musors.add(musor)

musor_timer = pygame.USEREVENT + 1
pygame.time.set_timer(musor_timer, 1000)

game_over = False
while not done:
    while not game_over:
        for i in range(0, tiles):
            screen.blit(road_image, (i * road_width + scroll, 0))
        scroll -= 2

        sprites.update()
        sprites.draw(screen)

        musors.update()
        musors.draw(screen)

        if abs(scroll) > road_width:
            scroll = 0

        hits = pygame.sprite.spritecollide(player, musors, True)
        if hits:
            game_over = True

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == musor_timer:
                spawn_musor()

        pygame.display.update()
    else:
        screen.blit(over_image, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.update()

    time.sleep(2)
    game_over = False