import pygame
import random
from settings import *

class Target:
    def __init__(self, obstacles):
        self.image = pygame.image.load("assets/images/heart.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TARGET_WIDTH, TARGET_HEIGHT))
        self.rect = self.image.get_rect(topleft=self.generate_position(obstacles))

    def generate_position(self, obstacles):
        while True:
            x = random.randint(0, WIDTH - TARGET_WIDTH)
            y = random.randint(0, HEIGHT - TARGET_HEIGHT)
            rect = pygame.Rect(x, y, TARGET_WIDTH, TARGET_HEIGHT)

            if not any(rect.colliderect(obstacle) for obstacle in obstacles):
                return x, y

    def reposition(self, obstacles):
        x, y = self.generate_position(obstacles)
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
