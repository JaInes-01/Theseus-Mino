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
        
    def push(self, speler):
        speler.pushed = True
        speler.push_start = time.time()
        #de push moet in dezelde richting van de beweging van de vijand gebeuren
        richting = -1 if self.rect.centerx > speler.rect.centerx else 1
        #speler.vx = richting*speler.snelheid
        speler.vy = (-speler.spring_hoogte)/2
        speler.op_grond = False
    
        
    def attack(self, speler):
        if speler.level_voltooid:
            return
        if speler.alive and self.rect.colliderect(speler.rect) and self.health > 0:
            bovenaanval = speler.vy > 0 and speler.rect.bottom <= self.rect.top + 5
            
            #De healthbar van de vijand daalt wanneer de speler op zijn hoofd springt
            if bovenaanval:
                if self.damage_timer > 0:
                    speler.health -= 1 
                    speler.damage_timer = speler.no_damage_time_left
                else:
                    self.health -= 1
                    self.push(speler)
                    self.damage_timer = self.no_damage_time_left
                    print("Enemy hit! New HP:", self.health)
            else:
                if speler.damage_timer <= 0:
                    speler.health -= 1
                    speler.damage_timer = speler.no_damage_time_left
                    self.push(speler)
                else:
                    pass
            if speler.health <= 0:
                speler.alive = False
                self.vertraag_duur = 1000
                self.vertraag()
                print("GAME OVER")
                 

    def patrol(self, goal_left, goal_right): #Eerste level: de minotaurus loopt heen en weer om de speler in te rammen 
        if self.facing_left == True:
            self.move(-self.vx, 0)
            if self.rect.left <= goal_left:
                self.facing_left = False
                self.vertraag()
                #wanneer de vijand een muur inramt krijgt de speler 1 punt
        else:
            self.move(self.vx, 0)
            if self.rect.right >= goal_right:
                self.facing_left = True
                self.vertraag()
                
                              
    def vertraag(self):
        self.vertraagd = True
        #Wanneer de functie wordt opgeroepen dan wordt de start gelijkgesteld aan de huidige tijd, die blijft doorlopen 
        self.vertraag_start = time.time() 
        vx = max(1, self.vx / 2) #verlaagde snelheid 
        self.vx = vx  
    
    def versnel(self):
        self.versneld = True 
        self.vx += self.versnelling 
        self.versnelling += 2
        
    #alle bewegingen samengevoegd  
    def beweging(self, speler, map_level, screen):
        self.zwaartekracht()  
        self.vy = self.collisie_y(map_level)
        self.move(0, self.vy)
        
        if self.op_grond == True:
            self.patrol(0, SCREENWIDTH)
            
        tijdsverschil = time.time()-self.vertraag_start
        if self.vertraagd == True:
            #wanneer het vershil tussen de start en de huidige tijd groter is dan de duur, dan is de vertraging afgelopen
            if tijdsverschil > self.vertraag_duur:
                self.vertraagd = False
                self.vx = self.snelheid 
                self.versnel()
                
        if self.damage_timer > 0:
            self.damage_timer -= self.no_damage_time_left/fps   # Decrease the timer
            if self.damage_timer < 0:
                self.damage_timer = 0   # Decrease the timer
            
        #voor de overgang naar de tweede level zal de minotaurus even verdoofd zijn
        if self.health < 1:
            self.vertraag()
            
            
    def draw(self, screen):
    # Start with a clean, untinted copy of the sprite
        temp_sprite = self.sprite.copy()

        if self.damage_timer > 0:
            tint = pygame.Surface(temp_sprite.get_size(), pygame.SRCALPHA)
            tint.fill((100, 0, 0, 80))  # Cyan-ish tint with transparency
            temp_sprite.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        if self.facing_left:
            temp_sprite = pygame.transform.flip(temp_sprite, True, False)
        screen.blit(temp_sprite, self.rect.topleft)
        
    def draw_healthbar(self, screen):# https://www.youtube.com/watch?v=E82_hdoe06M
        bar_width = self.basis #even lang als de speler
        bar_height = 7
        x = self.rect.x # x positie gelijk aan de linkerpositie van de speler
        y = self.rect.y - 10 # bar ligt een beetje boven de speler
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height)) # =rode balk = achtergrond van de healthbar
        groene_breedte = bar_width * (self.health / self.max_health) #geeft een percentage maal bar widht om te weten hoe groot de groen bar moet zijn
        pygame.draw.rect(screen, (0, 255, 0), (x, y, groene_breedte, bar_height))
        
    
class Vallende_steen(BewegendObject):     
    def __init__(self, snelheid, fact_basis, fact_hoogte, sprite_png):
        x = random.randint(0, SCREENWIDTH - 50)
        y = 0
        super().__init__(x, y,snelheid, fact_basis, fact_hoogte, sprite_png)
        self.vy = snelheid
        self.op_grond = False
        self.Fz = 0.5
        self.x = random.randint(0,SCREENWIDTH)
        self.y = 0
        self.basis = random.randint(10, 50) 
        self.hoogte = self.basis
        self.valt = False    
            
    def val(self):
        self.vy += self.Fz
        self.move(0,self.vy)

