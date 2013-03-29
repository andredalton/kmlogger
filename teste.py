import sys, pygame
import os

# Initialise screen
x = 0
y = 0

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

pygame.init()

size = width, height = 64, 64
black = 0, 0, 0

screen = pygame.display.set_mode(size, pygame.NOFRAME)

ball = pygame.image.load("img/play.png")
ball = pygame.transform.scale(ball, (60, 60))

ballrect = (1, 1)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()