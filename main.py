import pygame
import sys

# Инициализация pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong Game")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (77, 244, 246)
RED = (238, 82, 73)
YELLOW = (255, 255, 0)

# Параметры игры
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
bounce_count = 0

# Ракетки
left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Мяч
ball_img = None
ball = None

# Счет
score_left = 0
score_right = 0

# Шрифты
font = pygame.font.Font(None, 74)

# Функция для рисования игрового поля
def draw_field():
    screen.fill(GREEN)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 70, 5)
    pygame.draw.rect(screen, WHITE, (0, HEIGHT // 4, 50, HEIGHT // 2), 5)
    pygame.draw.rect(screen, WHITE, (WIDTH - 50, HEIGHT // 4, 50, HEIGHT // 2), 5)

# Функция для перемещения ракеток
def move_paddles(keys):
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

# Функция для перемещения мяча
def move_ball():
    global BALL_SPEED_X, BALL_SPEED_Y, score_left, score_right, bounce_count

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Отскок от верхнего и нижнего края
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y

    # Отскок от ракеток
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        BALL_SPEED_X = -BALL_SPEED_X
        bounce_count += 1

        # Увеличение скорости мяча после 8 отскоков
        if bounce_count == 8:
            BALL_SPEED_X *= 1.1
            BALL_SPEED_Y *= 1.1
            bounce_count = 0

    # Забитый мяч
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()

# Сброс мяча в центр поля
def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y, bounce_count
    ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
    BALL_SPEED_X = -BALL_SPEED_X
    bounce_count = 0

# Функция для отображения счета
def draw_score():
    left_text = font.render(str(score_left), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))
    right_text = font.render(str(score_right), True, WHITE)
    screen.blit(right_text, (WIDTH * 3 // 4, 20))

# Функция для отображения сообщения о победе
def show_winner(winner):
    screen.fill(GREEN)
    winner_text = font.render(f"Выиграл {winner}", True, WHITE)
    score_text = font.render(f"Итоговый счет: {score_left} - {score_right}", True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    pygame.time.wait(3000)  # Показать сообщение 3 секунды

# Функция для отображения меню
def show_menu():
    menu_font = pygame.font.Font(None, 74)
    easy_text = menu_font.render("1. Easy", True, WHITE)
    normal_text = menu_font.render("2. Normal", True, WHITE)

    while True:
        screen.fill(GREEN)
        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(normal_text, (WIDTH // 2 - normal_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'easy'
                if event.key == pygame.K_2:
                    return 'normal'

# Главная игровая функция
def game_loop():
    global ball_img, ball

    difficulty = show_menu()

    # Устанавливаем изображение мяча в зависимости от сложности
    if difficulty == 'easy':
        ball_img = pygame.image.load('ball.png')
    else:
        ball_img = pygame.image.load('ball1.png')

    ball = ball_img.get_rect()
    ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        move_paddles(keys)
        move_ball()

        if score_left == 5:
            show_winner("Синий")
            return
        if score_right == 5:
            show_winner("Красный")
            return

        draw_field()
        screen.blit(ball_img, ball)
        pygame.draw.rect(screen, BLUE, left_paddle)
        pygame.draw.rect(screen, RED, right_paddle)
        draw_score()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Запуск игры
if __name__ == "__main__":
    game_loop()
