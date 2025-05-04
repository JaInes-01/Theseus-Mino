import pygame
import time
SCREENWIDTH = 1000
SCREENHEIGHT = 800
from Objecten import BewegendObject


class Speler(BewegendObject):
    
    def __init__(self, x, y, snelheid, fact_basis, fact_hoogte, sprite_png, map_level, zwaard): #snelheid geeft gewoon weer hoe snel de speler zal bewegen
        super().__init__(x, y,snelheid, fact_basis, fact_hoogte, sprite_png)
        self.facing_left = False 
        self.vy = 0
        self.vx = 0
        self.snelheid = snelheid
        #springfucntie
        self.op_grond = False
        self.Fz = 1
        self.spring_hoogte = self.hoogte/3
        #collisie met vijand
        self.pushed = False
        self.push_start = 0
        self.push_duur = 0.5
        self.schild = False
        self.schild_start = 0
        self.schild_duur = 4
        self.hp = 0
        self.points = 0
        self.nodige_points = 9
        self.gewapend = False
        
    def horizontaal(self):
        vx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            vx = self.snelheid
            self.facing_left = False
        if keys[pygame.K_LEFT]:
            vx = -self.snelheid
            self.facing_left = True
        return vx
    
    def sprong(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.op_grond:
            self.vy = (-self.snelheid)*4 #verticale snelheid is negatief want naar boven gericht
            self.op_grond = False
        self.zwaartekracht()
        
    def zwaartekracht(self):
        self.vy += self.Fz #verticale snelheid wordt steeds groter, totdat het positief wordt en bijgevolg naar beneden wordt gericht
        
    def schild_aan(self):
        self.schild = True
        self.schild_start = time.time()
    
    def zwaard(self, zwaard):
        if self.rect.colliderect(zwaard.rect):
           zwaard.sprite.set_alpha(0)
           self.gewapend = True
           
    def collisie_x(self, vx, map_level):
        for tile in map_level.tile_list:
            future_x = pygame.Rect(self.rect.x + vx, self.rect.y, self.basis, self.hoogte)
            if tile.rect.colliderect(future_x):
                if vx > 0:
                   vx = tile.rect.left - self.rect.right #dx blijft dalen naarmate dat de speler dichter komt, totdat dx nul wordt
                elif vx < 0:
                    vx = tile.rect.right - self.rect.left
        return vx
    
    def collisie_y(self, map_level):
        vy = self.vy
        
        for tile in map_level.tile_list:
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
                    self.op_grond = False
        return vy
    
   
    
    def beweging(self, map_level):
        
        if not self.pushed:
            self.vx = self.horizontaal()
        else:
            tijdsverschil_push = time.time()-self.push_start 
            if tijdsverschil_push > self.push_duur:
                self.pushed = False
                self.vx = 0
                
        tijdsverschil_schild = time.time()-self.schild_start  
        if self.schild and tijdsverschil_schild > self.schild_duur:
            self.schild = False
            
        self.sprong()
        vx = self.collisie_x(self.vx, map_level)
        self.move(vx, 0)
        vy = self.collisie_y(map_level)
        self.move(0,vy)
        
        #ervoor zorgen dat speler niet uit de scherm komt
        if self.rect.left < 0: 
            self.rect.left = 0
        if self.rect.right > SCREENWIDTH:
            self.rect.right = SCREENWIDTH 
            
    def draw(self, screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False) #enkel horizontaal flippen
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)

            screen.blit(self.sprite, self.rect.topleft)



