import pygame
from Objecten import VastObject
SCREENWIDTH = 1000
SCREENHEIGHT = 800
aantal_blokken_horizontaal = 20
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal
aantal_blokken_verticaal = int(SCREENHEIGHT/tile_grootte)
class Map():
    def __init__(self, matrix):
        self.tile_list = []
        self.matrix = matrix
        for rij_index in range(len(self.matrix)):       #y-pos
            for kol_index in range(len(self.matrix[rij_index])):
                x = kol_index * tile_grootte
                y = rij_index * tile_grootte
                    
                if self.matrix[rij_index][kol_index] == 1: #nummer 1 is een blok
                    tile_afb = VastObject(x, y, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "blok.png")
                    self.tile_list.append(tile_afb)
                    
                elif self.matrix[rij_index][kol_index] == 2: #nummer 2 is een halve tegel
                    tile_afb = VastObject(x, y, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "halve.png")
                    self.tile_list.append(tile_afb)
                    
    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile.sprite, tile.rect.topleft)
