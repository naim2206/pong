import pygame

pygame.init()

FPS = 60
VEL = 3
VEL_BALL = 7
WIDTH, HEIGHT = 900, 500
WIDTH_PLAYER = 10
HEIGHT_PLAYER = 70
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINNER_FONT = pygame.font.SysFont("comicsans", 100)
POINTS_FONT = pygame.font.SysFont("comicsans", 50)
HIT_EVENT = pygame.USEREVENT + 1

left_points = 5
right_points = 5
run = True

draw_left_points = POINTS_FONT.render(str(left_points), 1, WHITE)
draw_right_points = POINTS_FONT.render(str(right_points), 1, WHITE)


def draw_window(left, right, ball, draw_left_points, draw_right_points):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, left)
    pygame.draw.rect(WIN, WHITE, right)
    pygame.draw.rect(WIN, WHITE, ball)
    WIN.blit(draw_left_points, (WIDTH // 2 - 20, 50))
    WIN.blit(draw_right_points, (WIDTH // 2 + 20, 50))
    pygame.display.update()


def left_handle_movement(keys_pressed, left):
    if keys_pressed[pygame.K_w] and left.y - VEL > 0:
        left.y -= VEL
    if keys_pressed[pygame.K_s] and left.y + VEL + left.height < HEIGHT - 15:
        left.y += VEL


def right_handle_movement(keys_pressed, right):
    if keys_pressed[pygame.K_UP] and right.y - VEL > 0:
        right.y -= VEL
    if keys_pressed[pygame.K_DOWN] and right.y + VEL + right.height < HEIGHT - 15:
        right.y += VEL


def ball_handle_movement(ball):
    global hit_player, hit_wall
    if hit_player == True:
        ball.x += VEL_BALL
    else:
        ball.x -= VEL_BALL

    if ball.y - VEL < 0 or ball.y + VEL + ball.height > HEIGHT - 15:
        hit_wall = not (hit_wall)

    if hit_wall:
        ball.y += VEL_BALL // 2
    else:
        ball.y -= VEL_BALL // 2


def handle_ball_hit(ball, left, right):
    if left.colliderect(ball) or right.colliderect(ball):
        pygame.event.post(pygame.event.Event(HIT_EVENT))


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH // 2 - draw_text.get_width() // 2,
            HEIGHT // 2 - draw_text.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    global hit_player, hit_wall, HEIGHT_PLAYER, VEL_BALL, left_points, right_points, run, VEL_BALL
    hit_player = True
    hit_wall = True
    left = pygame.Rect(10, HEIGHT // 2 - 50, WIDTH_PLAYER, HEIGHT_PLAYER)
    right = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, WIDTH_PLAYER, HEIGHT_PLAYER)
    ball = pygame.Rect(20, HEIGHT // 2 - 5, 10, 10)

    draw_left_points = POINTS_FONT.render(str(left_points), 1, WHITE)
    draw_right_points = POINTS_FONT.render(str(right_points), 1, WHITE)

    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == HIT_EVENT:
                hit_player = not (hit_player)

        if ball.x - VEL < 0:
            left_points -= 1
            VEL_BALL += 0.5
            main()
        elif ball.x + VEL + ball.width > WIDTH:
            right_points -= 1
            VEL_BALL += 0.5

            main()

        if left_points == 0:
            try:
                draw_winner("Right wins")
            except:
                break
            run = False
        if right_points == 0:
            try:
                draw_winner("Left wins")
            except:
                break
            run = False

        try:
            keys_pressed = pygame.key.get_pressed()
        except:
            break

        left_handle_movement(keys_pressed, left)
        right_handle_movement(keys_pressed, right)
        ball_handle_movement(ball)
        handle_ball_hit(ball, left, right)

        draw_window(left, right, ball, draw_left_points, draw_right_points)

    pygame.quit()


if __name__ == "__main__":
    main()
# main()
