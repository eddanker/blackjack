import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
FPS = 60
BG_COLOR = (0, 0, 0)

pygame.display.set_caption('CBC Blackjack!')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
timer = pygame.time.Clock()

run = True
while run: # basic game loop

    # run game at our framerate and fill screen with bg color
    timer.tick(FPS)
    screen.fill(BG_COLOR)

    # listen for basic events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()