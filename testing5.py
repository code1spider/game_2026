import pygame
import os
import time

pygame.init()
clock = pygame.time.Clock()

#HIDDEN SETTINGS

# Variables to track movement cooldown (in milliseconds)
MOVE_COOLDOWN = 200  # 0.2 seconds = 200ms
last_move_time = 0

# Constants
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10

SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE + 90

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("Map 1")
FONT = pygame.font.Font(None, 28)
#MAP

# Map 1
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

# LOAD IMAGES

def load_image(name):
    path = os.path.join("assets", name)
    return pygame.transform.scale(
        pygame.image.load(path).convert_alpha(),
        (TILE_SIZE, TILE_SIZE)
    )

# Only the images actually used by map 1
tile_images = {
    0: load_image("floor.png"),
    1: load_image("path.png"),
    2: load_image("debris.png"),
    3: load_image("machine.png"),
    4: load_image("floor.png"),
    5: load_image("doorshadow.png"),
}

#MAP PLAYER INTERACTIONS

def find_tile(tile_value, tile_map):
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == tile_value:
                return x, y
    return None

#MOVEMENT

# Walkability
def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return current_map[y][x] not in (2, 3)
    return False

player_image = load_image('Player.png')
current_map = map_one
player_pos = list(find_tile(5, current_map))

# Draw player
def draw_player():
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

def update_player_movement():
    global player_pos, last_move_time
    current_time = pygame.time.get_ticks()
    new_x, new_y = player_pos
    keys = pygame.key.get_pressed()

    # 2. Check if enough time has passed since the last move
    if current_time - last_move_time >= MOVE_COOLDOWN:
        moved = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if is_walkable(new_x - 1, new_y):
                new_x -= 1
                moved = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if is_walkable(new_x + 1, new_y):
                new_x += 1
                moved = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if is_walkable(new_x, new_y - 1):
                new_y -= 1
                moved = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if is_walkable(new_x, new_y + 1):
                new_y += 1
                moved = True

        # 3. If the player moved, update the position and reset the cooldown timer
        if moved:
            player_pos = [new_x, new_y]
            last_move_time = current_time

# INPUTS (will need to put HOW I'm going to change my game in here)

Input_boxes = {
    'row': pygame.Rect(
        10, MAP_HEIGHT * TILE_SIZE + 10, 80, 35),

    'col': pygame.Rect(
        110, MAP_HEIGHT * TILE_SIZE + 10, 80, 35),

    'value': pygame.Rect(
        210, MAP_HEIGHT * TILE_SIZE + 10, 80, 35),
}



input_text = {
    'row': '',
    'col': '',
    'value': ''
}


active_box = None #makes the selected box none at default, so boxes arent randomly selected

BUTTON_RECT = pygame.Rect(310, MAP_HEIGHT * TILE_SIZE + 10, 100, 35)

#MESSAGE

status_message = '' #AKA nothing by, just making empty space for WHEN it is called

#TILE CHANGING LOGIC

def change_tile():
    global status_message

    try:

        row = int(input_text["row"])
        col = int(input_text["col"])
        new_val = int(input_text["value"])

        #check if cordinates value is valid
        if not (0 <= row < MAP_HEIGHT):
            status_message = 'Column must be withing 0 and 9.'
            return

        if not (0 <= col < MAP_WIDTH):
            status_message = 'Column must be withing 0 and 9.'
            return
#check if tile value even exists
        if new_val not in tile_images:
            status_message = 'Tile number not valid.'
            return

#actually changing the tile
        current_map[row][col] = new_val

        # Clear input boxes
        input_text["row"] = ''
        input_text["col"] = ''
        input_text["value"] = ''

    except ValueError:

        status_message ='Error'

#Draw functions

def Draw_Input_boxes():

    control_y = MAP_HEIGHT * TILE_SIZE

    pygame.draw.rect(screen, (30, 30, 30),(0, control_y, SCREEN_WIDTH, 90)
    )

    #Needed for the input boxes, and lets the name apply to it
    row_label = FONT.render("Row", True,(255, 255, 255))
    column_label = FONT.render("Column", True,(255, 255, 255))
    value_label = FONT.render("Tile", True,(255, 255, 255))


    screen.blit(row_label, (10, control_y + 47))
    screen.blit(column_label, (110, control_y + 47))
    screen.blit(value_label, (210, control_y + 47))

# Draw actual input boxes
    for name, rect in Input_boxes.items():

        if active_box == name:
            color = (100, 180, 60)
        else:
            color = (255, 255, 255)

        pygame.draw.rect(screen, color, rect, 2)

        text_surface = FONT.render(input_text[name], True, (255, 255, 255))

        screen.blit(text_surface,(
        rect.x + 5,
        rect.y + 10
        ))

# DRAW CHANGE BUTTON
    pygame.draw.rect(screen, (70, 200, 70), BUTTON_RECT)

    button_text = FONT.render('change', True, (255, 255, 255))

    screen.blit(button_text, 
    (BUTTON_RECT.x + 5, 
    BUTTON_RECT.y + 3))

    #Draw in the status messages
    status_text = FONT.render(status_message, True, (255, 220, 200))

    screen.blit(status_text, (400, control_y + 20))

#main game loop

running = True


while running:

    #python events



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #mouse click code
    
        elif event.type == pygame.MOUSEBUTTONDOWN:

            active_box = None

            #check input boxes
            for name, rect in Input_boxes.items():

                if rect.collidepoint(event.pos):
                    active_box = name

            #check swapping/change button
            if BUTTON_RECT.collidepoint(event.pos):
                change_tile()

#KEYBOARD INPUTS

        elif event.type == pygame.KEYDOWN:

            #only works if a box is selected
            if active_box is not None:

            #backspace
                if event.key == pygame.K_BACKSPACE:

                    input_text[active_box] = (
                        input_text[active_box][:-1]
                    )


                #enter
                if event.key == pygame.K_RETURN:

                    change_tile()

                    #number keys
                elif event.unicode.isdigit():

                    input_text[active_box] += event.unicode

#player movement

    update_player_movement()

# Draw map

    for y in range(MAP_HEIGHT):

        for x in range(MAP_WIDTH):

            tile = current_map[y][x]

            screen.blit(
                tile_images[tile],
                (x * TILE_SIZE, y * TILE_SIZE)
            )

    # Draw player
    draw_player()

    #draw input controls

    Draw_Input_boxes()

    # Update the display as per FPS
    pygame.display.flip()
    clock.tick(60)  

    # Movement logic for player


pygame.quit()


