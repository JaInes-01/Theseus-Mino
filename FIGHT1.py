import pygame
SCREENWIDTH = 1000
SCREENHEIGHT = 750

pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
clock = pygame.time.Clock()
#sprites en achtergronden definiëren 
achtergrond = pygame.image.load("GevechtBackground.png")
achtergrond = pygame.transform.scale(achtergrond, (SCREENWIDTH,SCREENHEIGHT))
 

#de volgende code gebruiken om een zero matrix op te stellen
SCREENWIDTH = 1000
SCREENHEIGHT = 800
#scherm opdelen in vierkantjes ('tiles') om obstakels, platforms en grond in te voegen
aantal_blokken_horizontaal = 20
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal
aantal_blokken_verticaal = int(SCREENHEIGHT/tile_grootte)
#matrix opstellen die past bij het aantal blokken
rijen = aantal_blokken_verticaal
kolommen = aantal_blokken_horizontaal
zeros_matrix = [[0 for _ in range(kolommen)] for _ in range(rijen)]
for rij in zeros_matrix:
    print(rij)
    
map_zero = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

map_data = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
[3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2],
[0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

class Object:
    def __init__(self, x, y):
        pass
    
class VastObject(Object): #implementatie van figuur voor collisie-check
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
    def __init__(self, x, y, dx, dy, fact_basis, fact_hoogte, sprite_png):
        super().__init__(x, y, fact_basis, fact_hoogte, sprite_png)
        self.dx = dx
        self.dy = dy
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        


class Speler(BewegendObject):
    
    def __init__(self, x, y, dx, dy, fact_basis, fact_hoogte, sprite_png):
        super().__init__(x, y, dx, dy, fact_basis, fact_hoogte, sprite_png)
        self.facing_left = False 
        self.dy = 0 
        self.op_grond = False
        self.Fz = 1
        self.spring_hoogte = self.hoogte/4
        
    def beweging(self):
        dx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            dx = 10
            self.facing_left = False
        if keys[pygame.K_LEFT]:
            dx = -10
            self.facing_left = True
            
        #update de positie     
        
        
        #sprong
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.op_grond:
            self.dy = -self.spring_hoogte #verticale snelheid is negatief want naar boven gericht
            self.op_grond = False
            
        self.dy += self.Fz #verticale snelheid wordt steeds groter, totdat het positief wordt en bijgevolg naar beneden wordt gericht
        dy = self.dy #dy is niet constant zoals dx en hangt af van de sprong
        
        #collisie checken in x-richting
        for tile in niveau1.tile_list:
            future_x = pygame.Rect(self.rect.x + dx, self.rect.y, self.basis, self.hoogte)
            if tile.rect.colliderect(future_x):
                if dx > 0:
                    dx = tile.rect.left - self.rect.right #dx blijft dalen naarmate dat de speler dichter komt, totdat dx nul wordt
                elif dx < 0:
                    dx = tile.rect.right - self.rect.left
                
        for tile in niveau1.tile_list:
            future_y = pygame.Rect(self.rect.x, self.rect.y + dy, self.basis, self.hoogte)
            #collisie checken in y-richting
            #op het moment dat de collisie wordt waargenomen is er al overlapping behalve als de speler op die exact moment stopt te bewegen, dus moeten we een toekomstige scenario gebruiken
            if tile.rect.colliderect(future_y):
                #als de collsiie van boven gebeurt, als de speler valt
                if self.dy > 0:
                    dy = tile.rect.top - self.rect.bottom #afstand tot de bovenkant van de platform
                    self.dy = 0 #we willen dat de speler stil blijft
                    self.op_grond = True 
                #als de collisie van onder gebeurt, als de speler springt
                elif self.dy < 0:
                    dy = tile.rect.bottom - self.rect.top #afstand tot de onderkant van de platform
                    self.dy = 0
                    
                    
        self.move(dx, dy)
        
    def draw(self, screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False) #enkel horizontaal flippen
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)

        
class Bot(BewegendObject):
    def __init__(self, x, y, dx, dy, fact_basis, fact_hoogte, sprite_png):
        super().__init__(x, y, dx, dy, fact_basis, fact_hoogte, sprite_png)
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def patrol(self):
        if self.goal > self.x and self.goal == self.point_left:
            self.goal = self.point_right
            self.dx = self.snelheid
        if self.goal<self.x and self.goal == self.point_right:
            self.goal = self.point_left
            self.dx = -self.snelheid
        super().move(self.dx, self.dy)

def rooster(): #visueel hulpmiddel voor het opstellen van de map 
    for line in range(0,aantal_blokken_horizontaal):
        pygame.draw.line(screen, (255,255,255), (0, line*tile_grootte), (SCREENWIDTH, line*tile_grootte))
        pygame.draw.line(screen, (255,255,255), (line*tile_grootte, 0), (line*tile_grootte, SCREENHEIGHT))

class Map():
    def __init__(self, matrix):
        self.tile_list = []
        
        for rij_index in range(len(matrix)):       #y-pos
            for kol_index in range(len(matrix[rij_index])):
                x = kol_index * tile_grootte
                y = rij_index * tile_grootte
                    
                if matrix[rij_index][kol_index] == 1: #nummer 1 is een blok
                    tile_afb = VastObject(x, y, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "blok.png")
                    self.tile_list.append(tile_afb)
                    
                elif matrix[rij_index][kol_index] == 2: #nummer 2 is een halve tegel
                    tile_afb = VastObject(x, y, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "halve.png")
                    self.tile_list.append(tile_afb)
                    
                elif matrix[rij_index][kol_index] == 3:
                    tile_afb = VastObject(x, y,tile_grootte/SCREENWIDTH , tile_grootte/SCREENWIDTH, "plathard.png")
                    self.tile_list.append(tile_afb)
                    
                elif matrix[rij_index][kol_index] == 4:
                    tile_afb = VastObject(x, y,tile_grootte/SCREENWIDTH , tile_grootte/SCREENWIDTH, "zwaard2.png")
                    self.tile_list.append(tile_afb)
            
    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile.sprite, tile.rect.topleft)
            
list_of_objects=[]
Theseus = Speler(0, 500, 0, 2, 1/30, 1/30, "speler.png")
list_of_objects.append(Theseus)

niveau1 = Map(map_data)
list_of_objects.append(niveau1)

running = True 


while running:
    clock.tick(30)
    screen.fill((0, 0, 0))
    screen.blit(achtergrond,(0,0))
    #screen.blit(grond, (0, SCREENHEIGHT - 100))
    #rooster() 
    niveau1.draw(screen)
    
    for object in list_of_objects:
        if hasattr(object, "draw"):
            object.draw(screen)
        if hasattr(object,"patrol"):
            object.patrol()
    Theseus.beweging()
    #ervoor zorgen dat speler niet uit het scherm komt
    if Theseus.rect.left < 0: 
        Theseus.rect.left = 0
    if Theseus.rect.right > SCREENWIDTH:
        Theseus.rect.right = SCREENWIDTH 
        
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

     # Flip the display
    pygame.display.flip()
pygame.quit()


