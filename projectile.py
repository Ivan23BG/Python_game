from typing import Optional
import pygame
from game_object import GameObject
from enemy import Enemy


class Projectile(GameObject):
    """
    Represents a projectile fired by the player.

    Attributes:
        velocity (pygame.Vector2): The velocity of the projectile.
        speed (float): The speed of the projectile.
    """

    def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2, speed: float = 400) -> None:
        super().__init__(pos.x, pos.y, radius=5)
        self.velocity = direction.normalize() * speed


    def update(self, dt: float) -> None:
        """
        Updates the projectile's position.

        Args:
            dt (float): Delta time for frame-independent movement.
        """
        self.pos += self.velocity * dt


    def check_collision(self, enemies: list) -> Optional[Enemy]:
        """
        Checks for collision with any enemy.

        Args:
            enemies (list): The list of enemies.

        Returns:
            Optional[Enemy]: The enemy hit, or None if no collision.
        """
        for enemy in enemies:
            if (self.pos - enemy.pos).length() < self.radius + enemy.radius:
                return enemy
        return None
