import sys
import pygame
from settings import *
from screens import show_game_over
from player import Player
from target import Target
from obstacle import generate_obstacles
from background import create_gradient_background

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Target Rush")

        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.success_sound = pygame.mixer.Sound("assets/sounds/success.mp3")

        # Creazione degli oggetti di gioco
        self.obstacles = generate_obstacles()
        self.player = Player(self.obstacles)
        self.target = Target(self.obstacles)

        self.score = 0
        self.time_left = TIME_LIMIT
        self.pulse_effect = 0

        self.reset()

        # Timer
        self.TIMER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TIMER_EVENT, 1000)

        # Background pre-renderizzato
        self.background = create_gradient_background()


    def reset(self):
        """Funzione per reimpostare tutte le variabili e ricominciare il gioco."""
        self.obstacles = []
        self.obstacles = generate_obstacles()
        self.player = Player(self.obstacles)
        self.target = Target(self.obstacles)
        self.score = 0
        self.time_left = TIME_LIMIT
        self.pulse_effect = 0


    def run(self):
        while True:
            result = self.handle_events()
            if result == 'retry':
                self.reset()
            elif result == 'exit':
                return 'exit'
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'retry'
                elif event.key == pygame.K_q:
                    return 'exit'
            elif event.type == self.TIMER_EVENT:
                self.time_left -= 1
                if self.time_left <= 0:
                    if show_game_over(self.screen, self.font, self.score) == 'retry':
                        return 'retry'
                    else:
                        return 'exit'
                    
    def update(self):
        self.player.update(self.obstacles)
        if self.player.rect.colliderect(self.target.rect):
            self.score += 1
            self.target.reposition(self.obstacles)
            self.success_sound.play()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.target.draw(self.screen)
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (128, 0, 0), obstacle)

        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        timer_text = self.font.render(f"Time: {self.time_left}", True, TEXT_COLOR)
        self.screen.blit(score_text, (WIDTH - 150, 10))
        self.screen.blit(timer_text, (10, 10))

        pygame.display.flip()

def run_game():
    game = Game()
    result = game.run()
    if result == 'retry':
        return 'retry'
    else:
        return 'exit'
