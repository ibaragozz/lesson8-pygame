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
YELLOW = (255, 255, 0)

# Параметры игры
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Ракетки
left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Мяч
ball_img = pygame.image.load('ball.png')
ball = ball_img.get_rect()
ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2

# Счет
score_left = 0
score_right = 0

# Шрифты
font = pygame.font.Font(None, 74)


def draw_field():
    # Рисуем зеленое поле
    screen.fill(GREEN)

    # Рисуем центральную линию
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

    # Рисуем центральный круг
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 70, 5)

    # Рисуем штрафные зоны
    pygame.draw.rect(screen, WHITE, (0, HEIGHT // 4, 50, HEIGHT // 2), 5)
    pygame.draw.rect(screen, WHITE, (WIDTH - 50, HEIGHT // 4, 50, HEIGHT // 2), 5)


def move_paddles(keys):
    # Движение левой ракетки
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # Движение правой ракетки
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED


def move_ball():
    global BALL_SPEED_X, BALL_SPEED_Y, score_left, score_right

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Отскок от верхнего и нижнего края
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y

    # Отскок от ракеток
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        BALL_SPEED_X = -BALL_SPEED_X

    # Забитый мяч
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()


def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
    BALL_SPEED_X = -BALL_SPEED_X


def draw_score():
    left_text = font.render(str(score_left), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))

    right_text = font.render(str(score_right), True, WHITE)
    screen.blit(right_text, (WIDTH * 3 // 4, 20))


def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        move_paddles(keys)
        move_ball()

        draw_field()
        screen.blit(ball_img, ball)
        pygame.draw.rect(screen, YELLOW, left_paddle)
        pygame.draw.rect(screen, YELLOW, right_paddle)
        draw_score()

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    game_loop()
