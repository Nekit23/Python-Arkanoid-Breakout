import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800 # размер окна
fps = 60 
# насройки платформы
paddle_w = 330
paddle_h = 40
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h) #paddle экземпляр класса прямоугольник
# настройки мяча
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect) #ball экземпляр класса прямоугольник
dx, dy = 1, -1
# настройки блоков.Количество цветов в списке должно соответствовать количеству блоков в списке
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(5)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(5)]

pygame.init()#Инициализация функции pygame,в случае сбоя модуля не будет вызывать никаких исключений
sc = pygame.display.set_mode((WIDTH, HEIGHT))#display.set_mode создает игровое поле с заданными размерами
clock = pygame.time.Clock()#Объект clock позволяет контролировать частоту кадров в игре
# Фоновая картинка
img = pygame.image.load('1.jpg').convert()

#Создание в игре паузы
def pause():
    paused = True
    while paused:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        


        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
        clock.tick(15)

#Обнаружение столкновений мяча с блоками
def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAUSE:
            print
    
    sc.blit(img, (0, 0))
    # Прорисовка мира
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('blue'), paddle)
    pygame.draw.circle(sc, pygame.Color('yellow'), ball.center, ball_radius)
    # Движения мяча
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    # столкновения слева справа
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    # столкновения сверху
    if ball.centery < ball_radius:
        dy = -dy
    # столкновения с платформой
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
        # if dx > 0:
        #     dx, dy = (-dx, -dy) if ball.centerx < paddle.centerx else (dx, -dy)
        # else:
        #     dx, dy = (-dx, -dy) if ball.centerx >= paddle.centerx else (dx, -dy)
    # столкновения блоков
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        # special effect
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
    # Победа и проигрыш
    if ball.bottom > HEIGHT:
        print('GAME OVER!')
        exit()
    elif not len(block_list):
        print('WIN!!!')
        exit()
    # Контроль перемещения платформы
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed
    if key[pygame.K_ESCAPE]:
        pause()
    # Обновление экрана
    pygame.display.flip()
    clock.tick(fps) 
