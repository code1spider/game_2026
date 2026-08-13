import pygame
import os

pygame.init()

# Constants
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10

screen = pygame.display.set_mode(
    (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)
)
pygame.display.set_caption("Map 1")

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

# Load image
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

def find_tile(tile_value, tile_map):
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == tile_value:
                return x, y
    return None

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

    
    

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw map
# Draw map
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        tile = map_one[y][x]
        screen.blit(
            tile_images[tile],
            (x * TILE_SIZE, y * TILE_SIZE)
        )

# Draw player ON TOP of the map
draw_player()

pygame.display.flip()


pygame.quit()