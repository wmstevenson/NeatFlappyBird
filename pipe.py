import random
import pygame


class Pipe:

    VELOCITY_X = 4

    def __init__(self, window_width, window_height, x, color=(0, 200, 0)):
        self.window_width = window_width
        self.window_height = window_height
        self.x = x


        self.pipe_width = int(self.window_width * 50/288)
        self.vertical_gap = int(self.window_height *120/512)

        self.top_pipe_bottom = None
        self.bottom_pipe_top = None
        self.set_height()

        self.passed = False

        self.color = color

    def set_height(self):
        half_gap = self.vertical_gap // 2
        centre = random.randint(self.window_height // 4, self.window_height - self.window_height // 4)
        self.top_pipe_bottom = centre - half_gap
        self.bottom_pipe_top = centre + half_gap

    def move(self):
        self.x -= self.VELOCITY_X

    def draw(self, window):
        pygame.draw.rect(
            window, self.color, (self.x, 0, self.pipe_width, self.top_pipe_bottom)
        )

        pygame.draw.rect(
            window,
            self.color,
            (
                self.x,
                self.bottom_pipe_top,
                self.pipe_width,
                self.window_height - self.bottom_pipe_top,
            ),
        )

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.pipe_width, self.top_pipe_bottom)

        bottom_rect = pygame.Rect(
            self.x,
            self.bottom_pipe_top,
            self.pipe_width,
            self.window_height - self.bottom_pipe_top,
        )

        return top_rect, bottom_rect
