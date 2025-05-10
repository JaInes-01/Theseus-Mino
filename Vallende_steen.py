import pygame
import time
clock = pygame.time.Clock()
from Objecten import BewegendObject, SCREENWIDTH, SCREENHEIGHT, fps
import random 

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
vallende_stenen = []
laatste_val = time.time()
val_interval = 3
        

