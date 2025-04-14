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
thes = pygame.image.load("Theseus.png")
thes = pygame.transform.scale(thes, (thes.get_width()/2,thes.get_height()/2))
#thes = pygame.image.load

running = True 
while running:
    clock.tick(30)
    screen.fill((0, 0, 0))
    screen.blit(achtergrond,(0,0))
    screen.blit(grond, (0, SCREENHEIGHT - 100))
    screen.blit(thes, (0, 40))
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