import pygame
from settings import *

def create_gradient_background():
    background = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        color = tuple(min(255, int(BACKGROUND_COLOR[i] + (y / HEIGHT) * 60)) for i in range(3))
        pygame.draw.line(background, color, (0, y), (WIDTH, y))
    return background