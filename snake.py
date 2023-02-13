import math

import pygame
from pygame.color import THECOLORS


def find_size(window_size: (int, int), rel: float, cells: (int, int)):
    border = int(window_size[1] * rel)
    cell_size = math.floor((window_size[1] - border) / cells[1])
    frame_size = tuple(i * cell_size for i in cells)
    print(frame_size)
    border = tuple(int((window_size[i] - frame_size[i]) / 2) for i in range(2))
    start = tuple(window_size[i] - frame_size[i] - border[i] for i in range(2))
    end = tuple(window_size[i] - border[i] for i in range(2))
    return cell_size, *start, *end


if __name__ == "__main__":
    FPS = 30
    size = (1200, 800)
    cells = (18, 12)

    # Main screen
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill(THECOLORS['blue'])

    # Game screen
    cell_size, *frame = find_size(size, 0.05, cells)
    pygame.draw.rect(screen, (171, 216, 80), pygame.Rect(frame[0], frame[1], frame[2] - frame[0], frame[3] - frame[1]))

    # Grid
    even = True
    x_start, y_start, x_end, y_end = frame
    for y in range(y_start, y_end, cell_size):
        for x in range(x_start if even else x_start + cell_size, x_end, cell_size * 2):
            print(x, y)
            pygame.draw.rect(screen, (163, 210, 71), pygame.Rect(x, y, cell_size, cell_size))
        even = not even

    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    pygame.display.flip()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
