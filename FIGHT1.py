import pygame
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
    
class VastObject(Object): #implementatie van figuur voor collisie-check
    def __init__(self, x, y, basis, hoogte, sprite_png):
        super().__init__(x, y)
        self.basis = basis
        self.hoogte = hoogte
        self.sprite = pygame.image.load(sprite_png)
        self.sprite = pygame.transform.scale(self.sprite, (basis, hoogte))
        self.rect = pygame.Rect(x, y, basis, hoogte) #rechthoek voor collision-check en beweging van de speler
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.topleft)) #positie speler afhankelijk van rechthoek i.p.v. omgekeerd
        
    def collisie(self, andereObject):
        return self.rect.colliderect(andereObject.rect)
        
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
        self.vy = 0 
        self.op_grond = False
        self.Fz = 1
        self.hoogte = 15
        
    def beweeg(self):
        vx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            vx = 10
            self.facing_left = False
        if keys[pygame.K_LEFT]:
            vx = -10
            self.facing_left = True
        self.move(vx, self.vy) #de snelheid in de horizontale richitng is constant terwijl die in de verticale richting beïnvloed wordt door te springen
          
    def spring(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.op_grond:
            self.vy = -self.hoogte #verticale snelheid is negatief want naar boven gericht
            self.op_grond = False
            
        self.vy += self.Fz #verticale snelheid wordt steeds groter, totdat het positief wordt en bijgevolg naar beneden wordt gericht
        self.move(0, self.vy)     
    
        
    def draw(self, screen):
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.sprite, True, False) #enkel horizontaal flippen
            screen.blit(flipped_sprite, self.rect.topleft)
        else:
            screen.blit(self.sprite, self.rect.topleft)

        
class Bot(BewegendObject):
    def __init__(self, x, y, vx, vy, basis, hoogte, sprite_png):
        super().__init__(x, y, vx, vy, basis, hoogte, sprite_png)
        
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


list_of_objects=[]

thes_png = pygame.image.load("speler.png")
Theseus = Speler(0, 500, 2, 0, thes_png.get_width()*5, thes_png.get_height()*5, "speler.png")
list_of_objects.append(Theseus)

grond_png = pygame.image.load("grond.png")
grond_png = pygame.transform.scale(grond_png, (SCREENWIDTH, 100))
grond = VastObject(0,(SCREENHEIGHT-grond_png.get_height()), grond_png.get_width(), grond_png.get_height(), "grond.png") 

list_of_objects.append(grond)
running = True 


while running:
    clock.tick(30)
    screen.fill((0, 0, 0))
    screen.blit(achtergrond,(0,0))
    
    for object in list_of_objects:
        if hasattr(object, "draw"):
            object.draw(screen)
        if hasattr(object,"patrol"):
            object.patrol()
        if hasattr(object, "spring"):
            object.spring()
        if hasattr(object, "beweeg"):
            object.beweeg()
        
    if Theseus.collisie(grond) == True:
        Theseus.rect.bottom = grond.rect.top
        Theseus.vy = 0
        Theseus.op_grond = True
    else:
        Theseus.op_grond = False
    
    #ervoor zorgen dat speler niet uit het scherm komt
    if Theseus.rect.left < 0:
        Theseus.rect.left = 0
    if Theseus.rect.right > SCREENWIDTH:
        Theseus.rect.right = SCREENWIDTH 
        
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

     # Flip the display
    pygame.display.flip()
pygame.quit()
