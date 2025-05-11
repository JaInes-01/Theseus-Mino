import pygame
import time
from Vijand import Vijand, SCREENWIDTH, SCREENHEIGHT, fps
clock = pygame.time.Clock()

class Minotaurus2(Vijand):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.facing_left = False #in het begin kijkt de minotaurus naar links want hij zit helemaal links
        self.vx = snelheid
        self.vy = 0
        self.op_grond = False
        self.spring_hoogte = speler.spring_hoogte
        self.target = speler    
    
    def beweging(self, speler, map_level):
        self.zwaartekracht()  
        self.vy = self.collisie_y(map_level)
        self.move(0, self.vy)
        
        if self.op_grond:
            marge = 40
            if self.target.rect.centerx < self.rect.centerx and abs(self.target.rect.centerx - self.rect.centerx) > marge: #kijkt of de speler (via het middelpunt van rechthoek van speler) links van de minotaurus ligt
                self.move(-self.snelheid, 0) #minotaurus verplaats zich naar links met self.snelheid aantal pixels
                self.facing_left = True #Nodig voor draw functie om te weten of we de image moeten flippen of niet
            elif self.target.rect.centerx > self.rect.centerx and abs(self.target.rect.centerx - self.rect.centerx) > marge:
                self.move(self.snelheid, 0)
                self.facing_left = False
                
    def draw(self,screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)# gaat minautorus horizontaal flippen als het naar de een andere kant beweegt
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)





