import pygame
import os
import time
import random
import math #math is being added for later features


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
# GAME STATE
# ============================================================

#this will control things that can happen to the player, and the state of the room (safe/unsafe)

game_over = False
jumpscare_active = False

#used for cowardice (enemy_3)
enemy_active = False

#Used to stop player movement during an event
player_locked = False

# ============================================================
# enemy 2
# ============================================================

ENEMY_2_FIRST_ROOM = 20
ENEMY_2_LATER_CHANCE = 0.05

#time until active

FLUX_COOLDOWN = 10000

#active duration
FLUX_ACTIVE_DURATION = 2500
FLUX_SHAKE_DURATION = 2000
ENEMY_SHAKE_AMOUNT = 5

#lights flicker
SPAWN_FLICKER_DURATION = 2000

# ============================================================
# screen shake
# ============================================================

FLUX_PRE_SHAKE_DURATION = 1500

FLUX_POST_SHAKE_DURATION = 1500

FLUX_MILD_SHAKE_AMOUNT = 3

FLUX_MAJOR_SHAKE_AMOUNT = 8

SHAKE_UPDATE_INTERVAL = 35

# ============================================================
# enemy 3
# ============================================================

COWARDICE_LOCKER_TIME = 8000

COWARDICE_FACE_FADE_TIME = 5000

COWARDICE_JUMPSCARE_DELAY = 3000

cowardice_active = False

cowardice_cause = None

cowardice_start_time = 0

cowardice_enter_time = 0

# ============================================================
# FLUX STATE
# ============================================================

enemy_active = False
enemy_position = None

flux_timer_start = 0
flux_active_start = 0

flux_departure_time = 0

spawn_flicker_start = 0
spawn_flicker_active = False

LOCKER_INTERACTION_DISTANCE = 1.35

current_locker = None
is_hiding = False

flux_has_appeared = False
flux_encounter_finished = False

# ============================================================
# screen shake state
# ============================================================

shake_offset_x = 0
shake_offset_y = 0
last_shake_update = 0

# ============================================================
# ENEMY SETTINGS - temporarily commented out to focus on map
# ============================================================
#
## Enemy settings will eventually be moved here so that enemy behaviour can be changed without digging through the rest of the code.
#
#ENEMY_MOVE_COOLDOWN = 100
#enemny_last_move_time = 0
#
#enemy_pos = None
#enemy_direction = (0, 1)
#
#enemy_active = False
#
# ============================================================
# TILE IDs
# ============================================================

#keeping tile IDs named makes the map easier to understand, especially for coding

TILE_FLOOR = 0
TILE_PATH = 1
TILE_DEBRIS = 2
TILE_MACHINE = 3
TILE_FLOOR_ALT = 4
TILE_ENTRANCE = 5
TILE_EXIT = 6

# ============================================================
# MAP / TILE SETTINGS
# ============================================================

MAP_WIDTH = 12
MAP_HEIGHT = 12

TILE_WIDTH = 80
TILE_HEIGHT = 40

def load_map(map_number):

    return [row[:] for row in maps[map_number]]




## ============================================================
## 2.5D SETTINGS
## this section has been removed because it draws isometric, I will use faux 3D in its place
## ============================================================
#
#
#GAME_WIDTH = 800
#GAME_HEIGHT = 750
#
#OBJECT_HEIGHT = 100
#PLAYER_HEIGHT = 100
#
#
#UI_HEIGHT = 100
#
#
#SCREEN_WIDTH = GAME_WIDTH
#SCREEN_HEIGHT = GAME_WIDTH + UI_HEIGHT


# ============================================================
# FAUX 3D
# ============================================================

GAME_WIDTH = 800
GAME_HEIGHT = 650

UI_HEIGHT = 100

SCREEN_WIDTH = GAME_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT + UI_HEIGHT #Im adding the UI height in case I keep the tile changing logic

FOV = math.pi / 3

#number of rays is how many raycast rays, the column_width is how many in how small a space (making it accurate)
NUM_RAYS = 500
COLUMN_WIDTH = SCREEN_WIDTH / NUM_RAYS
PLAYER_RADIUS = 0.18

#Max distance the player will see before fog of war
MAX_DEPTH = 20

#used for raycasting logic for later

MOVE_SPEED = 3.0

TURN_SPEED = 2.2

#angle the player starts at
PLAYER_START_ANGLE = -math.pi / 2

# ============================================================
# SCREEN SETUP
# ============================================================

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

#removed pygame.display.set_caption("Map 1") as it is used for the isometric function aswell
pygame.display.set_caption("Faux 3D Map")

FONT = pygame.font.Font(None, 28)


# ============================================================
# MAP
#removed as this is for isometric, not faux 3D
# ============================================================
#
### Isometric needs origins
#
#MAP_ORIGIN_X = SCREEN_WIDTH // 2
#MAP_ORIGIN_Y = 180
#
# ============================================================
# MAP 1
# ============================================================

map_one = [
    [2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 6, 6, 0, 2, 0, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 2, 0, 0, 0, 1, 1, 0, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 0, 2, 0, 0, 1, 1, 0, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 7, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2],
    [2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 5, 5, 0, 3, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


# ============================================================
# MAP 2
# ============================================================

map_two = [
    [2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 6, 6, 0, 2, 0, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 2, 0, 0, 0, 1, 1, 0, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 1, 1, 0, 7, 0, 0, 2],
    [2, 0, 2, 0, 0, 1, 1, 0, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2],
    [2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 5, 5, 0, 3, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


# ============================================================
# MAP 3
# ============================================================

map_three = [
    [2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 6, 6, 0, 2, 0, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 2, 0, 0, 0, 1, 1, 0, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 0, 2, 0, 0, 1, 1, 7, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2],
    [2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 5, 5, 0, 3, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


# ============================================================
# MAP 4
# ============================================================

map_four = [
    [2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 6, 6, 0, 2, 0, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 2, 0, 0, 0, 1, 1, 7, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 0, 2, 0, 0, 1, 1, 0, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2],
    [2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 5, 5, 0, 3, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


# ============================================================
# MAP 5
# ============================================================

map_five = [
    [2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 6, 6, 0, 2, 0, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 2, 0, 0, 0, 1, 1, 0, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 1, 1, 7, 0, 0, 0, 2],
    [2, 0, 2, 0, 0, 1, 1, 0, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2],
    [2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 5, 5, 0, 3, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


# ============================================================
# MAP 6
# ============================================================

map_six = [
    [2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 6, 6, 0, 2, 0, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 2, 0, 0, 0, 1, 1, 0, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 0, 2, 0, 0, 1, 1, 7, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2],
    [2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 5, 5, 0, 3, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


# ============================================================
# MAP 7
# ============================================================

map_seven = [
    [2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 6, 6, 0, 2, 0, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 2, 0, 0, 0, 1, 1, 7, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2],
    [2, 0, 2, 0, 0, 1, 1, 0, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2],
    [2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 0, 0, 0, 5, 5, 0, 3, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
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
    7: load_image('machine.png')
}

# ============================================================
# FAUX 3D TEXTURES
# used to get the textures for the wall, roof, and door, these are just placeholders for now
# ============================================================

wall_texture = load_image("grass.png")
roof_texture = load_image("water.png")
door_texture = load_image("enemy.png")

try:
    
    locker_texture = load_image(
        "locker.png"
    )

except FileNotFoundError:

    locker_texture = door_texture


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

# removed player_pos = list(find_tile(5, current_map)) as it relys on the normal isometric grid

spawn_x, spawn_y = find_tile(TILE_ENTRANCE, current_map) #this is the new code that does nearly the same thing- making the player spawn on a tile 5 (the grid checks the same way per, so you always spawn on the left or right one btw)

player_x = spawn_x + 0.5
player_y = spawn_y + 0.5
#0.5 was chosen as it allows smaller movements than 1, making it feel like like a grid

player_angle = PLAYER_START_ANGLE #this is useless in practicality, but if I mispell one, this will fix it


# ============================================================
# Cowardice reset
# ============================================================

def reset_cowardice():

    global cowardice_active
    global cowardice_cause
    global cowardice_start_time
    global locker_enter_time

    cowardice_active = False
    cowardice_cause = None

    cowardice_start_time = 0
    locker_enter_time = 0

# ============================================================
# MAP ROOM PROGRESSION
# ============================================================

#this will make it so reaching the end will bring you to another map, I will however want to have fixed milestones for rooms here

specific_map_connections = {
    #this is where I can force milestones, useful for certain rooms, I'll update this later
}

def move_to_next_map():

#added more code to use for my textures 

    #changed global current_map_number, current_map, player_pos to exclude player_pos
    global current_map_number, current_map
    global current_map
    global player_x
    global player_y
    global player_angle
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
# reworked the below code as my globals have changed
#    player_x = spawn_x + 0.5
#    player_y = spawn_y + 0.5
#    player_angle = PLAYER_START_ANGLE

    spawn = find_tile(
        TILE_ENTRANCE,
        current_map
    )

    #will return an error if the map, for any reason, lacks an entrance
    if spawn is None:

        raise ValueError(
            f'Map {current_map_number + 1} '
            'does not contain an entrance tile'
        )

    spawn_x, spawn_y = spawn

    #put the player in the middle of the entrance tiles- makes the game more uniform and clean since it uses an even amount of space

    player_x = spawn_x + 0.5
    player_y = spawn_y + 0.5

    # Reset facing direction

    player_angle = PLAYER_START_ANGLE

# ============================================================
# OBJECT SETTINGS
# ============================================================

#this is where special properties can be added, like debris blocking movement and vision, or a machine may block movement but not vision, more tile types will be added in future so this will be updated appropriately

OBJECT_PROPERTIES = {
    2: {  # Debris
        'blocks_movement': True,
        'blocks_vision': True
    },

    3: {  # Machine,
        'blocks_movement': True,
        'blocks_vision': False
    },

    7: {
        'blocks_movement': True,
        'blocks_vision': True
    }

}

# ============================================================
# FAUX 3D RAYCASTING
#this will be used, in future, for making breaking line of sight for enemys
# ============================================================

wall_depth_buffer = [MAX_DEPTH] * NUM_RAYS

def get_tile(x, y):

    x = int(x)
    y= int(y)

    if y < 0 or y >= len(current_map):
        return None
    if x < 0 or x >= len(current_map):
        return None

    return current_map[y][x]

def is_wall(x, y):

    tile = get_tile(x, y)

    #block movement and vision
    return tile in (TILE_DEBRIS, TILE_MACHINE, TILE_EXIT)

def player_can_move_to(x, y):
    radius = PLAYER_RADIUS

    checks = [
        (x - radius, y - radius),
        (x + radius, y - radius),
        (x - radius, y + radius),
        (x + radius, y + radius),
    ]

    for cx, cy in checks:

#outside the map is treated as solid so the player cant walk out of the map
        if get_tile(cx, cy) is None:
            return False

        if is_wall(cx, cy):
            return False

    return True

# ============================================================
# RAYCASTING
# ============================================================

def cast_ray(ray_angle):

    ray_dir_x = math.cos(ray_angle)
    ray_dir_y = math.sin(ray_angle)

    #from here, I can use intergration to allow for the ray casting by differentiating in regards to x and y
    map_x = int(player_x)
    map_y = int(player_y)

    delta_dist_x = (
        abs(1 / ray_dir_x)
        if ray_dir_x != 0
        else float('inf')
    )

    delta_dist_y = (
            abs(1 / ray_dir_y)
            if ray_dir_y != 0
            else float('inf')
        )

    if ray_dir_x < 0:

        step_x = -1
        side_dist_x = (
            player_x - map_x
        ) * delta_dist_x

    else:

        step_x = 1
        side_dist_x = (
            map_x + 1.0 - player_x
        ) * delta_dist_x


    if ray_dir_y < 0:

        step_y = -1
        side_dist_y = (
            player_y - map_y
        ) * delta_dist_y

    else:

        step_y = 1
        side_dist_y = (
            map_y + 1.0 - player_y
        ) * delta_dist_y

    side = 0

    while True:
        if side_dist_x < side_dist_y:

            side_dist_x += delta_dist_x
            map_x += step_x
            side = 0

        else:

            side_dist_y += delta_dist_y
            map_y += step_y
            side = 1

        if (
            map_x < 0
            or map_y < 0
            or map_y >= len(current_map)
            or map_x >= len(current_map[map_y])
        ):
            return MAX_DEPTH, side

        # Only debris and machines are rendered as walls.
        if is_wall(map_x, map_y):

            if side == 0:

                distance = (
                    map_x
                    - player_x
                    + (1 - step_x) / 2
                ) / ray_dir_x

            else:

                distance = (
                    map_y
                    - player_y
                    + (1 - step_y) / 2
                ) / ray_dir_y

            distance = max(distance, 0.001)

            return min(distance, MAX_DEPTH), side


def draw_world():

    global wall_depth_buffer

# ========================================================
# DRAW ROOF
#will have the roof use a texture
# ========================================================

    roof_scaled = pygame.transform.smoothscale(
        roof_texture,
        (
                SCREEN_WIDTH,
                SCREEN_HEIGHT // 2
        )
    )

    screen.blit(
        roof_scaled,
        (0, 0)
    )

# ========================================================
# DRAW FLOOR
#will have the floor use a texture
# ========================================================

    pygame.draw.rect(
        screen,
        (45, 45, 45),
        (
                0,
                GAME_HEIGHT // 2,
                SCREEN_WIDTH,
                GAME_HEIGHT // 2
        )
    )

# ========================================================
# Reset depth buffer
# needed to make player perseption work properly
# ========================================================

    wall_depth_buffer = [
        MAX_DEPTH
        for _ in range(NUM_RAYS)
    ]

# ========================================================
# Raycasting Every Column

# ========================================================

    for ray in range(NUM_RAYS):

        camera_x = (
            2 * ray / NUM_RAYS
        ) - 1

        ray_angle = (
            player_angle
            + camera_x * (FOV / 2)
        )

        distance, side = cast_ray(
            ray_angle
        )

        wall_depth_buffer[ray] = distance

# ========================================================
# Walls
#needed to make the walls have a limit
# ========================================================

        wall_height = int(
            GAME_HEIGHT / distance
        )
    
        wall_top = (
            GAME_HEIGHT // 2
            - wall_height // 2
        )
    
        wall_bottom = (
            GAME_HEIGHT // 2
            + wall_height // 2
        )
    
    # ====================================================
    # DISTANCE SHADING
    # ====================================================
    
        brightness = max(
            35,
            min(
                210,
                int(
                    220 /
                    (1 + distance * 0.08)
                )
            )
        )
    
        hit_x_exact = (
            player_x
            + math.cos(ray_angle) * distance
        )
    
        hit_y_exact = (
            player_y
            + math.sin(ray_angle) * distance
        )
    
        hit_x = int(hit_x_exact)
        hit_y = int(hit_y_exact)
    
        tile = get_tile(
            hit_x,
            hit_y
        )
    
    # ====================================================
    # choose textures
    # ====================================================
    
        if tile == TILE_EXIT:
        
            current_wall_texture = door_texture
    
        else:
        
            current_wall_texture = wall_texture
    
        x = int(
            ray * SCREEN_WIDTH / NUM_RAYS
        )
    
        width = (
            math.ceil(
                SCREEN_WIDTH / NUM_RAYS
            ) + 1
        )
    
    # ====================================================
    # find texture position
    # ====================================================
    
        texture_width = (
            current_wall_texture.get_width()
        )
    
        texture_height = (
            current_wall_texture.get_height()
        )
    
        if side == 0:
        
            wall_position = hit_y_exact
    
        else:
        
            wall_position = hit_x_exact
    
        texture_position = (
            wall_position
            - math.floor(wall_position)
        )
    
        texture_x = int(
            texture_position
            * texture_width
        )
    
        texture_x = max(
            0,
            min(
                texture_width - 1,
                texture_x
            )
        )
    
            # ====================================================
            # GET ONE VERTICAL STRIP
            # ====================================================
    
        texture_column = (
            current_wall_texture.subsurface(
                pygame.Rect(
                    texture_x,
                    0,
                    1,
                    texture_height
                )
            )
        )
    
            # ====================================================
            # STRETCH STRIP TO WALL HEIGHT
            # ====================================================
    
        texture_column = pygame.transform.scale(
            texture_column,
            (
                width,
                max(
                    1,
                    wall_bottom - wall_top
                )
            )
        )
    
            # ====================================================
            # shading
            # ====================================================
    
        shade_surface = pygame.Surface(
            texture_column.get_size(),
            pygame.SRCALPHA
        )
        shade_amount = (
            255 - brightness
        )
    
        shade_surface.fill(
            (
                0,
                0,
                0,
                shade_amount
            )
        )
    
        texture_column.blit(
            shade_surface,
            (0, 0)
        )
    
        #draw wall column
    
        screen.blit(
            texture_column,
            (
                x,
                wall_top
            )
        )
    
        #wall texture
    
        if tile == TILE_EXIT:
        
            current_wall_texture = door_texture
    
        else:
        
            current_wall_texture = wall_texture
    
        x = int(
            ray * SCREEN_WIDTH / NUM_RAYS
        )
    
        width = math.ceil(
            SCREEN_WIDTH / NUM_RAYS
        ) + 1
    
        #draw wall
    
        texture_width = current_wall_texture.get_width()
        texture_height = current_wall_texture.get_height()
    
        hit_x_exact = (
            player_x
            + math.cos(ray_angle) * distance
        )
    
        hit_y_exact = (
            player_y
            + math.sin(ray_angle) * distance
        )
    
        if side == 0:
        
            wall_position = hit_y_exact
    
        else:
        
            wall_position = hit_x_exact
    
        texture_position = (
                wall_position
                - math.floor(wall_position)
            )
    
        texture_x = int(
            texture_position * texture_width
        )
        # Prevent texture_x going outside the image.
        texture_x = max(
            0,
            min(
                texture_width - 1,
                texture_x
            )
        )
        # Get one vertical strip from the wall texture.
        texture_column = current_wall_texture.subsurface(
            pygame.Rect(
                texture_x,
                0,
                1,
                texture_height
            )
        )
        # Stretch that strip to the height of the wall.
        texture_column = pygame.transform.scale(
            texture_column,
            (
                width,
                max(
                    1,
                    wall_bottom - wall_top
                )
            )
        )
        # Apply distance shading.
        shade_surface = pygame.Surface(
            texture_column.get_size(),
            pygame.SRCALPHA
        )
        shade_amount = 255 - brightness
        shade_surface.fill(
            (
                0,
                0,
                0,
                shade_amount
            )
        )
        texture_column.blit(
            shade_surface,
            (0, 0)
        )
        # Draw the wall column.
        screen.blit(
            texture_column,
            (
                x,
                wall_top
            )
        )


# ============================================================
# DRAW FAUX 3D MAP
#this will be used to draw the map, different than just the tiles, this will actually be how it looks, the draw function will be the easiest way to do this
#removed, replaced with draw_world
# ============================================================
#
#def draw_faux_map():
#    #sky
#    pygame.draw.rect(
#        screen, 
#        (100, 15, 65),
#        (0, 0, GAME_WIDTH, GAME_HEIGHT // 2)
#    )
#
#    #floor
#    pygame.draw.rect(
#        screen, 
#        (55, 60, 140),
#        (
#            0,
#            GAME_HEIGHT // 2,
#            GAME_WIDTH,
#            GAME_HEIGHT // 2
#        )
#    )
#
#    column_width = GAME_WIDTH / RAY_COUNT
#
#    for ray_number in range(RAY_COUNT):
#
#        #position of the ray across the FOV
#        camera_x = ray_number / RAY_COUNT
#
#        ray_angle = (
#            player_angle
#            - FOV / 2
#            + camera_x * FOV
#        )
#
#        distance, hit_x, hit_y = cast_ray(ray_angle)
#
#        #correct distortion
#        corrected_distance = max(
#            distance *
#            math.cos(ray_angle - player_angle)
#        )
#
#        corrected_distance = max(
#            corrected_distance,
#            0.001
#        )
#
#        #height of walls
#        wall_height = (
#            GAME_HEIGHT /
#            corrected_distance
#        )
#
#        wall_height = min(
#            wall_height,
#            GAME_HEIGHT * 2
#        )
#
#        wall_top = (
#            GAME_HEIGHT // 2
#            - wall_height // 2
#        )
#
#        wall_color = (100, 100, 100)
#
#        if hit_x is not None and hit_y is not None:
#
#            tile = current_map[hit_y][hit_x]
#
#            if tile == TILE_DEBRIS:
#                wall_color = (110, 90, 80)
#
#            elif tile == TILE_MACHINE:
#                wall_color = (80, 80, 120)
#
#        pygame.draw.rect(
#            screen,
#            wall_color,
#            (
#                int(ray_number * column_width),
#                int(wall_top),
#                int(column_width) + 1,
#                int(wall_bottom - wall_top)
#                )
#        )
#
# ============================================================
# PLAYER DRAWING
#removed- this code has already been fufilled by the FOV
# ============================================================

##draw player
#
#def draw_player():
#
#    x, y = player_pos
#
#    center_x, center_y = grid_to_screen(x, y)
#
#    image_width = player_image.get_width()
#    image_height = player_image.get_height()
#
#
#    #keep proportions of the player image, but also allow for height to be added to the image, so it can be seen as upright
#
#    scale = min(
#        TILE_WIDTH / image_width,
#        PLAYER_HEIGHT / image_height
#    )
#
#    new_width = max(
#        1,
#        int(image_width * scale)
#    )
#
#    new_height = max(
#        1,
#        int(image_height * scale)
#    )
#
#    scaled_player_image = pygame.transform.smoothscale(
#        player_image,
#        (
#            new_width,
#            new_height
#        )
#    )
#
#
#    ##player shadow effect, so it looks like it is standing upright
#
#    shadow_rect = pygame.Rect(
#        0,
#        0,
#        TILE_WIDTH // 2,
#        TILE_HEIGHT // 4
#    )
#
#    shadow_rect.center = (
#        center_x,
#        center_y + 2
#    )
#
#    pygame.draw.ellipse(
#        screen,
#        (20, 20, 20),
#        shadow_rect
#    )
#
#    screen.blit(
#        scaled_player_image,
#        (
#            center_x - new_width // 2,
#            center_y - new_height
#        )
#    )
#
#
# ============================================================
# DRAW MAP
#also removed, replaced with draw_world
# ============================================================
#
#def draw_map():
#
#    for y in range(MAP_HEIGHT):
#
#        for x in range(MAP_WIDTH):
#
#            tile = current_map[y][x]
#
#            if tile in floor_images:
#
#                draw_floor_tile(
#                    x,
#                    y,
#                    floor_images[tile]
#                )
#
#            else:
#
#                draw_failsafe_floor(
#                    x,
#                    y
#                )
#
#
#    objects = []
#
#    for y in range(MAP_HEIGHT):
#
#        for x in range(MAP_WIDTH):
#
#            tile = current_map[y][x]
#
#            if tile in (2, 3):
#
#                objects.append(
#                    (
#                        x + y,
#                        x,
#                        y,
#                        tile_images[tile]
#                    )
#                )
#
#
#
#    objects.sort(
#        key=lambda item: item[0]
#    )
#
#
#    for depth, x, y, image in objects:
#
#        draw_object(
#            x,
#            y,
#            image
#        )
#
#
## ============================================================
## WALKABILITY
#removed to make 3D collision instead as this code was for isometric functions
## ============================================================
#
#def is_walkable(x, y):
#
#    if not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
#        return False
#
#    tile = current_map[y][x]
#
#    #check whether this object blocks movement
#    if tile in OBJECT_PROPERTIES:
#
#        if OBJECT_PROPERTIES[tile]["blocks_movement"]:
#            return False
#
#    return True

# ============================================================
# CHECK ADJACENCY
#this will be fixed as player_pos no longer exists, so I will fix this section
# ============================================================
#this will be used to only make tile changer usable in certain situations, I will use this for later puzzles

def is_adjacent_to_tile(tile_value): #tile value must be a seperate function of tile_value = 3 for example

    interaction_distance = 1.25

    for y, row in enumerate(current_map):

        for x, tile in enumerate(row):

            if tile == tile_value:

                tile_x = x + 0.5
                tile_y = y + 0.5

                distance = math.hypot(
                    player_x - tile_x,
                    player_y - tile_y
                )

                if distance <= interaction_distance:
                    return True
            
    return False

def exitable():
    return is_adjacent_to_tile(TILE_EXIT)

def next_room():
    if exitable():
        move_to_next_map()

# ============================================================
# FLUX timer helpers
# ============================================================

def get_flux_cooldown():

    if not flux_has_appeared:

        return 0

    if flux_encounter_finished:

        return 0

    now = pygame.time.get_ticks()

    elapsed = (
        now - flux_timer_start
    )

    remaining = (

        FLUX_COOLDOWN
        - elapsed
    )

    return max(
        0,
        remaining
    )

    def flux_is_in_active_phase():

        if not enemy_active:

            return False

        if flux_encounter_finished:

            return False

        if flux_active_start == 0:

            return False

        now = pygame.time.get_ticks()

        active_elapsed = (

            now
            - flux_active_start
        )

        return (
            active_elapsed >= 0
            and
            active_elapsed < FLUX_ACTIVE_DURATION
        )

        def flux_active_elapsed():

            if not flux_is_in_active_phase():

                return 0

            now = pygame.time.get_ticks()

            return (

                now
                - flux_active_start
            )

# ============================================================
# cowardice exit trigger
# ============================================================

def cowardice_exit_trigger():

    global cowardice_active
    global cowardice_cause
    global cowardice_start_time
    global player_locked

    if not flux_has_appeared:
        return False

    if flux_encounter_finished:

        return False

        if flux_is_in_active_phase():

            return False

        if(
            cowardice_active
            and
            cowardice_cause == 'exit'
        ):

            return True

        cowardice_active = True
        cowardice_cause = 'exit'

        cowardice_start_time = (
            pygame.get.get_ticks()
        )

        player_locked = True

        print(
            'Cowardice: escape attempt'
        )

        trigger_jumpscare(
            'cowardice'
        )

        return True

# ============================================================
# Next Room
# ============================================================

def next_room():

    if not exitable():

        return

    if flux_is_in_active_phase():

        trigger_jumpscare(
            'flux'
        )

        return

    if cowardice_exit_trigger():

        return

    move_to_next_map()

# ============================================================
# PLAYER MOVEMENT
#uses player_pos which no longer exists, so im fixing this section aswell
# ============================================================

##player movement

def update_player_movement(dt):

    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()


        # Turning
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_angle -= TURN_SPEED * dt

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_angle += TURN_SPEED * dt

    # Movement direction
    move_x = 0
    move_y = 0

    forward_x = math.cos(player_angle)
    forward_y = math.sin(player_angle)

    right_x = math.cos(player_angle + math.pi / 2)
    right_y = math.sin(player_angle + math.pi / 2)

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        move_x += forward_x
        move_y += forward_y

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        move_x -= forward_x
        move_y -= forward_y
    #commented out to free E key for now
    #if keys[pygame.K_q]:
    #    move_x -= right_x
    #    move_y -= right_y
#
    #if keys[pygame.K_e]:
    #    move_x += right_x
    #    move_y += right_y

    # Normalise movement
    length = math.hypot(move_x, move_y)

    if length > 0:
        move_x /= length
        move_y /= length

        movement = MOVE_SPEED * dt

        new_x = player_x + move_x * movement
        new_y = player_y + move_y * movement

        if player_can_move_to(new_x, player_y):
            player_x = new_x

        if player_can_move_to(player_x, new_y):
            player_y = new_y
# ============================================================
# ENEMY MOVEMENT
# ============================================================

##ememy movement is separate from player movement because enemies can have completely different movement speeds

def update_enemy():

    return

# ============================================================
# LOCKER SYSTEM
# ============================================================

def find_nearby_locker():

    best = None

    best_distance = (
        LOCKER_INTERACTION_DISTANCE
    )

    for y, row in enumerate(current_map):

        for x, tile in enumerate(row):

            if tile != TILE_LOCKER:

                continue
        
        distance = math.hypot(

            player_x - (x + 0.5)
            player_y - (y + 0.5)
        )

    return best

def enter_locker(locker):

    global current_locker
    global is_hiding
    global player_x
    global player_y
    global player_angle
    global locker_enter_time
 
    if locker is None:
 
        return
 
    current_locker = locker
 
    is_hiding = True
 
    locker_enter_time = (
        pygame.time.get_ticks()
    )

    if (
        cowardice_active
        and
        cowardice_cause == 'exit'
    ):

    reset_cowardice()

    print('Cowardice: escape attempt abandoned')

    elif cowardice_cause == 'locker':

        reset_cowardice()

    player_y = (
        locker[1] + 0.5
    )
 
    player_angle = (
        player_angle + math.pi
    )
 
    player_angle %= (
        math.pi * 2
    )
 
 
def leave_locker():
 
    global current_locker
    global is_hiding
    global player_x
    global player_y
 
    if current_locker is not None:
 
        lx, ly = current_locker
 
        possible_positions = (
 
            (
                lx + 0.5,
                ly - 0.65
            ),
 
            (
                lx + 0.5,
                ly + 1.65
            ),
 
            (
                lx - 0.65,
                ly + 0.5
            ),
 
            (
                lx + 1.65,
                ly + 0.5
            )
 
        )
 
        for px, py in possible_positions:
 
            if player_can_move_to(
                px,
                py
            ):
 
                player_x = px
                player_y = py
 
                break
 
    is_hiding = False
    current_locker = None

    if (
        cowardice_active
        and
        cowardice_cause == "locker"
 
    ):
 
        reset_cowardice()
 
        print(
            "COWARDICE: manifestation cancelled."
        )

# ============================================================
# set flux
# ============================================================

def setup_enemy_2():

    global enemy_active
    global enemy_position

    global flux_timer_start
    global flux_active_start
    global flux_departure_time

    global spawn_flicker_start
    global spawn_flicker_active

    global flux_has_appeared
    global flux_encounter_finished
 
    global shake_offset_x
    global shake_offset_y
    global last_shake_update

    enemy_active = False
    enemy_position = None

    flux_timer_start = 0
    flux_active_start = 0
    flux_departure_time = 0

    spawn_flicker_start = 0
    spawn_flicker_active = False

    flux_has_appeared = False
    flux_encounter_finished = False

    shake_offset_x = 0
    shake_offset_y = 0
    last_shake_update = 0

    if room_number < ENEMY_2_FIRST_ROOM:

        return

    if room_number == ENEMY_2_FIRST_ROOM:

        should_spawn = True

    else:

        should_spawn = (

            random.random()
            < ENEMY_2_LATER_CHANCE
        )

    if not should_spawn:

        return

    entrance = find_tile(
        TILE_ENTRANCE,
        current_map
    )

    if entrance is None

        return

    enemy_position = entrance

    enemy_active = True

    flux_has_appeared = True
    flux_encounter_finished = False

    now = pygame.time.get_ticks()

    flux_timer_start = now

    flux_active_start = 0

    flux_departure_time = 0

    spawn_flicker_start = now
    spawn_flicker_active = True

    print(f'Flux spawned in room {room_number}')

    print("Flux countdown started: 10 seconds")

# ============================================================
# Trigger jumpscare
# ============================================================

def trigger_jumpscare(cause='unknown'):

    global jumpscare_active
    global game_over
    global player_locked
    global death_cause

    if game_over:

        return

    death_cause = cause

    jumpscare_active = True
    game_over = True
    player_locked = True

# ============================================================
# Flux kill
# ============================================================

def flux_can_kill_player():

    if not flux_is_in_active_phase():

        return False

    if game_over:

        return False

    if is_hiding:

        return False

    return True

# ============================================================
# update flux
# ============================================================

def update_enemy_2():

    global spawn_flicker_active
    global flux_active_start
    global enemy_active
    global enemy_position
    global flux_encounter_finished
    global flux_department_time

    if not flux_has_appeared

        return

    if flux_encounter_finished:

        return

    now = pygame.time.get_ticks()

# ============================================================
# lights flicker
# ============================================================

if spawn_flicker_active:

    if (

        now - spawn_flicker_start
        >= SPAWN_FLICKER_DURATION
    ):

    spawn_flicker_active = False

# ============================================================
# grace period
# ============================================================

    countdown_elapsed = (

        now
        - flux_timer_start
    )

    if countdown_elapsed < FLUX_COUNTDOWN:

        return

# ============================================================
# flux active
# ============================================================

    if flux_active_start == 0:

        flux_active_start = now

        print("Flux active")

        print("Flux has 2.5 seconds")

# ============================================================
# active phase
# ============================================================

    active_elapsed = (
 
        now
        - flux_active_start
 
    )
 
    if active_elapsed < FLUX_ACTIVE_DURATION:

        return

# ============================================================
# flux leaves
# ============================================================

    enemy_active = False
    enemy_position = None
 
    flux_encounter_finished = True
 
    spawn_flicker_active = False
 
    flux_departure_time = now
 
    print(
        "FLUX has disappeared. Encounter finished."
    )
 
 
def update_enemy_flicker():
 
    update_enemy_2()

# ============================================================
# cowardice locker trigger
# ============================================================

def trigger_cowardice_locker():
 
    global cowardice_active
    global cowardice_cause
    global cowardice_start_time
 
    if game_over:
 
        return
 
    if (
 
        cowardice_active
        and
        cowardice_cause == "locker"
 
    ):
 
        return
 
    cowardice_active = True
 
    cowardice_cause = "locker"
 
    cowardice_start_time = (
        pygame.time.get_ticks()
    )
 
    print(
        "COWARDICE has noticed the player hiding."
    )

# ============================================================
# update cowardice
# ============================================================

def update_cowardice():

    if not cowardice_active:

        now = pygame.time.get_ticks()

        if (

            locker_enter_time > 0
            and
            now - locker_enter_time
            >= COWARDICE_LOCKER_TIME
        ):

            trigger_cowardice_locker()

        return
    
    if game_over:

        return

    now = pygame.time.get_ticks()

# ============================================================
# Locker cowardice
# ============================================================

    if cowardice_cause == "locker":
 
        if not is_hiding:
 
            reset_cowardice()
 
            return
 
        elapsed = (
 
            now
            - cowardice_start_time
 
        )
 
        total_time = (
 
            COWARDICE_FACE_FADE_TIME
            +
            COWARDICE_JUMPSCARE_DELAY
 
        )
 
        if elapsed >= total_time:
 
            trigger_jumpscare(
                "cowardice"
            )
 
            return

# ============================================================
# exit cowardice
#this doesnt do anything
# ============================================================

    elif cowardice_cause == 'exit':

        trigger_jumpscare(
            'cowardice'
        )

# ============================================================
# flux screen shake
# ============================================================

def get_flux_shake():

    global shake_offset_x
    global shake_offset_y
    global last_shake_update

    if is_hiding:

        shake_offset_x = 0
        shake_offset_y = 0

        return 0, 0

    if not flux_has_appeared:

        shake_offset_x = 0
        shake_offset_y = 0

        return 0, 0

    now = pygame.time.get_ticks()

    amount 0

    # ========================================================
    # BEFORE ACTIVE
    # ========================================================
 
    if (
 
        not flux_encounter_finished
        and
        flux_timer_start > 0
 
    ):
 
        elapsed = (
            now - flux_timer_start
        )
 
        time_until_active = (
 
            FLUX_COUNTDOWN
            - elapsed
 
        )
 
        if (
 
            time_until_active > 0
            and
            time_until_active <= FLUX_PRE_SHAKE_DURATION
 
        ):
 
            # Mild shake.
            amount = FLUX_MILD_SHAKE_AMOUNT
 
    # ========================================================
    # DURING ACTIVE
    # ========================================================
 
    if flux_is_in_active_phase():
 
        # Strong shake throughout the ENTIRE active phase.
        amount = FLUX_MAJOR_SHAKE_AMOUNT
 
    # ========================================================
    # AFTER FLUX LEAVES
    # ========================================================
 
    elif (
 
        flux_encounter_finished
        and
        flux_departure_time > 0
 
    ):
 
        elapsed_since_departure = (
 
            now
            - flux_departure_time
 
        )
 
        if (
 
            elapsed_since_departure
            < FLUX_POST_SHAKE_DURATION
 
        ):
 
            # Mild residual shaking.
            amount = FLUX_MILD_SHAKE_AMOUNT
 
    # ========================================================
    # NO SHAKE
    # ========================================================

    if amount <= 0:

        shake_offset_x = 0
        shake_offset_y = 0

        return 0, 0

    #random shake

    if (
        now - last_shake_update
        >= SHAKE_UPDATE_INTERVAL
    ):

    

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
# exit prompt
#will make a popup to leave when adjacent to or on an exit
# ============================================================

def draw_exit_prompt():

    if not exitable():
        return

    prompt_text = FONT.render(
        "Press E to interact",
        True,
        (255, 255, 255)
    )

    prompt_rect = prompt_text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            GAME_HEIGHT - 50
        )
    )

    #background

    background_rect = prompt_rect.inflate(30, 15)

    pygame.draw.rect(
        screen,
        (20, 20, 20),
        background_rect
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        background_rect,
        2
    )

    screen.blit(
        prompt_text,
        prompt_rect
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

    dt = clock.tick(60) / 1000.0

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

            if event.key == pygame.K_e:

                if exitable():
                    next_room()

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

    update_player_movement(dt)
#removed this code to prevent instant leaving

#    if get_tile(player_x, player_y) == TILE_EXIT:
#        move_to_next_map()


    # ========================================================
    # DRAW EVERYTHING
    # ========================================================

    # Draw map

    screen.fill((0, 0, 0))

    draw_world()

    draw_room_number()

    draw_exit_prompt()

# removed draw_player() as it's function is already being done by other code
    

    # ============================================================
    # ENEMY DRAWING
    #temporarily commented out until faux 3D map has been made, as its the main priority
    # ============================================================
#
#    def draw_enemy():
#        if not enemy_active:
#            return
#
#        if enemy_position is None:
#            return
#
#        x, y = enemy_position
#
#        center_x, center_y = grid_to_screen(x, y)
#
#        image_width = enemy_image.get.width()
#        image_height = enemy_image.get.height()
#
#        shadow_rect.center = (
#            center_x, center_y + 2
#        )
#
#        pygame.draw.ellipse(
#            screen,
#            (20, 20, 20),
#            shadow_rect
#        )

    #draw input controls
    if is_adjacent_to_tile(3):

        Draw_Input_boxes()




    # Update the display as per FPS

    pygame.display.flip()


    # Movement logic for player


pygame.quit()