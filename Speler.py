import pygame
SCREENWIDTH = 1000
SCREENHEIGHT = 800
from Objecten import BewegendObject
from Map import Map

class Speler(BewegendObject):
    
    def __init__(self, x, y, vx, vy, fact_basis, fact_hoogte, sprite_png, niveau):
        super().__init__(x, y, vx, vy, fact_basis, fact_hoogte, sprite_png)
        self.facing_left = False 
        self.vy = 0 
        self.op_grond = False
        self.Fz = 1
        self.spring_hoogte = self.hoogte/4
        self.map = niveau
        
    def beweging(self):
        vx = 0 #speler blijft statisch indien geen keys gedrukt worden
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            vx = 5
            self.facing_left = False
        if keys[pygame.K_LEFT]:
            vx = -5
            self.facing_left = True
              
        #sprong
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.op_grond:
            self.vy = -self.spring_hoogte #verticale snelheid is negatief want naar boven gericht
            self.op_grond = False
        
        #zwaartekracht werkt op elk moment
        self.vy += self.Fz #verticale snelheid wordt steeds groter, totdat het positief wordt en bijgevolg naar beneden wordt gericht
        
        #dy definiëren
        vy = self.vy #dy is niet constant zoals dx en hangt af van de sprong
        
        #collisie checken in x-richting
        for tile in self.map.tile_list:
            future_x = pygame.Rect(self.rect.x + vx, self.rect.y, self.basis, self.hoogte)
            if tile.rect.colliderect(future_x):
                if vx > 0:
                    vx = tile.rect.left - self.rect.right #dx blijft dalen naarmate dat de speler dichter komt, totdat dx nul wordt
                elif vx < 0:
                    vx = tile.rect.right - self.rect.left
                    
        #collisie checken in y-richting        
        for tile in self.map.tile_list:
            #op het moment dat de collisie wordt waargenomen is er al overlapping behalve als de speler op die exact moment stopt te bewegen, dus moeten we een toekomstige scenario gebruiken
            future_y = pygame.Rect(self.rect.x, self.rect.y + vy, self.basis, self.hoogte)
            
            if tile.rect.colliderect(future_y):
                #als de collsiie van boven gebeurt, als de speler valt
                if self.vy > 0:
                    vy = tile.rect.top - self.rect.bottom #afstand tot de bovenkant van de platform
                    self.vy = 0 #we willen dat de speler stil blijft
                    self.op_grond = True 
                #als de collisie van onder gebeurt, als de speler springt
                elif self.vy < 0:
                    vy = tile.rect.bottom - self.rect.top #afstand tot de onderkant van de platform
                    self.vy = 0
                    
                    
        self.move(vx, vy)
        
    def draw(self, screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False) #enkel horizontaal flippen
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)


