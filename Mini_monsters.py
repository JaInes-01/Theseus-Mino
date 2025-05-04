import pygame
import time
from Vijand import Vijand
from Minotaurus1 import Minotaurus1
SCREENWIDTH = 1000
SCREENHEIGHT = 800
aantal_blokken_horizontaal = 20
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal

class Mini_monsters(Minotaurus1):
    def __init__(self, x, y, snelheid, basis, hoogte, sprite_png, speler, map_level):
        super().__init__(x, y, snelheid, basis, hoogte, sprite_png, speler, map_level)
        self.goal_l = x - tile_grootte
        self.goal_r = x + 2*tile_grootte 
        self.vy = 0
        self.op_grond = False
        self.hp = 0
        self.nodige_hp = -1
        
    def attack(self, speler):
        keys = pygame.key.get_pressed()
        if self.rect.colliderect(speler.rect) and speler.gewapend and keys[pygame.K_s]:
            self.hp -= 1
            speler.points += 3
            print("Enemy hit! New HP:", self.hp)
        
        print("Speler geraakt zonder schild, HP:", speler.hp)
        
    def beweging(self, speler, map_level, screen):
        self.zwaartekracht() 
        self.vy = self.collisie_y(map_level)
        self.move(0, self.vy)
        if self.op_grond == True:
            self.patrol(self.goal_l, self.goal_r)
        
    
    def draw(self,screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)#gaat minautorus horizontaal flippen als het naar de een andere kant beweegt
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)