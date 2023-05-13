import pygame

# READ ONLY
WIDTH, HEIGHT = 10, 20
TILE_SIZE = 45
GAME_RES = WIDTH*TILE_SIZE, HEIGHT*TILE_SIZE
FPS = 60  # Refresh rate

pygame.init()
game_screen = pygame.display.set_mode(GAME_RES)
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

shape = shapes[0]

while True:
    game_screen.fill(pygame.Color("Black"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Draw grid
    [pygame.draw.rect(game_screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Draw figure
    for i in range(4):  # All shapes consist of 4 tiles
        shapes_rect.x = shape[i].x * TILE_SIZE
        shapes_rect.y = shape[i].y * TILE_SIZE
        pygame.draw.rect(game_screen, pygame.Color("red"), shapes_rect)

    pygame.display.flip()
    clock.tick(FPS)
