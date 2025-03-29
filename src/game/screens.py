import pygame
import sys
from settings import WIDTH, HEIGHT, TEXT_COLOR


class OptionSlider:
    def __init__(self, label, min_value, max_value, step, default, font, screen_rect, index, total_sliders):
        self.label = label
        self.min = min_value
        self.max = max_value
        self.step = step
        self.value = default
        self.font = font
        self.width = 300
        self.height = 20
        self.handle_radius = 10
        self.dragging = False

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = screen_rect.centerx
        vertical_spacing = 80
        total_height = total_sliders * vertical_spacing
        start_y = screen_rect.centery - total_height // 2
        self.rect.y = start_y + index * vertical_spacing

        self.label_surface = self.font.render(f"{self.label}: {self.value}", True, TEXT_COLOR)
        self.label_rect = self.label_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 10))

    def draw(self, screen):
        self.label_surface = self.font.render(f"{self.label}: {self.value}", True, TEXT_COLOR)
        screen.blit(self.label_surface, self.label_rect)

        pygame.draw.rect(screen, (180, 180, 180), self.rect)

        pos_ratio = (self.value - self.min) / (self.max - self.min)
        handle_x = self.rect.x + int(pos_ratio * self.rect.width)
        handle_center = (handle_x, self.rect.y + self.rect.height // 2)
        pygame.draw.circle(screen, (255, 100, 100), handle_center, self.handle_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            rel_x = max(0, min(self.rect.width, rel_x))
            ratio = rel_x / self.rect.width
            raw_value = self.min + ratio * (self.max - self.min)
            stepped_value = round(raw_value / self.step) * self.step
            self.value = int(max(self.min, min(self.max, stepped_value)))

def show_settings_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Impostazioni di Gioco")
    font = pygame.font.Font(None, 36)
    screen_rect = screen.get_rect()

    slider_labels = [
        ("Durata Partita (s)", 10, 120, 5, 30),
        ("Numero di Ostacoli", 5, 22, 1, 10),
        ("Velocità Giocatore", 1, 10, 1, 5),
    ]

    sliders = [OptionSlider(label, min_val, max_val, step, default, font, screen_rect, i, len(slider_labels))
               for i, (label, min_val, max_val, step, default) in enumerate(slider_labels)]

    button_width = 200
    button_height = 50
    start_button = pygame.Rect(0, 0, button_width, button_height)
    start_button.centerx = screen_rect.centerx
    start_button.y = sliders[-1].rect.bottom + 50

    clock = pygame.time.Clock()

    while True:
        screen.fill((20, 20, 50))

        for slider in sliders:
            slider.draw(screen)

        pygame.draw.rect(screen, (50, 150, 50), start_button, border_radius=8)
        text_surf = font.render("Avvia Gioco", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=start_button.center)
        screen.blit(text_surf, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for slider in sliders:
                slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                return {
                    "TIME_LIMIT": sliders[0].value,
                    "OBSTACLES_NUMBER": sliders[1].value,
                    "RECT_SPEED": sliders[2].value
                }

        clock.tick(60)


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


if __name__ == "__main__":
    pygame.init()
    show_settings_menu()
