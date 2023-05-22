"""
Basic Tetris game using pygame.
"""

import pygame
from copy import deepcopy
from random import choice, randrange


# READ ONLY
WIDTH, HEIGHT = 10, 20
TILE_SIZE = 45
GAME_RES = WIDTH*TILE_SIZE, HEIGHT*TILE_SIZE
RES = 750, 940
FPS = 60  # Refresh rate

pygame.init()
sc = pygame.display.set_mode(RES)
game_screen = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

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
shape = deepcopy(choice(shapes))

background = pygame.image.load("img/bg.jpg").convert()
game_background = pygame.image.load("img/game_bg.jpg").convert()

########## HELPER FUNCTIONS START ##########


def out_of_bounds():
    """
    Function to make sure shape doesn't go out of bounds.

    Returns:
    - False = in bounds
    - True = out of bounds
    """
    if shape[i].x < 0 or shape[i].x > WIDTH - 1:
        return False
    elif shape[i].y > HEIGHT - 1 or field[shape[i].y][shape[i].x]:
        return False
    return True

########## HELPER FUNCTIONS END ##########


########## DRIVER CODE ##########
while True:
    dx, rotate = 0, False
    sc.blit(background, (0, 0))
    sc.blit(game_screen, (20, 20))
    game_screen.blit(game_background, (0, 0))

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
                    field[shape_old[i].y][shape_old[i].x] = pygame.Color(
                        "white")
                shape = deepcopy(choice(shapes))
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
    line = HEIGHT - 1
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WIDTH):
            if field[row][i]:
                count += 1

            field[line][i] = field[row][i]

        if count < WIDTH:
            line -= 1

    # Draw grid
    [pygame.draw.rect(game_screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Draw figure
    for i in range(4):  # All shapes consist of 4 tiles
        shapes_rect.x = shape[i].x * TILE_SIZE
        shapes_rect.y = shape[i].y * TILE_SIZE
        pygame.draw.rect(game_screen, pygame.Color("white"), shapes_rect)

    # Draw field
    for y, r in enumerate(field):
        for x, c in enumerate(r):
            if c:
                shapes_rect.x, shapes_rect.y = x * TILE_SIZE, y * TILE_SIZE
                pygame.draw.rect(game_screen, c, shapes_rect)

    pygame.display.flip()
    clock.tick(FPS)
