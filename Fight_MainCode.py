import pygame
import time
import math 
from Objecten import VastObject, BewegendObject 
from Speler import Speler 
from Vijand import Vijand
from Minotaurus1 import Minotaurus1
from Minotaurus2 import Minotaurus2
from Map import Map
from Mini_monsters import Mini_monsters 
SCREENWIDTH = 1000
SCREENHEIGHT = 800

background = pygame.image.load("background_fight.png")
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
intro_background = pygame.image.load("intro_fight.png")
intro_background = pygame.transform.scale(intro_background, (SCREENWIDTH, SCREENHEIGHT))
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()
fps = 30

#de volgende code gebruiken om een zero matrix op te stellen

#scherm opdelen in vierkantjes ('tiles') om obstakels, platforms en grond in te voegen
aantal_blokken_horizontaal = 20
tile_grootte = SCREENWIDTH/aantal_blokken_horizontaal
aantal_blokken_verticaal = int(SCREENHEIGHT/tile_grootte)
#matrix opstellen die past bij het aantal blokken
rijen = aantal_blokken_verticaal
kolommen = aantal_blokken_horizontaal
zeros_matrix = [[5 for _ in range(kolommen)] for _ in range(rijen)]
for rij in zeros_matrix:
    print(rij)
    
map_zero = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


  #matrix voor de map    
map_niv2 =matrix = [[1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


map_niv1 = [[1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

map_niv3 = [[1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


niveau1 = Map(map_niv1)
niveau2 = Map(map_niv2)
niveau3 = Map(map_niv3)

Zwaard = VastObject(tile_grootte, 5*tile_grootte, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "zwaard2.png")

Theseus = Speler(20, 500, 5, 1/30, 1/30, "speler.png", niveau2, Zwaard)
Mino1 = Minotaurus1(700, 550, 6 , 1/10, 1/10, "Minotaurus.png", Theseus, niveau1)

Mini1 = Mini_monsters(5*tile_grootte, 9*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
Mini2 = Mini_monsters(11*tile_grootte, 3*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
Mini3 = Mini_monsters(17*tile_grootte, 7*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)

#LEVEL3
stenen = pygame.sprite.Group()
Mino2 = Minotaurus2(700, 550, 6 , 1/10, 1/10, "Minotaurus.png", Theseus, niveau1, stenen)

#we maken een dictionary aan van alle levels, met hun map, objecten en vijand
levels = {1:{"map": niveau1, "vijand" : [Mino1]}, 2:{"map": niveau2, "vijand": [Mini1, Mini2]}, 3:{"map": niveau3, "vijand": [Mino2]}}

def reset_level():
    global Theseus, Mino1, Mino2
    map_data = levels[huidige_level]["map"]
    
    if huidige_level == 1:
        Theseus = Speler(20, 500, 5, 1/30, 1/30, "speler.png", map_data, Zwaard)
        #Mino1 = Minotaurus1(700, 400, 6, 1/10, 1/10, "Minotaurus.png", Theseus, niveau1)
        levels[huidige_level]["vijand"] = Mino1
    
    if huidige_level == 2:
        Theseus = Speler(20, 500, 5, 1/30, 1/30, "speler.png", map_data, Zwaard)
        #Mini1 = Mini_monsters(4*tile_grootte, 3*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
        levels[huidige_level]["vijand"] = [Mini1, Mini2, Mini3]
    
    if huidige_level == 3:
        Theseus = Speler(20, 500, 5, 1/30, 1/30, "speler.png", map_data, Zwaard)
        levels[huidige_level]["vijand"] = [Mino2]
        
arrival_duur = 2
arrival_start = 0
arriving = False 
huidige_level = 1

def game_run(levels):
    global huidige_level
    if huidige_level > len(levels):
        return 
    map_data = levels[huidige_level]["map"]
    vijanden = levels[huidige_level]["vijand"]  
    
    if not isinstance(vijanden, list):
        vijanden = [vijanden]
    
    for vijand in vijanden:
        vijand.beweging(Theseus, map_data, screen)  # Update each enemy's movement
        vijand.draw(screen)  # Draw each enemy
        vijand.attack(Theseus)
    #if huidige_level == 1:
    map_data.draw(screen)
    Theseus.draw(screen)
    Theseus.beweging(map_data)

        
    if huidige_level == 2:
        Zwaard.draw(screen) 
        if Theseus.rect.colliderect(Zwaard.rect):
           Zwaard.sprite.set_alpha(0)
           
          #  #deur wordt geopend
        #if time.time()-arrival_start > arrival_duur:
         #   vijand.draw(screen)
         #   vijand.beweging(Theseus, map_data, screen)
        #vijand.attack(Theseus)
    
    if huidige_level == 3:
        stenen.beweging()
        stenen.draw(screen)
    
    #De speler krijgt 3 levens en de vijand 4. Om de spel langer te laten te duren moet de speler de vijand misntens 20 keer de muur inrammen 
    if Theseus.hp < -3:
        reset_level()
    elif vijand.hp < vijand.nodige_hp and Theseus.points > Theseus.nodige_points and Theseus.rect.right == SCREENWIDTH:
        huidige_level += 1
        reset_level()

intro_duur = 4
intro_start = 0
speler_intro = BewegendObject(0, 675, 3, 1/15, 1/15, "speler_intro.png")
Minotaurus_intro = BewegendObject(800, 500, 5, 1/5, 1/5, "Minotaurus_intro.png")
Fight_intro = BewegendObject(250, -100, 5, 1/2, 1/2, "FIGHT_intro.png")
move_duration = 1

def intro():
    global intro_start, speler_intro, Minotaurus_intro
    intro_start = time.time()
    move_start_time = time.time()
    while time.time() - intro_start < intro_duur:
        screen.blit(intro_background, (0, 0))
        if time.time() - move_start_time < move_duration:
            speler_intro.move(2, 0)
            Minotaurus_intro.move(-2, 0) 
            Fight_intro.move(0,3)
        speler_intro.draw(screen)
        Minotaurus_intro.draw(screen)
        Fight_intro.draw(screen)
        pygame.display.flip()  # Update the display
        
running = True
reset_level()
intro_displayed = False 
while running:
    clock.tick(30)
    if not intro_displayed:
        intro()
        intro_displayed = True
    if time.time() - intro_start > intro_duur:
        intro_finished = True
    
    if intro_finished == True:
        screen.blit(background, (0, 0))
        game_run(levels)
    
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
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  

                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
