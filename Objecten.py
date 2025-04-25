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
    def __init__(self, x, y, vx, vy, fact_basis, fact_hoogte, sprite_png):
        super().__init__(x, y, fact_basis, fact_hoogte, sprite_png)
        self.vx = vx
        self.vy = vy
    
    def move(self, vx, vy):
        self.rect.x += vx
        self.rect.y += vy

def volg_speler(self,Speler):#https://stackoverflow.com/questions/50769980/how-do-i-make-an-enemy-follow-the-player-in-pygame(kan gebruiken voor later als minotaurus ook verticaal beweegt)
    marge = 2 #als de speler statisch is en zijn center niet goed overeenkomt met de mino zal de minotaurus heen en weer bewegen
    #kijkt of de speler (via het middelpunt van rechthoek van speler) links van de minotaurus ligt
    if Speler.rect.centerx < self.rect.centerx - marge: #minotaurus verplaatst zich enkel als afstand >= marge 
        super().move(-self.vx,0) 
        self.facing_left = True #Nodig voor draw functie om te weten of we de image moeten flippen of niet
       
    elif Speler.rect.centerx > self.rect.centerx + marge:
        super().move(self.vx,0)
        self.facing_left = False