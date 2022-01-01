import os
import pygame


def load_level(filename):
    filename = "assets/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


text_map = load_level('text_map.txt')  # example map
map_cord = set()
width, height = 1200, 900
seredina_w, seredina_h = width * 0.5, height * 0.5
povorot_vectora = 1 / seredina_w  # чувствительность мышки
BLOCK_SIZE_X = (width / len(text_map[0])) // 1
BLOCK_SIZE_Y = (height / len(text_map)) // 1
image_stena = pygame.image.load(os.path.join('data', 'stena_zamshelaya.jfif'))
razmer_image = (image_stena.get_width(), image_stena.get_height())
for j, row in enumerate(text_map):
    for i, bloc in enumerate(row):
        if bloc == 'W':
            map_cord.add((i * BLOCK_SIZE_X, j * BLOCK_SIZE_Y))
