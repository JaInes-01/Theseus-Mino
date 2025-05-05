import pygame
import time
from Vijand import Vijand 
SCREENWIDTH = 1000
SCREENHEIGHT = 800
aantal_blokken_horizontaal = 20
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

class Minotaurus2(Vijand):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level, stenen):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.facing_left = True #in het begin kijkt de minotaurus naar links want hij zit helemaal links
        self.vy = snelheid
        self.vx = snelheid
        self.op_grond = False
        self.spring_hoogte = speler.spring_hoogte
        self.state = "cooldown"        
        self.last_throw_time = time.time()
        self.gooi_tel = 0
            

    def beweging(self, speler, map_level, screen, stenen):
        
        self.zwaartekracht()
        self.move(0, self.vy)
        self.vy = self.collisie_y(map_level) 
        
        huidige_tijd = time.time()
    
        if self.state == "gooien":
            if self.gooi_tel < 3 and huidige_tijd - self.laatste_gooi_tijd > 0.5:
                self.gooi_steen(stenen)
                self.gooi_tel += 1
                self.laatste_gooi_tijd = huidige_tijd
            elif self.gooi_tel >= 3:
                self.state = "charging"
                self.charge_direction = 1 if speler.rect.centerx > self.rect.centerx else -1
                self.vx = snelheid*self.charge_direction

        elif self.state == "charging":
            self.move(self.vx, 0)
            if (self.charge_direction == 1 and self.rect.right > SCREENWIDTH) or (self.charge_direction == -1 and self.rect.left < 0):
               self.state = "cooldown"
               self.gooi_tel = 0
               self.cooldown_start = huidige_tijd
               self.vx = 0

            elif self.state == "cooldown":
                if huidige_tijd - self.cooldown_start > 2:
                    self.state = "gooien"

    def goooien(self, pygame.sprite.Group()):
        richting = -1 if self.facing_left else 1
        steen = Steen(self.rect.centerx, self.rect.centery, 5, 1/15, 1/15, "Steen.png", richting)
        stenen.add(steen)
        
    
    def draw(self,screen):
    
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)# gaat minautorus horizontaal flippen als het naar de een andere kant beweegt
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)

