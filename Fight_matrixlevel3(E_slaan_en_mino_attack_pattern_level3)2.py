import pygame
import math 
import time

SCREENWIDTH = 1000
SCREENHEIGHT = 750

pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
clock = pygame.time.Clock()
fps = 30

 

#de volgende code gebruiken om een zero matrix op te stellen
SCREENWIDTH = 1000
SCREENHEIGHT = 800
#scherm opdelen in vierkantjes ('tiles') om obstakels, platforms en grond in te voegen
aantal_blokken_horizontaal = 20
tile_grootte = SCREENWIDTH//aantal_blokken_horizontaal
tile_grootte = SCREENWIDTH//aantal_blokken_horizontaal
aantal_blokken_verticaal = int(SCREENHEIGHT/tile_grootte)
#matrix opstellen die past bij het aantal blokken
rijen = aantal_blokken_verticaal
kolommen = aantal_blokken_horizontaal
zeros_matrix = [[5 for _ in range(kolommen)] for _ in range(rijen)]
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

map_back = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

def teken_background(matrix):
    for rij_index in range(len(matrix)):       #y-pos
        for kol_index in range(len(matrix[rij_index])):
            x = kol_index * tile_grootte
            y = rij_index * tile_grootte
            rect = pygame.Rect(kol_index * tile_grootte, rij_index * tile_grootte, tile_grootte, tile_grootte)
            if matrix[rij_index][kol_index] == 0:
                pygame.draw.rect(screen, (27, 75, 105), rect)
            elif matrix[rij_index][kol_index] == 1:
                pygame.draw.rect(screen, (0, 0, 0), rect)
  #matrix voor de map    
map_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]   
]



    
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
        
        
def frames(aantal_frames,):
    frames = []
    for i in range(aantal_frames):
       frames.append(afbeelding(sprite_sheet, i, 24, 24, ))
    return frames 

        
class Speler(BewegendObject):
    
    def __init__(self, x, y, vx, vy, fact_basis, fact_hoogte, sprite_png):
        super().__init__(x, y, vx, vy, fact_basis, fact_hoogte, sprite_png)
        self.facing_left = False 
        self.vy = 0 
        self.op_grond = False
        self.Fz = 1
        self.spring_hoogte = self.hoogte/4
        self.max_health = 3 #max aantal levens is 3 
        self.health = self.max_health
        self.alive = True #om te weten of het game over is of niet
        self.damage_timer = 0 #wachttijd tss schade (dus tijd die nog moet aftellen)
        self.no_damage_time_left = 1000 #speler is tijdens 1 sec onkwetsbaar nadat hij geraakt werd
        self.sla_cooldown = 0  # tijd tussen twee slagen
   
    def beweging(self):
        if not self.alive:
            return# speler stopt direct wnr hij dood is (dus hp helemaal op)
        if self.damage_timer > 0:#controleer of de speler nog kwetsbaar is als groter dan 0 dan is speler nog steeds onkwetsbaar
            self.damage_timer -= clock.get_time()#https://www.pygame.org/docs/ref/time.html (clock.get_time() geeft hvl milisecondes zijn voorbij gegaan sinds de vorige frame) dit toont hoe lang nog de speler onkwetsbaar is
 
        vx = 0 #speler blijft statisch indien geen keys gedrukt worden
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            vx = 5
            self.facing_left = False
        if keys[pygame.K_LEFT]:
            vx = -5
            self.facing_left = True
              
        #sprong
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.op_grond:
            self.vy = -self.spring_hoogte #verticale snelheid is negatief want naar boven gericht
            self.op_grond = False
        
        #zwaartekracht werkt op elk moment
        self.vy += self.Fz #verticale snelheid wordt steeds groter, totdat het positief wordt en bijgevolg naar beneden wordt gericht
        
        #dy definiëren
        vy = self.vy #dy is niet constant zoals dx en hangt af van de sprong
        
        #collisie checken in x-richting
        for tile in niveau1.tile_list:
            future_x = pygame.Rect(self.rect.x + vx, self.rect.y, self.basis, self.hoogte)
            if tile.rect.colliderect(future_x):
                if vx > 0:
                    vx = tile.rect.left - self.rect.right #dx blijft dalen naarmate dat de speler dichter komt, totdat dx nul wordt
                elif vx < 0:
                    vx = tile.rect.right - self.rect.left
                
        for tile in niveau1.tile_list:
            #op het moment dat de collisie wordt waargenomen is er al overlapping behalve als de speler op die exact moment stopt te bewegen, dus moeten we een toekomstige scenario gebruiken
            future_y = pygame.Rect(self.rect.x, self.rect.y + vy, self.basis, self.hoogte)
            #collisie checken in y-richting

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
                    
                    
        self.move(vx, vy)
   
    
        if keys[pygame.K_e] and self.sla_cooldown <= 0:
             if self.rect.colliderect(Minotaurus1.rect.inflate(20, 20)):
                 Minotaurus1.health -= 1
                 self.sla_cooldown = 1000  # 1 seconde cooldown
                 if Minotaurus1.health <= 0:
                     if Minotaurus1 in list_of_objects:
                        list_of_objects.remove(Minotaurus1)
    
    def draw(self, screen):
        if not self.alive:
            return# speler word niet meer op scherm getkent wnr hij dood is
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False) #enkel horizontaal flippen
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)
    
    def draw_healthbar(self, screen):# https://www.youtube.com/watch?v=E82_hdoe06M
        bar_width = self.basis #even lang als de speler
        bar_height = 5
        x = self.rect.x # x positie gelijk aan de linkerpositie van de speler
        y = self.rect.y - 10 # bar ligt een beetje boven de speler
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height)) # =rode balk = achtergrond van de healthbar
        groene_breedte = bar_width * (self.health / self.max_health) #geeft een percentage maal bar widht om te weten hoe groot de groen bar moet zijn
        pygame.draw.rect(screen, (0, 255, 0), (x, y, groene_breedte, bar_height))#wordt getekent op de rode bar hoe minder hp de speler heeft hoe kleiner de groene bar en groter de rode bar

class Bot(BewegendObject):
    def __init__(self, x, y, snelheid, fact_basis, fact_hoogte, sprite_png):
        super().__init__(x, y, fact_basis, fact_hoogte, sprite_png)
        self.snelheid = snelheid
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def patrol(self):
        if self.goal > self.x and self.goal == self.point_left:
            self.goal = self.point_right
            self.vx = self.snelheid
        if self.goal<self.x and self.goal == self.point_right:
            self.goal = self.point_left
            self.vx = -self.snelheid
        super().move(self.vx, self.vy)

def rooster():
    for line in range(0,aantal_blokken_horizontaal):
        pygame.draw.line(screen, (255,255,255), (0, line*tile_grootte), (SCREENWIDTH, line*tile_grootte))
        pygame.draw.line(screen, (255,255,255), (line*tile_grootte, 0), (line*tile_grootte, SCREENHEIGHT))

class Steen(BewegendObject):
    def __init__(self, x, y, snelheid, fact_basis, fact_hoogte, sprite_png, richting):
        super().__init__(x, y, snelheid * richting, 0, fact_basis, fact_hoogte, sprite_png)
        
    def beweging_steen(self):
        self.move(self.vx, self.vy)

class Vijand(BewegendObject):
    def __init__(self, x, y, vx, vy, basis, hoogte, sprite_png):
        super().__init__(x, y, vx, vy, basis, hoogte, sprite_png)
        self.state = "fase1"#begint naar links te lopen
        self.laatste_gooi_tijd = time.time()#slaat laatste moment op dat de mino de steen heeft gegooid
        self.gooi_aantal = 0#zodat we weten hvl keren de mino al een steen heeft gegooid (omdat hij mag max 3 keren stenen gooien (3 keren wnr hij rechts is en 3 keren wnr links dan loop) )
        self.spring_hoogte = 15
        self.op_grond = False#nodig voor Fz zodat hij alleen kan springen wnr hij op de grond is 
        self.vx = vx #tot nu toe beweegt hij alleen maar horizontaal
        self.vy = 0
        self.facing_left = True
        self.max_health = 5
        self.health = self.max_health
    
    def zwaartekracht(self):
        self.vy += 1#vy word 1 groter(Fz brengt mino omlaag)
        if self.vy > 10: #anders valt te snel
            self.vy = 10
    
    def collisie_y(self, map_level):
        self.op_grond = False
        for tile in map_level.tile_list:#pos van mino als hij springt of valt
            future_y = pygame.Rect(self.rect.x, self.rect.y + self.vy, self.basis, self.hoogte)
            if tile.rect.colliderect(future_y):# kijkt of mino raakt obstakel
                if self.vy > 0:#als mino valt
                    self.rect.bottom = tile.rect.top#zorgt dat mino niet door vloer gaat en dat mino landt op de grond (door de onderkant van de mino gelijk stellen aan bovenkant van tegel)
                    self.vy = 0#zodat hij stopt met vallen wnr hij de grond raakt
                    self.op_grond = True#zodat we kunnen weten of de mino kan springen of niet
                elif self.vy < 0:#als mino naar omhoog aan bewegen is en raakt de onderkant van een tegel dan gaat hij niet erdoor maar bots hij er tegen
                    self.rect.top = tile.rect.bottom
                    self.vy = 0#mino stopt met stijgen
        return self.vy
    
    def gooi_steen(self, stenen):
       if self.facing_left:
           richting = -1 #als mino kijkt naar links steen word naar links gegooid (dus richting -1)
       else: 
           richting = 1#steen naar rechts
       steen = Steen(self.rect.centerx, self.rect.centery, 5, 1/15, 1/15, "Steen.png", richting)#steen object gemaakt dat uit midden van mino komt met vx=5, grootte 1/15 van scherm
       stenen.add(steen)# de steen word dan toegevoegd aan de groep stenen zodat we het kunnen zien op het scherm

    def beweging(self, speler, map_level, screen, stenen):#beweging/aanval patroon van mino, gebeurt in meerdere fases die zich herhalen
        self.zwaartekracht()#roept functie zwaartekracht op (dat vy verhoogt)
        self.move(0, self.vy)#veranderd y pos
        self.vy = self.collisie_y(map_level)#of wel 0 of vy afhankelijk of hij de grond raakt of niet

        huidige_tijd = time.time()#slaat huidige tijdstip op in sec(zodat we weten wnr hij voor het laatst iets gedaan heeft)

# Loop naar links
        if self.state == "fase1":  # kijkt of we in fase 1 zijn
           self.facing_left = True
           if self.rect.left > 0:#mino beweegt enkel als hij nog niet aan de ran is 
              self.move(-self.vx, 0)# beweegt horizontaal naar links met snelheid vx
           else:
               self.state = "fase2"# nu begint de tweede fase (gooien van stenen) van het aanval (dus wnr mino helemaal links staat)
               self.gooi_aantal = 0
               self.laatste_gooi_tijd = huidige_tijd
# Gooi stenen links
        elif self.state == "fase2":  #kijkt of we in fase 2 zijn
             if self.gooi_aantal < 3 and huidige_tijd - self.laatste_gooi_tijd > 0.5:# als het aantal gegooide stenen kleiner is dan 3(das onze max) en de laatste steen gegooid was niet minder dan 0,5 sec geleden
                self.gooi_steen(stenen)# roept functie gooi steen op zodat de mino een steen gooit
                self.gooi_aantal += 1
                self.laatste_gooi_tijd = huidige_tijd
             elif self.gooi_aantal >= 3:#als er 3 stenen werden gegooid dan gaan we in fase 3
                  self.state = "fase3"
                  self.vx = 10
                  self.facing_left = False
# Charge naar rechts
        elif self.state == "fase3":
           if self.rect.right < SCREENWIDTH:
               self.move(self.vx, 0)
           else:
              self.state = "fase4"
              self.gooi_aantal = 0
              self.laatste_gooi_tijd = huidige_tijd

# Gooi stenen rechts
        elif self.state == "fase4":  
           if self.gooi_aantal < 3 and huidige_tijd - self.laatste_gooi_tijd > 0.5:
               self.gooi_steen(stenen)
               self.gooi_aantal += 1
               self.laatste_gooi_tijd = huidige_tijd
           elif self.gooi_aantal >= 3:
               self.state = "fase5"
# Loop naar midden
        elif self.state == "fase5":
           midden = SCREENWIDTH // 2
           if self.rect.centerx < midden:#dus als mino links van mid staat dan gaat hij naar rechts
              richting = 1 
           else: 
               richting = -1 # als hij rechts staat dan gaat hij naar links
           self.move(richting * self.vx, 0) #horizontale beweging van mino
           self.state = "fase6"

    # Spring als speler onder zit
        elif self.state == "fase6": 
           if self.op_grond and speler.rect.centerx > self.rect.left and speler.rect.centerx < self.rect.right: #zit mino op grond plus zit speler op rechter en (dus onder mino)linker kant van mino
               self.vy = -self.spring_hoogte# mino springt
           if not self.op_grond:
               # Mino in de lucht
               if self.rect.colliderect(speler.rect) and speler.damage_timer <= 0: #kijkt of de speler nog onder de mino is en of de speler kwetsbaar is
                   speler.health -= 1
                   speler.damage_timer = speler.no_damage_time_left#speler tijdelijk ontkwetsbaar
                   if speler.health <= 0:
                       speler.alive = False
               return# stopt met rest van functie (omdat we willen dat hij pas verder gaat wnr hij terug op de grond zit)
           else:
               self.state = "fase1"# wnr hij op de grond staat gaat hij terug naar fase 1 en herbegint het hele cyclus opnieuw

                
    def draw(self,screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)# gaat minautorus horizontaal flippen als het naar de een andere kant beweegt
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)
       
    
    def raakt_speler_van_voor(self, speler): # kijkt of de mino de speler van voor raakt
        if self.rect.colliderect(speler.rect): # kijken of de recht(rechthoek rond de sprite) elkaar overlappen via colliderect()
            if self.facing_left and self.rect.centerx > speler.rect.centerx:#kijk of de mino naar rechts kijkt en of zijn linkerkant(dus van de rechthoek) groter is dan die van de speler (dus hij kijkt of de mino de speler van voor raakt)
                return True
            elif not self.facing_left and self.rect.centerx < speler.rect.centerx:#zelfde als vorige maar omgekeerd dus wanneer de mino naar rechts kijkt en de speler via zijn voorkant raakt
                return True
        return False
    

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
                    tile_afb = VastObject(x, y,tile_grootte/SCREENWIDTH , tile_grootte/SCREENWIDTH, "zwaard2.png")
                    self.tile_list.append(tile_afb)
                    
                    
    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile.sprite, tile.rect.topleft)

list_of_objects=[]


Theseus = Speler(20, 500, 0, 2, 1/30, 1/30, "speler.png")
list_of_objects.append(Theseus)

stenen = pygame.sprite.Group()
Minotaurus1 = Vijand(800, 550, 4, 0, 1/10, 1/10, "Minotaurus.png")
list_of_objects.append(Minotaurus1)

#Steen = Projectiel(800, 550, 3, 3, 1/15, 1/15, "Steen.png", Theseus.rect.x, Theseus.rect.y)
#list_of_objects.append(Steen)

niveau1 = Map(map_data)
list_of_objects.append(niveau1)

running = True 


while running:
    clock.tick(30)
    screen.fill((0, 0, 0))
    
    #rooster()
    teken_background(map_back)
    niveau1.draw(screen)
    
    for object in list_of_objects:
        if hasattr(object, "draw"):
            object.draw(screen)
        if hasattr(object,"patrol"):
            object.patrol()
        if isinstance(object, Vijand):
            object.beweging(Theseus, niveau1, screen, stenen)
        elif hasattr(object, "beweging"):
            object.beweging()
        if hasattr(object, "volg_speler"):
            object.volg_speler(Theseus)
            
    Theseus.draw_healthbar(screen)
    
    for steen in list(stenen):
        steen.beweging_steen()
        steen.draw(screen)
        if Theseus.alive and Theseus.damage_timer <= 0:
        if steen.rect.colliderect(Theseus.rect):
            Theseus.health -= 1
            Theseus.damage_timer = Theseus.no_damage_time_left
            stenen.remove(steen) 
            if Theseus.health <= 0:
                Theseus.alive = False
                print("GAME OVER")
    
        
        
    if Theseus.alive and Theseus.damage_timer <= 0:
        if Minotaurus1.raakt_speler_van_voor(Theseus):
            Theseus.health -= 1  # 1 leven verliezen
            Theseus.damage_timer = Theseus.no_damage_time_left  # reset timer
            if Theseus.health <= 0:
                Theseus.alive = False
                print("GAME OVER")
            
        #if hasattr(object, "Gooien"):
            #object.Gooien(Theseus)
    #ervoor zorgen dat speler niet uit het scherm komt
    if Theseus.rect.left < 0: 
        Theseus.rect.left = 0
    if Theseus.rect.right > SCREENWIDTH:
        Theseus.rect.right = SCREENWIDTH
    
    if not Theseus.alive:# zorgt voor game over tekst wnr theseus healtbar=0
        font = pygame.font.SysFont(None, 80)# lettertype en grootte
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))#Zet tekst om naar afbeelding (True -> gladde randen)
        text_rect = game_over_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2))#rechthoek van game over afbeelding in het midden van afbeelding zetten
        screen.blit(game_over_text, text_rect)#tekent afbeelding op scherm

        
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