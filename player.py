import pygame


class player:
    def __init__(self):
        self.x = 300
        self.y = 400

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += 0
            self.y += -5
        if keys[pygame.K_s]:
            self.x += 0
            self.y += 5
        if keys[pygame.K_a]:
            self.x += -5
            self.y += 0
        if keys[pygame.K_d]:
            self.x += 5
            self.y += 0
