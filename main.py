import math
import os
import pygame
import sys
from pygame import Color
from random import randint
from datetime import datetime
import time

from map import *
from player import *


def time_convert(n):
    if n // 60 >= 1:
        if n // 3600 >= 1:
            return f'{n // 3600} ч {(n % 3600) // 60} мин {round((n % 3600) % 60)} сек'
        return f'{n // 60} мин {round(n % 60)} сек'
    return f'{round(n % 60)} сек'


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
        self.rect = pygame.Rect((a, b, BLOCK_SIZE_X, BLOCK_SIZE_Y))

    def update(self):
        pygame.draw.rect(screen, "black",
                         (self.rect.x * 0.1, self.rect.y * 0.1, BLOCK_SIZE_X * 0.1 + 1, BLOCK_SIZE_Y * 0.1 + 1))


class Raycast(pygame.sprite.Sprite):
    def __init__(self, group, r):
        super().__init__(group)
        self.ray = r
        self.nach_x = x + SIZE * 0.5
        self.nach_y = y + SIZE * 0.5

    def update(self, cord, spisok_slice, BLOCK_SIZE_X, BLOCK_SIZE_Y, x, y):
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

        for _ in range(0, width, int(BLOCK_SIZE_X)):  # проходим по вертикалям пока не найдем пересечение со стеной
            if cos_a != 0:
                depth_v = (m - self.nach_x) / cos_a
            else:
                depth_v = m
            k_vert = self.nach_y + depth_v * sin_a  # находим координаты пересечения с вертикалью
            if ((m + dm) // BLOCK_SIZE_X * BLOCK_SIZE_X, k_vert // BLOCK_SIZE_Y * BLOCK_SIZE_Y) in cord:
                break  # проверка на пересечение со стеной
            m += dm * BLOCK_SIZE_X  # переходим к седующей вертикали

        if sin_a >= 0:  # находим блюжайшую горизонталь в зависимости от знака угла
            k = y0 + BLOCK_SIZE_Y
            dk = 1  # устанавливаем шаг между горизонталями
        else:
            k = y0
            dk = -1

        for _ in range(0, height, int(BLOCK_SIZE_Y)):  # проходим по горизонталям пока не найдем пересечение со стеной
            if sin_a != 0:
                depth_h = (k - self.nach_y) / sin_a
            else:
                depth_h = k
            m_gorizont = self.nach_x + depth_h * cos_a  # находим координаты пересечения с горизонталью
            if (m_gorizont // BLOCK_SIZE_X * BLOCK_SIZE_X, (k + dk) // BLOCK_SIZE_Y * BLOCK_SIZE_Y) in cord:
                break  # проверка на пересечение со стеной
            k += dk * BLOCK_SIZE_Y  # переходим к следующей горизонтали
        if depth_v < depth_h:  # выбираем из горизонтали и вертикали ближайшую к нам
            depth = depth_v
            smeshenie = k_vert % BLOCK_SIZE_Y / BLOCK_SIZE_Y  # вычисляем долю смещения по вертикали
            xx, yy = m, k_vert
        else:
            depth = depth_h
            smeshenie = m_gorizont % BLOCK_SIZE_X / BLOCK_SIZE_X  # вычисляем долю смещения по горизонтали
            xx, yy = m_gorizont, k
        if 0 < xx < dlina_karty and 0 < yy < shirina_karty:
            depth *= math.cos(vector - cur_angle)  # убираем эффект выпуклости стен
            if depth != 0:
                p_h = PROJ_COEFF / depth  # получаем высоту проекции
            else:
                p_h = 0
            if p_h <= 360:  # вычисляем яркость в зависимости от дальность
                brightness = p_h
            else:
                brightness = 360
            vozvrash(smeshenie, self.ray, p_h, brightness, xx, yy, depth, spisok_slice)


class Raycastbullet(pygame.sprite.Sprite):
    def __init__(self, group, x, y, vect):
        super().__init__(group)
        self.rect = pygame.Rect((x + SIZE * 0.5 + math.cos(vect) * 3, y + SIZE * 0.5 + math.sin(vect) * 3, 10, 10))
        self.vect = vect
        vystrel_bullet.play()
        pygame.sprite.groupcollide(rays_bullet, steny, True, False)

    def update(self):
        self.rect.x = self.rect.x + speed * 2 * math.cos(self.vect)
        self.rect.y = self.rect.y + speed * 2 * math.sin(self.vect)
        pygame.draw.circle(screen, 'orange', (self.rect.x * 0.1, self.rect.y * 0.1), 1)
        x1 = x + SIZE * 0.5
        y1 = y + SIZE * 0.5
        sin_a = math.sin(vector)
        cos_a = math.cos(vector)
        x2, y2 = x1 + 2000 * cos_a, y1 + 2000 * sin_a  # откладываем прямую вперёд
        sin_a_2 = math.sin(vector + OBZOR / 2 + 0.25)
        cos_a_2 = math.cos(vector + OBZOR / 2 + 0.25)
        x3, y3 = x1 + 2000 * cos_a_2, y1 + 2000 * sin_a_2  # откладываем прямую вправо
        sin_a_3 = math.sin(vector - OBZOR / 2 - 0.25)
        cos_a_3 = math.cos(vector - OBZOR / 2 - 0.25)
        x4, y4 = x1 + 2000 * cos_a_3, y1 + 2000 * sin_a_3  # откладываем прямую влево
        ugol = treug(self.rect.x, self.rect.y, x1, y1, x2, y2, x3, y3)  # угол вправо, если есть
        ugol1 = treug(self.rect.x, self.rect.y, x1, y1, x2, y2, x4, y4)  # угол влево, если есть
        if ugol is None:
            if ugol1 is not None:
                ugol = ugol1
        if ugol is not None:
            if ugol < - 1:  # иногда вылетают странные значения, которые убираем с помощью периода арктангенса
                ugol = ugol % (math.pi * 2)
            elif ugol > 1:
                ugol = -((math.pi * 2) % ugol)
            ugol2 = OBZOR / 2 + ugol  # угол спрайта в нашем обзоре
            shirina = (ugol2 / OBZOR) * width  # дальность спрайта от левого угла монитора
            if math.cos(vector + ugol) != 0:  # взято из стен
                depth_v = (self.rect.x - x1) / math.cos(vector + ugol)
            else:
                depth_v = self.rect.x
            if math.sin(vector + ugol) != 0:
                depth_h = (self.rect.y - y1) / math.sin(vector + ugol)
            else:
                depth_h = self.rect.y
            if depth_v < depth_h:
                depth = depth_v
            else:
                depth = depth_h
            depth *= math.cos(ugol)
            if depth != 0:
                p_h = PROJ_COEFF / depth
            else:
                p_h = 0
            dlina = razmer_image_bullet[1] / razmer_image_bullet[0] * (p_h // 10)  # длина проекции спрайта
            ray_2 = int((shirina - dlina / 2) / SCALE)  # луч падающий на правую левую сторону проекции
            ray_3 = int((shirina + dlina / 2) / SCALE)  # луч падающий на правую правую сторону проекции
            ray_razn = ray_3 - ray_2  # количество лучей, заимаемых проекцией
            zhuzhanie = randint(0, 5)
            for i in range(ray_razn):
                if 0 < ray_2 + i < NUM_RAYS:
                    vozvrash(i / ray_razn, ray_2 + i, p_h, 'bullet', zhuzhanie, vozvrat_prep)


class Raycast_hero_bullet(pygame.sprite.Sprite):
    def __init__(self, group, x, y, vect):
        super().__init__(group)
        self.rect = pygame.Rect((x + SIZE * 0.5 + math.cos(vect) * 3, y + SIZE * 0.5 + math.sin(vect) * 3, 10, 10))
        self.vect = vect
        vystrel_bullet.play()
        pygame.sprite.groupcollide(rays_hero_bullet, steny, True, False)

    def update(self):
        self.rect.x = self.rect.x + speed * 2 * math.cos(self.vect)
        self.rect.y = self.rect.y + speed * 2 * math.sin(self.vect)
        pygame.draw.circle(screen, 'orange', (self.rect.x * 0.1, self.rect.y * 0.1), 1)
        x1 = x + SIZE * 0.5
        y1 = y + SIZE * 0.5
        sin_a = math.sin(vector)
        cos_a = math.cos(vector)
        x2, y2 = x1 + 2000 * cos_a, y1 + 2000 * sin_a  # откладываем прямую вперёд
        sin_a_2 = math.sin(vector + OBZOR / 2 + 0.25)
        cos_a_2 = math.cos(vector + OBZOR / 2 + 0.25)
        x3, y3 = x1 + 2000 * cos_a_2, y1 + 2000 * sin_a_2  # откладываем прямую вправо
        sin_a_3 = math.sin(vector - OBZOR / 2 - 0.25)
        cos_a_3 = math.cos(vector - OBZOR / 2 - 0.25)
        x4, y4 = x1 + 2000 * cos_a_3, y1 + 2000 * sin_a_3  # откладываем прямую влево
        ugol = treug(self.rect.x, self.rect.y, x1, y1, x2, y2, x3, y3)  # угол вправо, если есть
        ugol1 = treug(self.rect.x, self.rect.y, x1, y1, x2, y2, x4, y4)  # угол влево, если есть
        if ugol is None:
            if ugol1 is not None:
                ugol = ugol1
        if ugol is not None:
            if ugol < - 1:  # иногда вылетают странные значения, которые убираем с помощью периода арктангенса
                ugol = ugol % (math.pi * 2)
            elif ugol > 1:
                ugol = -((math.pi * 2) % ugol)
            ugol2 = OBZOR / 2 + ugol  # угол спрайта в нашем обзоре
            shirina = (ugol2 / OBZOR) * width  # дальность спрайта от левого угла монитора
            if math.cos(vector + ugol) != 0:  # взято из стен
                depth_v = (self.rect.x - x1) / math.cos(vector + ugol)
            else:
                depth_v = self.rect.x
            if math.sin(vector + ugol) != 0:
                depth_h = (self.rect.y - y1) / math.sin(vector + ugol)
            else:
                depth_h = self.rect.y
            if depth_v < depth_h:
                depth = depth_v
            else:
                depth = depth_h
            depth *= math.cos(ugol)
            if depth != 0:
                p_h = PROJ_COEFF / depth
            else:
                p_h = 0
            dlina = razmer_image_bullet[1] / razmer_image_bullet[0] * (p_h // 10)  # длина проекции спрайта
            ray_2 = int((shirina - dlina / 2) / SCALE)  # луч падающий на правую левую сторону проекции
            ray_3 = int((shirina + dlina / 2) / SCALE)  # луч падающий на правую правую сторону проекции
            ray_razn = ray_3 - ray_2  # количество лучей, заимаемых проекцией
            zhuzhanie = randint(0, 5)
            for i in range(ray_razn):
                if 0 < ray_2 + i < NUM_RAYS:
                    vozvrash(i / ray_razn, ray_2 + i, p_h, 'hero_bullet', zhuzhanie, vozvrat_prep)


class Raycastprep(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.xx = x
        self.yy = y

    def update(self, vector, x, y):
        x1 = x + SIZE * 0.5
        y1 = y + SIZE * 0.5
        sin_a = math.sin(vector)
        cos_a = math.cos(vector)
        x2, y2 = x1 + 2000 * cos_a, y1 + 2000 * sin_a  # откладываем прямую вперёд
        sin_a_2 = math.sin(vector + OBZOR / 2 + 0.25)
        cos_a_2 = math.cos(vector + OBZOR / 2 + 0.25)
        x3, y3 = x1 + 2000 * cos_a_2, y1 + 2000 * sin_a_2  # откладываем прямую вправо
        sin_a_3 = math.sin(vector - OBZOR / 2 - 0.25)
        cos_a_3 = math.cos(vector - OBZOR / 2 - 0.25)
        x4, y4 = x1 + 2000 * cos_a_3, y1 + 2000 * sin_a_3  # откладываем прямую влево
        ugol = treug(self.xx, self.yy, x1, y1, x2, y2, x3, y3)  # угол вправо, если есть
        ugol1 = treug(self.xx, self.yy, x1, y1, x2, y2, x4, y4)  # угол влево, если есть
        if ugol is None:
            if ugol1 is not None:
                ugol = ugol1
        if ugol is not None:
            if ugol < - 1:  # иногда вылетают странные значения, которые убираем с помощью периода арктангенса
                ugol = ugol % (math.pi * 2)
            elif ugol > 1:
                ugol = -((math.pi * 2) % ugol)
            ugol2 = OBZOR / 2 + ugol  # угол спрайта в нашем обзоре
            shirina = (ugol2 / OBZOR) * width  # дальность спрайта от левого угла монитора
            if math.cos(vector + ugol) != 0:  # взято из стен
                depth_v = (self.xx - x1) / math.cos(vector + ugol)
            else:
                depth_v = self.xx
            if math.sin(vector + ugol) != 0:
                depth_h = (self.yy - y1) / math.sin(vector + ugol)
            else:
                depth_h = self.yy
            if depth_v < depth_h:
                depth = depth_v
            else:
                depth = depth_h
            depth *= math.cos(ugol)
            if depth != 0:
                p_h = PROJ_COEFF / depth
            else:
                p_h = 0
            dlina = razmer_image_vase[1] / razmer_image_vase[0] * (p_h // 2)  # длина проекции спрайта
            ray_2 = int((shirina - dlina / 2) / SCALE)  # луч падающий на правую левую сторону проекции
            ray_3 = int((shirina + dlina / 2) / SCALE)  # луч падающий на правую правую сторону проекции
            ray_razn = ray_3 - ray_2  # количество лучей, заимаемых проекцией
            for i in range(ray_razn):
                if 0 < ray_2 + i < NUM_RAYS:
                    vozvrash(i / ray_razn, ray_2 + i, p_h, 'prep', 0, vozvrat_prep)


class Raycastenemy(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.rect = pygame.Rect((x, y, SIZE * 3, SIZE * 3))

    def update(self, vector, x0, y0):
        if ((self.rect.x - x) ** 2 + (self.rect.y - y) ** 2) ** 0.5 > BLOCK_SIZE_X * (
                2 ** 0.5):  # враг двигается если расстояние от него до героя меньше диагонали квадрата стены
            dx = self.rect.x - x
            dy = self.rect.y - y
            if dx > 0:
                self.rect.x -= 1
                if (self.rect.x // BLOCK_SIZE_X * BLOCK_SIZE_X, self.rect.y // BLOCK_SIZE_Y * BLOCK_SIZE_Y) in map_cord:
                    self.rect.x += 1
            else:
                self.rect.x += 1
                if (self.rect.x // BLOCK_SIZE_X * BLOCK_SIZE_X, self.rect.y // BLOCK_SIZE_Y * BLOCK_SIZE_Y) in map_cord:
                    self.rect.x -= 1
            if dy > 0:
                self.rect.y -= 1
                if (self.rect.x // BLOCK_SIZE_X * BLOCK_SIZE_X, self.rect.y // BLOCK_SIZE_Y * BLOCK_SIZE_Y) in map_cord:
                    self.rect.y += 1
            else:
                self.rect.y += 1
                if (self.rect.x // BLOCK_SIZE_X * BLOCK_SIZE_X, self.rect.y // BLOCK_SIZE_Y * BLOCK_SIZE_Y) in map_cord:
                    self.rect.y -= 1
        pygame.draw.circle(screen, 'red', (self.rect.x * 0.1, self.rect.y * 0.1), SIZE * 0.5)
        x1 = x0 + SIZE * 0.5
        y1 = y0 + SIZE * 0.5
        sin_a = math.sin(vector)
        cos_a = math.cos(vector)
        x2, y2 = x1 + 2000 * cos_a, y1 + 2000 * sin_a  # откладываем прямую вперёд
        sin_a_2 = math.sin(vector + OBZOR / 2 + 0.25)
        cos_a_2 = math.cos(vector + OBZOR / 2 + 0.25)
        x3, y3 = x1 + 2000 * cos_a_2, y1 + 2000 * sin_a_2  # откладываем прямую вправо
        sin_a_3 = math.sin(vector - OBZOR / 2 - 0.25)
        cos_a_3 = math.cos(vector - OBZOR / 2 - 0.25)
        x4, y4 = x1 + 2000 * cos_a_3, y1 + 2000 * sin_a_3  # откладываем прямую влево
        ugol = treug(self.rect.x, self.rect.y, x1, y1, x2, y2, x3, y3)  # угол вправо, если есть
        ugol1 = treug(self.rect.x, self.rect.y, x1, y1, x2, y2, x4, y4)  # угол влево, если есть
        if num_image % 4 == 2 or num_image % 4 == 3:
            self.vystrel()
        if ugol is None:
            if ugol1 is not None:
                ugol = ugol1
        if ugol is not None:
            if ugol < - 1:  # иногда вылетают странные значения, которые убираем с помощью периода арктангенса
                ugol = ugol % (math.pi * 2)
            elif ugol > 1:
                ugol = -((math.pi * 2) % ugol)
            ugol2 = OBZOR / 2 + ugol  # угол спрайта в нашем обзоре
            shirina = (ugol2 / OBZOR) * width  # дальность спрайта от левого угла монитора
            if math.cos(vector + ugol) != 0:  # взято из стен
                depth_v = (self.rect.x - x1) / math.cos(vector + ugol)
            else:
                depth_v = self.rect.x
            if math.sin(vector + ugol) != 0:
                depth_h = (self.rect.y - y1) / math.sin(vector + ugol)
            else:
                depth_h = self.rect.y
            if depth_v < depth_h:
                depth = depth_v
            else:
                depth = depth_h
            depth *= math.cos(ugol)
            if depth != 0:
                p_h = PROJ_COEFF / depth
            else:
                p_h = 0
            dlina = soldiers_razmer[num_image % 4][1] / soldiers_razmer[num_image % 4][0] * (
                    p_h // 2)  # длина проекции спрайта
            ray_2 = int((shirina - dlina / 2) / SCALE)  # луч падающий на правую левую сторону проекции
            ray_3 = int((shirina + dlina / 2) / SCALE)  # луч падающий на правую правую сторону проекции
            ray_razn = ray_3 - ray_2  # количество лучей, заимаемых проекцией
            for i in range(ray_razn):
                if 0 < ray_2 + i < NUM_RAYS:
                    vozvrash(i / ray_razn, ray_2 + i, p_h, 'enemy', 0, vozvrat_prep)

    def vystrel(self):
        ugol = math.atan2(y - self.rect.y, x - self.rect.x)
        Raycastbullet(rays_bullet, self.rect.x + math.cos(ugol) * 5, self.rect.y + math.sin(ugol) * 5, ugol)


class Raycastpet(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.xx = x
        self.yy = y
        self.vect = 0

    def update(self, vector, x, y):
        self.vect += 0.01
        run = True
        while run:
            for i in range(50, -1, -1):
                xxx = x + i * math.cos(self.vect)
                yyy = y + i * math.sin(self.vect)
                if (xxx // BLOCK_SIZE_X * BLOCK_SIZE_X, yyy // BLOCK_SIZE_Y * BLOCK_SIZE_Y) not in map_cord:
                    self.xx = xxx
                    self.yy = yyy
                    run = False
                    break
        x1 = x + SIZE * 0.5
        y1 = y + SIZE * 0.5
        sin_a = math.sin(vector)
        cos_a = math.cos(vector)
        x2, y2 = x1 + 2000 * cos_a, y1 + 2000 * sin_a  # откладываем прямую вперёд
        sin_a_2 = math.sin(vector + OBZOR / 2 + 0.25)
        cos_a_2 = math.cos(vector + OBZOR / 2 + 0.25)
        x3, y3 = x1 + 2000 * cos_a_2, y1 + 2000 * sin_a_2  # откладываем прямую вправо
        sin_a_3 = math.sin(vector - OBZOR / 2 - 0.25)
        cos_a_3 = math.cos(vector - OBZOR / 2 - 0.25)
        x4, y4 = x1 + 2000 * cos_a_3, y1 + 2000 * sin_a_3  # откладываем прямую влево
        ugol = treug(self.xx, self.yy, x1, y1, x2, y2, x3, y3)  # угол вправо, если есть
        ugol1 = treug(self.xx, self.yy, x1, y1, x2, y2, x4, y4)  # угол влево, если есть
        if ugol is None:
            if ugol1 is not None:
                ugol = ugol1
        if ugol is not None:
            if ugol < - 1:  # иногда вылетают странные значения, которые убираем с помощью периода арктангенса
                ugol = ugol % (math.pi * 2)
            elif ugol > 1:
                ugol = -((math.pi * 2) % ugol)
            ugol2 = OBZOR / 2 + ugol  # угол спрайта в нашем обзоре
            shirina = (ugol2 / OBZOR) * width  # дальность спрайта от левого угла монитора
            if math.cos(vector + ugol) != 0:  # взято из стен
                depth_v = (self.xx - x1) / math.cos(vector + ugol)
            else:
                depth_v = self.xx
            if math.sin(vector + ugol) != 0:
                depth_h = (self.yy - y1) / math.sin(vector + ugol)
            else:
                depth_h = self.yy
            if depth_v < depth_h:
                depth = depth_v
            else:
                depth = depth_h
            depth *= math.cos(ugol)
            if depth != 0:
                p_h = PROJ_COEFF / depth
            else:
                p_h = 0
            dlina = razmer_image_muha[1] / razmer_image_muha[0] * (p_h // 10)  # длина проекции спрайта
            ray_2 = int((shirina - dlina / 2) / SCALE)  # луч падающий на правую левую сторону проекции
            ray_3 = int((shirina + dlina / 2) / SCALE)  # луч падающий на правую правую сторону проекции
            ray_razn = ray_3 - ray_2  # количество лучей, заимаемых проекцией
            zhuzhanie = randint(0, 5)
            for i in range(ray_razn):
                if 0 < ray_2 + i < NUM_RAYS:
                    vozvrash(i / ray_razn, ray_2 + i, p_h, 'pet', zhuzhanie, vozvrat_prep)


def treug(x0, y0, x1, y1, x2, y2, x3, y3):  # находится ли спрайт между в треугольнике составленном из точек
    if ((x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0) >= 0 and (x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0) >= 0 and
            (x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0) >= 0):
        return math.atan2(y0 - y1, x0 - x1) - math.atan2(y2 - y1, x2 - x1)
    elif ((x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0) <= 0 and (x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0) <= 0 and
          (x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0) <= 0):
        return math.atan2(y0 - y1, x0 - x1) - math.atan2(y2 - y1, x2 - x1)


def vozvrash(*args):
    args[-1].append(args[:-1])


def obrabot(smeshenie, ray, p_h, brightness):  # отрисовка стены
    cropped = pygame.Surface((SCALE, razmer_image[1]))  # создаем surface для частички изображения
    if int(smeshenie * razmer_image[0]) + SCALE <= razmer_image[
        0]:  # узнаем не больше ли координаты нужной части картинки самой картинки
        cropped.blit(image_stena, (0, 0),
                     (int(smeshenie * razmer_image[0]), 0, SCALE,
                      razmer_image[1]))  # размещаем часть изображения на surface
    else:
        cropped.blit(image_stena, (0, 0),
                     (razmer_image[0] - SCALE, 0, SCALE, razmer_image[1]))
    cropped = pygame.transform.scale(cropped, (SCALE, p_h))  # изменяем размер surface под размер проекции
    pygame.Surface.set_alpha(cropped, brightness)  # изменяем прозрачность surface
    pygame.draw.rect(screen, 'black',
                     (ray * SCALE, height // 2 - p_h // 2, SCALE, p_h))  # рисуем черную стену
    screen.blit(cropped, (ray * SCALE, height // 2 - p_h // 2))  # отображаем на стене surface


def obrabot_prep(smeshenie, ray, p_h, obj, zhuzhanie):  # отрисовка спрайта
    if obj == 'prep':
        cropped = pygame.Surface((SCALE, razmer_image_vase[1]))  # создаем surface для частички изображения
        cropped = pygame.Surface.convert_alpha(cropped)
        cropped.fill((0, 0, 0, 0))  # делаем его прозрачным
        if int(smeshenie * razmer_image_vase[0]) + SCALE <= razmer_image_vase[
            0]:  # узнаем не больше ли координаты нужной части картинки самой картинки
            cropped.blit(image_vase, (0, 0),
                         (int(smeshenie * razmer_image_vase[0]), 0, SCALE,
                          razmer_image_vase[1]))  # размещаем часть изображения на surface
        else:
            cropped.blit(image_vase, (0, 0),
                         (razmer_image_vase[0] - SCALE, 0, SCALE, razmer_image_vase[1]))
        cropped = pygame.transform.scale(cropped, (SCALE, p_h // 2))  # изменяем размер surface под размер проекции
        screen.blit(cropped, (ray * SCALE, height // 2))
    elif obj == 'pet':
        cropped = pygame.Surface((SCALE, razmer_image_muha[1]))  # создаем surface для частички изображения
        cropped = pygame.Surface.convert_alpha(cropped)
        cropped.fill((0, 0, 0, 0))  # делаем его прозрачным
        if int(smeshenie * razmer_image_muha[0]) + SCALE <= razmer_image_muha[
            0]:  # узнаем не больше ли координаты нужной части картинки самой картинки
            cropped.blit(image_muha, (0, 0),
                         (int(smeshenie * razmer_image_muha[0]), 0, SCALE,
                          razmer_image_muha[1]))  # размещаем часть изображения на surface
        else:
            cropped.blit(image_muha, (0, 0),
                         (razmer_image_muha[0] - SCALE, 0, SCALE, razmer_image_muha[1]))
        cropped = pygame.transform.scale(cropped, (SCALE, p_h // 10))  # изменяем размер surface под размер проекции
        screen.blit(cropped, (ray * SCALE, height // 2 - zhuzhanie))
    elif obj == 'bullet':
        cropped = pygame.Surface((SCALE, razmer_image_bullet[1]))  # создаем surface для частички изображения
        cropped = pygame.Surface.convert_alpha(cropped)
        cropped.fill((0, 0, 0, 0))  # делаем его прозрачным
        if int(smeshenie * razmer_image_bullet[0]) + SCALE <= razmer_image_bullet[
            0]:  # узнаем не больше ли координаты нужной части картинки самой картинки
            cropped.blit(image_bullet, (0, 0),
                         (int(smeshenie * razmer_image_bullet[0]), 0, SCALE,
                          razmer_image_bullet[1]))  # размещаем часть изображения на surface
        else:
            cropped.blit(image_bullet, (0, 0),
                         (razmer_image_bullet[0] - SCALE, 0, SCALE, razmer_image_bullet[1]))
        cropped = pygame.transform.scale(cropped, (SCALE, p_h // 10))  # изменяем размер surface под размер проекции
        screen.blit(cropped, (ray * SCALE, height // 2 + p_h // 10 - zhuzhanie))
    elif obj == 'hero_bullet':
        cropped = pygame.Surface((SCALE, razmer_image_bullet[1]))  # создаем surface для частички изображения
        cropped = pygame.Surface.convert_alpha(cropped)
        cropped.fill((0, 0, 0, 0))  # делаем его прозрачным
        if int(smeshenie * razmer_image_bullet[0]) + SCALE <= razmer_image_bullet[
            0]:  # узнаем не больше ли координаты нужной части картинки самой картинки
            cropped.blit(image_bullet, (0, 0),
                         (int(smeshenie * razmer_image_bullet[0]), 0, SCALE,
                          razmer_image_bullet[1]))  # размещаем часть изображения на surface
        else:
            cropped.blit(image_bullet, (0, 0),
                         (razmer_image_bullet[0] - SCALE, 0, SCALE, razmer_image_bullet[1]))
        cropped = pygame.transform.scale(cropped, (SCALE, p_h // 10))  # изменяем размер surface под размер проекции
        screen.blit(cropped, (ray * SCALE, height // 2 + p_h // 10 - zhuzhanie))
    elif obj == 'enemy':
        im = soldiers_im[num_image % 4]
        razmer_im = soldiers_razmer[num_image % 4]
        cropped = pygame.Surface((SCALE, razmer_im[1]))  # создаем surface для частички изображения
        cropped = pygame.Surface.convert_alpha(cropped)
        cropped.fill((0, 0, 0, 0))  # делаем его прозрачным
        if int(smeshenie * razmer_im[0]) + SCALE <= razmer_im[
            0]:  # узнаем не больше ли координаты нужной части картинки самой картинки
            cropped.blit(im, (0, 0),
                         (int(smeshenie * razmer_im[0]), 0, SCALE,
                          razmer_im[1]))  # размещаем часть изображения на surface
        else:
            cropped.blit(im, (0, 0),
                         (razmer_im[0] - SCALE, 0, SCALE, razmer_im[1]))
        cropped = pygame.transform.scale(cropped, (SCALE, p_h // 2))  # изменяем размер surface под размер проекции
        screen.blit(cropped, (ray * SCALE, height // 2))


class Persona(pygame.sprite.Sprite):  # для перемещения и отрисовки персонажа
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect((x, y, SIZE, SIZE))
        self.hp = 50

    def update(self):
        self.rect.x = x
        self.rect.y = y
        pygame.draw.circle(screen, 'white', ((self.rect.x + SIZE * 0.5) * 0.1,
                                             (self.rect.y + SIZE * 0.5) * 0.1), SIZE * 0.5)

    def shot(self):
        self.hp -= 1

    def check(self):
        if self.hp <= 0:
            return False
        return True


def drawTextbars(screen, txt, x, y, size=45, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text = font.render(txt, True, color)
    screen.blit(text, (x, y))


def drawHP(screen, txt, x, y, hp, size=45):
    font = pygame.font.Font(None, size)
    if hp > 8:
        text = font.render(txt, True, (255, 255, 255))
    elif hp == 7:
        text = font.render(txt, True, (255, 200, 200))
    elif hp == 6:
        text = font.render(txt, True, (255, 160, 160))
    elif hp == 5:
        text = font.render(txt, True, (255, 120, 120))
    elif hp == 4:
        text = font.render(txt, True, (255, 80, 80))
    elif hp == 3:
        text = font.render(txt, True, (255, 40, 40))
    elif hp == 2:
        text = font.render(txt, True, (255, 10, 10))
    else:
        text = font.render(txt, True, (255, 0, 0))
    screen.blit(text, (x, y))


pygame.init()
size = width, height  # задаются в файле map, как и другие свойства карты
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Руины замка")
pygame.display.flip()
pygame.font.init()
start_text = pygame.font.SysFont('Bodoni MT Black', 120)
textsurface = start_text.render('СТАРТ', False, (28, 110, 103))
leave = start_text.render('ВЫХОД', False, (28, 110, 103))
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = l_image("zamok.jpg")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
all_sprites.draw(screen)
# задаем музыку
enemy_dead = pygame.mixer.Sound('data/enemy_dead.wav')
lose_sound = pygame.mixer.Sound('data/lose.mp3')
vystrel_bullet = pygame.mixer.Sound('data/vystrel.mp3')
pygame.mixer.music.load('data/fon_music.mp3')

pauseWindow = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = l_image("pause.png")
sprite.rect = sprite.image.get_rect()
pauseWindow.add(sprite)

menu = True
running = False
pygame.mixer.music.play(-1)
while menu:
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:  # теперь выход на кнопке ESCAPE
            menu = False
            running = False
        if pygame.mouse.get_focused():
            if 300 < pygame.mouse.get_pos()[0] < 900 and 400 < pygame.mouse.get_pos()[1] < 600:
                pygame.draw.rect(screen, (84, 98, 111), (300, 400, 600, 200), 30)
                textsurface = start_text.render('СТАРТ', False, (84, 98, 111))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    menu = False
                    running = True
            else:
                textsurface = start_text.render('СТАРТ', False, (28, 110, 103))
                pygame.draw.rect(screen, (28, 110, 103), (300, 400, 600, 200), 30)
            if 300 < pygame.mouse.get_pos()[0] < 900 and 700 < pygame.mouse.get_pos()[1] < 900:
                leave = start_text.render('ВЫХОД', False, (84, 98, 111))
                pygame.draw.rect(screen, (84, 98, 111), (300, 700, 600, 200), 30)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    menu = False
            else:
                leave = start_text.render('ВЫХОД', False, (28, 110, 103))
                pygame.draw.rect(screen, (28, 110, 103), (300, 700, 600, 200), 30)
        screen.blit(textsurface, (450, 460))
        screen.blit(leave, (450, 760))
    pygame.display.flip()

while running:
    pygame.mixer.music.load('data/fon_music.mp3')
    pygame.mixer.music.play(-1)
    pauseMenu = False
    points = 0
    mobs = 2
    last_running = True
    start_time = time.time()
    heightMap = height + 900  # Изменённый размер для поля
    map_number = 0
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load(os.path.join('data', 'gun.png'))
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    rays = pygame.sprite.Group()
    rays_prep = pygame.sprite.Group()
    steny = pygame.sprite.Group()
    rays_muha = pygame.sprite.Group()
    rays_enemy = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    personazh = pygame.sprite.Group()
    image_vase.set_colorkey((0, 0, 0))
    image_bullet.set_colorkey((0, 0, 0))
    vector = 0
    rays_bullet = pygame.sprite.Group()
    rays_hero_bullet = pygame.sprite.Group()
    for i in range(NUM_RAYS):  # создаем лучи
        Raycast(rays, i)
    for elem in prep_cord:  # создаем лучи
        Raycastprep(rays_prep, elem[0], elem[1])
    for i, j in map_cord:
        Stena(steny, i, j)  # инициализируем стены
    Raycastpet(rays_muha, cord_muha[0], cord_muha[1])
    for i in cord_soldiers:  # создаем врагов
        Raycastenemy(rays_enemy, i[0], i[1])
    hero = Persona(personazh)  # инициализируем персонажа
    pygame.mouse.set_visible(False)
    speed_count = 0  # счетчик частоты смены кадров в анимации врагов
    num_image = 0  # номер отображаемой картинки в анимации врага
    while running:
        speed_count += 1
        for event in pygame.event.get():
            if mobs == 0:
                map_number += 1
                mobs = vofen[map_number][0]
                map_cord = set()
                text_map = load_level(maps[map_number][0])
                if map_number > 1:
                    if y - SIZE > 900:
                        y -= 859  # если ты находишься в нижней зоне карты, то тебя перекидывает вверх
                    else:
                        y = 80  # иначе на минимальную точку карты
                cord_soldiers = []
                for i in range(mobs):
                    cord_soldiers.append((enemyCoords[map_number][i][0] * BLOCK_SIZE_X,
                                            enemyCoords[map_number][i][1] * BLOCK_SIZE_Y))
                for i in cord_soldiers:
                    Raycastenemy(rays_enemy, i[0], i[1])
                for j, row in enumerate(text_map):
                    for i, bloc in enumerate(row):
                        if bloc == 'W':
                            map_cord.add((i * BLOCK_SIZE_X, j * BLOCK_SIZE_Y))
                steny = pygame.sprite.Group()
                for i, j in map_cord:
                    Stena(steny, i, j)
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.mixer.music.pause()
                pygame.mouse.set_visible(True)
                pauseMenu = True
                pauseWindow.draw(screen)
                pygame.display.flip()
                while pauseMenu:
                    for eIr in pygame.event.get():
                        if eIr.type == pygame.QUIT:
                            pauseMenu = False
                            running = False
                        if eIr.type == pygame.MOUSEBUTTONUP:
                            pos = eIr.pos
                            if 370 < pos[0] < 850 and 306 < pos[1] < 416:
                                pauseMenu = False
                                pygame.mouse.set_visible(False)
                                pygame.mixer.music.unpause()
                            if 370 < pos[0] < 850 and 480 < pos[1] < 590:
                                pauseMenu = False
                                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.mouse.get_focused():
                    Raycast_hero_bullet(rays_hero_bullet, x, y, vector)
        if pygame.key.get_pressed()[pygame.K_q]:
            map_cord = set()
            for j, row in enumerate(text_map2):
                for i, bloc in enumerate(row):
                    if bloc == 'W':
                        map_cord.add((i * BLOCK_SIZE_X, j * BLOCK_SIZE_Y))
            steny = pygame.sprite.Group()
            for i, j in map_cord:
                Stena(steny, i, j)
        if pygame.key.get_pressed()[pygame.K_w]:
            for _ in range(speed):  # для более плавного движения, вместо 5 + проверка, 5 раз по 1 и каждый раз проверка
                if width - SIZE + 1 > x + math.cos(vector) > 0:
                    x += math.cos(vector)
                    personazh.update()
                    if pygame.sprite.groupcollide(steny, personazh, False,
                                                  False):  # проверка на столкновение с препядствием
                        x -= math.cos(vector)
                        personazh.update()
                if heightMap - SIZE + 1 > y + math.sin(vector) > 0:
                    y += math.sin(vector)
                    personazh.update()
                    if pygame.sprite.groupcollide(steny, personazh, False, False):
                        y -= math.sin(vector)
                        personazh.update()
                else:
                    print(height - SIZE + 1)
                    print(y)
        if pygame.key.get_pressed()[pygame.K_s]:
            for _ in range(speed):
                if width - SIZE + 1 > x - math.cos(vector) > 0:
                    x -= math.cos(vector)
                    personazh.update()
                    if pygame.sprite.groupcollide(steny, personazh, False, False):
                        x += math.cos(vector)
                        personazh.update()
                if heightMap - SIZE + 1 > y - math.sin(vector) > 0:
                    y -= math.sin(vector)
                    personazh.update()
                    if pygame.sprite.groupcollide(steny, personazh, False, False):
                        y += math.sin(vector)
                        personazh.update()
        if pygame.key.get_pressed()[pygame.K_a]:
            for _ in range(speed):
                if width - SIZE + 1 > x - math.cos(vector + 90) > 0:
                    x -= math.cos(vector + 90)
                    personazh.update()
                    if pygame.sprite.groupcollide(steny, personazh, False, False):
                        x += math.cos(vector + 90)
                        personazh.update()
                if heightMap - SIZE + 1 > y - math.sin(vector + 90) > 0:
                    y -= math.sin(vector + 90)
                    personazh.update()
                    if pygame.sprite.groupcollide(steny, personazh, False, False):
                        y += math.sin(vector + 90)
                        personazh.update()
        if pygame.key.get_pressed()[pygame.K_d]:
            for _ in range(speed):
                if width - SIZE + 1 > x - math.cos(vector - 90) > 0:
                    x -= math.cos(vector - 90)
                    personazh.update()
                    if pygame.sprite.groupcollide(steny, personazh, False, False):
                        x += math.cos(vector - 90)
                        personazh.update()
                if heightMap - SIZE + 1 > y - math.sin(vector - 90) > 0:
                    y -= math.sin(vector - 90)
                    personazh.update()
                    if pygame.sprite.groupcollide(steny, personazh, False, False):
                        y += math.sin(vector - 90)
                        personazh.update()
        if pygame.mouse.get_focused():
            vector += povorot_vectora * (pygame.mouse.get_pos()[0] - seredina_w)  # прибавляем изменение положения мышки
            if vector > 180:  # умноженное на чувствительность мышки
                vector = -180
            elif vector < -180:
                vector = 180
        pygame.mouse.set_pos([seredina_w, seredina_h])  # возвращаем мышку обратно в центр
        screen.fill('black')
        pygame.draw.rect(screen, (0, 0, 230), (0, 0, width, height / 2))  # потолок
        pygame.draw.rect(screen, (50, 50, 50), (0, height / 2, width, height / 2))  # пол
        vozvrat = []
        pygame.sprite.groupcollide(rays_bullet, steny, True, False)
        pygame.sprite.groupcollide(rays_hero_bullet, steny, True, False)
        p = len(pygame.sprite.groupcollide(rays_hero_bullet, rays_enemy, True, True))
        if p != 0:
            enemy_dead.play()
            points += 10 * p
            mobs -= p
        if any(pygame.sprite.groupcollide(rays_bullet, personazh, True, False)):
            hero.shot()
            if not hero.check():
                pygame.mouse.set_visible(True)
                pygame.mixer.music.pause()
                pygame.mixer.music.load('data/lose.mp3')
                pygame.mixer.music.play(-1)
                running = False
                lose_sound.play()
                vremya = datetime.now()
                while last_running:
                    screen.blit(zamok_image, (0, 0))
                    drawTextbars(screen, f"Количество набранных очков: {points}", 100, 50, 45, (255, 0, 0))
                    drawTextbars(screen, f"Оставшееся количество врагов: {mobs}", 100, 100, 45, (255, 0, 0))
                    drawTextbars(screen, f'Пройдено уровней: {map_number}', 100, 150, 45, (255, 0, 0))
                    drawTextbars(screen, f"Дата смерти: {vremya}", 100, 200, 45, (255, 0, 0))
                    for event in pygame.event.get():
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            last_running = False
                    if 300 < pygame.mouse.get_pos()[0] < 900 and 400 < pygame.mouse.get_pos()[1] < 600:
                        pygame.draw.rect(screen, (84, 98, 111), (300, 400, 600, 200), 30)
                        textsurface = start_text.render('ЗАНОВО', False, (84, 98, 111))
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            running = True
                            last_running = False
                    else:
                        textsurface = start_text.render('ЗАНОВО', False, (28, 110, 103))
                        pygame.draw.rect(screen, (28, 110, 103), (300, 400, 600, 200), 30)
                    if 300 < pygame.mouse.get_pos()[0] < 900 and 700 < pygame.mouse.get_pos()[1] < 900:
                        leave = start_text.render('ВЫХОД', False, (84, 98, 111))
                        pygame.draw.rect(screen, (84, 98, 111), (300, 700, 600, 200), 30)
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            running = False
                            last_running = False
                    else:
                        leave = start_text.render('ВЫХОД', False, (28, 110, 103))
                        pygame.draw.rect(screen, (28, 110, 103), (300, 700, 600, 200), 30)
                    screen.blit(textsurface, (450, 460))
                    screen.blit(leave, (450, 760))
                    pygame.display.flip()
                pygame.mixer.pause()
                break
        rays.update(map_cord, vozvrat, BLOCK_SIZE_X, BLOCK_SIZE_Y, x, y)
        for elem in vozvrat:
            obrabot(elem[0], elem[1], elem[2], elem[3])
        vozvrat_prep = []
        rays_prep.update(vector, x, y)
        rays_muha.update(vector, x, y)
        rays_enemy.update(vector, x, y)
        rays_bullet.update()
        rays_hero_bullet.update()
        vozvrat_prep = sorted(vozvrat_prep, key=lambda x: x[2])  # сначала обрабатываем дальние лучи
        for elem in vozvrat_prep:
            if elem[2] >= vozvrat[elem[1]][2]:  # если наша проекция больше проекции стены
                obrabot_prep(elem[0], elem[1], elem[2], elem[3], elem[4])
        steny.update()
        personazh.update()
        if speed_count % 5 == 0:
            num_image += 1
        all_sprites.draw(screen)
        drawTextbars(screen, "Осталось врагов: " + str(mobs), 130, 0)
        drawTextbars(screen, "Очки: " + str(points), 130, 50)
        drawHP(screen, f"Жизни: {hero.hp}", 130, 100, hero.hp)
        clock.tick(fps)
        pygame.display.flip()
        if map_number == 10 and mobs == 0:
            pygame.mouse.set_visible(True)
            pygame.mixer.music.pause()
            pygame.mixer.music.load('data/win.mp3')
            pygame.mixer.music.play(-1)
            while last_running:
                screen.blit(win_image, (0, 0))
                drawTextbars(screen, f"Количество набранных очков: {points}", 100, 50, 45)
                drawTextbars(screen, f"Убито врагов: {points / 10}", 100, 100, 45)
                drawTextbars(screen, f'Пройдено уровней: {map_number}', 100, 150, 45)
                drawTextbars(screen, f"Время прохождения: {time_convert(time.time() - start_time)}", 100, 200, 45)
                for event in pygame.event.get():
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        last_running = False
                if 300 < pygame.mouse.get_pos()[0] < 900 and 400 < pygame.mouse.get_pos()[1] < 600:
                    pygame.draw.rect(screen, (84, 98, 111), (300, 400, 600, 200), 30)
                    textsurface = start_text.render('ЗАНОВО', False, (84, 98, 111))
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pygame.mixer.music.pause()
                        running = True
                        last_running = False
                else:
                    textsurface = start_text.render('ЗАНОВО', False, (28, 110, 103))
                    pygame.draw.rect(screen, (28, 110, 103), (300, 400, 600, 200), 30)
                if 300 < pygame.mouse.get_pos()[0] < 900 and 700 < pygame.mouse.get_pos()[1] < 900:
                    leave = start_text.render('ВЫХОД', False, (84, 98, 111))
                    pygame.draw.rect(screen, (84, 98, 111), (300, 700, 600, 200), 30)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        running = False
                        last_running = False
                else:
                    leave = start_text.render('ВЫХОД', False, (28, 110, 103))
                    pygame.draw.rect(screen, (28, 110, 103), (300, 700, 600, 200), 30)
                screen.blit(textsurface, (450, 460))
                screen.blit(leave, (450, 760))
                pygame.display.flip()
            pygame.mixer.pause()
            break
pygame.quit()
