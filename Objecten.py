#dit is de eerste superklasse dus definiëren we de basisinstellingen hier
import pygame 
import random 
import time
clock = pygame.time.Clock()
SCREENWIDTH = 1000
SCREENHEIGHT = 800
fps = 30


vallende_stenen = []
laatste_val = time.time()
val_interval = 3
    
class VastObject(): #invoegen van vaste objecten zoals tiles en wapens, hier worden de png's geload en geschaald
    def __init__(self, x, y, fact_basis, fact_hoogte, sprite_png): 
        #we gebruiken schalingsfactoren zodat de verhouding tussen de dimensies van alle objecten en de scherminstellingen dezelfde blijven indien we deze veranderen
        self.afbeelding = pygame.image.load(sprite_png)
        originele_basis = self.afbeelding.get_width()
        originele_hoogte = self.afbeelding.get_height()
        self.verhouding_hb = originele_hoogte/originele_basis
        #wanneer we de grootte van de sprites aanpassen willen we de verhouding breedte-hoogte niet wijzigen
        self.basis = int(SCREENWIDTH*fact_basis) 
        if fact_basis == fact_hoogte:# dit betekent dat de verhouding dezelfde blijft
            self.hoogte = int(self.basis*self.verhouding_hb)
        else: #in het geval dat we de verhouding willen veranderen
            self.hoogte = int(SCREENHEIGHT*fact_hoogte)
        self.sprite = pygame.transform.scale(self.afbeelding, (self.basis, self.hoogte))
        self.rect = pygame.Rect(x, y, self.basis, self.hoogte) #rechthoek voor collision-check en beweging van de speler
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.topleft))
        

class BewegendObject(VastObject): 
    def __init__(self, x, y, snelheid, fact_basis, fact_hoogte, sprite_png):
        super().__init__(x, y, fact_basis, fact_hoogte, sprite_png)
        self.vx = snelheid
        self.vy = snelheid
        
    
    def move(self, snelheidx, snelheidy):
        #positie aanpassen door snelheidscomponeneten toe te voegen aan de huidige positie
        self.rect.x += snelheidx 
        self.rect.y += snelheidy
