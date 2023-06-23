import pygame
import time
import os
import random
import neat

pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800
FONT = pygame.font.SysFont("comicsas", 60)
SMALL_FONT = pygame.font.SysFont("comicsas", 24)
MED_FONT = pygame.font.SysFont("comicsas", 40)
PAUSED = False

GEN = 0
BEST_SCORE = 0
SPEED = 30
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

pygame.display.set_caption("W3ndig0 Flappy Bird AI Trainer")
pygame.display.set_icon(BIRD_IMGS[0])


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
    VEL = SPEED

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMGS[0], False, True)
        self.PIPE_BOTTOM = PIPE_IMGS[0]

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        birdMask = bird.getMask()
        topMask = pygame.mask.from_surface(self.PIPE_TOP)
        bottomMask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        topOffset = (self.x - bird.x, self.top - round(bird.y))
        bottomOffset = (self.x - bird.x, self.bottom - round(bird.y))

        topPoint = birdMask.overlap(topMask, topOffset)
        bottomPoint = birdMask.overlap(bottomMask, bottomOffset)

        if topPoint or bottomPoint:
            return True

        return False


class Base:
    VEL = SPEED
    WIDTH = BASE_IMGS[0].get_width()
    IMG = BASE_IMGS[0]

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.WIDTH + self.x2

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.WIDTH + self.x1

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def drawWindow(win, birds, pipes, base, score, gen, BEST_SCORE):
    win.blit(BG_IMGS[0], (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        bird.draw(win)

    base.draw(win)
    text = SMALL_FONT.render("W3ndig0", 1, (0, 0, 0))
    scoreText = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    genText = FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    bestScoreText = MED_FONT.render(
        "Best Score: " + str(BEST_SCORE), 1, (255, 255, 255)
    )

    win.blit(scoreText, (WIN_WIDTH - 10 - scoreText.get_width(), 5))
    win.blit(genText, (10, 10))
    win.blit(bestScoreText, (10, 50))

    win.blit(text, (WIN_WIDTH - 5 - text.get_width(), WIN_HEIGHT - text.get_height()))

    if PAUSED:
        pause_text = FONT.render("PAUSED", True, (255, 255, 255))
        resume_text = SMALL_FONT.render("Press ESC to resume", True, (255, 255, 255))
        pause_width = pause_text.get_width()
        pause_height = pause_text.get_height()

        win.blit(
            pause_text,
            (WIN_WIDTH // 2 - pause_width // 2, WIN_HEIGHT // 2 - pause_height // 2),
        )
        win.blit(
            resume_text,
            (
                WIN_WIDTH // 2 - resume_text.get_width() // 2,
                WIN_HEIGHT // 2 + pause_height,
            ),
        )

    pygame.display.update()


def evalGenomes(genomes, config):
    global GEN
    global BEST_SCORE
    global PAUSED
    GEN += 1
    nets = []
    genom = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        genom.append(g)

    pipes = [Pipe(WIN_WIDTH + 100)]
    base = Base(730)
    score = 0
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    jump_flag = False
    gameOver = False
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    PAUSED = not PAUSED

        if PAUSED:
            continue

        pipeInd = 0
        if len(birds) > 0:
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                pipeInd = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            genom[x].fitness += 0.1
            output = nets[birds.index(bird)].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipeInd].height),
                    abs(bird.y - pipes[pipeInd].bottom),
                )
            )

            if output[0] > 0.5:
                bird.jump()

        addPipe = False
        rem = []
        bird.move()

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if not jump_flag and not gameOver:
        #         bird.jump()
        #         jump_flag = True

        # if event.type == pygame.MOUSEBUTTONUP:
        #     jump_flag = False

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    gameOver = True
                    genom[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    genom.pop(x)
                    if BEST_SCORE < score:
                        BEST_SCORE = score

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    addPipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

                # if not gameOver:
            pipe.move()
            base.move()

        if addPipe:
            score += 1
            for g in genom:
                g.fitness += 10
            pipes.append(Pipe(WIN_WIDTH + 100))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                gameOver = True
                genom[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                genom.pop(x)

        drawWindow(win, birds, pipes, base, score, GEN, BEST_SCORE)


def run(configPath):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        configPath,
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(evalGenomes, 1000)


def play():
    localDir = os.path.dirname(__file__)
    configPath = os.path.join(localDir, "config-feedforward.txt")
    run(configPath)
