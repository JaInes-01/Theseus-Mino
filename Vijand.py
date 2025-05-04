import pygame 
import time 
from Objecten import VastObject, BewegendObject
 
SCREENWIDTH = 1000
SCREENHEIGHT = 800

class Vijand(BewegendObject):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png)
        self.target = speler
        self.snelheid = snelheid
        self.op_grond = False
        self.vy = 0
        self.vx = snelheid #tot nu toe beweegt hij alleen maar horizontaal
        self.hp = 0
        #de vijand moet ook een schild hebben zodat die niet in een keer meerdere hp punten verliest
        self.schild = False
        self.schild_start = 0
        self.schild_duur = 2
        
    def zwaartekracht(self):
        if not self.op_grond:
            self.vy += 1 #verticale snelheid wordt steeds groter, totdat het positief wordt en bijgevolg naar beneden wordt gericht
            
    def collisie_x(self, snelheid, map_level):
        for tile in map_level.tile_list:
            future_x = pygame.Rect(self.rect.x + self.vx, self.rect.y, self.basis, self.hoogte)
            if tile.rect.colliderect(future_x):
                if self.vx > 0:
                   vx = tile.rect.left - self.rect.right #dx blijft dalen naarmate dat de speler dichter komt, totdat dx nul wordt
                elif vx < 0:
                    vx = tile.rect.right - self.rect.left
                    
    def collisie_y(self, map_level):
        vy = self.vy
        for tile in map_level.tile_list:
            future_y = pygame.Rect(self.rect.x, self.rect.y + vy, self.basis, self.hoogte)
            if tile.rect.colliderect(future_y):
                if self.vy > 0:  # Als de vijand valt
                    vy = tile.rect.top - self.rect.bottom
                    self.vy = 0
                    self.op_grond = True
                elif self.vy < 0:  # Als de vijand springt
                    vy = tile.rect.bottom - self.rect.top
                    self.vy = 0
                    self.op_grond = False
        return vy
    
    def schild_aan(self):
        self.schild = True
        self.schild_start = time.time()

