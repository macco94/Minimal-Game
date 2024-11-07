import sys
import pygame
import random
from settings import *
from screens import show_game_over

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minimal Game")

    font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    success_sound = pygame.mixer.Sound("assets/sounds/success.mp3")
    
    player_image = pygame.image.load("assets/images/robot1.png").convert_alpha()
    player_image = pygame.transform.scale(player_image, (RECT_WIDTH+10, RECT_HEIGHT+10))

    target_image = pygame.image.load("assets/images/heart.png").convert_alpha()
    target_image = pygame.transform.scale(target_image, (RECT_HEIGHT,RECT_HEIGHT))


    def generate_obstacle_position(width, height, margin=20, max_attempts=1000):
        for _ in range(max_attempts):
            x = random.randint(0, WIDTH - width)
            y = random.randint(0, HEIGHT - height)
            rect = pygame.Rect(x, y, width, height)

        # Verifica che l'ostacolo sia a distanza di almeno 'margin' da tutti gli ostacoli esistenti
        if not any(rect.inflate(margin * 2, margin * 2).colliderect(obstacle) for obstacle in obstacles):
            return x, y

        # Se non trova una posizione sicura dopo max_attempts, stampa un avviso e posiziona un fallback
        print("Warning: Unable to find a non-overlapping position for obstacle. Using fallback position.")
        return WIDTH // 2, HEIGHT // 2


    # Generazione degli ostacoli iniziali con un margine di 20 pixel tra di loro
    obstacles = []
    for _ in range(OBSTACLES_NUMBER):
        obs_x, obs_y = generate_obstacle_position(50, 50, margin=20)
        obstacles.append(pygame.Rect(obs_x, obs_y, 50, 50))


    def generate_safe_position(width, height, margin=5, max_attempts=10000):
        for _ in range(max_attempts):
            x = random.randint(0, WIDTH - width)
            y = random.randint(0, HEIGHT - height)
            rect = pygame.Rect(x, y, width, height)

        if not any(rect.inflate(margin * 2, margin * 2).colliderect(obstacle) for obstacle in obstacles):
            return x, y

        print("Warning: Unable to find a safe position. Using fallback position.")
        return WIDTH // 2, HEIGHT // 2


    rect_x, rect_y = generate_safe_position(RECT_WIDTH, RECT_HEIGHT)
    target_x, target_y = generate_safe_position(TARGET_WIDTH, TARGET_HEIGHT, margin=5)



    score = 0
    time_left = TIME_LIMIT
    pulse_effect = 0  #Effetto pulsazione per il bersaglio
    rect_speed = RECT_SPEED


    #Timer
    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == TIMER_EVENT:
                time_left -= 1
                if time_left <= 0:
                    running = False

        keys = pygame.key.get_pressed()
        new_x, new_y = rect_x, rect_y


        if keys[pygame.K_a]:
            new_x -= RECT_SPEED
        if keys[pygame.K_d]:
            new_x += RECT_SPEED
        if keys[pygame.K_w]:
            new_y -= RECT_SPEED
        if keys[pygame.K_s]:
            new_y += RECT_SPEED

        new_x = max(0, min(WIDTH - RECT_WIDTH, new_x))
        new_y = max(0, min(HEIGHT - RECT_HEIGHT, new_y))

        player_rect = pygame.Rect(new_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
        if not any(player_rect.colliderect(obstacle) for obstacle in obstacles):
            rect_x = new_x  #Aggiorno solo se non c'è collisione

        player_rect = pygame.Rect(rect_x, new_y, RECT_WIDTH, RECT_HEIGHT)
        if not any(player_rect.colliderect(obstacle) for obstacle in obstacles):
            rect_y = new_y  #Aggiorno solo se non c'è collisione


        rect_rect = pygame.Rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
        target_rect = pygame.Rect(target_x, target_y, TARGET_WIDTH + pulse_effect, TARGET_HEIGHT + pulse_effect)
        if rect_rect.colliderect(target_rect):
            score += 1
            target_x, target_y = generate_safe_position(TARGET_WIDTH, TARGET_HEIGHT, margin=35)
            success_sound.play()

            #TODO Incremento progressivo della difficoltà
            #rect_speed = min(rect_speed + 0.5, 15)
            #time_left = max(time_left - 2, 10)


        # Effetto di pulsazione del bersaglio
        pulse_effect = (pulse_effect + 1) % 6

        # Sfondo sfumato
        for y in range(HEIGHT):
            color = tuple(min(255, int(BACKGROUND_COLOR[i] + (y / HEIGHT) * 60)) for i in range(3))
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

        #pygame.draw.rect(screen, RECT_BORDER_COLOR, rect_rect.inflate(6, 6), border_radius=5)
        #pygame.draw.rect(screen, RECT_COLOR, rect_rect, border_radius=5)

        screen.blit(player_image, (rect_x, rect_y))

        #pygame.draw.rect(screen, TARGET_BORDER_COLOR, target_rect.inflate(4, 4), border_radius=5)
        #pygame.draw.rect(screen, TARGET_COLOR, target_rect, border_radius=5)

        screen.blit(target_image, (target_x, target_y))

        for obstacle in obstacles:
            pygame.draw.rect(screen, (128, 0, 0), obstacle)  # Colore rosso scuro per gli ostacoli


        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        timer_text = font.render(f"Time: {time_left}", True, TEXT_COLOR)
        screen.blit(score_text, (WIDTH - 150, 10))
        screen.blit(timer_text, (10, 10))

        pygame.display.flip()

    #Game Over
    return show_game_over(screen, font, score)