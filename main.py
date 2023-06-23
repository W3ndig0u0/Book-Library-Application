import pygame
import time
import os
import random
import neat

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [
    pygame.transform.scale2x(
        pygame.image.load(os.path.join("imgs", "bird" + str(x) + ".png"))
    )
    for x in range(1, 4)
]


PIPE_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
]
BASE_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
]
BG_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))]


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tickCount = 0
        self.vel = 0
        self.height = self.y
        self.imgCount = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10
        self.tickCount = 0
        self.height = self.y

    def move(self):
        self.tickCount += 1

        # ?Upp eller ned
        d = self.vel * self.tickCount + 1.5 * self.tickCount**2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        self.y += d

        # ?sänk ej under hopp
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.imgCount += 1

        # TODO: Improve the code hehe
        if self.imgCount < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.imgCount < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.imgCount < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.imgCount < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.imgCount == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.imgCount = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.imgCount = self.ANIMATION_TIME * 2

        rotatedImage = pygame.transform.rotate(self.img, self.tilt)
        newRect = rotatedImage.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotatedImage, newRect.topleft)

    def getMask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMGS[0], false, True)
        self.PIPE_BOTTOm = PIPE_IMGS[0]

        self.passed = false
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOm, (self.x, self.bottom))


def drawWindow(win, bird):
    win.blit(BG_IMGS[0], (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        drawWindow(win, bird)

    pygame.quit()
    quit()


main()
