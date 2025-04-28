import pygame 
from Objecten import VastObject, BewegendObject
SCREENWIDTH = 1000
SCREENHEIGHT = 800

class Vijand(BewegendObject):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png)
        self.facing_left = True #in het begin kijkt de minotaurus naar links want hij zit helemaal links
        self.vx = snelheid #tot nu toe beweegt hij alleen maar horizontaal
        self.projectielen = []
        #we zetten intervallen tussen de gooien
        self.gooi_timer=0

    def patrol(self):#nu beweegt de minotaurus heen en weer dit is de eerste 'attaque' van het spel
        if self.facing_left:
            self.rect.x -= self.vx
            if self.rect.left <= 0:
                self.facing_left = False
        else:
            self.rect.x += self.vx
            if self.rect.right >= SCREENWIDTH:
                self.facing_left = True
                
    def draw(self,screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)# gaat minautorus horizontaal flippen als het naar de een andere kant beweegt
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)
        for p in self.projectielen:
            p.draw(screen)

