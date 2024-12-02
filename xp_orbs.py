import pygame
import random

from xp_orb import XpOrb



class XpOrbs:
    def __init__(self) -> None:
        self.orbs = []
        self.max_orbs = 50
        self.spawn_rate = 1 / 60 # percent chance per tick


    def add(self, orb):
        self.orbs.append(orb)


    def remove(self, orb):
        self.orbs.remove(orb)


    def draw(self, screen):
        for orb in self.orbs:
            orb.draw(screen)


    def draw_with_offset(self, screen, offset):
        for orb in self.orbs:
            orb.draw_with_offset(screen, offset)


    def spawn(self):
        if len(self.orbs) < self.max_orbs:
            if random.random() < self.spawn_rate:
                new_orb = XpOrb()
                self.add(new_orb)


    def update(self, player):
        for orb in self.orbs:
            if orb.update(player):
                self.remove(orb)
                player.handle_xp(orb)