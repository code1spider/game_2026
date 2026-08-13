import pygame
import sys
import os
import time
import random

# Constants

game_state = "main"
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10
WINDOW_WIDTH = MAP_WIDTH * TILE_SIZE
WINDOW_HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60

# Map definitions
map_one = [
    [0, 0, 4, 3, 3, 3, 3, 4, 2, 0],
    [0, 0, 0, 4, 3, 3, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 0, 0, 0, 0],
    [2, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 2, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 2],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]

map_two = [
    [6, 6, 6, 6, 5, 5, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [9, 1, 1, 1, 1, 1, 1, 1, 1, 8],
    [9, 1, 1, 1, 1, 1, 1, 1, 1, 8],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
]

map_three = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

map_four = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 10, 0, 0, 0, 9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Puzzle variables
start_1 = 0
pins_clicked = [False] * 8
pin_values = [10, 5, 15, 20, 5, 10, -5, -10]
pin_rects = []
for i in range(8):
    col = i % 4
    row = i // 4
    x = 100 + col * 60
    y = 100 + row * 60
    pin_rects.append(pygame.Rect(x, y, 40, 40))

# Initialize Pygame
pygame.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tile Map with Entities + Chase")
clock = pygame.time.Clock()

# Load image helper
def load_image(name):
    path = os.path.join("assets", name)
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), (TILE_SIZE, TILE_SIZE))

# Load tiles
tile_images = {
    0: load_image("floor.png"),
    1: load_image("path.png"),
    2: load_image("debris.png"),
    3: load_image("machine.png"),
    4: load_image("floor.png"),  # Marker for friend spawn
    5: load_image("doorshadow.png"),
    6: load_image("floor.png"),
    8: load_image("doorshadow.png"),
    9: load_image("doorshadow.png"),
    10: load_image("letter.png"),
    11: load_image("friend.png")
}

# Load entities
player_image = load_image("player.png")
friend_image = load_image("friend.png")
end_led_off = load_image("end_led_off.png")
end_led_on = load_image("end_led_on.png")
end_led_wrong = load_image("end_led_wrong.png")

# --- Add enemy setup ---
enemy_image = load_image("enemy.png")  # make sure this asset exists
enemy_pos = [0, 0]
enemy_active = False  # turns on when in map_three
ENEMY_MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_MOVE_EVENT, 500)

# Utility to find the first tile with a given value
def find_tile(tile_value, tile_map):
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == tile_value:
                return x, y
    return None

# Prompt for player name
def get_player_name_and_code():
    name_input = ""
    input_active = True
    input_box = pygame.Rect(100, 200, 200, 40)
    font_big = pygame.font.SysFont(None, 36)

    while input_active:
        screen.fill((0, 0, 0))
        prompt = font_big.render("Enter your name:", True, (255, 255, 255))
        screen.blit(prompt, (100, 150))

        txt_surface = font_big.render(name_input, True, (255, 255, 0))
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name_input:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                else:
                    name_input += event.unicode

        pygame.display.flip()
        clock.tick(30)

    # --- Access code logic ---
    if len(name_input) == 1:
        return name_input, 2571  # fallback if name too short
        print(f"[DEBUG] Name: 2571")

    second_char = name_input[1].lower()

    if not second_char.isalpha():
        return name_input, 17  # fallback if second char is not a letter

    # Access code is position in alphabet: a=1, b=2, ..., z=26
    alphabet_code = ord(second_char) - ord('a') + 1
    access_code = int(f"25{alphabet_code}")


    print(f"[DEBUG] Name: {name_input}, Second letter: '{second_char.upper()}', Access Code: {access_code}")

    return name_input, access_code


player_name, access_code_room3 = get_player_name_and_code()

# Current map and player position — start on map_two tile 5
current_map = map_two
player_pos = list(find_tile(5, current_map))

friend_pos = [8, 3]  # stays static for now

# Walkability
def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return current_map[y][x] not in (2, 3)
    return False


# Draw map
def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = current_map[y][x]
            image = tile_images.get(tile)
            if image:
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

# Draw player
def draw_player():
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

# Show interaction message
def show_message(text):
    msg = font.render(text, True, (255, 255, 255))
    screen.blit(msg, (20, WINDOW_HEIGHT - 40))

# Draw puzzle screen
def draw_puzzle():
    screen.fill((10, 10, 10))
    big_font = pygame.font.SysFont(None, 48)
    text = big_font.render("Circuit Puzzle: Solve the numbers!", True, (0, 255, 0))
    screen.blit(text, (50, 20))

    for i, rect in enumerate(pin_rects):
        color = (100, 100, 100) if not pins_clicked[i] else (0, 200, 0)
        pygame.draw.rect(screen, color, rect)
        pin_text = font.render(f"Pin {i+1}", True, (255, 255, 255))
        screen.blit(pin_text, (rect.x, rect.y - 20))

    if all(pins_clicked):
        if start_1 == 50:
            screen.blit(end_led_on, (400, 100))
            win_text = font.render("Correct combination!", True, (0, 255, 0))
            screen.blit(win_text, (400, 160))
        else:
            screen.blit(end_led_wrong, (400, 100))
            lose_text = font.render("Incorrect. Try again.", True, (255, 0, 0))
            screen.blit(lose_text, (400, 160))
    else:
        screen.blit(end_led_off, (400, 100))

    value_text = font.render(f"Value: {start_1}", True, (255, 255, 0))
    screen.blit(value_text, (50, 300))

# Puzzle logic
def handle_puzzle():
    global game_state, start_1, pins_clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_state = "main"
            start_1 = 0
            pins_clicked = [False] * 8
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(pin_rects):
                if rect.collidepoint(mouse_pos) and not pins_clicked[i]:
                    start_1 += pin_values[i]
                    pins_clicked[i] = True

# Game loop
running = True
dontspam = 0
new_x, new_y = player_pos

while running:
    screen.fill((0, 0, 0))

    if game_state != "puzzle":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    keys = pygame.key.get_pressed()

    if game_state == 'puzzle':
        handle_puzzle()
        draw_puzzle()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Drawing
    draw_map()
    draw_player()

    current_tile = current_map[player_pos[1]][player_pos[0]]

    if game_state == "main":
        if current_tile == 4:
            show_message("Press E to interact.")
            dontspam = 1
            if keys[pygame.K_e]:
                game_state = "puzzle"
        else:
            dontspam = 0
    
    if game_state == 'main':
        if current_tile == 10:
            show_message("Press E to interact.")

    pygame.display.flip()
    clock.tick(FPS)

    # Movement logic for player
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if is_walkable(new_x - 1, new_y):
            new_x -= 1
            time.sleep(0.2)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if is_walkable(new_x + 1, new_y):
            new_x += 1
            time.sleep(0.2)
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        if is_walkable(new_x, new_y - 1):
            new_y -= 1
            time.sleep(0.2)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if is_walkable(new_x, new_y + 1):
            new_y += 1
            time.sleep(0.2)

    player_pos = [new_x, new_y]

    # After moving, check if on tile 5 to switch maps
    current_tile = current_map[player_pos[1]][player_pos[0]]

    if current_tile == 5:
        if current_map == map_one:
            current_map = map_two
            player_pos = (4, 1)
            new_x, new_y = player_pos
        else:
            current_map = map_one
            player_pos = (4, 8)
            new_x, new_y = player_pos

    # Password / code input when on tile 8 in map_two
    if current_tile == 8 and current_map == map_two:
        code_input = ""
        input_box = pygame.Rect(100, 200, 200, 40)
        font_big = pygame.font.SysFont(None, 36)
        entering = True
        while entering:
            screen.fill((0, 0, 0))
            prompt = font_big.render(f"Access Code Required, {player_name}:", True, (255, 255, 255))
            screen.blit(prompt, (50, 150))
            txt_surface = font_big.render(code_input, True, (255, 255, 0))
            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if code_input.isdigit() and int(code_input) == access_code_room3:
                            current_map = map_three
                            print(f"[DEBUG] NOTICE: END OF DEMO")
                            player_pos = [1, 4]
                            
                            # Activate enemy in chase mode
                            enemy_active = True
                            # Choose a spawn position for enemy not same as player & walkable
                            while True:
                                ex = random.randint(0, MAP_WIDTH - 1)
                                ey = random.randint(0, MAP_HEIGHT - 1)
                                if [ex, ey] != player_pos and current_map[ey][ex] != 2:
                                    enemy_pos = [ex, ey]
                                    break

                            entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        code_input = code_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        entering = False

                    else:
                        if len(code_input) < 4 and event.unicode.isdigit():
                            code_input += event.unicode
        new_x, new_y = player_pos

    # If in map_three tile 8, go back and disable chase
    elif current_tile == 8 and current_map == map_three:
        current_map = map_two
        player_pos = [8, 4]
        new_x, new_y = player_pos
        enemy_active = True

    # Spawn enemy at a random walkable position, not on player





    # Switch map if on tile 9
    if current_tile == 9:
        if current_map == map_two:
            current_map = map_four
            player_pos = [8, 4]
        else:
            current_map = map_two
            player_pos = [1, 5]
        new_x, new_y = player_pos


    # Letter overlay for tile 10
    if current_tile == 10:
        if keys[pygame.K_e]:
            screen = pygame.display.set_mode((400, 400))
            pygame.display.set_caption("Letter Overlay Example")
            letter_image = pygame.image.load("code.png")
            letter_image = pygame.transform.scale(letter_image, screen.get_size())
            show_letter = True
            while show_letter:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        show_letter = False
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        show_letter = False
                screen.fill((0, 0, 0))
                screen.blit(letter_image, (0, 0))
                pygame.display.flip()

pygame.quit()
sys.exit()
