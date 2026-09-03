import pygame
import os
import time
import random


# ============================================================
# PYGAME SETUP
# ============================================================

pygame.init()
clock = pygame.time.Clock()




# ============================================================
# HIDDEN SETTINGS
# ============================================================

# Variables to track movement cooldown (in milliseconds)
MOVE_COOLDOWN = 200  # 0.2 seconds = 200ms
last_move_time = 0

room_number = 1




# ============================================================
# MAP / TILE SETTINGS
# ============================================================

MAP_WIDTH = 10
MAP_HEIGHT = 10

TILE_WIDTH = 80
TILE_HEIGHT = 40

def load_map(map_number):

    return [row[:] for row in maps[map_number]]




# ============================================================
# 2.5D SETTINGS
# ============================================================


GAME_WIDTH = 800
GAME_HEIGHT = 750

OBJECT_HEIGHT = 100
PLAYER_HEIGHT = 100


UI_HEIGHT = 100


SCREEN_WIDTH = GAME_WIDTH
SCREEN_HEIGHT = GAME_WIDTH + UI_HEIGHT


# ============================================================
# SCREEN SETUP
# ============================================================

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("Map 1")

FONT = pygame.font.Font(None, 28)


# ============================================================
# MAP
# ============================================================

## Isometric needs origins

MAP_ORIGIN_X = SCREEN_WIDTH // 2
MAP_ORIGIN_Y = 180

# ============================================================
# MAP 1
# ============================================================

map_one = [
    [0, 0, 0, 0, 6, 6, 0, 2, 0, 0],
    [0, 2, 2, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 0],
    [2, 0, 0, 0, 1, 1, 0, 2, 2, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 2, 0, 0, 1, 1, 0, 0, 2, 0],
    [0, 2, 2, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 5, 5, 0, 3, 0, 0],
]


# ============================================================
# MAP 2
# ============================================================

map_two = [
    [0, 0, 0, 2, 6, 6, 2, 0, 0, 0],
    [0, 2, 0, 2, 0, 1, 2, 0, 0, 0],
    [0, 2, 0, 0, 0, 1, 0, 0, 2, 0],
    [0, 0, 0, 2, 0, 1, 0, 2, 2, 0],
    [0, 0, 2, 2, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 0, 0, 0],
    [0, 2, 2, 0, 0, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 3, 2, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]


# ============================================================
# MAP 3
# ============================================================

map_three = [
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 2, 2, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 2, 2, 0, 0, 0, 0],
    [2, 0, 2, 0, 0, 0, 3, 2, 2, 0],
    [6, 0, 2, 0, 1, 1, 0, 0, 0, 0],
    [6, 0, 0, 0, 1, 1, 0, 2, 0, 0],
    [0, 2, 0, 0, 1, 1, 0, 2, 2, 0],
    [0, 2, 2, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]


# ============================================================
# MAP 4
# ============================================================

map_four = [
    [0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
    [0, 2, 0, 2, 0, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 1, 0, 0, 2, 0],
    [0, 0, 0, 2, 2, 1, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 1, 0, 2, 0, 6],
    [0, 0, 2, 0, 0, 1, 0, 2, 2, 6],
    [0, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 0, 2, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]


# ============================================================
# MAP 5
# ============================================================

map_five = [
    [0, 0, 0, 0, 6, 6, 0, 0, 0, 0],
    [0, 2, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 2, 0, 1, 0, 2, 0, 2, 0],
    [2, 0, 0, 0, 1, 0, 0, 0, 2, 0],
    [0, 0, 2, 0, 1, 0, 2, 2, 0, 0],
    [0, 2, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 2, 2, 0, 0, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 2, 2, 0, 0],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]


# ============================================================
# MAP 6
# ============================================================

map_six = [
    [0, 2, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 2, 0, 2, 2, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 2, 0],
    [2, 2, 0, 0, 1, 1, 0, 2, 2, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 2, 0, 0],
    [0, 2, 2, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 2, 0, 2, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 5, 5, 0, 0, 6, 6],
]


# ============================================================
# MAP 7
# ============================================================

map_seven = [
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 2, 2, 0, 0, 2, 0, 2, 0, 0],
    [0, 0, 2, 0, 0, 2, 0, 0, 0, 0],
    [0, 2, 0, 0, 2, 0, 0, 2, 2, 0],
    [6, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 2, 2, 0, 2, 0, 2, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 2, 2, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]


maps = [
    map_one,
    map_two,
    map_three,
    map_four,
    map_five,
    map_six,
    map_seven
]


# ============================================================
# LOAD IMAGES
# ============================================================

##Loading images will need to be done vastly differently as they should NOT be constant, but rather able to be changed to allow 2.5D control
##Can use try code, aswell as checking for file names and could likely use alpha for the player to not overwrite the tiles
##Could likely use a tuple to use 'isinstance' which I have just learned on google summary AI

def load_image(name, dimensions=None):

    try:
        path = os.path.join("assets", name)

        img_surface = pygame.image.load(path).convert_alpha()

        if isinstance(dimensions, (tuple, list)) and len(dimensions) == 2: #2 because it is needed for the precise length I need I think (More testing later)
            img_surface = pygame.transform.smoothscale(
                img_surface,
                dimensions
            )

        return img_surface

    #except statement needed for try function
    except pygame.error as e:
        raise FileNotFoundError(
            f"Unable to load image '{name}': {e}"
        )


# ============================================================
# TILE IMAGES
# ============================================================

# Only the images actually used by map 1

tile_images = {
    0: load_image("floor.png"),
    1: load_image("path.png"),
    2: load_image("debris.png"),
    3: load_image("machine.png"),
    4: load_image("floor.png"),
    5: load_image("doorshadow.png"),
    6: load_image("doorshadow.png"),
}


# ============================================================
# FLOOR IMAGES
# ============================================================

##floor images are resized to the size of one isometric tile

floor_images = {}

for tile_id in (0, 1, 5, 6):

    floor_images[tile_id] = pygame.transform.smoothscale(
        tile_images[tile_id],
        (TILE_WIDTH, TILE_HEIGHT)
    )


# ============================================================
# PLAYER IMAGE
# ============================================================

player_image = load_image(
    'Player.png'
)


# ============================================================
# MAP / PLAYER INTERACTIONS
# ============================================================

def find_tile(tile_value, tile_map):

    for y, row in enumerate(tile_map):

        for x, tile in enumerate(row):

            if tile == tile_value:

                return x, y

    return None

# change starting map, aswell as player position (this should be easy as the player will always spawn in the same spot, but this means a tile 5 could be anywhere)
current_map_number = 0

current_map = load_map(current_map_number)

player_pos = list(find_tile(5, current_map))

# ============================================================
# MAP ROOM PROGRESSION
# ============================================================

#this will make it so reaching the end will bring you to another map, I will however want to have fixed milestones for rooms here

specific_map_connections = {
    #this is where I can force milestones, useful for certain rooms, I'll update this later
}

def move_to_next_map():

    global current_map_number, current_map, player_pos
    global room_number

    room_number += 1


    # Check if there's a specific connection for the current map

    if current_map_number in specific_map_connections:

        current_map_number = (
            specific_map_connections[current_map_number]
        )

    else:

        # Default behavior: randomly select another map

        possible_maps = list(
            range(len(maps))
        )

        # Don't immediately load the same map twice

        if len(possible_maps) > 1:

            possible_maps.remove(
                current_map_number
            )

        current_map_number = random.choice(
            possible_maps
        )

    # Change the actual map

    current_map = load_map(current_map_number)

    # Start at the entrance

    player_pos = list(
        find_tile(5, current_map)
    )

        

# ============================================================
# ISOMETRIC CONVERSION
# ============================================================

##grid into isometric conversion

def grid_to_screen(x, y):

    display_x = MAP_ORIGIN_X + (x - y) * (TILE_WIDTH // 2)
    display_y = MAP_ORIGIN_Y + (x + y) * (TILE_HEIGHT // 2)

    return display_x, display_y


# ============================================================
# DIAMOND POINTS
# ============================================================

##diamond point

def get_diamond_points(center_x, center_y):

    half_width = TILE_WIDTH // 2
    half_height = TILE_HEIGHT // 2

    return (
        (center_x, center_y - half_height),  # Top
        (center_x + half_width, center_y),   # Right
        (center_x, center_y + half_height),  # Bottom
        (center_x - half_width, center_y)    # Left
    )


# ============================================================
# DRAW FLOOR TILE
# ============================================================

##draw floor tile

def draw_floor_tile(x, y, image):

    center_x, center_y = grid_to_screen(x, y)

    tile_surface = pygame.Surface(
        (TILE_WIDTH, TILE_HEIGHT),
        pygame.SRCALPHA
    )

    tile_surface.blit(
        image,
        (0, 0)
    )

    mask = pygame.Surface(
        (TILE_WIDTH, TILE_HEIGHT),
        pygame.SRCALPHA
    )

    mask_points = (
        (TILE_WIDTH // 2, 0),  # Top
        (TILE_WIDTH, TILE_HEIGHT // 2),  # Right
        (TILE_WIDTH // 2, TILE_HEIGHT),  # Bottom
        (0, TILE_HEIGHT // 2)  # Left
    )

    pygame.draw.polygon(
        mask,
        (255, 255, 255),
        mask_points
    )

    tile_surface.blit(
        mask,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    screen.blit(
        tile_surface,
        (
            center_x - TILE_WIDTH // 2,
            center_y - TILE_HEIGHT // 2
        )
    )


# ============================================================
# FAILSAFE FLOOR
# ============================================================

##in case of glitching- extra floor

def draw_failsafe_floor(x, y):

    center_x, center_y = grid_to_screen(x, y)

    pygame.draw.polygon(
        screen,
        (100, 100, 100),
        get_diamond_points(center_x, center_y)
    )

    pygame.draw.polygon(
        screen,
        (0, 0, 0),
        get_diamond_points(center_x, center_y),
        1
    )


# ============================================================
# UPRIGHT OBJECTS
# ============================================================

##Add extra details, upright objects

def draw_object(
    x,
    y,
    image,
    height=OBJECT_HEIGHT
):

    center_x, center_y = grid_to_screen(x, y)

    image_width = image.get_width()
    image_height = image.get_height()


    ##keep original proportions of the image, but also allow for height to be added to the image, so it can be seen as upright

    scale = min(
        TILE_WIDTH / image_width,
        height / image_height
    )

    new_width = max(
        1,
        int(image_width * scale)
    )

    new_height = max(
        1,
        int(image_height * scale)
    )

    scaled_image = pygame.transform.smoothscale(
        image,
        (
            new_width,
            new_height
        )
    )


    #shadow effect for the object, so it looks like it is standing upright

    shadow_rect = pygame.Rect(
        0,
        0,
        TILE_WIDTH // 2,
        TILE_HEIGHT // 4
    )

    shadow_rect.center = (
        center_x,
        center_y + 2
    )

    pygame.draw.ellipse(
        screen,
        (20, 20, 20),
        shadow_rect
    )

    screen.blit(
        scaled_image,
        (
            center_x - new_width // 2,
            center_y - new_height
        )
    )


# ============================================================
# PLAYER DRAWING
# ============================================================

##draw player

def draw_player():

    x, y = player_pos

    center_x, center_y = grid_to_screen(x, y)

    image_width = player_image.get_width()
    image_height = player_image.get_height()


    #keep proportions of the player image, but also allow for height to be added to the image, so it can be seen as upright

    scale = min(
        TILE_WIDTH / image_width,
        PLAYER_HEIGHT / image_height
    )

    new_width = max(
        1,
        int(image_width * scale)
    )

    new_height = max(
        1,
        int(image_height * scale)
    )

    scaled_player_image = pygame.transform.smoothscale(
        player_image,
        (
            new_width,
            new_height
        )
    )


    ##player shadow effect, so it looks like it is standing upright

    shadow_rect = pygame.Rect(
        0,
        0,
        TILE_WIDTH // 2,
        TILE_HEIGHT // 4
    )

    shadow_rect.center = (
        center_x,
        center_y + 2
    )

    pygame.draw.ellipse(
        screen,
        (20, 20, 20),
        shadow_rect
    )

    screen.blit(
        scaled_player_image,
        (
            center_x - new_width // 2,
            center_y - new_height
        )
    )


# ============================================================
# DRAW MAP
# ============================================================

def draw_map():

    for y in range(MAP_HEIGHT):

        for x in range(MAP_WIDTH):

            tile = current_map[y][x]

            if tile in floor_images:

                draw_floor_tile(
                    x,
                    y,
                    floor_images[tile]
                )

            else:

                draw_failsafe_floor(
                    x,
                    y
                )


    objects = []

    for y in range(MAP_HEIGHT):

        for x in range(MAP_WIDTH):

            tile = current_map[y][x]

            if tile in (2, 3):

                objects.append(
                    (
                        x + y,
                        x,
                        y,
                        tile_images[tile]
                    )
                )



    objects.sort(
        key=lambda item: item[0]
    )


    for depth, x, y, image in objects:

        draw_object(
            x,
            y,
            image
        )


# ============================================================
# WALKABILITY
# ============================================================

def is_walkable(x, y):

    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:

        return current_map[y][x] not in (2, 3)

    return False

# ============================================================
# CHECK ADJACENCY
# ============================================================
#this will be used to only make tile changer usable in certain situations, I will use this for later puzzles

def is_adjacent_to_tile(tile_value): #tile value must be a seperate function of tile_value = 3 for example

    player_x, player_y = player_pos

    adjacent_tiles = [
        (player_x - 1, player_y),  # Left
        (player_x + 1, player_y),  # Right
        (player_x, player_y - 1),  # Up
        (player_x, player_y + 1)   # Down
    ]

    for x, y in adjacent_tiles:
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            if current_map[y][x] == tile_value:
                return True

    return False

# ============================================================
# PLAYER MOVEMENT
# ============================================================

##player movement

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

            if current_map[new_y][new_x] == 6:

                move_to_next_map()


# ============================================================
# TILE EDITOR / INPUTS
# ============================================================

## inputs

CONTROL_Y = GAME_HEIGHT + 10


Input_boxes = {

    'row': pygame.Rect(
        10,
        CONTROL_Y,
        80,
        35
    ),

    'col': pygame.Rect(
        110,
        CONTROL_Y,
        80,
        35
    ),

    'value': pygame.Rect(
        210,
        CONTROL_Y,
        80,
        35
    ),
}


input_text = {
    'row': '',
    'col': '',
    'value': ''
}


active_box = None #makes the selected box none at default, so boxes arent randomly selected

BUTTON_RECT = pygame.Rect(
    310,
    CONTROL_Y,
    100,
    35
)


# ============================================================
# STATUS MESSAGE
# ============================================================

#MESSAGE

status_message = '' #AKA nothing by, just making empty space for WHEN it is called


# ============================================================
# TILE CHANGING LOGIC
# ============================================================

def change_tile():

    global status_message

    try:

        row = int(input_text["row"])
        col = int(input_text["col"])
        new_val = int(input_text["value"])


        #check if cordinates value is valid

        if not (0 <= row < MAP_HEIGHT):

            status_message = 'Row must be within 0 and 9.'

            return


        if not (0 <= col < MAP_WIDTH):

            status_message = 'Column must be within 0 and 9.'

            return

        
        # ====================================================
        # EXIT PROTECTION
        # ====================================================

        #This must be added here as tile 6 HAS to be added to the banned list first
        #can not change existing tile 6
        if current_map[row][col] == 6:

            status_message = 'Cannot change exit tile.'

            return

        #new exit tiles cant be made

        if new_val == 6:

            status_message = 'Cannot create exit tile.'

            return

        # ====================================================
        # CHECK TILE VALUE
        # ====================================================

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

        status_message = 'Tile changed'


    except ValueError:

        status_message = 'Error'


# ============================================================
# DRAW INPUT BOXES / UI
# ============================================================

#Draw functions

def Draw_Input_boxes():

    control_y = CONTROL_Y #this makes sure i dont make a caps lock error, as I have done before


    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (0, control_y, SCREEN_WIDTH, UI_HEIGHT)
    )


    #Needed for the input boxes, and lets the name apply to it

    row_label = FONT.render(
        "Row",
        True,
        (255, 255, 255)
    )

    column_label = FONT.render(
        "Column",
        True,
        (255, 255, 255)
    )

    value_label = FONT.render(
        "Tile",
        True,
        (255, 255, 255)
    )


    screen.blit(
        row_label,
        (10, control_y + 47)
    )

    screen.blit(
        column_label,
        (110, control_y + 47)
    )

    screen.blit(
        value_label,
        (210, control_y + 47)
    )


    # Draw actual input boxes

    for name, rect in Input_boxes.items():

        if active_box == name:

            color = (100, 180, 60)

        else:

            color = (255, 255, 255)


        pygame.draw.rect(
            screen,
            color,
            rect,
            2
        )


        text_surface = FONT.render(
            input_text[name],
            True,
            (255, 255, 255)
        )


        screen.blit(
            text_surface,
            (
                rect.x + 5,
                rect.y + 10
            )
        )


    # DRAW CHANGE BUTTON

    pygame.draw.rect(
        screen,
        (70, 200, 70),
        BUTTON_RECT
    )


    button_text = FONT.render(
        'change',
        True,
        (255, 255, 255)
    )


    screen.blit(
        button_text,
        (
            BUTTON_RECT.x + 5,
            BUTTON_RECT.y + 3
        )
    )


    #Draw in the status messages

    status_text = FONT.render(
        status_message,
        True,
        (255, 220, 200)
    )


    screen.blit(
        status_text,
        (
            400,
            control_y + 20
        )
    )

# ============================================================
# ROOM NUMBER DISPLAY
# ============================================================

#shows my room number

def draw_room_number():

    room_text = FONT.render(
        f"Room: {room_number}",
        True,
        (255, 255, 255)
    )

    text_rect = room_text.get_rect(
        center=(
SCREEN_WIDTH // 2, 70
        )
    )

    screen.blit(
        room_text,
        text_rect
    )


# ============================================================
# MAIN GAME LOOP
# ============================================================

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


    # ========================================================
    # DRAW EVERYTHING
    # ========================================================

    # Draw map

    screen.fill((0, 0, 0))

    draw_room_number()

    draw_map()


    draw_player()


    #draw input controls
    if is_adjacent_to_tile(3):

        Draw_Input_boxes()




    # Update the display as per FPS

    pygame.display.flip()

    clock.tick(60)


    # Movement logic for player


pygame.quit()