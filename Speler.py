import pygame
import time
clock = pygame.time.Clock()
from Objecten import BewegendObject, SCREENWIDTH, SCREENHEIGHT, fps


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
        self.push_duur = 0.3
        self.max_health = 3 #max aantal levens is 3 
        self.health = self.max_health
        self.alive = True #om te weten of het game over is of niet
        
        self.damage_timer = 0 #wachttijd tss schade (dus tijd die nog moet aftellen)
        self.no_damage_time_left = 2 #speler is tijdens 1 sec onkwetsbaar nadat hij geraakt werd
        
        self.nodige_points = 9
        self.gewapend = False
        self.m_pressed = False 
        self.K_RIGHT = False
        self.K_LEFT = False
        self.level_voltooid = False 
        self.inventory = [] 
    def horizontaal(self):
        vx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            vx = self.snelheid
            self.facing_left = False
        if keys[pygame.K_LEFT]:
            vx = -self.snelheid
            self.facing_left = True
        
        #als de speler gewapend is en op m drukt dan is er een special attack waarin hij versnelt
        if self.m_pressed and self.gewapend:
            if keys[pygame.K_RIGHT]:
                vx = self.snelheid*2
                self.facing_left = False
            if keys[pygame.K_LEFT]:
                vx = -self.snelheid*2
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
        if self.damage_timer > 0:
            self.damage_timer -= self.no_damage_time_left/fps   # Decrease the timer
            if self.damage_timer < 0:
                self.damage_timer = 0
        if not self.alive:
            return# speler stopt direct wnr hij dood is (dus hp helemaal op)
        
        if self.pushed:
            if time.time() - self.push_start > self.push_duur:
                self.pushed = False
                self.vx = 0
        else: 
            self.vx = self.horizontaal()
              
        self.sprong()
        vx = self.collisie_x(self.vx, map_level)
        self.move(vx, 0)
        vy = self.collisie_y(map_level)
        self.move(0,vy)
        
        if self.gewapend and self.m_pressed:
            print("gewapend en m_pressed")
            
        #ervoor zorgen dat speler niet uit de scherm komt
        if self.rect.left < 0: 
            self.rect.left = 0
        if self.rect.right > SCREENWIDTH:
            self.rect.right = SCREENWIDTH 
        
        
    def draw(self, screen):
        
        if self.damage_timer > 0:
        # Flash effect: only draw every 100 ms
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                return  # skip drawing this frame
        
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False) #enkel horizontaal flippen
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)

            screen.blit(self.sprite, self.rect.topleft)


    def draw_healthbar(self, screen):# https://www.youtube.com/watch?v=E82_hdoe06M
        bar_width = self.basis #even lang als de speler
        bar_height = 5
        x = self.rect.x # x positie gelijk aan de linkerpositie van de speler
        y = self.rect.y - 10 # bar ligt een beetje boven de speler
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height)) # =rode balk = achtergrond van de healthbar
        groene_breedte = bar_width * (self.health / self.max_health) #geeft een percentage maal bar widht om te weten hoe groot de groen bar moet zijn
        pygame.draw.rect(screen, (0, 255, 0), (x, y, groene_breedte, bar_height))



