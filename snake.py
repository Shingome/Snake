import pygame
from pygame.color import THECOLORS


def find_cell_size(frame_size):
    size = int(frame_size[1] / 18)
    while frame_size[0] % size != 0 and frame_size[1] % size != 0:
        size += 1
        print(size)
    return size


FPS = 30
size = (800, 600)

#Screen
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(THECOLORS['blue'])

#Game screen
frame = tuple(int(i) for i in (size[0] * 0.05, size[1] * 0.05, size[0] * 0.9, size[1] * 0.9))
pygame.draw.rect(screen, (171, 216, 80), pygame.Rect(frame))

#Grid
cell = find_cell_size((frame[2], frame[3]))
even = True
x_start = frame[0]
y_start = frame[1]
x_end = frame[2] + frame[0]
y_end = frame[3] + frame[1]
for y in range(y_start, y_end, cell):
    for x in range(x_start if even else x_start + cell, x_end, cell * 2):
        pygame.draw.rect(screen, (163, 210, 71), pygame.Rect(x, y, cell, cell))
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
