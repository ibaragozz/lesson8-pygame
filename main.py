import pygame

pygame.init()

window_size = 800, 600
screen = pygame.display.set_mode((window_size))
pygame.display.set_caption("My Test Game")


running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()


pygame.quit()