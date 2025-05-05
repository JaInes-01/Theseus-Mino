import pygame
import math
from Objecten import VastObject, BewegendObject

class Steen(BewegendObject):
    def __init__(self, x, y, snelheid, fact_basis, fact_hoogte, sprite_png, richting):
        super().__init__(x, y, snelheid, fact_basis, fact_hoogte, sprite_png)
        self.vx = snelheid*richting

    def beweging(self):
        self.move(self.vx, 0)
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.topleft))

