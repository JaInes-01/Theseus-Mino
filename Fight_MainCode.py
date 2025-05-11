import pygame
import sys
import time
import math 
from Objecten import VastObject, BewegendObject, SCREENWIDTH, SCREENHEIGHT
from Speler import Speler 
from Vijand import Vijand
from Minotaurus1 import Minotaurus1, Vallende_steen, vallende_stenen, laatste_val, val_interval
from Minotaurus2 import Minotaurus2
from Mini_monsters import Mini_monsters
from Map import Map, aantal_blokken_horizontaal, tile_grootte, aantal_blokken_verticaal, map_niv1, map_niv2
pygame.init()
clock = pygame.time.Clock()
fps = 30

background = pygame.image.load("background_fight.png")
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
intro_background = pygame.image.load("intro_fight.png")
intro_background = pygame.transform.scale(intro_background, (SCREENWIDTH, SCREENHEIGHT))

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
niveau1 = Map(map_niv1)
niveau2 = Map(map_niv2)

#we maken een dictionary aan van alle levels, met hun map, objecten en vijand
levels = {1:{"map": niveau1}, 2:{"map": niveau2}}
huidige_level = 1
start_time_level = None
gevecht_gewonnen = False
vijanden = []

def reset_level():
    global vijanden, Theseus, Zwaard, Mino2
    map_data = levels[huidige_level]["map"]
    Zwaard = VastObject(tile_grootte, 7*tile_grootte, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "zwaard2.png")
    if huidige_level == 1:
        Theseus = Speler(20, 500, 5, 1/30, 1/30, "speler.png", map_data, Zwaard)
        Mino1 = Minotaurus1(800, 400, 6, 1/10, 1/10, "Minotaurus.png", Theseus, niveau1)
        levels[huidige_level]["vijand"] = Mino1
    
    if huidige_level == 2:
        global start_time_level, Mino2
        start_time_level = time.time()
        Theseus = Speler(20, 500, 5, 1/30, 1/30, "speler.png", map_data, Zwaard)
        Mini1 = Mini_monsters(4*tile_grootte, 2*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
        Mini2 = Mini_monsters(11*tile_grootte, 2*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
        Mini3 = Mini_monsters(17*tile_grootte, 6*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
        Mino2 = Minotaurus2(0, 500, 6, 1/10, 1/10, "Minotaurus.png", Theseus, niveau2)
        levels[huidige_level]["vijand"] = [Mini1, Mini2, Mini3]
    
def game_run(levels):
    global huidige_level, gevecht_gewonnen, laatste_val, start_time_level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    if huidige_level > len(levels):
        return 
    
    screen.blit(background, (0, 0))
    map_data = levels[huidige_level]["map"]
    map_data.draw(screen)
    vijanden = levels[huidige_level]["vijand"]  
    pijl = VastObject(800, 500, 1/9, 1/9, "pijl_gevecht.png")
    
    #aangezien level 2 meerdere vijanden heeft, maken we van alle vijanden een lijst
    if not isinstance(vijanden, list):
        vijanden = [vijanden]
    for vijand in vijanden:
        vijand.beweging(Theseus, map_data, screen) 
        vijand.draw(screen)  
        vijand.attack(Theseus)
        vijand.draw_healthbar(screen)
                
    if huidige_level == 1:
        nu = time.time()
        if 0 < vijand.health < 4 and (Theseus.alive):
            if nu - laatste_val >= val_interval:
                val_steen = Vallende_steen(5, 1/15, 1/15, "Steen_wapen.png")
                vallende_stenen.append(val_steen)
                laatste_val = nu
            for steen in vallende_stenen:
                steen.val()
                steen.draw(screen)
                #als de speler een steen op zijn hoofd krijgt, dan verliest hij hp
                if steen.rect.colliderect(Theseus.rect) and Theseus.damage_timer == 0:
                    Theseus.health -= 1
                    Theseus.damage_timer = Theseus.no_damage_time_left
        
        if vijand.health < 1:  # Controleer of vijand verslagen is
            pijl.draw(screen) #vokg de pijl om naar level 2 te gaan
            if Theseus.rect.right == SCREENWIDTH: # Ga naar level 2
                reset_level()  # Reset de level instellingen
                return  # Stop de huidige run en ga verder met de nieuwe level

    if huidige_level == 2:
        Zwaard.draw(screen) 
        if time.time() - start_time_level > 5: #aangezien de minotaurus geneutraliseerd is in level 1 neemt het een beetje tijd voordat hij verschijnt
            Mino2.draw(screen)
            Mino2.beweging(Theseus, niveau2)
            if Theseus.rect.colliderect(Mino2.rect):
                Theseus.alive = False
        if Theseus.rect.colliderect(Zwaard.rect):
            Theseus.inventory.append(Zwaard)
            Zwaard.sprite.set_alpha(0)
        if len(Theseus.inventory) > 0:
            Theseus.gewapend = True 
        else:
            Theseus.gewapend = False
        if all(vijand.health <= 0 for vijand in vijanden):  # Controleer of alle vijanden verslagen zijn
            return gewonnen(True)
    #we tekenen Theseus op het einde zodat hij op de voorgrond verschijnt        
    Theseus.draw(screen)
    Theseus.beweging(map_data)
    Theseus.draw_healthbar(screen)
    if Theseus.health <= 0:
        Theseus.alive = False 
    if not Theseus.alive:
        return game_over(True)
    
class Intro:
    def __init__(self):
        self.speler = BewegendObject(0, 675, 3, 1/15, 1/15, "speler_intro.png")
        self.minotaurus = BewegendObject(800, 500, 5, 1/5, 1/5, "Minotaurus_intro.png")
        self.fight = BewegendObject(250, -100, 5, 1/2, 1/2, "FIGHT_intro.png")
        self.background = pygame.transform.scale(pygame.image.load("intro_fight.png"), (SCREENWIDTH, SCREENHEIGHT))
        self.anim_start = time.time()
        self.anim_duur = 1
        self.displayed = False
        self.finished = False

    def run(self, screen):
        if time.time() - self.anim_start < self.anim_duur:
            screen.blit(self.background, (0, 0))
            self.speler.move(4, 0)
            self.minotaurus.move(-4, 0)
            self.fight.move(0, 4)
        self.speler.draw(screen)
        self.minotaurus.draw(screen)
        self.fight.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

intro = Intro()
running = True
reset_level()

def gevecht():
    intro = Intro()
    running = True
    reset_level()
    game_started = False
    
    while running:
        clock.tick(fps)
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_m:  # Check if 'M' is pressed
                    print('M gets pressed')  # Debugging line to check if it's being detected
                    Theseus.m_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:  # Check if 'M' is released
                    Theseus.m_pressed = False
                    
        if not intro.displayed:
            intro.run(screen)
            if time.time() - intro.anim_start >= intro.anim_duur:
                intro.displayed = True
                print('intro_displayed')
                font = pygame.font.SysFont(None, 40)
                game_over_text = font.render("Press 'p' to start", True, (255, 255, 255))
                text_rect = game_over_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2))
                screen.blit(game_over_text, text_rect)

        elif intro.displayed and not intro.finished:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:  # Proceed to the game when 'p' is pressed
                screen.blit(background, (0, 0))
                intro.finished = True
                print('intro_finished')
                
        if intro.finished:
            game_run(levels)
        
            
    
        #we geven een return value aan de gevecht functie die aangeeft of de speler gewonnen had of verloren voordat hij het gevecht ver
        pygame.display.flip()
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    clock = pygame.time.Clock()
    gevecht()
    pygame.quit()   
