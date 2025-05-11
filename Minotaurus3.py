import pygame
import time
from Objecten import VastObject, BewegendObject, SCREENWIDTH, SCREENHEIGHT, fps
from Vijand import Vijand
clock = pygame.time.Clock()
stenen = pygame.sprite.Group()

class Minotaurus3(Vijand):
    def __init__(self, x, y, snelheid, fact_basis, fact_hoogte, sprite_png, speler, map_level, stenen):
        super().__init__(x, y, snelheid, fact_basis, fact_hoogte, sprite_png, speler, map_level)
        self.state = "fase1"#begint naar links te lopen
        self.laatste_gooi_tijd = time.time()#slaat laatste moment op dat de mino de steen heeft gegooid
        self.gooi_aantal = 0#zodat we weten hvl keren de mino al een steen heeft gegooid (omdat hij mag max 3 keren stenen gooien (3 keren wnr hij rechts is en 3 keren wnr links dan loop) )
        self.spring_hoogte = 15
        self.op_grond = False#nodig voor Fz zodat hij alleen kan springen wnr hij op de grond is 
        self.vx = snelheid #tot nu toe beweegt hij alleen maar horizontaal
        self.vy = 0
        self.facing_left = True
        self.max_health = 5
        self.health = self.max_health
        self.stenen = stenen 
        
    def zwaartekracht(self):
        self.vy += 1#vy word 1 groter(Fz brengt mino omlaag)
        if self.vy > 10: #anders valt te snel
            self.vy = 10
            
    
    def gooi_steen(self):
       if self.facing_left:
           richting = -1 #als mino kijkt naar links steen word naar links gegooid (dus richting -1)
       else: 
           richting = 1#steen naar rechts
       steen = Steen(self.rect.centerx, self.rect.centery, 5, 1/15, 1/15, "Steen.png", richting)#steen object gemaakt dat uit midden van mino komt met vx=5, grootte 1/15 van scherm
       self.stenen.add(steen)# de steen word dan toegevoegd aan de groep stenen zodat we het kunnen zien op het scherm

    def beweging(self, speler, map_level, screen):#beweging/aanval patroon van mino, gebeurt in meerdere fases die zich herhalen
        self.zwaartekracht()#roept functie zwaartekracht op (dat vy verhoogt)
        self.move(0, self.vy)#veranderd y pos
        self.vy = self.collisie_y(map_level)#of wel 0 of vy afhankelijk of hij de grond raakt of niet

        huidige_tijd = time.time()#slaat huidige tijdstip op in sec(zodat we weten wnr hij voor het laatst iets gedaan heeft)

# Loop naar links
        if self.state == "fase1":  # kijkt of we in fase 1 zijn
           self.facing_left = True
           self.move(-self.vx, 0)# beweegt horizontaal naar links met snelheid vx
           if self.rect.left <= 0:#als de x pos van de linkerzijde van rechthoek 0 is
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
            self.move(self.vx, 0)
            if self.rect.right >= SCREENWIDTH:#stopt wnr hij einde van scherm raakt
               self.state = "fase4"
               self.gooi_aantal = 0 # aantal stenen die werden gegooid word gereset
               self.laatste_gooi_tijd = huidige_tijd
# Gooi stenen rechts
        elif self.state == "fase4":  
           if self.gooi_tel < 3 and huidige_tijd - self.laatste_gooi_tijd > 0.5:
               self.gooi_steen(stenen)
               self.gooi_aantal += 1
               self.laatste_gooi_tijd = huidige_tijd
           elif self.gooi_tel >= 3:
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

       
    
    def attack(self, speler): # kijkt of de mino de speler van voor raakt
        #wanneer de speler een level heeft voltooid willen we niet dat hij nog aangevald kan worden
        if speler.level_voltooid:
            return
        #aanvallen gebeuren wanneer de speler levend is en wanneer er een collisie is onder bepaalde vw
        
        #we willen niet dat geneutraliseerde vijanden nog kunnen aanvallen
        if speler.alive and self.rect.colliderect(speler.rect) and self.health > 0:
            
            horizonaanval = abs(speler.rect.centerx - self.rect.centerx) <= 10
            bovenaanval = speler.vy > 0 and speler.rect.bottom <= self.rect.top + 20
            print("bovenaanval:", bovenaanval, "enemy shield:", self.damage_timer)
            
            #zelfde aanval als level1
            if bovenaanval:
                #als de speler aanvalt en de onkwetsbaarheid van de vijand nog actief is dan verliest de speler hp 
                if self.damage_timer > 0:
                    speler.health -= 0.5
                    self.push(speler)
                    speler.damage_timer = speler.no_damage_time_left
                    print("enemy shield:", self.damage_timer, "player hp:", speler.health)
                else:
                    self.health -= 0.5
                    self.push(speler)
                    self.damage_timer = self.no_damage_time_left
                    speler.damage_timer = speler.no_damage_time_left
                    print("Enemy hit! New HP:", self.health)
            
            #nieuwe aanval op de vijand: langs de zijkant als m gedrukt wordt en als speler gewapend is
            elif horizonaanval:
                print("Speler shield:", speler.damage_timer) 
                keys = pygame.key.get_pressed()
                #speler gewapend + k => vijand verliest hp
                #speler moet nu kwestbaarc zijn om attack uit te voeren
                if speler.m_pressed and speler.gewapend and speler.damage_time==0:
                    self.health -= 0.5
                    self.push(speler)
                    speler.damage_timer = speler.no_damage_time_left
                    print("Side attack! Enemy HP:", self.health)
                    
                #speler gewapend maar m niet gedrukt => speler verliest hp
                else:
                    if speler.damage_timer == 0:
                        speler.health -= 0.5
                        self.push(speler)
                        speler.damage_timer = speler.no_damage_time_left
                        print("Player hit! New Player HP:", speler.health)

            if speler.health <= 0:
                speler.alive = False
                print("GAME OVER")
    
    def draw(self,screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)# gaat minautorus horizontaal flippen als het naar de een andere kant beweegt
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)
        
class Steen(BewegendObject):
    def __init__(self, x, y, snelheid, fact_basis, fact_hoogte, sprite_png, richting):
        super().__init__(x, y, snelheid * richting, 0, fact_basis, fact_hoogte, sprite_png)
        
    def beweging_steen(self):
        self.move(self.vx, self.vy)
        

