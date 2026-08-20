import pygame
import os
import time

pygame.init()
clock = pygame.time.Clock()

running = True

#HIDDEN SETTINGS

# Variables to track movement cooldown (in milliseconds)
MOVE_COOLDOWN = 200  # 0.2 seconds = 200ms
last_move_time = 0

# Constants
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10

screen = pygame.display.set_mode(
    (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)
)
pygame.display.set_caption("Map 1")

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
    
    'Column': pygame.Rect(90, MAP_HEIGHT * TILE_SIZE + 10, 80, 35),

    "Value":  pygame.Rect(210, MAP_HEIGHT * TILE_SIZE + 10, 80, 35),

}

input_text = {
    'row': '',
    'Column': '',
    'Value': ''
}

selected_box = None #makes the selected box none at default, so boxes arent randomly selected

Button_Rect = pygame.Rect(310, MAP_HEIGHT * TILE_SIZE + 10, 100, 35)

#MESSAGE

Status_message = '' #AKA nothing by, just making empty space for WHEN it is called

#TILE CHANGING LOGIC

def tile_edit():
    global status_message

    try:

        row = int(input_text["row"])
        col = int(input_text["col"])
        new_val = int(input_text["value"])

        #check if cordinates value is valid
        if not (0 <= row < MAP_HEIGHT):
            Status_message = 'Column must be withing 0 and 9.'
            return

        if not (0 <= row < MAP_WIDTH):
            Status_message = 'Column must be withing 0 and 9.'
            return
#check if tile value even exists
        if new_val not in tile_images:
            Status_message = 'Tile number not valid.'
            return

#actually changing the tile
        current_map[row][column] = new_val

        Status_message = 'success'

    except ValueError:

        Status_message ='Error'

#Draw functions

def draw_input_boxes():

    control_y = MAP_HEIGHT * TILE_SIZE

    pygame.draw.rect(screen, (30, 30, 30),(0, control_y, SCREEN WIDTH, 90)
    )

    screen.blit(row_label, (10, control_y + 47))
    screen.blit(column_label, (110, control_y + 47))
    screen.blit(value_label, (210, control_y + 47))

# Draw actual input boxes

def print_map(grid):
    """Helper function to print the map nicely."""
    for row in grid:
        print(" ".join(str(cell) for cell in row))
    print("-" * 20)

while running:
    def test():

        keys = pygame.key.get_pressed()

        if keys[pygame.K_b]:

            try:
                # 2. Ask user for directions/coordinates
                # Remember: Python lists are 0-indexed (0 to 9 for a 10x10 grid)
                row = int(input("Enter row index (0-9): "))
                col = int(input("Enter column index (0-9): "))
                new_val = int(input("Enter new value for this tile: "))

                # 3. Update the specific grid position directly
                map_one[row][col] = new_val

                # 4. Show the updated map
                print("\nUpdated Map:")
                print_map(map_one)

            #will occur if the row and index are not correctly usable
            except IndexError:
                print("Error: Coordinate out of bounds! Choose numbers between 0 and 9.")
            except ValueError:
                print("Error: Please enter numbers only.")
    

#MAIN LOOP

# Needed for Pygame to run
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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


    # Update the display as per FPS
    pygame.display.flip()
    clock.tick(60)  

    # Movement logic for player


pygame.quit()


