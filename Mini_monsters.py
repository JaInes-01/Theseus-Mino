import pygame
import time
from Vijand import Vijand
from Minotaurus1 import Minotaurus1, SCREENWIDTH, SCREENHEIGHT, fps

aantal_blokken_horizontaal = 20
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal

clock = pygame.time.Clock()
class Mini_monsters(Minotaurus1):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.goal_l = x - tile_grootte
        self.goal_r = x + 2*tile_grootte 
        self.vy = 0
        self.op_grond = False
        
        self.damage_timer = 0 #wachttijd tss schade (dus tijd die nog moet aftellen)
        self.no_damage_time_left = 1000 #speler is tijdens 1 sec onkwetsbaar nadat hij geraakt werd
        
        self.max_health = 2
        self.health = self.max_health
        self.nodige_hp = 0
        
        
    def attack(self, speler):
        
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
                    speler.health -= 1 
                    self.push(speler)
                    speler.damage_timer = speler.no_damage_time_left
                    print("enemy shield:", self.damage_timer, "player hp:", speler.health)
                else:
                    self.health -= 1
                    self.push(speler)
                    self.damage_timer = self.no_damage_time_left
                    speler.damage_timer = speler.no_damage_time_left
                    print("Enemy hit! New HP:", self.health)
            
            #nieuwe aanval op de vijand: langs de zijkant als m gedrukt wordt en als speler gewapend is
            elif horizonaanval:
                print("Speler shield:", speler.damage_timer) 
                keys = pygame.key.get_pressed()
                #speler gewapend + k => vijand verliest hp
                if speler.m_pressed and speler.gewapend:
                    self.health -= 1
                    self.push(speler)
                    speler.damage_timer = speler.no_damage_time_left
                    print("Side attack! Enemy HP:", self.health)
                    
                #speler gewapend maar m niet gedrukt => speler verliest hp
                else:
                    if speler.damage_timer == 0:
                        speler.health -= 1
                        self.push(speler)
                        speler.damage_timer = speler.no_damage_time_left
                        print("Player hit! New Player HP:", speler.health)
                
        
            if speler.health <= 0:
                speler.alive = False
                print("GAME OVER")
            
    def beweging(self, speler, map_level, screen):
        self.zwaartekracht() 
        self.vy = self.collisie_y(map_level)
        self.move(0, self.vy)
        if self.op_grond == True:
            self.patrol(self.goal_l, self.goal_r)
            
       
        if self.damage_timer > 0:
            self.damage_timer -= self.no_damage_time_left/fps
            if self.damage_timer < 0:
                self.damage_timer = 0
