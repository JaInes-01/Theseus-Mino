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
        return vy
    
class Minotaurus1(Vijand):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.facing_left = True #in het begin kijkt de minotaurus naar links want hij zit helemaal links
        self.vertraagd = False #wanneer de vijand botst tegen de speler willen we dat hij voor enkele seconden vertraagt
        self.vertraag_duur = 2
        self.vertraag_start = 0
    
    def push(self, speler):
        if not speler.schild:
            speler.pushed = True
            speler.schild = True
            speler.push_start = time.time()
            speler.schild_start = time.time()
            #de push moet in dezelde richting van de beweging van de vijand gebeuren
            richting = -1 if self.rect.centerx > speler.rect.centerx else 1
            speler.vx = richting*speler.snelheid
            speler.vy = (-speler.spring_hoogte)/2
            speler.op_grond = False
        
    def attack(self, speler):
        #De healthbar van de vijand daalt wanneer de speler op zijn hoofd springt
        if self.rect.colliderect(speler.rect) and speler.rect.bottom > self.rect.top:
            self.push(speler)
            self.hp -= 1
            speler.points += 1
        
        #De healthbar van de speler daalt als die de vijand raakt langs de zijkant en als de schild niet actief is
        elif self.rect.colliderect(speler.rect) and speler.rect.bottom < self.rect.top and not speler.schild:
            self.push(speler)
            speler.schild_aan()
            speler.hp -= 1
            print("Speler geraakt zonder schild, HP:", speler.hp)  # Debugging
        return self.hp, speler.hp, speler.points
        
    
        
    def patrol(self): #Eerste level: de minotaurus loopt heen en weer om de speler in te rammen 
        if self.facing_left == True:
            self.move(-self.vx, 0)
            if self.rect.left <= 0:
                self.facing_left = False
                self.vertraag()
        else:
            self.move(self.vx, 0)
            if self.rect.right >= SCREENWIDTH:
                self.facing_left = True
                self.vertraag()
                
    def vertraag(self):
        self.vertraagd = True
        #Wanneer de functie wordt opgeroepen dan wordt de start gelijkgesteld aan de huidige tijd, die blijft doorlopen 
        self.vertraag_start = time.time() 
        self.vx = 1 #verlaagde snelheid 
    
    
    
    #alle bewegingen samengevoegd  
    def beweging(self, speler, map_level):
        self.zwaartekracht()  
        self.vy = self.collisie_y(map_level)
        self.move(0, self.vy) 
        self.patrol()
        tijdsverschil = time.time()-self.vertraag_start
        if self.vertraagd == True:
            #wanneer het vershil tussen de start en de huidige tijd groter is dan de duur, dan is de vertraging afgelopen
            if tijdsverschil > self.vertraag_duur:
                self.vertraagd = False
                self.vx = self.snelheid
        
    def draw(self,screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)#gaat minautorus horizontaal flippen als het naar de een andere kant beweegt
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)
            
        
class Minotaurus2(Vijand):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.facing_left = True #in het begin kijkt de minotaurus naar links want hij zit helemaal links
    
    
    def volg_speler(self, speler):#https://stackoverflow.com/questions/50769980/how-do-i-make-an-enemy-follow-the-player-in-pygame(kan gebruiken voor later als minotaurus ook verticaal beweegt)
        marge = 2
        if self.target.rect.centerx < self.rect.centerx and abs(self.target.rect.centerx - self.rect.centerx) > marge: #kijkt of de speler (via het middelpunt van rechthoek van speler) links van de minotaurus ligt
           self.move(-self.snelheid, 0) #minotaurus verplaats zich naar links met self.snelheid aantal pixels
           self.facing_left = True #Nodig voor draw functie om te weten of we de image moeten flippen of niet
        elif self.target.rect.centerx > self.rect.centerx and abs(self.target.rect.centerx - self.rect.centerx) > marge:
             self.move(self.snelheid, 0)
             self.facing_left = False
             
        return 
    
    def beweging(self, speler, map_level):
        self.zwaartekracht()  # Roep zwaartekracht aan
        self.vy = self.collisie_y(map_level)  # Controleer collisie met tegels
        self.move(0, self.vy)  # Beweeg de vijand verticaal

        # Hier kan je ook de horizontale beweging toevoegen
        self.volg_speler(speler)  # Volg de speler

    
    def attack(self, speler):
        return None 
    
    def draw(self,screen):
       if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)# gaat minautorus horizontaal flippen als het naar de een andere kant beweegt
            screen.blit(flipped_sprite, self.rect.topleft)
       else:
            screen.blit(self.sprite, self.rect.topleft)

