import os
import pygame
import sqlite3


def load_level(filename):
    filename = "assets/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map

x = "levels.db"
con = sqlite3.connect(x)
cur = con.cursor()
maps = cur.execute("""SELECT ways FROM levelWays""").fetchall()
con.close()
text_map = load_level(maps[0][0])
text_map2 = load_level(maps[1][0])  # example map
map_cord = set()
prep_cord = set()
width, height = 1200, 900
polovina_width, polovina_height = width // 2, height // 2
seredina_w, seredina_h = width * 0.5, height * 0.5
povorot_vectora = 1 / seredina_w  # чувствительность мышки
BLOCK_SIZE_X = (width / len(text_map[0])) // 1
BLOCK_SIZE_Y = (height / len(text_map)) // 1
image_stena = pygame.image.load(os.path.join('data', 'stena_zamshelaya.jfif'))
razmer_image = (image_stena.get_width(), image_stena.get_height())
image_vase = pygame.image.load(os.path.join('data', 'vase.png'))
razmer_image_vase = (image_vase.get_width(), image_vase.get_height())
image_muha = pygame.image.load(os.path.join('data', 'muha.png'))
razmer_image_muha = (image_muha.get_width(), image_muha.get_height())
image_bullet = pygame.image.load(os.path.join('data', 'bullet.png'))
razmer_image_bullet = (image_bullet.get_width(), image_bullet.get_height())
zamok_image = pygame.image.load(os.path.join('data', 'end_zamok.jpg'))
image_solder0 = pygame.transform.scale(pygame.image.load(os.path.join('data/anim_soldier', '0.png')),
                                       (BLOCK_SIZE_X, BLOCK_SIZE_Y))
image_solder1 = pygame.transform.scale(pygame.image.load(os.path.join('data/anim_soldier', '1.png')),
                                       (BLOCK_SIZE_X, BLOCK_SIZE_Y))
image_solder2 = pygame.transform.scale(pygame.image.load(os.path.join('data/anim_soldier', '2.png')),
                                       (BLOCK_SIZE_X, BLOCK_SIZE_Y))
image_solder3 = pygame.transform.scale(pygame.image.load(os.path.join('data/anim_soldier', '3.png')),
                                       (BLOCK_SIZE_X, BLOCK_SIZE_Y))
razmer_image_0 = (image_solder0.get_width(), image_solder0.get_height())
razmer_image_1 = (image_solder1.get_width(), image_solder1.get_height())
razmer_image_2 = (image_solder2.get_width(), image_solder2.get_height())
razmer_image_3 = (image_solder3.get_width(), image_solder3.get_height())
soldiers_im = [image_solder0, image_solder1, image_solder2, image_solder3]
soldiers_razmer = [razmer_image_0, razmer_image_1, razmer_image_2, razmer_image_3]
cord_soldiers = [(5.5 * BLOCK_SIZE_X, 5.5 * BLOCK_SIZE_Y), (7 * BLOCK_SIZE_X, 7 * BLOCK_SIZE_Y)]
dlina_karty, shirina_karty = len(text_map[0]) * BLOCK_SIZE_X, len(text_map) * BLOCK_SIZE_Y
for j, row in enumerate(text_map):
    for i, bloc in enumerate(row):
        if bloc == 'W':
            map_cord.add((i * BLOCK_SIZE_X, j * BLOCK_SIZE_Y))
dlina_karty, shirina_karty = len(text_map[0]) * BLOCK_SIZE_X, len(text_map) * BLOCK_SIZE_Y
prep = ((4, 4), (6.5, 5))
for elem in prep:
    prep_cord.add((elem[0] * BLOCK_SIZE_X, elem[1] * BLOCK_SIZE_Y))
cord_muha = (420, 320)
