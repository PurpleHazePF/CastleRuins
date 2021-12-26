import math
import os
import pygame
import sys

from map import *
from player import *


def l_image(name):
    fullname = os.path.join('assets', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def check(coords, sizex, sizey, x2, y2, size2):
    for a, b in coords:  # проверка на пересечение прямоугольника игрока и прямоугольника препятствия
        a, b = a + 1, b + 1  # тк отсчет от нуля,то добавляю потерянное,иначе будет расстояниемежду препятствием игероем
        if ((a <= x2 <= a + sizex and b <= y2 <= b + sizey) or
                (a <= x2 + size2 <= a + sizex and b <= y2 + size2 <= b + sizey) or
                (a <= x2 + size2 <= a + sizex and b <= y2 <= b + sizey) or
                (a <= x2 <= a + sizex and b <= y2 + size2 <= b + sizey)):
            return True
    return False


pygame.init()
size = width, height  # задаются в файле map, как и другие свойства карты
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Руины замка")
running = True
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = l_image("bg1.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
vector = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.key.get_pressed()[pygame.K_w]:
        for _ in range(speed):  # для более плавного движения, вместо 5 + проверка, 5 раз по 1 и каждый раз проверка
            if width - SIZE + 1 > x + math.cos(vector) > 0:
                x += math.cos(vector)
                if check(map_cord, BLOCK_SIZE_X, BLOCK_SIZE_Y, x, y, SIZE):  # проверка на столкновение с препядствием
                    x -= math.cos(vector)
            if height - SIZE + 1 > y + math.sin(vector) > 0:
                y += math.sin(vector)
                if check(map_cord, BLOCK_SIZE_X, BLOCK_SIZE_Y, x, y, SIZE):
                    y -= math.sin(vector)
    if pygame.key.get_pressed()[pygame.K_s]:
        for _ in range(speed):
            if width - SIZE + 1 > x - math.cos(vector) > 0:
                x -= math.cos(vector)
                if check(map_cord, BLOCK_SIZE_X, BLOCK_SIZE_Y, x, y, SIZE):
                    x += math.cos(vector)
            if height - SIZE + 1 > y - math.sin(vector) > 0:
                y -= math.sin(vector)
                if check(map_cord, BLOCK_SIZE_X, BLOCK_SIZE_Y, x, y, SIZE):
                    y += math.sin(vector)
    if pygame.key.get_pressed()[pygame.K_a]:
        vector -= 0.07
        if vector > 180:
            vector = -180
        elif vector < -180:
            vector = 180
    if pygame.key.get_pressed()[pygame.K_d]:
        vector += 0.07
        if vector > 180:
            vector = -180
        elif vector < -180:
            vector = 180
    all_sprites.draw(screen)
    pygame.draw.circle(screen, 'red', (x + SIZE * 0.5, y + SIZE * 0.5), SIZE * 0.5)
    # теперь рисуем линию из (координат шарика) в (координаты шарика+направления(vector)*на длину стороны квадрата)
    # если что, то линия - это диагональ квадрата c шириной и высотой длина взгляда
    pygame.draw.line(screen, "red", (x + SIZE * 0.5, y + SIZE * 0.5),
                     (x + SIZE * 0.5 + math.cos(vector) * dlina_vzglyada[0],
                      y + SIZE * 0.5 + math.sin(vector) * dlina_vzglyada[1]))
    for i, j in map_cord:  # отрисовка препятствий
        pygame.draw.rect(screen, (8, 75, 108), (i, j, BLOCK_SIZE_X, BLOCK_SIZE_Y))
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
