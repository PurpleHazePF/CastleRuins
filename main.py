import pygame
from player import player
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen.fill("gray")
pygame.display.set_caption("Руины замка")
running = True
pl = player()
pygame.draw.circle(screen, "red", (pl.x, pl.y), 10)
logic = False
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        screen.fill("gray")
        pl.movement()
        pygame.draw.circle(screen, "red", (pl.x, pl.y), 10)
    pygame.display.flip()
pygame.quit()