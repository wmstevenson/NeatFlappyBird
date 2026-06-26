import pygame


class Bird:
    GRAVITY = 0.5
    JUMP = -10
    TERMINAL_VELOCTY_Y = 10
    RADIUS = 20

    def __init__(self, x, y, color=(255, 255, 0)):
        self.x = x
        self.y = y
        self.velocity_y = 0

        self.color = color

    def flap(self):
        self.velocity_y = self.JUMP

    def move(self):
        self.velocity_y += self.GRAVITY

        if self.velocity_y > self.TERMINAL_VELOCTY_Y:
            self.velocity_y = self.TERMINAL_VELOCTY_Y

        self.y += self.velocity_y

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.RADIUS)

    def get_rect(self):
        rect = pygame.Rect(
            self.x - self.RADIUS, self.y - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2
        )
        return rect
