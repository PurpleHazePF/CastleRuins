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
logic = False

def check(cords, size1, x, y, size2):                                                
    def f(x1, x2, y1, y2):                                                           
        return y1 <= x1 <= y2 or x1 <= y1 <= x2                                      
                                                                                     
    flag = False                                                                     
    for i, j in cords:  # проверка на пересечение каждого препядствия и героя        
        if f(i, i + size1, x, x + size2) and f(j, j + size1, y, y + size2):          
            flag = True                                                              
            break                                                                    
    if flag:                                                                         
        return False                                                                 
    return True                                                                      

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
                if not check(map_cord, BLOCK_SIZE, x, y, SIZE): # проверка на столкновение с препядствием     
                    x -= math.cos(vector) * 5                        
            if 650 > y + math.sin(vector) * 5 > 0:                   
                y += math.sin(vector) * 5                            
                if not check(map_cord, BLOCK_SIZE, x, y, SIZE):      
                    y -= math.sin(vector) * 5                        
        if keys[pygame.K_s]:                                         
            if 900 > x - math.cos(vector) * 5 > 0:                   
                x -= math.cos(vector) * 5                            
                if not check(map_cord, BLOCK_SIZE, x, y, SIZE):      
                    x += math.cos(vector) * 5                        
            if 650 > y - math.sin(vector) * 5 > 0:                   
                y -= math.sin(vector) * 5                            
                if not check(map_cord, BLOCK_SIZE, x, y, SIZE):      
                    y += math.sin(vector) * 5                        
                # проверка что персонаж на поле                      
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
        pygame.draw.rect(screen, 'red', (x, y, 10, 10))      
        #теперь рисуем линию из (координат шарика) в (координаты шарика+направления(vector)*на длину стороны квадрата)
        #если что, то линия - это диагональ квадрата c шириной и высотой длина взгляда
        pygame.draw.line(screen, "red", (x, y), (x + math.cos(vector) * dlina_vzglyada[0],
                                                 y + math.sin(vector) * dlina_vzglyada[1]))
        for i, j in map_cord:  # отрисовка препядствий                               
            pygame.draw.rect(screen, (8, 75, 108), (i, j, BLOCK_SIZE, BLOCK_SIZE), 1)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
