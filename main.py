import pygame
from player import *
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen.fill("gray")
pygame.display.set_caption("Руины замка")
running = True
pygame.draw.circle(screen, "red", (x, y), 10)
logic = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        screen.fill("gray")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            x += 0
            y += -speed
        if keys[pygame.K_s]:
            x += 0
            y += speed
        if keys[pygame.K_a]:
            x += -speed
            y += 0
        if keys[pygame.K_d]:
            x += speed
            y += 0
        pygame.draw.circle(screen, "red", (x, y), 10)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()