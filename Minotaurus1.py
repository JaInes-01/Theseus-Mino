import pygame
import time
import random
from Objecten import VastObject, BewegendObject, SCREENWIDTH, SCREENHEIGHT, fps
from Vijand import Vijand, SCREENWIDTH, SCREENHEIGHT, fps
clock = pygame.time.Clock()
vallende_stenen = []
laatste_val = time.time()
val_interval = 3

#klasse minotaurus 1 erft van vijand- klasse 
class Minotaurus1(Vijand):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.facing_left = True #in het begin kijkt de minotaurus naar links want hij zit helemaal links
        self.op_grond = False# om te weten of minotaurus op grond staat of niet (nodig voor zwaartekracht)
        self.vertraagd = False #want wanneer de vijand botst tegen de speler willen we dat hij voor enkele seconden vertraagt
        self.versneld = False
        self.vertraag_duur = 1#tijd tot dat hij normale snelheid heeft
        self.vertraag_start = 0#tijdstip waarop vetraging begon (om vergelijken met huidige tijd)
        self.max_health = 6 #max aantal levens van minotaurus 
        self.health = self.max_health#wnr de minotaurus geslaan word dan verlaagt zijn totale leven
        self.alive = True # boolean om aan te geven of de minotaurus nog leeft (True) of dood is (False)
        
        self.damage_timer = 0 #wachttijd tss schade (dus tijd die nog moet aftellen)
        self.no_damage_time_left = 1000 #speler is tijdens 1 sec onkwetsbaar nadat hij geraakt werd
        
        self.versnelling = 4 # Waarde waarmee de snelheid toeneemt wanneer de minotaurus versnelt
        self.nodige_health = 0
# Functie om de speler weg te duwen nadat hij de vijand heeft geraakt of zelf geraakt werd
   def push(self, speler):
       speler.pushed = True  # Zet een vlag aan bij de speler dat hij net een duw kreeg (kan handig zijn voor animatie of gedrag)
       speler.push_start = time.time()  # Starttijd van de duw (kan gebruikt worden om te weten hoelang de speler wegvliegt)

     # Bepaal in welke richting de speler wordt geduwd:
     # Als de vijand rechts staat van de speler, dan duwen we naar links (-1)
     # Anders duwen we naar rechts (+1)
       richting = -1 if self.rect.centerx > speler.rect.centerx else 1
    # Je zou hier ook horizontale duw kunnen doen, maar dat is (mogelijk) uitgezet
    # speler.vx = richting * speler.snelheid
       speler.vy = (-speler.spring_hoogte) / 2  # De speler vliegt ook een beetje omhoog bij de duw, halve spronghoogte
       speler.op_grond = False  # Speler is tijdelijk in de lucht

# Aanval-functie van de vijand — bepaalt wat er gebeurt als hij de speler raakt
    def attack(self, speler):
        # Als het level al voltooid is, hoeft de vijand niets meer te doen
        if speler.level_voltooid:
            return
        # Check of de speler leeft én of er een botsing is én de vijand is nog niet dood
        if speler.alive and self.rect.colliderect(speler.rect) and self.health > 0:
             # Check of het een aanval van boven is: speler valt neer + onderkant speler is vlak boven de vijand
            bovenaanval = speler.vy > 0 and speler.rect.bottom <= self.rect.top + 5
            
            #De healthbar van de vijand daalt wanneer de speler op zijn hoofd springt
            if bovenaanval:
                if self.damage_timer > 0:# Vijand is nog in cooldown
                    speler.health -= 1 # Speler raakt gewond in plaats van vijand
                    speler.damage_timer = speler.no_damage_time_left# Speler tijdelijk onkwetsbaar
                else:
                    self.health -= 1# Vijand verliest een leven
                    self.push(speler)# Speler krijgt een duw terug
                    self.damage_timer = self.no_damage_time_left# Vijand wordt tijdelijk onkwetsbaar
                    print("Enemy hit! New HP:", self.health)# Debug: nieuwe levens van vijand
            # Als het GEEN bovenaanval is (botsing van voor of zijkant)
            else:
                if speler.damage_timer <= 0:# Speler is kwetsbaar
                    speler.health -= 1# Speler verliest leven
                    speler.damage_timer = speler.no_damage_time_left# Speler tijdelijk onkwetsbaar
                    self.push(speler) # Speler wordt weggeduwd
                else:
                    pass # Speler is in cooldown → geen schade
            # Als de speler geen levens meer heeft → spel voorbij
            if speler.health <= 0:
                speler.alive = False# Zet speler op dood
                self.vertraag_duur = 1000# Vijand vertraagt voor 1 seconde 
                self.vertraag()# Activeer de vertraging
                print("GAME OVER")# Debug print
                 
    # Beweging van de Minotaurus heen en weer tussen twee punten
    def patrol(self, goal_left, goal_right): #Eerste level: de minotaurus loopt heen en weer om de speler in te rammen 
        if self.facing_left == True:# Als hij naar links kijkt
            self.move(-self.vx, 0)# Beweeg naar links met snelheid vx
            # Als hij het linkerdoel bereikt heeft (bijv. een muur of grens)
            if self.rect.left <= goal_left:
                self.facing_left = False# Kijkrichting verandert naar rechts
                self.vertraag()# Wordt even trager (simulatie van botsing of draaien)
                #wanneer de vijand een muur inramt krijgt de speler 1 punt
        else:# Als hij naar rechts kijkt
            self.move(self.vx, 0)# Beweeg naar rechts met snelheid vx
             # Als hij het rechterdoel bereikt heeft
            if self.rect.right >= goal_right:
                self.facing_left = True # Kijkrichting verandert naar links
                self.vertraag()  # Wordt even trager (simuleert de impact van botsing of draaien)

                
    # Functie om de Minotaurus tijdelijk trager te maken                         
    def vertraag(self):
        self.vertraagd = True
        #Wanneer de functie wordt opgeroepen dan wordt de start gelijkgesteld aan de huidige tijd, die blijft doorlopen 
        self.vertraag_start = time.time() # Sla het huidige tijdstip op → zo weten we hoelang hij vertraagd is
        vx = max(1, self.vx / 2) #verlaagde snelheid 
        self.vx = vx   # Pas de snelheid aan

    # Functie om de Minotaurus sneller te maken
    def versnel(self):
        self.versneld = True 
        self.vx += self.versnelling 
        self.versnelling += 2
        
    #alle bewegingen samengevoegd  
    def beweging(self, speler, map_level, screen):
        self.zwaartekracht()  # zwaartekracht toepassen (verhoogt verticale snelheid als hij niet op de grond zit)
        self.vy = self.collisie_y(map_level)# checkt of hij de grond raakt en past vy aan op basis van botsing
        self.move(0, self.vy)# beweegt verticaal (alleen y-richting hier)

        # Als de Minotaurus op de grond staat, mag hij horizontaal heen en weer patrouilleren
        if self.op_grond == True:
            self.patrol(0, SCREENWIDTH) # loopt heen en weer over het hele scherm
         # bereken hoe lang de Minotaurus al vertraagd is   
        tijdsverschil = time.time()-self.vertraag_start
        if self.vertraagd == True:
            #wanneer het vershil tussen de start en de huidige tijd groter is dan de duur, dan is de vertraging afgelopen
            if tijdsverschil > self.vertraag_duur:
                self.vertraagd = False# stop met vertragen
                self.vx = self.snelheidzet #snelheid terug naar oorspronkelijke snelheid
                self.versnel()# versnelt opnieuw 

                
        if self.damage_timer > 0:
            self.damage_timer -= self.no_damage_time_left/fps   # Decrease the timer
            if self.damage_timer < 0:
                self.damage_timer = 0   # Decrease the timer
            
        #voor de overgang naar de tweede level zal de minotaurus even verdoofd zijn
        if self.health < 1:
            self.vertraag()
            
    # Tekent de Minotaurus op het scherm        
    def draw(self, screen):
    # Begin met een kopie van het sprite-object
        temp_sprite = self.sprite.copy()

        # Als de Minotaurus net geraakt is, krijgt hij een visuele tint om schade aan te geven
        if self.damage_timer > 0:
            tint = pygame.Surface(temp_sprite.get_size(), pygame.SRCALPHA)
            tint.fill((100, 0, 0, 80))  # Cyan-ish tint with transparency
            temp_sprite.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            
 # Als hij naar links kijkt, draai zijn sprite horizontaal om
        if self.facing_left:
            temp_sprite = pygame.transform.flip(temp_sprite, True, False)
        # Teken de sprite op het scherm op zijn huidige positie
        screen.blit(temp_sprite, self.rect.topleft)
        
    # Tekent de gezondheidsbalk boven de Minotaurus    
    def draw_healthbar(self, screen):# https://www.youtube.com/watch?v=E82_hdoe06M
        bar_width = self.basis #even lang als de speler
        bar_height = 7
        x = self.rect.x # x positie gelijk aan de linkerpositie van de speler
        y = self.rect.y - 10 # bar ligt een beetje boven de speler
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height)) # =rode balk = achtergrond van de healthbar
        groene_breedte = bar_width * (self.health / self.max_health) #geeft een percentage maal bar widht om te weten hoe groot de groen bar moet zijn
        pygame.draw.rect(screen, (0, 255, 0), (x, y, groene_breedte, bar_height))
        
  # Een klasse voor vallende stenen die uit de lucht vallen   
class Vallende_steen(BewegendObject):     
    def __init__(self, snelheid, fact_basis, fact_hoogte, sprite_png):
        # Kies een willekeurige horizontale positie waar de steen zal vallen
        x = random.randint(0, SCREENWIDTH - 50)
        y = 0# start helemaal bovenaan het scherm (y = 0)
# Roep de constructor aan van de bovenliggende klasse BewegendObject
        super().__init__(x, y,snelheid, fact_basis, fact_hoogte, sprite_png)
        self.vy = snelheid# Zet de verticale snelheid van de steen
        self.op_grond = False# Boolean om bij te houden of de steen al de grond heeft geraakt
        self.Fz = 0.5# Zwaartekrachtconstante (zorgt voor geleidelijke versnelling naar beneden)
        self.x = random.randint(0,SCREENWIDTH)# Kies een random x-positie
        self.y = 0# Zet de y-positie opnieuw op 0 
        self.basis = random.randint(10, 50) # Kies een willekeurige grootte voor de steen tussen 10 en 50 pixels
        self.hoogte = self.basis# Vierkante steen (hoogte = breedte)
        self.valt = False    # Boolean om te controleren of de steen in val is 
     
    #steen naar beneden te laten vallen
    def val(self):
        self.vy += self.Fzv# zwaartekracht verhoogt de snelheid elke frame
        self.move(0,self.vy)# verplaats de steen verticaal naar beneden volgens huidige snelheid


