"""
Basic Tetris game using pygame.
Author: Alex Kelso 

Python Version: 3.9.10
"""

import pygame
from copy import deepcopy
from random import choice, randrange


########## HELPER FUNCTIONS START ##########


def out_of_bounds():
    """
    Check to make sure shape doesn't go out of bounds.

    Returns:
    - False = in bounds
    - True = out of bounds
    """
    if shape[i].x < 0 or shape[i].x > WIDTH - 1:
        return False
    elif shape[i].y > HEIGHT - 1 or field[shape[i].y][shape[i].x]:
        return False
    return True


def get_random_color():
    """
    Get random color for next shape that appears.

    Returns: 
    - Random color code 3-tuple
    """
    return (randrange(30, 256), randrange(30, 256), randrange(30, 256))


def get_high_score():
    """
    Gets high score by reading it from file on record.
    """
    try:
        with open("high_score") as f:
            return f.readline()
    except FileNotFoundError:
        with open("high_score", "w") as f:
            f.write("0")


def set_high_score(high_score, score):
    """
    Sets high score by writing to file on record.
    """
    hs = max(int(high_score), score)
    with open("high_score", "w") as f:
        f.write(str(hs))

########## HELPER FUNCTIONS END ##########


########## GAME SETUP START ##########
WIDTH, HEIGHT = 10, 20
TILE_SIZE = 45
GAME_RES = WIDTH*TILE_SIZE, HEIGHT*TILE_SIZE
RES = 750, 940
FPS = 60  # Refresh rate

pygame.init()
sc = pygame.display.set_mode(RES)
game_screen = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()


# Creating shape sizes and location
grid = [pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        for x in range(WIDTH) for y in range(HEIGHT)]

shapes_coordinates = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                      [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                      [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                      [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                      [(0, 0), (0, -1), (0, 1), (-1, -1)],
                      [(0, 0), (0, -1), (0, 1), (1, -1)],
                      [(0, 0), (0, -1), (0, 1), (-1, 0)]]

shapes = [[pygame.Rect(x+WIDTH // 2, y+1, 1, 1) for x, y in coordinate_set]
          for coordinate_set in shapes_coordinates]
shapes_rect = pygame.Rect(0, 0, TILE_SIZE-2, TILE_SIZE-2)
field = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

anim_count, anim_speed, anim_limit = 0, 60, 2000
shape, next_shape = deepcopy(choice(shapes)), deepcopy(choice(shapes))
random_color, next_random_color = get_random_color(), get_random_color()


# Background images
background = pygame.image.load("img/bg.jpg").convert()
game_background = pygame.image.load("img/game_bg.jpg").convert()

# Word fonts
main_font = pygame.font.Font("font/font.ttf", 65)
font = pygame.font.Font("font/font.ttf", 50)

# Sidebar texts
tetris_title = main_font.render("TETRIS", True, pygame.Color("orange"))
score_title = font.render("SCORE", True, pygame.Color("green"))
high_score_title = font.render("HIGH SCORE", True, pygame.Color("purple"))

# Score vars and scheme
score, lines = 0, 0
score_scheme = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

########## GAME SETUP STOP ##########


########## MAIN START ##########
while True:
    dx, rotate = 0, False
    sc.blit(background, (0, 0))
    sc.blit(game_screen, (20, 20))
    game_screen.blit(game_background, (0, 0))
    high_score = get_high_score()

    # Slight delay for full lines
    for i in range(lines):
        pygame.time.wait(200)

    # EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

    # Move x
    shape_old = deepcopy(shape)
    for i in range(4):
        shape[i].x += dx
        if not out_of_bounds():
            shape = deepcopy(shape_old)
            break

    # Move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        shape_old = deepcopy(shape)
        for i in range(4):
            shape[i].y += 1
            if not out_of_bounds():
                for i in range(4):
                    field[shape_old[i].y][shape_old[i].x] = random_color
                shape, random_color = next_shape, next_random_color
                next_shape, next_random_color = deepcopy(
                    choice(shapes)), get_random_color()
                anim_limit = 2000
                break

    # Rotate CW
    center = shape[0]
    shape_old = deepcopy(shape)
    if rotate:
        for i in range(4):
            # Rotate all four block constituents
            x = shape[i].y - center.y
            y = shape[i].x - center.x
            shape[i].x = center.x - x
            shape[i].y = center.y + y

            if not out_of_bounds():
                shape = deepcopy(shape_old)
                break

    # Check filled lines
    line, lines = HEIGHT - 1, 0
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WIDTH):
            if field[row][i]:
                count += 1

            field[line][i] = field[row][i]
        if count < WIDTH:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # Compute score
    score += score_scheme[lines]

    # Draw grid
    [pygame.draw.rect(game_screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Draw figure
    for i in range(4):  # All shapes consist of 4 tiles
        shapes_rect.x = shape[i].x * TILE_SIZE
        shapes_rect.y = shape[i].y * TILE_SIZE
        pygame.draw.rect(game_screen, random_color, shapes_rect)

    # Draw field
    for y, r in enumerate(field):
        for x, c in enumerate(r):
            if c:
                shapes_rect.x, shapes_rect.y = x * TILE_SIZE, y * TILE_SIZE
                pygame.draw.rect(game_screen, c, shapes_rect)

    # Draw next shape
    for i in range(4):  # All shapes consist of 4 tiles
        shapes_rect.x = next_shape[i].x * TILE_SIZE + 380
        shapes_rect.y = next_shape[i].y * TILE_SIZE + 185
        pygame.draw.rect(sc, next_random_color, shapes_rect)

    # Sidebar text
    sc.blit(tetris_title, (485, 20))
    sc.blit(score_title, (510, 760))
    sc.blit(font.render(str(score), True, pygame.Color("white")), (510, 840))

    # Game over handling - clear grid and reset params
    for i in range(WIDTH):
        if field[0][i]:
            set_high_score(high_score, score)
            field = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_shape in grid:
                pygame.draw.rect(game_screen, get_random_color(), i_shape)
                sc.blit(game_screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
