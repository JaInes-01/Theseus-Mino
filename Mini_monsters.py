import pygame
import time
from Vijand import Vijand
from Minotaurus1 import Minotaurus1, SCREENWIDTH, SCREENHEIGHT
aantal_blokken_horizontaal = 20
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal
player_is_attacking = None 
class Mini_monsters(Minotaurus1):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.goal_l = x - tile_grootte
        self.goal_r = x + 2*tile_grootte 
        self.vy = 0
        self.op_grond = False 
        self.max_health = 2
        self.health = self.max_health
        self.nodige_hp = 0
        
    def attack(self, speler):
        if speler.alive and self.rect.colliderect(speler.rect):
            bovenaanval = speler.vy > 0 and speler.rect.bottom <= self.rect.top + 5
            #De healthbar van de vijand daalt wanneer de speler op zijn hoofd springt
            if bovenaanval:
                self.health -= 1
                self.push(speler)
                print("Enemy hit! New HP:", self.health)
            else:
                keys = pygame.key.get_pressed()
                if not speler.schild:
                    # Check if the player is armed and attacking
                    if speler.gewapend and player_is_attacking:
                        self.health -= 1
                        self.push(speler)
                        print("Side attack! Enemy HP:", self.health)
                    else:
                        # Player takes damage
                        speler.health -= 1
                        speler.schild_aan()
                        self.push(speler)
                        print("Player hit! New Player HP:", speler.health)
                else:
                    print("Player is shielded, no damage taken.")
                    if speler.gewapend and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                        self.health -= 1
                        self.push(speler)
                    
            if speler.health <= 0:
                speler.alive = False
                self.vertraag_duur = 1000
                self.vertraag()
                print("GAME OVER")
            
    def beweging(self, speler, map_level, screen):
        self.zwaartekracht() 
        self.vy = self.collisie_y(map_level)
        self.move(0, self.vy)
        if self.op_grond == True:
            self.patrol(self.goal_l, self.goal_r)
        
    
    