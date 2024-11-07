# screens.py

import pygame
import sys
from settings import WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR

def draw_text(screen, text, font, color, x, y, shadow=False):
    """Funzione per disegnare testo con ombra."""
    if shadow:
        shadow_color = (50, 50, 50)  #Grigio scuro per l'ombra
        shadow_surface = font.render(text, True, shadow_color)
        screen.blit(shadow_surface, (x + 2, y + 2))
    
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def show_game_over(screen, font, score):

    game_over_bg = (30, 30, 60)  #blu scuro per lo sfondo
    screen.fill(game_over_bg)

    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 36)

    draw_text(screen, "Game Over!", title_font, TEXT_COLOR, WIDTH // 2 - 140, HEIGHT // 2 - 100, shadow=True)
    draw_text(screen, f"Final Score: {score}", font, TEXT_COLOR, WIDTH // 2 - 80, HEIGHT // 2 - 30, shadow=True)

    retry_text = "Press R to Retry"
    quit_text = "Press Q to Quit"

    retry_x, retry_y = WIDTH // 2 - 100, HEIGHT // 2 + 50
    quit_x, quit_y = WIDTH // 2 - 100, HEIGHT // 2 + 100

    pygame.draw.rect(screen, (50, 50, 150), (retry_x - 10, retry_y - 5, 220, 40), border_radius=10)  #Sfondo pulsante Riprova
    pygame.draw.rect(screen, (150, 50, 50), (quit_x - 10, quit_y - 5, 220, 40), border_radius=10)    #Sfondo pulsante Esci

    draw_text(screen, retry_text, button_font, TEXT_COLOR, retry_x, retry_y, shadow=True)
    draw_text(screen, quit_text, button_font, TEXT_COLOR, quit_x, quit_y, shadow=True)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'retry'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
