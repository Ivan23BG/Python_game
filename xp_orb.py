import pygame
import random

class XpOrb:
    def __init__(self, x, y, radius):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius

    def move(self, move_x, move_y):
        self.pos.x += move_x
        self.pos.y += move_y

    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.pos, self.radius)


    def draw_with_offset(self, screen, offset_x, offset_y):
        pygame.draw.circle(screen, "blue", self.pos - pygame.Vector2(offset_x, offset_y), self.radius)