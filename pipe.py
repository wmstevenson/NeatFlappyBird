import random
import pygame


class Pipe:
    GAP = 200
    MARGIN = 50
    VELOCITY_X = 5
    WIDTH = 80

    def __init__(self, window_height, x, color=(0, 200, 0)):
        self.window_height = window_height
        self.x = x

        self.top_pipe_bottom = None
        self.bottom_pipe_top = None
        self.set_height()

        self.passed = False

        self.color = color

    def set_height(self):
        self.top_pipe_bottom = random.randint(
            self.MARGIN, self.window_height - self.GAP - self.MARGIN
        )

        self.bottom_pipe_top = self.top_pipe_bottom + self.GAP

    def move(self):
        self.x -= self.VELOCITY_X

    def draw(self, window):
        pygame.draw.rect(
            window, self.color, (self.x, 0, self.WIDTH, self.top_pipe_bottom)
        )

        pygame.draw.rect(
            window,
            self.color,
            (
                self.x,
                self.bottom_pipe_top,
                self.WIDTH,
                self.window_height - self.bottom_pipe_top,
            ),
        )

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.WIDTH, self.top_pipe_bottom)

        bottom_rect = pygame.Rect(
            self.x,
            self.bottom_pipe_top,
            self.WIDTH,
            self.window_height - self.bottom_pipe_top,
        )

        return top_rect, bottom_rect
