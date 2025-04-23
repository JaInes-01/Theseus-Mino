import pygame
import math
SCREENWIDTH = 1140
SCREENHEIGHT = 720

pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
clock = pygame.time.Clock()
#sprites en achtergronden definiëren 
achtergrond = pygame.image.load("GevechtBackground.png")
grond = pygame.image.load("grond.png")
grond = pygame.transform.scale(grond, (SCREENWIDTH, 100)) 


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

    
class VastObject(Object): #implementatie van figuur collisie-checker
    def __init__(self, x, y, basis, hoogte, sprite_png):
        super().__init__(x, y)
        self.basis = basis
        self.hoogte = hoogte
        self.sprite = pygame.image.load(sprite_png)
        self.sprite = pygame.transform.scale(self.sprite, (basis, hoogte))
        self.rect = pygame.Rect(x, y, basis, hoogte) #rechthoek voor collision-check en beweging van de speler
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.topleft)) #positie speler afhankelijk van rechthoek i.p.v. omgekeerd
        
class BewegendObject(VastObject): 
    def __init__(self, x, y, vx, vy, basis, hoogte, sprite_png):
        super().__init__(x, y, basis, hoogte, sprite_png)
        self.vx = vx
        self.vy = vy
    
    def move(self, vx, vy):
        self.rect.x += vx
        self.rect.y += vy
        self.x = self.rect.x
        self.y = self.rect.y


class Speler(BewegendObject):
    
    def __init__(self, x, y, vx, vy, basis, hoogte, sprite_png):
        super().__init__(x, y, vx, vy, basis, hoogte, sprite_png)
        self.facing_left = False 
    def beweeg(self):
        vx = 0
        vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            vx = 10
            self.facing_left = False
        if keys[pygame.K_LEFT]:
            vx = -10
            self.facing_left = True
        if keys[pygame.K_UP]:
            vy = -10
        if keys[pygame.K_DOWN]:
            vy = 10
        self.move(vx,vy)
        
    def draw(self, screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False) #enkel horizontaal flippen
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)

        
class Bot(BewegendObject):
    def __init__(self, x, y, vx, vy, basis, hoogte, sprite_png):
        super().__init__(x, y)
        self.vx = vx
        self.vy = vy
        self.basis = basis
        self.hoogte = hoogte 
        self.sprite = pygame.image.load(sprite_png)
        self.sprite = pygame.transform.scale(self.sprite, (basis, hoogte))
        self.rect = pygame.Rect(x, y, basis, hoogte) 
        
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


class Minotaurus(BewegendObject):
    def __init__(self, x, y, vx, vy, basis, hoogte, sprite_png):
        super().__init__(x, y, vx, vy, basis, hoogte, sprite_png)
        self.facing_left = True
        self.snelheid = vx

    def patrol(self):#nu beweegt de minotaurus heen en weer dit is de eerste 'attaque' van het spel
        if self.facing_left:
            self.rect.x -= self.snelheid
            if self.rect.left <= 0:
                self.facing_left = False
        else:
            self.rect.x += self.snelheid
            if self.rect.right >= SCREENWIDTH:
                self.facing_left = True

    def draw(self, screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False)
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)

# Objecten laden
thes = pygame.image.load("Theseus.png")
theseus = Speler(0, 500, 2, 0, int(thes.get_width() / 2), int(thes.get_height() / 2), "Theseus.png")

mino = pygame.image.load("Minotaurus.png")
minotaurus = Minotaurus(900, 500, 2, 0, int(mino.get_width() / 2), int(mino.get_height() / 2), "Minotaurus.png")

list_of_objects = [theseus, minotaurus]

# Spel-lus
running = True
while running:
    clock.tick(30)
    screen.fill((0, 0, 0))
    screen.blit(achtergrond, (0, 0))
    screen.blit(grond, (0, SCREENHEIGHT - 100))

    for object in list_of_objects:
        if hasattr(object, "draw"):
            object.draw(screen)
        if hasattr(object, "patrol"):
            object.patrol()
        if hasattr(object, "beweeg"):
            object.beweeg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    pygame.display.flip()

pygame.quit()
