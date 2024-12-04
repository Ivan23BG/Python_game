import pygame
import random
from typing import Optional
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class XpOrb:
    """
    Represents an experience orb in the game.

    Attributes:
        pos (pygame.Vector2): The position of the orb.
        radius (int): The radius of the orb's representation.
        xp (int): The amount of experience the orb grants when collected.
    """

    def __init__(self, radius: int = 15, xp: int = 5) -> None:
        """
        Initializes an XpOrb with a random position, radius, and experience value.

        Args:
            radius (int): The radius of the orb. Defaults to 15.
            xp (int): The experience value of the orb. Defaults to 5.
        """
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.xp = xp


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the orb as a blue circle on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        pygame.draw.circle(screen, "blue", self.pos, self.radius)


    def draw_with_offset(self, screen: pygame.Surface, offset: pygame.Vector2) -> None:
        """
        Draws the orb with an offset, useful for camera systems.

        Args:
            screen (pygame.Surface): The game screen surface.
            offset (pygame.Vector2): The offset to apply.
        """
        pygame.draw.circle(screen, "blue", self.pos - offset, self.radius)


    def update(self, player: "Player") -> Optional[int]:
        """
        Updates the orb's state by checking for collision with the player.

        Args:
            player (Player): The player object.

        Returns:
            Optional[int]: Returns 1 if a collision is detected, otherwise None.
        """
        if self.check_player_collision(player):
            return 1  # Collision detected


    def check_player_collision(self, player: "Player") -> bool:
        """
        Checks if the orb collides with the player.

        Args:
            player (Player): The player object.

        Returns:
            bool: True if a collision is detected, otherwise False.
        """
        return self.collision_detected(player)


    def collision_detected(self, player: "Player") -> bool:
        """
        Determines if the orb and player are overlapping.

        Args:
            player (Player): The player object.

        Returns:
            bool: True if the player and orb collide, otherwise False.
        """
        return (self.pos - player.pos).length() < player.radius + self.radius
