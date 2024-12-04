import pygame
import random
from typing import List
from xp_orb import XpOrb
import math


class XpOrbs:
    """
    Manages a collection of experience orbs in the game.

    Attributes:
        orbs (List[XpOrb]): The list of currently active orbs.
        max_orbs (int): The maximum number of orbs allowed in the game.
        spawn_rate (float): The probability of spawning a new orb each tick.
    """

    def __init__(self) -> None:
        """
        Initializes an XpOrbs manager with default values.
        """
        self.orbs: List[XpOrb] = []
        self.max_orbs: int = 50
        self.spawn_rate: float = 1 / 20  # Percent chance per frame.


    def add(self, orb: XpOrb) -> None:
        """
        Adds a new experience orb to the collection.

        Args:
            orb (XpOrb): The orb to add.
        """
        self.orbs.append(orb)


    def remove(self, orb: XpOrb) -> None:
        """
        Removes an experience orb from the collection.

        Args:
            orb (XpOrb): The orb to remove.
        """
        self.orbs.remove(orb)


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all experience orbs on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        for orb in self.orbs:
            orb.draw(screen)


    def draw_with_offset(self, screen: pygame.Surface, offset: pygame.Vector2) -> None:
        """
        Draws all orbs with an offset, useful for camera systems.

        Args:
            screen (pygame.Surface): The game screen surface.
            offset (pygame.Vector2): The offset to apply.
        """
        for orb in self.orbs:
            orb.draw_with_offset(screen, offset)


    def spawn(self, player: "Player") -> None:
        """
        Spawns a new orb if the maximum number of orbs is not reached
        and the random spawn condition is met.
        """
        if len(self.orbs) < self.max_orbs:
            if random.random() < self.spawn_rate:
                
                # Generate random spawn position and attributes
                radius = 400  # Distance from player
                angle = random.uniform(0, 2 * math.pi)
                distance = math.sqrt(random.uniform(0, 1)) * radius + 150  # Random distance from player

                # Convert polar coordinates to Cartesian
                x = distance * math.cos(angle) + player.pos.x
                y = distance * math.sin(angle) + player.pos.y
                
                # Create and add the new orb
                orb = XpOrb(radius=15, xp=5)
                orb.pos = pygame.Vector2(x, y)
                self.add(orb)


    def update(self, player: "Player") -> None:
        """
        Updates all orbs, checking for collisions with the player
        and removing orbs that are collected.

        Args:
            player (Player): The player object.
        """
        for orb in self.orbs:
            if orb.update(player):
                self.remove(orb)
                player.handle_xp(orb)
