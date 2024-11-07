import pygame
import random
from settings import *

def generate_obstacles():
    obstacles = []
    for _ in range(OBSTACLES_NUMBER):
        x, y = generate_obstacle_position(50, 50, obstacles)
        obstacles.append(pygame.Rect(x, y, 50, 50))
    return obstacles

def generate_obstacle_position(width, height, obstacles, margin=55):
    while True:
        x = random.randint(0, WIDTH - width)
        y = random.randint(0, HEIGHT - height)
        rect = pygame.Rect(x, y, width, height)
        if not any(rect.inflate(margin * 2, margin * 2).colliderect(obstacle) for obstacle in obstacles):
            return x, y