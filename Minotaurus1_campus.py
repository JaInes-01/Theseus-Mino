import pygame
import time
from Vijand import Vijand
SCREENWIDTH = 1000
SCREENHEIGHT = 800

class Minotaurus1(Vijand):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.facing_left = True #in het begin kijkt de minotaurus naar links want hij zit helemaal links
        self.op_grond = False
        self.vertraagd = False #wanneer de vijand botst tegen de speler willen we dat hij voor enkele seconden vertraagt
        self.versneld = False
        self.vertraag_duur = 1
        self.vertraag_start = 0
        self.max_health = 3 #max aantal levens is 3 
        self.health = self.max_health
        self.alive = True 
        self.damage_timer = 0 
        self.no_damage_time_left = 1000
        self.versnelling = 4
        self.nodige_health = 0
        
    def push(self, speler):
        speler.push_start = time.time()
        #de push moet in dezelde richting van de beweging van de vijand gebeuren
        richting = -1 if self.rect.centerx > speler.rect.centerx else 1
        speler.vx = richting*speler.snelheid
        speler.vy = (-speler.spring_hoogte)/2
        speler.op_grond = False
        
    
    
    def attack(self, speler): # kijkt of de mino de speler van voor raakt
        if speler.alive and not speler.schild:
            if self.rect.colliderect(speler.rect): # kijken of de recht(rechthoek rond de sprite) elkaar overlappen via colliderect()
                if self.rect.top < speler.rect.bottom:
                    self.push(speler)
                    speler.health -= 1
                    speler.schild_aan()
                    
            #De healthbar van de vijand daalt wanneer de speler op zijn hoofd springt
                elif speler.vy > 0 and abs(self.rect.top - speler.rect.bottom) < 3:
            #als de collsiie van boven gebeurt, als de speler valt
                    self.health -= 1
                    self.push(speler)
                    print("Enemy hit! New HP:", self.health)#debugging output 
                    
            if speler.health <= 0:
                speler.alive = False 
                print("GAME OVER")
                 
        
    
        
    def patrol(self, goal_left, goal_right): #Eerste level: de minotaurus loopt heen en weer om de speler in te rammen 
        if self.facing_left == True:
            self.move(-self.vx, 0)
            if self.rect.left <= goal_left:
                self.facing_left = False
                self.vertraag()
                #wanneer de vijand een muur inramt krijgt de speler 1 punt
        else:
            self.move(self.vx, 0)
            if self.rect.right >= goal_right:
                self.facing_left = True
                self.vertraag()
                
                   
                
    def vertraag(self):
        
        self.vertraagd = True
        #Wanneer de functie wordt opgeroepen dan wordt de start gelijkgesteld aan de huidige tijd, die blijft doorlopen 
        self.vertraag_start = time.time() 
        vx = max(1, self.vx / 2) #verlaagde snelheid 
        self.vx = vx  
    
    def versnel(self):
        
        self.versneld = True 
        self.vx += self.versnelling 
        self.versnelling += 1
        
    #alle bewegingen samengevoegd  
    def beweging(self, speler, map_level, screen):
        self.zwaartekracht()  
        self.vy = self.collisie_y(map_level)
        self.move(0, self.vy)
        
        if self.op_grond == True:
            self.patrol(0, SCREENWIDTH)
            
        tijdsverschil = time.time()-self.vertraag_start
        if self.vertraagd == True:
            #wanneer het vershil tussen de start en de huidige tijd groter is dan de duur, dan is de vertraging afgelopen
            if tijdsverschil > self.vertraag_duur:
                self.vertraagd = False
                self.vx = self.snelheid 
                self.versnel()
                
        tijdsverschil_schild = time.time()-self.schild_start  
        if self.schild and tijdsverschil_schild > self.schild_duur:
            self.schild = False
        #voor de overgang naar de tweede level zal de minotaurus even verdoofd zijn
        
        if self.hp < -4 and speler.points > 10:
            self.vertraag()
            
            
    def draw(self, screen):
    # Start with a clean, untinted copy of the sprite
        temp_sprite = self.sprite.copy()

        if self.schild:
        # Create tint overlay
            tint = pygame.Surface(temp_sprite.get_size(), pygame.SRCALPHA)
            tint.fill((100, 0, 0, 80))  # Cyan-ish tint with transparency
            temp_sprite.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    # Flip the sprite if needed
        if self.facing_left:
            temp_sprite = pygame.transform.flip(temp_sprite, True, False)

    # Draw the final result
        screen.blit(temp_sprite, self.rect.topleft)
        