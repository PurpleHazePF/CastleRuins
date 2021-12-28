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
        # pygame.draw.rect(screen, "blue", (self.rect.x, self.rect.y, BLOCK_SIZE_X, BLOCK_SIZE_Y))

    def update(self):
        pygame.draw.rect(screen, "blue", (self.rect.x, self.rect.y, BLOCK_SIZE_X, BLOCK_SIZE_Y))


class Raycast(pygame.sprite.Sprite):
    def __init__(self, group, r):
        super().__init__(group)
        self.ray = r
        self.nach_x = x + SIZE * 0.5
        self.nach_y = y + SIZE * 0.5

    def update(self):
        self.nach_x = x + SIZE * 0.5
        self.nach_y = y + SIZE * 0.5
        cur_angle = vector - OBZOR / 2 + DELTA_ANGLE * self.ray  # откладывем нужный угол
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        x0 = self.nach_x // BLOCK_SIZE_X * BLOCK_SIZE_X
        y0 = self.nach_y // BLOCK_SIZE_Y * BLOCK_SIZE_Y

        if cos_a >= 0:  # находим блюжайшую вертикаль в зависимости от знака угла
            m = x0 + BLOCK_SIZE_X
            dm = 1  # устанавливаем шаг между вертикалями
        else:
            m = x0
            dm = -1

        for i in range(0, width, int(BLOCK_SIZE_X)):  # проходим по вертикалям пока не найдем пересечение со стеной
            if cos_a != 0:
                depth_v = (m - self.nach_x) / cos_a
            else:
                depth_v = m
            k = self.nach_y + depth_v * sin_a  # находим координаты пересечения с вертикалью
            if ((m + dm) // BLOCK_SIZE_X * BLOCK_SIZE_X, k // BLOCK_SIZE_Y * BLOCK_SIZE_Y) in map_cord:
                break  # проверка на пересечение со стеной
            m += dm * BLOCK_SIZE_X  # переходим к седующей вертикали

        if sin_a >= 0:  # находим блюжайшую горизонталь в зависимости от знака угла
            k = y0 + BLOCK_SIZE_Y
            dk = 1  # устанавливаем шаг между горизонталями
        else:
            k = y0
            dk = -1

        for j in range(0, height, int(BLOCK_SIZE_Y)):  # проходим по горизонталям пока не найдем пересечение со стеной
            if sin_a != 0:
                depth_h = (k - self.nach_y) / sin_a
            else:
                depth_h = k
            m = self.nach_x + depth_h * cos_a  # находим координаты пересечения с горизонталью
            if (m // BLOCK_SIZE_X * BLOCK_SIZE_X, (k + dk) // BLOCK_SIZE_Y * BLOCK_SIZE_Y) in map_cord:
                break  # проверка на пересечение со стеной
            k += dk * BLOCK_SIZE_Y  # переходим к следующей горизонтали

        if depth_v < depth_h:  # выбираем из горизонтали и вертикали ближайшую к нам
            depth = depth_v
        else:
            depth = depth_h

        depth *= math.cos(vector - cur_angle)  # убираем эффект выпуклости стен
        if depth != 0:
            p_h = PROJ_COEFF / depth  # получаем высоту проекции
        else:
            p_h = 0
        pygame.draw.rect(screen, 'ORANGE',
                         (self.ray * SCALE, height // 2 - p_h // 2, SCALE, p_h))  # отображаем стену


class Persona(pygame.sprite.Sprite):  # для перемещения и отрисовки персонажа
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect((0, 0, SIZE, SIZE))
        self.rect.x = x
        self.rect.y = y
        # pygame.draw.circle(screen, 'red', (self.rect.x + SIZE * 0.5, self.rect.y + SIZE * 0.5), SIZE * 0.5)

    def update(self):
        self.rect.x = x
        self.rect.y = y
        # pygame.draw.circle(screen, 'red', (self.rect.x + SIZE * 0.5, self.rect.y + SIZE * 0.5), SIZE * 0.5)


pygame.init()
size = width, height  # задаются в файле map, как и другие свойства карты
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Руины замка")
running = True

all_sprites = pygame.sprite.Group()
rays = pygame.sprite.Group()
steny = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
personazh = pygame.sprite.Group()
sprite.image = l_image("bg1.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)

vector = 0

for i in range(NUM_RAYS):  # создаем лучи
    Raycast(rays, i)

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
                                                  False):  # проверка на столкновение с препядствием
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
        screen.fill('black')
        pygame.draw.rect(screen, (0, 0, 230), (0, 0, width, height / 2))  # потолок
        pygame.draw.rect(screen, (50, 50, 50), (0, height / 2, width, height / 2))  # пол
        personazh.update()
        rays.update()
    # теперь рисуем линию из (координат шарика) в (координаты шарика+направления(vector)*на длину стороны квадрата)
    # если что, то линия - это диагональ квадрата c шириной и высотой длина взгляда
    # pygame.draw.line(screen, "red", (x + SIZE * 0.5, y + SIZE * 0.5),
    #                 (x + SIZE * 0.5 + math.cos(vector) * dlina_vzglyada[0],
    #                  y + SIZE * 0.5 + math.sin(vector) * dlina_vzglyada[1]))
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
