import pygame
import sys
import random
import pickle
import os

speed = 15

# window sizes
frame_size_x = 1380
frame_size_y = 840

check_errors = pygame.init()

if check_errors[1] > 0:
    print("Error " + check_errors[1])
else:
    print("Game Successfully initialized")

# initialize game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
violet = pygame.Color(148, 0, 211)
yellow = pygame.Color(255, 255, 0)
celeste = pygame.Color(0, 255, 255)
gray = pygame.Color(128, 128, 128)

# initial snake color
snake_color = green

fps_controller = pygame.time.Clock()
# one snake square size
square_size = 60

# variable to store the highest score
high_score = 0
high_score_file = "high_score.pkl"
volume = 0.5


def load_high_score():
    global high_score
    if os.path.exists(high_score_file):
        with open(high_score_file, 'rb') as file:
            high_score = pickle.load(file)


def save_high_score():
    with open(high_score_file, 'wb') as file:
        pickle.dump(high_score, file)


load_high_score()


def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction, last_food_pos
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    last_food_pos = None
    spawn_food()
    score = 0


def spawn_food():
    global food_pos, food_spawn, last_food_pos
    while True:
        new_food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                        random.randrange(1, (frame_size_y // square_size)) * square_size]
        if new_food_pos != last_food_pos:
            food_pos = new_food_pos
            food_spawn = True
            break


init_vars()


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)

    game_window.blit(score_surface, score_rect)


def show_high_score(color, font, size):
    high_score_font = pygame.font.SysFont(font, size)
    high_score_surface = high_score_font.render(
        "High Score: " + str(high_score), True, color)
    high_score_rect = high_score_surface.get_rect()
    high_score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.15)

    game_window.blit(high_score_surface, high_score_rect)


def play_menu_music():
    pygame.mixer.music.load('hola.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)


def stop_menu_music():
    pygame.mixer.music.stop()


def set_volume(new_volume):
    global volume
    volume = new_volume
    pygame.mixer.music.set_volume(volume)


def main_menu():
    global snake_color
    play_menu_music()
    menu_options = ["Play Game", "Change Color",
                    "Options", "Show High Score", "Exit"]
    selected_option = 0

    while True:
        game_window.fill(black)
        title_font = pygame.font.SysFont('consolas', 60)
        title_surface = title_font.render("Snake Game", True, green)
        game_window.blit(title_surface, (frame_size_x / 3, frame_size_y / 8))

        menu_font = pygame.font.SysFont('consolas', 50)

        for i, option in enumerate(menu_options):
            color = white
            if i == selected_option:
                option = "-> " + option
                color = yellow
            menu_surface = menu_font.render(option, True, color)
            game_window.blit(menu_surface, (frame_size_x /
                             3, frame_size_y / 3 + i * 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Play Game
                        stop_menu_music()
                        return
                    elif selected_option == 1:  # Change Color
                        change_color_menu()
                    elif selected_option == 2:  # Options
                        options_menu()
                    elif selected_option == 3:  # Show High Score
                        show_record()
                    elif selected_option == 4:  # Exit
                        save_high_score()
                        pygame.quit()
                        sys.exit()


def options_menu():
    menu_options = ["Volume: " + str(int(volume * 100)) + "%", "Back"]
    selected_option = 0

    while True:
        game_window.fill(black)
        menu_font = pygame.font.SysFont('consolas', 50)

        for i, option in enumerate(menu_options):
            color = white
            if i == selected_option:
                option = "-> " + option
                color = yellow
            menu_surface = menu_font.render(option, True, color)
            game_window.blit(menu_surface, (frame_size_x /
                             3, frame_size_y / 3 + i * 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Adjust Volume
                        adjust_volume_menu()
                        menu_options[0] = "Volume: " + \
                            str(int(volume * 100)) + "%"
                    elif selected_option == 1:  # Back
                        return
                elif event.key == pygame.K_ESCAPE:
                    return


def adjust_volume_menu():
    global volume
    adjusting = True

    while adjusting:
        game_window.fill(black)
        menu_font = pygame.font.SysFont('consolas', 50)

        volume_surface = menu_font.render(
            f'Volume: {int(volume * 100)}%', True, white)
        game_window.blit(volume_surface, (frame_size_x / 3, frame_size_y / 3))

        back_surface = menu_font.render(
            'Use LEFT/RIGHT to adjust, ENTER to confirm', True, white)
        game_window.blit(
            back_surface, (frame_size_x / 3, frame_size_y / 3 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    volume = max(0.0, volume - 0.1)
                    set_volume(volume)
                elif event.key == pygame.K_RIGHT:
                    volume = min(1.0, volume + 0.1)
                    set_volume(volume)
                elif event.key == pygame.K_RETURN:
                    adjusting = False


def show_record():
    while True:
        game_window.fill(black)
        record_font = pygame.font.SysFont('consolas', 50)
        record_surface = record_font.render(
            f'High Score: {high_score}', True, white)
        back_surface = record_font.render('Press ESC to go back', True, white)
        game_window.blit(record_surface, (frame_size_x / 3, frame_size_y / 3))
        game_window.blit(back_surface, (frame_size_x / 3, frame_size_y / 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


def change_color_menu():
    global snake_color
    colors = {
        "Violet": violet,
        "Red": red,
        "Blue": blue,
        "Green": green,
        "Yellow": yellow,
        "Celeste": celeste,
        "Gray": gray
    }

    menu_options = list(colors.keys())
    selected_option = 0

    while True:
        game_window.fill(black)
        menu_font = pygame.font.SysFont('consolas', 50)

        for i, color_name in enumerate(menu_options):
            color = white
            if i == selected_option:
                color_name = "-> " + color_name
                color = colors[color_name.split(' ')[-1]]
            menu_surface = menu_font.render(color_name, True, color)
            game_window.blit(menu_surface, (frame_size_x /
                             4, frame_size_y / 6 + i * 70))

        back_surface = menu_font.render('Press ESC to go back', True, white)
        game_window.blit(back_surface, (frame_size_x / 4,
                         frame_size_y / 6 + len(menu_options) * 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    selected_color_name = menu_options[selected_option]
                    snake_color = colors[selected_color_name]
                    return
                elif event.key == pygame.K_ESCAPE:
                    return


def game_loop():
    global direction, head_pos, snake_body, food_pos, food_spawn, score, last_food_pos, high_score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord("w") and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord("s") and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT or event.key == ord("a") and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT or event.key == ord("d") and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    main_menu()
                    return

        if direction == "UP":
            head_pos[1] -= square_size
        elif direction == "DOWN":
            head_pos[1] += square_size
        elif direction == "LEFT":
            head_pos[0] -= square_size
        else:
            head_pos[0] += square_size

        if head_pos[0] < 0:
            head_pos[0] = frame_size_x - square_size
        elif head_pos[0] > frame_size_x - square_size:
            head_pos[0] = 0
        elif head_pos[1] < 0:
            head_pos[1] = frame_size_y - square_size
        elif head_pos[1] > frame_size_y - square_size:
            head_pos[1] = 0

        # eating apple
        snake_body.insert(0, list(head_pos))
        if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
            last_food_pos = food_pos
            if score > high_score:
                high_score = score
                save_high_score()
        else:
            snake_body.pop()

        # spawn food
        if not food_spawn:
            spawn_food()

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, snake_color, pygame.Rect(
                pos[0] + 2, pos[1] + 2,
                square_size - 2, square_size - 2))

        pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0],
                                                       food_pos[1], square_size, square_size))

        # game over conditions
        for block in snake_body[1:]:
            if head_pos[0] == block[0] and head_pos[1] == block[1]:
                init_vars()

        show_score(1, white, 'consolas', 20)
        show_high_score(white, 'consolas', 20)
        pygame.display.update()
        fps_controller.tick(speed)


main_menu()
while True:
    game_loop()
