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


class Stena(pygame.sprite.Sprite):  # для отрисовки стен
    def __init__(self, group, a, b):
        super().__init__(group)
        self.rect = pygame.Rect((0, 0, BLOCK_SIZE_X, BLOCK_SIZE_Y))
        self.rect.x = a
        self.rect.y = b
        pygame.draw.rect(screen, "blue", (self.rect.x, self.rect.y, BLOCK_SIZE_X, BLOCK_SIZE_Y))

    def update(self):
        pygame.draw.rect(screen, "blue", (self.rect.x, self.rect.y, BLOCK_SIZE_X, BLOCK_SIZE_Y))


class Raycast(pygame.sprite.Sprite):  # пока что не используется
    def __init__(self, group):
        super().__init__(group)
        self.nach_x = x + SIZE * 0.5
        self.nach_y = y + SIZE * 0.5
        self.kon_x = x + SIZE * 0.5 + math.cos(vector) * width
        self.kon_y = y + SIZE * 0.5 + math.sin(vector) * height
        self.rect = pygame.Rect((self.nach_x, self.nach_y, self.kon_x, self.kon_y))
        pygame.draw.line(screen, "red", (self.nach_x, self.nach_y), (self.kon_x, self.kon_y))

    def update(self):
        self.nach_x = x + SIZE * 0.5
        self.nach_y = y + SIZE * 0.5
        if pygame.sprite.spritecollideany(self, steny):
            pass


class Persona(pygame.sprite.Sprite):  # для перемещения и отрисовки персонажа
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect((0, 0, SIZE, SIZE))
        self.rect.x = x
        self.rect.y = y
        pygame.draw.circle(screen, 'red', (self.rect.x + SIZE * 0.5, self.rect.y + SIZE * 0.5), SIZE * 0.5)

    def update(self):
        self.rect.x = x
        self.rect.y = y
        pygame.draw.circle(screen, 'red', (self.rect.x + SIZE * 0.5, self.rect.y + SIZE * 0.5), SIZE * 0.5)


pygame.init()
size = width, height  # задаются в файле map, как и другие свойства карты
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Руины замка")
running = True

all_sprites = pygame.sprite.Group()
rays = pygame.sprite.Group()  # пока что не используется
steny = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
personazh = pygame.sprite.Group()
sprite.image = l_image("bg1.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)

vector = 0
for i, j in map_cord:
    Stena(steny, i, j)  # инициализируем стены
Persona(personazh)  # инициализируем персонажа
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.key.get_pressed()[pygame.K_w]:
        for _ in range(speed):  # для более плавного движения, вместо 5 + проверка, 5 раз по 1 и каждый раз проверка
            if width - SIZE + 1 > x + math.cos(vector) > 0:
                x += math.cos(vector)
                personazh.update()
                if pygame.sprite.groupcollide(steny, personazh, False,
                                              False):  # проверка на столкновение с препяnствием
                    x -= math.cos(vector)
                    personazh.update()
            if height - SIZE + 1 > y + math.sin(vector) > 0:
                y += math.sin(vector)
                personazh.update()
                if pygame.sprite.groupcollide(steny, personazh, False, False):
                    y -= math.sin(vector)
                    personazh.update()
    if pygame.key.get_pressed()[pygame.K_s]:
        for _ in range(speed):
            if width - SIZE + 1 > x - math.cos(vector) > 0:
                x -= math.cos(vector)
                personazh.update()
                if pygame.sprite.groupcollide(steny, personazh, False, False):
                    x += math.cos(vector)
                    personazh.update()
            if height - SIZE + 1 > y - math.sin(vector) > 0:
                y -= math.sin(vector)
                personazh.update()
                if pygame.sprite.groupcollide(steny, personazh, False, False):
                    y += math.sin(vector)
                    personazh.update()
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
    steny.update()
    personazh.update()
    # теперь рисуем линию из (координат шарика) в (координаты шарика+направления(vector)*на длину стороны квадрата)
    # если что, то линия - это диагональ квадрата c шириной и высотой длина взгляда
    pygame.draw.line(screen, "red", (x + SIZE * 0.5, y + SIZE * 0.5),
                     (x + SIZE * 0.5 + math.cos(vector) * dlina_vzglyada[0],
                      y + SIZE * 0.5 + math.sin(vector) * dlina_vzglyada[1]))
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
