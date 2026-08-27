import pygame
import os
import time

pygame.init()
clock = pygame.time.Clock()

##my comments will use single ## like this one to distuingush MY comments

#HIDDEN SETTINGS

# Variables to track movement cooldown (in milliseconds)
MOVE_COOLDOWN = 200  # 0.2 seconds = 200ms
last_move_time = 0

##Since diagonal controls are NOT symetrical on all sides having a constant TILE_SIZE will not work, I would instead need different width and height values, ergo TILE_SIZE should be removed.
# Constants


# >>> ADD:
# For the 2.5D version, you will eventually want separate
# width/height values for the "floor" tiles.
#
# For example:

#
# TILE_WIDTH = 80
# TILE_HEIGHT = 40
#
# You can keep TILE_SIZE for now while experimenting,
# or eventually REMOVE TILE_SIZE if nothing uses it anymore.

MAP_WIDTH = 10
MAP_HEIGHT = 10

##Will also need to change sizes of tiles and the screen, I will keep the idea to make TILE_SIZE into two seperate width and height

TILE_WIDTH = 20
TILE_HEIGHT = 40

#I should likely also replace by screen size code as TILE_SIZE will be removed
screen_width = 1000
screen_height = 1100

# >>> REMOVE/REPLACE LATER:
# These two values currently assume that your map is a normal
# square grid.
#
# SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
# SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE + 90
#
# For 2.5D, you'll eventually want a fixed/larger screen size
# because the map will be drawn diagonally.


screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("Map 1")
FONT = pygame.font.Font(None, 28)
#MAP
#---------------------------

#---------------------------
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

# >>> KEEP:
# Your map itself does NOT need to become 3D.
# This exact 2D list can continue being your map.
#
# The 2.5D effect happens when you DRAW this map.
#
# So you do NOT need to turn this into something complicated.

#--------------------
# LOAD IMAGES
#--------------------


def load_image(name):
    path = os.path.join("assets", name)
    return pygame.transform.scale(
        pygame.image.load(path).convert_alpha(),
        (TILE_SIZE, TILE_SIZE)
    )

# >>> CHANGE/REPLACE LATER:
# At the moment, this function forces EVERY image to be
# TILE_SIZE x TILE_SIZE.
#
# That worked for your original 2D version.
#
# For 2.5D, your floor, player, machine, debris, etc.
# probably shouldn't all have the exact same dimensions.
#
# You can eventually change this function so that it
# loads the original image without automatically scaling it.
#
# IMPORTANT:
# Don't change this yet if you want to work on one thing
# at a time. This is simply one of the areas you'll need
# to revisit.


# Only the images actually used by map 1
tile_images = {
    0: load_image("floor.png"),
    1: load_image("path.png"),
    2: load_image("debris.png"),
    3: load_image("machine.png"),
    4: load_image("floor.png"),
    5: load_image("doorshadow.png"),
}

# >>> KEEP:
# You can continue using these SAME sprites.
#
# You don't need a completely new set of assets just
# because you're making the game 2.5D.
#
# What changes is how/where they are DRAWN.

#---------------------------------------
#MAP PLAYER INTERACTIONS
#---------------------------------------

def find_tile(tile_value, tile_map):
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == tile_value:
                return x, y
    return None

# >>> KEEP:
# This still works because your underlying map is still
# a normal 2D grid.
#
# You don't need to change how you find tiles.


#MOVEMENT

# Walkability
def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return current_map[y][x] not in (2, 3)
    return False

# >>> KEEP:
# Your movement system can remain grid-based.
#
# W = y - 1
# S = y + 1
# A = x - 1
# D = x + 1
#
# The 2.5D effect does NOT require you to rewrite this.


player_image = load_image('Player.png')
current_map = map_one
player_pos = list(find_tile(5, current_map))


# >>> ADD:
# You will need a function that converts your normal grid
# coordinates into 2.5D/isometric screen coordinates.
#
# Something conceptually like:
#
# def grid_to_screen(x, y):
#     ...
#
# This is one of the MOST IMPORTANT additions.
#
# Your player can still be at:
#
# player_pos = [4, 5]
#
# but grid_to_screen() figures out where [4, 5] should
# actually appear on the screen.

#-----------------------------------
# 2.5D conversion
#-----------------------------------

##This is new and will be needed to affect the cordinate system as they will now be tilted
## Need to make a new variable to use mathematic functions, however they will be guesswork as I do not know how they should look, so this will be revisted
set_x = 80
set_y = 100


def Dimension(x, y):

    display_x = set_x * TILE_WIDTH

    display_y = set_y * TILE_HEIGHT

    return display_x, display_y

#---------------------------------
#---------------------------------
 ##According to the AI suggestion code, I should remove this:
 # Draw player
#def draw_player():
   # screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))
# Draw player
#def draw_player():
#    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

#because it only works on a square grid, so I will replace it with drawing the new diagonal player/floor

# >>> REMOVE/REPLACE THIS DRAWING POSITION:
#
# The current:
#
# player_pos[0] * TILE_SIZE
# player_pos[1] * TILE_SIZE
#
# is what makes the player appear on the normal square grid.
#
# Eventually you want to:
#
# 1. Take player_pos[0] and player_pos[1]
# 2. Pass them through your new grid_to_screen()
# 3. Use the returned screen position to draw Player.png
#
# You can also eventually add a shadow underneath the player.
#
# KEEP the function itself.
# You're mainly changing HOW the player gets positioned.

##My new variable has to draw the images in regards to x and y, this means they could be unique, now, instead of debris tiles being flat and making no sense, for instance, they can look like genuine rubble

def draw_new_floor_tile(x,y, image):

    set_x, set_y = dimension(x, y)
    points = [
        (set_x, set_y),
    ]

    


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

# >>> KEEP THIS ENTIRE FUNCTION:
# Your movement logic doesn't need to know that the map
# LOOKS 2.5D.
#
# It still moves through the same x/y grid.


# INPUTS (will need to put HOW I'm going to change my game in here)

Input_boxes = {
    'row': pygame.Rect(
        10, MAP_HEIGHT * TILE_SIZE + 10, 80, 35),

    'col': pygame.Rect(
        110, MAP_HEIGHT * TILE_SIZE + 10, 80, 35),

    'value': pygame.Rect(
        210, MAP_HEIGHT * TILE_SIZE + 10, 80, 35),
}

# >>> REMOVE/REPLACE LATER:
# These positions are based on:
#
# MAP_HEIGHT * TILE_SIZE
#
# which assumes your map is a normal square rectangle.
#
# Once you change the map's screen size/position,
# you'll want your control panel to be positioned using
# the bottom of the SCREEN instead.
#
# The actual input boxes themselves can stay.


input_text = {
    'row': '',
    'col': '',
    'value': ''
}

# >>> KEEP:
# Your input system does not need to know about 2.5D.


active_box = None #makes the selected box none at default, so boxes arent randomly selected

BUTTON_RECT = pygame.Rect(310, MAP_HEIGHT * TILE_SIZE + 10, 100, 35)

# >>> REMOVE/REPLACE LATER:
# Same reason as the Input_boxes above.
#
# Eventually position this relative to the bottom control
# area rather than MAP_HEIGHT * TILE_SIZE.


#MESSAGE

status_message = '' #AKA nothing by, just making empty space for WHEN it is called

# >>> KEEP:
# Status messages have nothing to do with the map's perspective.


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

# >>> KEEP THIS ENTIRE FUNCTION:
#
# This is actually one of the BEST parts of your current
# structure for 2.5D.
#
# You are changing:
#
#     current_map[row][col]
#
# The renderer will then look at that value and draw the
# appropriate thing in the 2.5D world.
#
# You DON'T need a separate "2.5D change tile" function.
#
# For example:
#
# 0 -> floor
# 1 -> path
# 2 -> debris
# 3 -> machine
#
# can continue working exactly the same way.


#Draw functions

def Draw_Input_boxes():

    control_y = MAP_HEIGHT * TILE_SIZE

    # >>> REMOVE/REPLACE LATER:
    # This is another place where MAP_HEIGHT * TILE_SIZE
    # assumes a normal square map.
    #
    # Eventually use a fixed control-panel position,
    # probably something based on SCREEN_HEIGHT.


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

# >>> MOST OF THIS FUNCTION CAN STAY:
# The only real issue is WHERE the control panel is placed.
#
# Your actual text boxes, button, status message, etc.
# don't need to become 2.5D.


# ============================================================
# >>> ADD A NEW DRAWING FUNCTION(S) HERE
# ============================================================
#
# This is where you'll start building the 2.5D part.
#
# You will probably want a function like:
#
#     draw_floor_tile(x, y)
#
# which:
#
# 1. Takes the normal grid x/y
# 2. Converts it using grid_to_screen()
# 3. Draws a diamond instead of a square
#
# You can initially use pygame.draw.polygon()
# to make the diamond.
#
# AFTER you get that working, you can work on putting
# floor.png/path.png inside those diamond shapes.
#
# ------------------------------------------------------------
#
# You will probably also want another function like:
#
#     draw_object(x, y, image, height)
#
# for:
#
#     debris.png
#     machine.png
#
# This is where you can make those sprites look like
# they're standing UP from the floor.
#
# ------------------------------------------------------------
#
# IMPORTANT:
#
# Don't try to solve all of this at once.
#
# First:
#       Make ONE diamond.
#
# Then:
#       Make the whole map into diamonds.
#
# Then:
#       Put your sprites on it.
#
# Then:
#       Make the sprites have height.
#
# Then:
#       Make the player work.
#
# Then:
#       Make tile changing work with the new display.
#
# ============================================================


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

    # >>> REMOVE/REPLACE THIS ENTIRE MAP-DRAWING SECTION:
    #
    # This is the other BIG section that needs changing.
    #
    # Your current code says:
    #
    #     "Take x/y and put the image at x*TILE_SIZE,
    #      y*TILE_SIZE."
    #
    # That creates your current flat square map.
    #
    # Eventually replace this drawing approach with something
    # that:
    #
    #     1. Goes through the map
    #     2. Converts x/y using grid_to_screen()
    #     3. Draws the floor as an isometric diamond
    #     4. Draws objects/sprites on top
    #
    # KEEP THE TWO FOR LOOPS.
    #
    # You still want:
    #
    #     for y in range(MAP_HEIGHT):
    #         for x in range(MAP_WIDTH):
    #
    # because your map is STILL a 2D grid.
    #
    # You're just changing what happens INSIDE those loops.


    # Draw player
    draw_player()

    # >>> KEEP THIS FUNCTION CALL:
    #
    # The function itself will eventually have new drawing
    # code inside it, but you still call draw_player()
    # here.


    #draw input controls

    Draw_Input_boxes()

    # >>> KEEP:
    # Your editor/control panel remains a normal 2D UI.
    #
    # You DON'T want the row/column/tile input boxes to become
    # isometric. They should stay flat on the screen.


    # Update the display as per FPS
    pygame.display.flip()
    clock.tick(60)  

    # Movement logic for player


pygame.quit()
