import pygame
import math
from player import *
import os
import sys
pygame.init()
size = width, height = 900, 650
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen.fill("gray")
pygame.display.set_caption("Руины замка")
running = True
pygame.draw.circle(screen, "red", (x, y), 10)
logic = False

def l_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = l_image("bg1.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        screen.fill("gray")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if 900 > x + math.cos(vector) * 5 > 0:
                x += math.cos(vector) * 5
            if 650 > y + math.sin(vector) * 5 > 0:
                y += math.sin(vector) * 5
        if keys[pygame.K_s]:
            if 900 > x - math.cos(vector) * 5 > 0:
                x -= math.cos(vector) * 5
            if 650 > y - math.sin(vector) * 5 > 0:
                y -= math.sin(vector) * 5
                #проверка что персонаж на поле
        if keys[pygame.K_a]:
            vector -= 0.07
            if vector > 180:
                vector = -180
            elif vector < -180:
                vector = 180
        if keys[pygame.K_d]:
            vector += 0.07
            if vector > 180:
                vector = -180
            elif vector < -180:
                vector = 180
        all_sprites.draw(screen)
        pygame.draw.circle(screen, "red", (x, y), 10)
        #теперь рисуем линию из (координат шарика) в (координаты шарика+направления(vector)*на длину стороны квадрата)
        #если что, то линия - это диагональ квадрата c шириной и высотой длина взгляда
        pygame.draw.line(screen, "red", (x, y), (x + math.cos(vector) * dlina_vzglyada[0],
                                                 y + math.sin(vector) * dlina_vzglyada[1]))
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()