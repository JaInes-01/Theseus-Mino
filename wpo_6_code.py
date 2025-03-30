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


class Figuur(Object):
    def __init__(self, x, y, kleur):
        super().__init__(x, y)
        self.kleur = kleur

    def inFiguur(self):
        pass

    def draw(self):
        pass

    def botsing(self, andereFiguur):
        if(isinstance(self,Cirkel)): #x,y is midden van de cirkel en voor de botsing willen we linker en rechter bovenhoek.
            x1 = self.x-self.radius
            y1 = self.y-self.radius
            x2 = self.x + self.radius
            y2 = self.y + self.radius
        else: #voor een rechthoek is x en y de linkerbovenhoek
            x1 = self.x
            y1 = self.y
            x2 = self.x + self.breedte
            y2 = self.y + self.hoogte
        if(isinstance(andereFiguur,Cirkel)):
            andereFiguurx1 = andereFiguur.x-andereFiguur.radius
            andereFiguury1 = andereFiguur.y-andereFiguur.radius
            andereFiguurx2 = andereFiguur.x + andereFiguur.radius
            andereFiguury2 = andereFiguur.y + andereFiguur.radius
        else:
            andereFiguurx1 = andereFiguur.x
            andereFiguury1 = andereFiguur.y
            andereFiguurx2 = andereFiguur.x + andereFiguur.breedte
            andereFiguury2 = andereFiguur.y + andereFiguur.hoogte
        # https://silentmatt.com/rectangle-intersection/

        if x1 < andereFiguurx2 and x2 > andereFiguurx1 and y1 < andereFiguury2 and y2 > andereFiguury1:
            return True
        else:
            return False


class Cirkel(Figuur):
    def __init__(self, x, y, kleur, radius):
        super().__init__(x, y, kleur)
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, self.kleur, (self.x, self.y), self.radius)


class Rechthoek(Figuur):
    pass

class VastObject(Object):
    pass


class BewegendObject(Object):
    def move(self, vx, vy):
        self.x += vx
        self.y += vy


class Speler(BewegendObject,Rechthoek):
    pass


class Bot(BewegendObject, Cirkel):
    def __init__(self, x, y, kleur,radius,point_left, point_right,snelheid):
        super().__init__(x, y, kleur,radius)
        self.vx = snelheid
        self.vy = 0
        self.point_left = point_left
        self.point_right = point_right
        self.goal = point_right
        self.snelheid = snelheid

    def patrol(self):
        if self.goal > self.x and self.goal == self.point_left:
            self.goal = self.point_right
            self.vx = self.snelheid
        if self.goal<self.x and self.goal == self.point_right:
            self.goal = self.point_left
            self.vx = -self.snelheid
        super().move(self.vx, self.vy)


class Knop(VastObject, Figuur):
    pass


class Obstakel(Figuur):
    pass

list_of_objects = []
bot1 = Bot(x=500, y=475, kleur=(0, 0, 255), radius = 25, point_left=200, point_right=700, snelheid=2)
list_of_objects.append(bot1)
# Run until the user asks to quit
running = True
while running:
    clock.tick(20)
    screen.fill((255, 255, 255))

    for object in list_of_objects:
        if hasattr(object, "draw"):
            object.draw()
        if hasattr(object,"patrol"):
            object.patrol()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
