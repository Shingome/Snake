import math
import pygame
import random as rd
from pygame.color import THECOLORS


class Food:
    def __init__(self, cells: (int, int), cell_size: int, x_start: int, y_start: int):
        self.food_pos = (x_start + cell_size * rd.choice(range(cells[0])),
                         y_start + cell_size * rd.choice(range(cells[1])))
        self.eaten = False
        self.draw_food(cell_size)

    def draw_food(self, cell_size):
        pygame.draw.rect(screen, THECOLORS['red'],
                         pygame.Rect(self.food_pos[0], self.food_pos[1], cell_size, cell_size))


class Snake:
    def __init__(self, screen, cell_size: int, position: (int, int), even: bool, direction: str):
        self.head_size = cell_size
        self.screen = screen
        self.color = THECOLORS['purple']
        self.head = pygame.draw.rect(screen, self.color,
                                     pygame.Rect(position[0], position[1], self.head_size, self.head_size))
        self.direction = direction
        self.directions = {"UP": (0, -cell_size), "DOWN": (0, cell_size),
                           "RIGHT": (cell_size, 0), "LEFT": (-cell_size, 0)}
        self.body = [position]
        self.body_count = 1
        self.even = even
        self.alive = True

    def change_direction(self, direction: str):
        if self.directions[direction][0] == -self.directions[self.direction][0] \
                and self.directions[direction][1] == -self.directions[self.direction][1]:
            return
        self.direction = direction

    def move(self, food: Food):
        # Move head
        self.head.move_ip(self.directions[self.direction])

        # Borders
        if self.head.x <= frame[0] - cell_size:
            self.head.x = frame[2] - cell_size
        elif self.head.x >= frame[2]:
            self.head.x = frame[0]
        elif self.head.y <= frame[1] - cell_size:
            self.head.y = frame[3] - cell_size
        elif self.head.y >= frame[3]:
            self.head.y = frame[1]

        self.body.append((self.head.x, self.head.y))
        if len(self.body) > self.body_count:
            color = cell_colors[0] if self.even else cell_colors[1]
            pygame.draw.rect(self.screen, color,
                             pygame.Rect(self.body[0][0], self.body[0][1], self.head_size, self.head_size))
            self.even = not self.even
            self.body.pop(0)

        for i in self.body:
            pygame.draw.rect(self.screen, self.color, pygame.Rect(i[0], i[1], self.head_size, self.head_size))

        if (self.head.x, self.head.y) == food.food_pos:
            self.add_tailor()
            food.eaten = True

        for i in self.body[:len(self.body) - 1]:
            if self.head.x == i[0] and self.head.y == i[1]:
                self.death()

    def add_tailor(self):
        self.body_count += 1

    def death(self):
        for i in self.body:
            pygame.draw.rect(screen, THECOLORS['red'], pygame.Rect(i[0], i[1], self.head_size, self.head_size))
        self.alive = False


def find_size(window_size: (int, int), rel: float, cells: (int, int)):
    border = math.floor(window_size[1] * rel)
    cell_size = math.floor((window_size[1] - border) / cells[1])
    frame_size = tuple(i * cell_size for i in cells)
    border = tuple((window_size[i] - frame_size[i]) // 2 for i in range(2))
    start = tuple(window_size[i] - frame_size[i] - border[i] for i in range(2))
    end = tuple(window_size[i] - border[i] for i in range(2))
    return cell_size, *start, *end


if __name__ == "__main__":
    FPS = 5
    size = (1200, 800)
    cells = (18, 12)
    cell_colors = ((171, 216, 80), (163, 210, 71))

    # Main screen
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill(THECOLORS['blue'])
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    # Game screen
    cell_size, *frame = find_size(size, 0.05, cells)
    pygame.draw.rect(screen, cell_colors[0], pygame.Rect(frame[0], frame[1], frame[2] - frame[0], frame[3] - frame[1]))

    # Grid
    even = True
    x_start, y_start, x_end, y_end = frame
    for y in range(y_start, y_end, cell_size):
        for x in range(x_start if even else x_start + cell_size, x_end, cell_size * 2):
            pygame.draw.rect(screen, cell_colors[1], pygame.Rect(x, y, cell_size, cell_size))
        even = not even

    # Init snake and food
    pos = tuple(frame[i] + cell_size * (cells[i] // 2) for i in range(2))
    even = bool((cells[0] // 2) % 2)
    snake = Snake(screen, cell_size, pos, even, "UP")
    food = Food(cells, cell_size, x_start, y_start)

    # Run
    pygame.display.flip()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
                elif event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")

        if snake.alive:
            snake.move(food)

        if food.eaten:
            food = Food(cells, cell_size, x_start, y_start)

        pygame.display.update()
