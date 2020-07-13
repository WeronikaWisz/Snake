from pygame.locals import *
from random import randint
import pygame, sys
image = pygame.image.load("waz.png")
image2 = pygame.image.load("jablko.png")
image3 = pygame.image.load("przeszkoda.png")
tlo = pygame.image.load('tapeta.png')


class Player(object):
    x = [0]
    y = [0]
    step = 5
    direction = 0
    length = 3
    coll = False

    def __init__(self, length):
        self.length = length
        for i in range(0, 3000):
            self.x.append(-100)
            self.y.append(-100)

        # inicjalizacja
        self.x[1] = 1 * 30
        self.x[2] = 2 * 30

    def tick(self):

            # update poprzednich pozycji
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # update glowy
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
                if 1275 < self.x[0] <= 1285:
                    self.x[0] = 0 + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
                if 5 > self.x[0] >= -5:
                    self.x[0] = 1280 - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
                if 5 > self.y[0] >= -5:
                    self.y[0] = 720 - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
                if 715 < self.y[0] <= 725:
                    self.y[0] = 0 + self.step

    def draw(self, screen):
        for i in range(0, self.length):
            screen.blit(image, (self.x[i], self.y[i]))

    def collision(self):
        for i in range(10, self.length):
            if self.x[i] - 28 <= self.x[0] <= self.x[i] + 28:
                if self.y[i] - 29 <= self.y[0] <= self.y[i] + 29:
                    self.coll = True


class Bar:
    x = 0
    y = 0
    step = 30

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, screen):
        screen.blit(image2, (self.x, self.y))


class Block:
    x = 0
    y = 0
    step = 30

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, screen):
        screen.blit(image3, (self.x, self.y))


class Game(object):

    pause = False
    counter = 0
    start = True
    counter2 = 0

    def __init__(self):

        # inicjalizacja
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE)
        self.window = pygame.display.get_surface()
        pygame.display.set_caption('Snake')
        self.snake = Player(3)
        self.apple = Bar(10,10)
        self.block = Block(20,20)

        while True:

            # obsluga zdarzen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                else:
                    pass

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                    self.snake.direction = 0

            if keys[K_LEFT]:
                    self.snake.direction = 1

            if keys[K_UP]:
                    self.snake.direction = 2

            if keys[K_DOWN]:
                    self.snake.direction = 3

            if keys[K_SPACE]:
                if not self.pause:
                    self.pause = True

            # rysowanie
            self.screen.fill((0, 0, 0))
            self.window.blit(tlo, (0, 0))
            self.draw()
            pygame.display.flip()

    def eat(self):
        for i in range(0, self.snake.length):
            if self.snake.x[i] - 29 <= self.apple.x <= self.snake.x[i] + 29:
                if self.snake.y[i] - 40 <= self.apple.y <= self.snake.y[i] + 40:
                    self.apple.x = randint(1, 9) * 130
                    self.apple.y = randint(1, 9) * 70
                    self.snake.length = self.snake.length + 1
                    self.snake.step += 0.1
                    self.counter += 1
                    if self.counter % 3 == 0:
                        self.random()

    def spot(self):
        for i in range(0, self.snake.length):
            if self.snake.x[i] - 30 <= self.block.x <= self.snake.x[i] + 30:
                if self.snake.y[i] - 30 <= self.block.y <= self.snake.y[i] + 30:
                    self.snake.coll = True

    def random(self):
        self.block.x = randint(1, 9) * 130
        self.block.y = randint(1, 9) * 70
        while self.apple.x - 30 <= self.block.x <= self.apple.x + 30 or self.apple.y - 40 <= self.block.y <= self.apple.y + 40:
            self.block.x = randint(1, 9) * 130
            self.block.y = randint(1, 9) * 70

    def draw(self):
        font = pygame.font.SysFont(None, 40)
        font2 = pygame.font.SysFont(None, 80)
        if self.start:
            title = font2.render("Snake Game", True, (130, 30, 40))
            intro = font.render("press space to play", True, (170, 50, 80))
            self.screen.blit(intro, (465, 250))
            self.screen.blit(title, (420, 180))
        if self.pause:
            self.start = False
            self.snake.tick()
            self.eat()
            self.spot()
            if not self.snake.coll:
                self.snake.collision()
            if self.snake.coll:
                text = font2.render("Game Over", True, (130, 30, 40))
                self.screen.blit(text, (450, 180))
                self.counter2 += 1
            if self.counter2 == 40:
                exit(0)
            self.apple.draw(self.screen)
            self.block.draw(self.screen)
        self.snake.draw(self.screen)
        text = font.render("Score: " + str(self.counter), True, (0, 0, 0))
        self.screen.blit(text, (0, 0))


if __name__ == "__main__":
    Game()