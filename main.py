import math
import os
import pygame
import sys
from pygame import Color

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


class Raycastprep(pygame.sprite.Sprite):
    def __init__(self, group, r):
        super().__init__(group)
        self.ray = r
        self.nach_x = x + SIZE * 0.5
        self.nach_y = y + SIZE * 0.5

    def update(self, cord, spisok_slice, x, y):
        x1 = x + SIZE * 0.5
        y1 = y + SIZE * 0.5
        sin_a = math.sin(vector)
        cos_a = math.cos(vector)
        x2, y2 = x1 + 2000 * cos_a, y1 + 2000 * sin_a
        sin_a_2 = math.sin(vector + OBZOR / 2 + 0.25)
        cos_a_2 = math.cos(vector + OBZOR / 2 + 0.25)
        x3, y3 = x1 + 2000 * cos_a_2, y1 + 2000 * sin_a_2
        sin_a_3 = math.sin(vector - OBZOR / 2 - 0.25)
        cos_a_3 = math.cos(vector - OBZOR / 2 - 0.25)
        x4, y4 = x1 + 2000 * cos_a_3, y1 + 2000 * sin_a_3
        for elem in cord: #правая часть экрана
            ugol = treug(elem[0], elem[1], x1, y1, x2, y2, x3, y3)
            if ugol is not None:
                if ugol < - 1:
                    ugol = ugol % (math.pi * 2)
                ugol2 = OBZOR / 2 + ugol
                ray = int(ugol2 / DELTA_ANGLE)
                shirina = (ugol2 / OBZOR) * width
                if cos_a != 0:
                    depth_v = (elem[0] - x1) / math.cos(vector + ugol)
                else:
                    depth_v = elem[0]
                if sin_a != 0:
                    depth_h = (elem[1] - y1) / math.sin(vector + ugol)
                else:
                    depth_h = elem[1]
                if depth_v < depth_h:
                    depth = depth_v
                else:
                    depth = depth_h
                depth *= math.cos(ugol)
                if depth != 0:
                    p_h = PROJ_COEFF / depth
                else:
                    p_h = 0
                dlina = razmer_image_vase[1] / razmer_image_vase[0] * (p_h // 2)
                ray_2 = int((shirina - dlina / 2) / SCALE)
                ray_3 = int((shirina + dlina / 2) / SCALE)
                ray_razn = ray_3 - ray_2
                for i in range(ray_razn):
                    if 0 < ray_2 + i < NUM_RAYS:
                        vozvrash(i / (ray_3 - ray_2), ray_2 + i, p_h, vozvrat_prep)


        for elem in cord: # левая часть
            ugol = treug(elem[0], elem[1], x1, y1, x2, y2, x4, y4)
            if ugol is not None:
                if ugol > 1:
                    ugol = -((math.pi * 2) % ugol)
                ugol2 = OBZOR / 2 + ugol
                ray = int(ugol2 / DELTA_ANGLE)
                shirina = (ugol2 / OBZOR) * width
                if cos_a != 0:
                    depth_v = (elem[0] - x1) / math.cos(vector + ugol)
                else:
                    depth_v = elem[0]
                if sin_a != 0:
                    depth_h = (elem[1] - y1) / math.sin(vector + ugol)
                else:
                    depth_h = elem[1]
                if depth_v < depth_h:
                    depth = depth_v
                else:
                    depth = depth_h
                depth *= math.cos(ugol)
                if depth != 0:
                    p_h = PROJ_COEFF / depth
                else:
                    p_h = 0
                dlina = razmer_image_vase[1] / razmer_image_vase[0] * (p_h // 2)
                ray_2 = int((shirina - dlina / 2) / SCALE)
                ray_3 = int((shirina + dlina / 2) / SCALE)
                ray_razn = ray_3 - ray_2
                for i in range(ray_razn):
                    if 0 < ray_2 + i < NUM_RAYS:
                        vozvrash(i / (ray_3 - ray_2), ray_2 + i, p_h, vozvrat_prep)




def treug(x0, y0, x1, y1, x2, y2, x3, y3):
    if ((x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0) >= 0 and (x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0) >= 0 and
            (x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0) >= 0):
        return math.atan2(y0 - y1, x0 - x1) - math.atan2(y2 - y1, x2 - x1)
    elif ((x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0) <= 0 and (x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0) <= 0 and
          (x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0) <= 0):
        return math.atan2(y0 - y1, x0 - x1) - math.atan2(y2 - y1, x2 - x1)


def vozvrash(*args):
    args[-1].append(args[:-1])


def obrabot(smeshenie, ray, p_h, brightness):
    cropped = pygame.Surface((SCALE, razmer_image[1]))  # создаем surface для частички изображения
    if int(smeshenie * razmer_image[0]) + SCALE <= razmer_image[0]:  # узнаем не больше ли координаты нужной части картинки самой картинки
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


def obrabot_prep(smeshenie, ray, p_h):
    cropped = pygame.Surface((SCALE, razmer_image_vase[1]))  # создаем surface для частички изображения
    cropped = pygame.Surface.convert_alpha(cropped)
    cropped.fill((0, 0, 0, 0))
    if int(smeshenie * razmer_image_vase[0]) + SCALE <= razmer_image_vase[0]:  # узнаем не больше ли координаты нужной части картинки самой картинки
        cropped.blit(image_vase, (0, 0),
                     (int(smeshenie * razmer_image_vase[0]), 0, SCALE,
                      razmer_image_vase[1]))  # размещаем часть изображения на surface
    else:
        cropped.blit(image_vase, (0, 0),
                     (razmer_image_vase[0] - SCALE, 0, SCALE, razmer_image_vase[1]))
    cropped = pygame.transform.scale(cropped, (SCALE, p_h // 2))  # изменяем размер surface под размер проекции
    screen.blit(cropped, (ray * SCALE, height // 2))


class Persona(pygame.sprite.Sprite):  # для перемещения и отрисовки персонажа
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect((0, 0, SIZE, SIZE))
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x = x
        self.rect.y = y
        pygame.draw.circle(screen, 'white', ((self.rect.x + SIZE * 0.5) * 0.1,
                                             (self.rect.y + SIZE * 0.5) * 0.1), SIZE * 0.5)


pygame.init()
size = width, height  # задаются в файле map, как и другие свойства карты
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Руины замка")
running = True

all_sprites = pygame.sprite.Group()
rays = pygame.sprite.Group()
rays_prep = pygame.sprite.Group()
steny = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
personazh = pygame.sprite.Group()
sprite.image = l_image("bg1.png")
image_vase.set_colorkey((0, 0, 0))
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
vector = 0
for i in range(NUM_RAYS):  # создаем лучи
    Raycast(rays, i)

for i in range(1):  # создаем лучи
    Raycastprep(rays_prep, i)

for i, j in map_cord:
    Stena(steny, i, j)  # инициализируем стены
Persona(personazh)  # инициализируем персонажа
pygame.mouse.set_visible(False)
while running:
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:  # теперь выход на кнопке ESCAPE
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
        for _ in range(speed):
            if width - SIZE + 1 > x - math.cos(vector + 90) > 0:
                x -= math.cos(vector + 90)
                personazh.update()
                if pygame.sprite.groupcollide(steny, personazh, False, False):
                    x += math.cos(vector + 90)
                    personazh.update()
            if height - SIZE + 1 > y - math.sin(vector + 90) > 0:
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
            if height - SIZE + 1 > y - math.sin(vector - 90) > 0:
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
    rays.update(map_cord, vozvrat, BLOCK_SIZE_X, BLOCK_SIZE_Y, x, y)
    for elem in vozvrat:
        obrabot(elem[0], elem[1], elem[2], elem[3])
    vozvrat_prep = []
    rays_prep.update(prep_cord, vozvrat, x, y)
    vozvrat_prep = sorted(vozvrat_prep, key=lambda x: x[2])
    for elem in vozvrat_prep:
        if elem[2] >= vozvrat[elem[1]][2]:
            obrabot_prep(elem[0], elem[1], elem[2])
    steny.update()
    personazh.update()
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
