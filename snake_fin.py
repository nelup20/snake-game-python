import pygame, sys, time, random


difficulty = 25

frame_size_x = 720
frame_size_y = 480

# White border/play-area 
border_size_x = 650
border_size_y = 380
border_pos_x = 35
border_pos_y = 50

check_errors = pygame.init()

if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


fps_controller = pygame.time.Clock()


snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

# Food position will be within the white border, 4 is border_pos_x / 10 + 0.5, 6 is border_pos_y / 10 + 1, 
food_pos = [random.randrange(4, ((border_size_x-border_pos_x)//10)) * 10, random.randrange(6, ((border_size_y-border_pos_y)//10)) * 10]
food_spawn = True


direction = 'RIGHT'
change_to = direction

score = 0

speed_multiplier = 1
food_range_multiplier = 1

def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    # 3 secunde ii pre mult ptu sleep imo
    time.sleep(1)
    pygame.quit()
    sys.exit()


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Multiply by speed_multiplier
    if direction == 'UP':
        snake_pos[1] -= 10 * speed_multiplier
    if direction == 'DOWN':
        snake_pos[1] += 10 * speed_multiplier
    if direction == 'LEFT':
        snake_pos[0] -= 10 * speed_multiplier
    if direction == 'RIGHT':
        snake_pos[0] += 10 * speed_multiplier

    snake_body.insert(0, list(snake_pos))

    # Am facut aici ca sa fie un range/game de valori. Ca daca faci exact == atunci cind ridici viteza snakeu nu poate sa ajunga fix la pozitia aceea, asa ca mai bine am pus ca daca valoarea positiei la snake e mai mare decit valaoare pozitiei la food - the multiplier 
    if snake_pos[0] > food_pos[0] - food_range_multiplier and snake_pos[0] < food_pos[0] +  food_range_multiplier and snake_pos[1] > food_pos[1] - food_range_multiplier and snake_pos[1] < food_pos[1] + food_range_multiplier:
        score += 1
        food_spawn = False

        #aici la fiecare +10 puncte (10, 20, 30 etc.) speed multiplier + food_range_multiplier se ridica, adica la 10 puncte speed o sa fie 10 * 1.5, la 20 o sa fie 10 * 2.0
        if score % 10 == 0:
            speed_multiplier += 0.5
            food_range_multiplier += 5
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(4, ((border_size_x-border_pos_x)//10)) * 10, random.randrange(6, ((border_size_y-border_pos_y)//10)) * 10]
    food_spawn = True

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(int(pos[0]), int(pos[1]), 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    #Draw white rectangle, final argument 5 = width --> makes only border white, inside is transparent
    pygame.draw.rect(game_window, pygame.Color(255,255,255), pygame.Rect(border_pos_x, border_pos_y, border_size_x, border_size_y), 5)

    #Game Over if you cross any of the borders. Add border position + length/height of the border to get the true position (X,Y); -5 here is just to adjust so it visually is more correct, if u get rid of -5 you'll see it's not 100% perfect 
    if snake_pos[0] < 0 or snake_pos[0] >= border_size_x + border_pos_x - 5 or snake_pos[0] < border_pos_x:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] >= border_size_y + border_pos_y or snake_pos[1] < border_pos_y:
        game_over()
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    fps_controller.tick(difficulty)