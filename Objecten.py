import pygame 
SCREENWIDTH = 1000
SCREENHEIGHT = 800

    
class VastObject(): #implementatie van figuur voor collisie-check
    def __init__(self, x, y, fact_basis, fact_hoogte, sprite_png): #we gebruiken relatieve dimsensies zodat de verhouding tussen de dimensies van alle objecten dezelfde blijven indien we de scherminstellingen veranderen
        self.afbeelding = pygame.image.load(sprite_png)
        originele_basis = self.afbeelding.get_width()
        originele_hoogte = self.afbeelding.get_height()
        self.verhouding_hb = originele_hoogte/originele_basis
        
        self.basis = int(SCREENWIDTH*fact_basis)
        if fact_basis == fact_hoogte:# dit betekent dat de verhouding dezelfde blijft
            self.hoogte = int(self.basis*self.verhouding_hb)
        else: #in het geval dat we de verhouding willen veranderen
            self.hoogte = int(SCREENHEIGHT*fact_hoogte)
        
        self.sprite = pygame.transform.scale(self.afbeelding, (self.basis, self.hoogte))
        self.rect = pygame.Rect(x, y, self.basis, self.hoogte) #rechthoek voor collision-check en beweging van de speler
        #x, y = rect.topleft
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.topleft)) #positie speler afhankelijk van rechthoek i.p.v. omgekeerd
        

        
class BewegendObject(VastObject): 
    def __init__(self, x, y, snelheid, fact_basis, fact_hoogte, sprite_png):
        super().__init__(x, y, fact_basis, fact_hoogte, sprite_png)
        self.snelheid = snelheid
        
    
    def move(self, snelheidx, snelheidy):
        self.rect.x += snelheidx #de snelheid die verantwoordelijk is voor de beweging is niet per se dezelfde als die in het argument
        self.rect.y += snelheidy
