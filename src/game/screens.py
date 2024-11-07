import pygame
import sys
from settings import WIDTH, HEIGHT, TEXT_COLOR

def draw_text(screen, text, font, color, x, y, center=False, shadow=False):
    """Funzione per disegnare testo con opzioni aggiuntive."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)

    if shadow:
        shadow_surface = font.render(text, True, (50, 50, 50))
        shadow_rect = shadow_surface.get_rect()
        shadow_rect.center = text_rect.center
        screen.blit(shadow_surface, (shadow_rect.x + 2, shadow_rect.y + 2))

    screen.blit(text_surface, text_rect)

class Button:
    def __init__(self, text, font, color, rect_color, x, y, width, height):
        self.text = text
        self.font = font
        self.color = color
        self.rect_color = rect_color
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, screen):
        # Cambia il colore se il pulsante è sotto il mouse
        current_color = tuple(min(255, c + 40) if self.hovered else c for c in self.rect_color)
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        draw_text(screen, self.text, self.font, self.color, self.rect.centerx, self.rect.centery, center=True)

    def is_hovered(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

def show_game_over(screen, font, score):
    clock = pygame.time.Clock()

    game_over_bg = (30, 30, 60)
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 36)

    # Pulsanti
    button_width, button_height = 220, 50
    retry_button = Button(
        text="Press R to Retry",
        font=button_font,
        color=TEXT_COLOR,
        rect_color=(50, 50, 150),
        x=WIDTH // 2 - button_width // 2,
        y=HEIGHT // 2 + 20,
        width=button_width,
        height=button_height,
    )
    quit_button = Button(
        text="Press Q to Quit",
        font=button_font,
        color=TEXT_COLOR,
        rect_color=(150, 50, 50),
        x=WIDTH // 2 - button_width // 2,
        y=HEIGHT // 2 + 90,
        width=button_width,
        height=button_height,
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(game_over_bg)

        # Titolo e punteggio
        draw_text(screen, "Game Over!", title_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 100, center=True, shadow=True)
        draw_text(screen, f"Final Score: {score}", font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 30, center=True, shadow=True)

        # Gestione pulsanti
        for button in [retry_button, quit_button]:
            button.is_hovered(mouse_pos)
            button.draw(screen)

        pygame.display.flip()

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
            elif retry_button.is_clicked(event):
                return 'retry'
            elif quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        clock.tick(60)  # Limita il frame rate a 60 FPS
