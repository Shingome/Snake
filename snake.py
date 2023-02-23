import pygame
from pygame.color import THECOLORS
from food import Food


class Snake:
    def __init__(self, game, position: (int, int), even: bool, direction: str, color=THECOLORS['purple']):
        self.game = game
        self.color = color
        self.head = pygame.draw.rect(self.game.screen, self.color,
                                     pygame.Rect(position[0], position[1], self.game.cell_size, self.game.cell_size))
        self.pos = [*position]
        self.direction = direction
        self.directions = {"UP": (0, -self.game.cell_size), "DOWN": (0, self.game.cell_size),
                           "RIGHT": (self.game.cell_size, 0), "LEFT": (-self.game.cell_size, 0)}
        self.body = [position]
        self.body_count = 1
        self.even = even
        self.alive = True

    def change_direction(self, direction: str):
        if self.directions[direction][0] == -self.directions[self.direction][0] \
                and self.directions[direction][1] == -self.directions[self.direction][1]:
            return
        self.direction = direction

    def move(self):
        self.head.move_ip(self.directions[self.direction])
        self.pos = [self.head.x, self.head.y]
        self.check_borders()
        self.change_body()
        self.check_death()

    def check_borders(self):
        if self.pos[0] <= self.game.frame[0] \
                or self.pos[0] >= self.game.frame[2] - self.game.cell_size \
                or self.pos[1] <= self.game.frame[1] \
                or self.pos[1] >= self.game.frame[3] - self.game.cell_size:
            self.death()

    def change_body(self):
        self.body.append(tuple(self.pos))

        if len(self.body) > self.body_count:
            color = self.game.cell_colors[0] if self.even else self.game.cell_colors[1]
            pygame.draw.rect(self.game.screen, color,
                             pygame.Rect(self.body[0][0], self.body[0][1], self.game.cell_size, self.game.cell_size))
            self.even = not self.even
            self.body.pop(0)

        for i in self.body:
            pygame.draw.rect(self.game.screen, self.color, pygame.Rect(i[0], i[1],
                                                                       self.game.cell_size, self.game.cell_size))

    def check_food(self, food: Food):
        if (self.pos[0], self.pos[1]) == food.pos:
            self.add_tailor()
            food.eaten = True

    def check_death(self):
        for i in self.body[:len(self.body) - 1]:
            if self.pos[0] == i[0] and self.pos[1] == i[1]:
                self.death()

    def add_tailor(self):
        self.body_count += 1

    def death(self):
        for i in self.body:
            pygame.draw.rect(self.game.screen, THECOLORS['red'], pygame.Rect(i[0], i[1],
                                                                             self.game.cell_size, self.game.cell_size))
        self.alive = False
