import random
import pygame
from settings import *

class Player:
    def __init__(self, obstacles):
        self.image = pygame.image.load("assets/images/robot1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (RECT_WIDTH, RECT_HEIGHT))
        self.rect = self.image.get_rect(topleft=self.generate_position(obstacles))

    def generate_position(self, obstacles, margin=30):
        while True:
            x = random.randint(0, WIDTH - TARGET_WIDTH)
            y = random.randint(0, HEIGHT - TARGET_HEIGHT)
            rect = pygame.Rect(x, y, TARGET_WIDTH, TARGET_HEIGHT)
            if not any(rect.colliderect(obstacle) for obstacle in obstacles):
                return x, y

    def update(self, obstacles):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.rect.x, self.rect.y

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_x -= RECT_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_x += RECT_SPEED
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_y -= RECT_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_y += RECT_SPEED

        new_x = max(0, min(WIDTH - RECT_WIDTH, new_x))
        new_y = max(0, min(HEIGHT - RECT_HEIGHT, new_y))

        # Movimento orizzontale
        new_rect = pygame.Rect(new_x, self.rect.y, self.rect.width, self.rect.height)
        if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
            self.rect.x = new_x

        # Movimento verticale
        new_rect = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)
        if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
            self.rect.y = new_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
