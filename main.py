import pygame
import math
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
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        screen.fill("gray")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            x += math.cos(vector) * 5
            y += math.sin(vector) * 5
        if keys[pygame.K_s]:
            x -= math.cos(vector) * 5
            y -= math.sin(vector) * 5
        if keys[pygame.K_a]:
            vector -= 0.1
            if vector > 180:
                vector = -180
            elif vector < -180:
                vector = 180
        if keys[pygame.K_d]:
            vector += 0.1
            if vector > 180:
                vector = -180
            elif vector < -180:
                vector = 180
        pygame.draw.circle(screen, "red", (x, y), 10)
        #теперь рисуем линию из (координат шарика) в (координаты шарика+направления(vector)*на длину стороны квадрата)
        #если что, то линия - это диагональ квадрата c шириной и высотой длина взгляда
        pygame.draw.line(screen, "red", (x, y), (x + math.cos(vector) * dlina_vzglyada[0],
                                                 y + math.sin(vector) * dlina_vzglyada[1]))
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()