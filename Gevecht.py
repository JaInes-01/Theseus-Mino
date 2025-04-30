# Simple pygame program

# Import and initialize the pygame library
import pygame
import math
SCREENWIDTH = 1000
SCREENHEIGHT = 500

pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
clock = pygame.time.Clock()

class Object: 
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Figuur(Object): # figuur klasse aanmaken -> speler en vijand voorstellen als rechthoek voor botsing
    def __init__(self, x, y):
        super().__init__(x, y)
    def draw(self):
        pass
    def botsing(self, andereFiguur): #MOET AANGEPAST WORDEN
        if(isinstance(self,Cirkel)): #x,y is midden van de cirkel en voor de botsing willen we linker en rechter bovenhoek.
            x1 = self.x-self.radius
            y1 = self.y-self.radius
            x2 = self.x + self.radius
            y2 = self.y + self.radius
        else: #voor een rechthoek is x en y de linkerbovenhoek
            x1 = self.x
            y1 = self.y
            x2 = self.x + self.basis
            y2 = self.y + self.hoogte
        if(isinstance(andereFiguur,Cirkel)):
            andereFiguurx1 = andereFiguur.x-andereFiguur.radius
            andereFiguury1 = andereFiguur.y-andereFiguur.radius
            andereFiguurx2 = andereFiguur.x + andereFiguur.radius
            andereFiguury2 = andereFiguur.y + andereFiguur.radius
        else:
            andereFiguurx1 = andereFiguur.x
            andereFiguury1 = andereFiguur.y
            andereFiguurx2 = andereFiguur.x + andereFiguur.basis
            andereFiguury2 = andereFiguur.y + andereFiguur.hoogte
        # https://silentmatt.com/rectangle-intersection/

        if x1 < andereFiguurx2 and x2 > andereFiguurx1 and y1 < andereFiguury2 and y2 > andereFiguury1:
            return True
        else:
            return False
        
class Rechthoek(Figuur):
    def __init__(self, x, y, basis, hoogte):
        super().__init__(x,y)
        self.basis = basis
        self.hoogte = hoogte
        

class Vast_object(Object):#voor de gevechten zal het handig zijn om de platforms en wapens als vaste objecten te beschouwen
    def __init__(self, x, y, afbeelding):
        super().__init__(x, y)
        #self.afbeelding =  
        
class Bewegend_object(Object):
    def move(self, vx, vy):
        self.x += vx
        self.y += vy
        
class Speler(Bewegend_object, Rechthoek):
    def __init__(self, x, y, vx, vy, afbeelding1, afbeelding2, afbeelding3): #meerdere afbeelding voor een animatie (?)
        super().__init__(x, y, vx, vy, basis, hoogte)
        #self.afbeelding= 
        
    def beweeg(self):
        vx = 0
        vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            vx = 10
        if keys[pygame.K_LEFT]:
            vx = -10
        if keys[pygame.K_UP]: #moet aangepast worden voor effect van zwaartekracht
            vy = -10
        if keys[pygame.K_DOWN]:
            vy = 10
        super().move(vx,vy)
    
class Bot(Bewegend_object, Rechthoek):
    def __init__(self, x, y,vx,vy,):
        
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
    pygame.display.flip()
pygame.quit()