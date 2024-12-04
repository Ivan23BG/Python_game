import pygame
from typing import Optional


class GameObject:
    """
    A base class for all game objects.

    Attributes:
        pos (pygame.Vector2): Position of the object.
        radius (int): Radius of the object for collisions and rendering.
    """

    def __init__(self, x: float, y: float, radius: int) -> None:
        self.pos = pygame.Vector2(x, y)
        self.radius = radius

    def draw(self, screen: pygame.Surface, color: str) -> None:
        """
        Draws the object on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
            color (str): The color of the object.
        """
        pygame.draw.circle(screen, color, self.pos, self.radius)

    def draw_with_offset(self, screen: pygame.Surface, offset: pygame.Vector2, color: str) -> None:
        """
        Draws the object with a positional offset.

        Args:
            screen (pygame.Surface): The game screen surface.
            offset (pygame.Vector2): The positional offset.
            color (str): The color of the object.
        """
        pygame.draw.circle(screen, color, self.pos - offset, self.radius)
