import pygame
import sys
import time
import math 
from Objecten import VastObject, BewegendObject, SCREENWIDTH, SCREENHEIGHT
from Speler import Speler 
from Vijand import Vijand
from Minotaurus1 import Minotaurus1
#from Minotaurus2 import Minotaurus2
from Map import Map, aantal_blokken_horizontaal, tile_grootte, aantal_blokken_verticaal, map_niv1, map_niv2
from Mini_monsters import Mini_monsters
from Vallende_steen import Vallende_steen, vallende_stenen, laatste_val, val_interval
from MinotaurusVolg import MinotaurusVolg

background = pygame.image.load("background_fight.png")
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
intro_background = pygame.image.load("intro_fight.png")
intro_background = pygame.transform.scale(intro_background, (SCREENWIDTH, SCREENHEIGHT))
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()
fps = 30

niveau1 = Map(map_niv1)
niveau2 = Map(map_niv2)
#niveau3 = Map(map_niv3)



#LEVEL3
#stenen = pygame.sprite.Group()
#Mino2 = Minotaurus2(700, 550, 6 , 1/10, 1/10, "Minotaurus.png", Theseus, niveau1, stenen)

#we maken een dictionary aan van alle levels, met hun map, objecten en vijand
levels = {1:{"map": niveau1}, 2:{"map": niveau2}}

huidige_level = 1
gevecht_gewonnen = False
vijanden = []

start_time_level = None
def reset_level():
    global vijanden, Theseus, Zwaard, MinoVolg
    map_data = levels[huidige_level]["map"]
    Zwaard = VastObject(tile_grootte, 7*tile_grootte, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "zwaard2.png")
    if huidige_level == 1:
        Theseus = Speler(20, 500, 5, 1/30, 1/30, "speler.png", map_data, Zwaard)
        Mino1 = Minotaurus1(800, 400, 6, 1/10, 1/10, "Minotaurus.png", Theseus, niveau1)
        levels[huidige_level]["vijand"] = Mino1
    
    if huidige_level == 2:
        global start_time_level, MinoVolg
        start_time_level = time.time()
        Theseus = Speler(20, 500, 5, 1/30, 1/30, "speler.png", map_data, Zwaard)
        Mini1 = Mini_monsters(4*tile_grootte, 2*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
        Mini2 = Mini_monsters(11*tile_grootte, 2*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
        Mini3 = Mini_monsters(17*tile_grootte, 6*tile_grootte, 2, tile_grootte/SCREENWIDTH, tile_grootte/SCREENWIDTH, "Monster.png", Theseus, niveau2)
        MinoVolg= MinotaurusVolg(0, 500, 6, 1/10, 1/10, "Minotaurus.png", Theseus, niveau2)
        levels[huidige_level]["vijand"] = [Mini1, Mini2, Mini3]
    
    
        

def game_run(levels):
    global huidige_level, gevecht_gewonnen, laatste_val, start_time_level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    if huidige_level > len(levels):
        return 
    map_data = levels[huidige_level]["map"]
    vijanden = levels[huidige_level]["vijand"]  
    pijl = VastObject(800, 500, 1/9, 1/9, "pijl_gevecht.png")
    
    if not isinstance(vijanden, list):
        vijanden = [vijanden]
    screen.blit(background, (0, 0))
    for vijand in vijanden:
        vijand.beweging(Theseus, map_data, screen) 
        vijand.draw(screen)  
        vijand.attack(Theseus)
        vijand.draw_healthbar(screen)
        
    map_data.draw(screen)
    
            
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
        if vijand.health < 1:
            pijl.draw(screen)
            if Theseus.rect.right == SCREENWIDTH:
                huidige_level += 1
                reset_level()
                
      
    if huidige_level == 2:
        #if Theseus.rect.bottom < SCREENHEIGHT - 7*tile_grootte:
        if time.time()-start_time_level > 5:
            MinoVolg.draw(screen)
            MinoVolg.beweging(Theseus, niveau2)
            if Theseus.rect.colliderect(MinoVolg.rect):
                Theseus.alive = False
            
        Zwaard.draw(screen) 
        if Theseus.rect.colliderect(Zwaard.rect):
            Theseus.inventory.append(Zwaard)
            Zwaard.sprite.set_alpha(0)
        if len(Theseus.inventory) > 0:
            Theseus.gewapend = True 
        else:
            Theseus.gewapend = False
        if all(vijand.health <= 0 for vijand in vijanden):
            pijl = VastObject(800, 5*tile_grootte, 1/9, 1/9, "pijl_gevecht.png")
            pijl.draw(screen)
            if Theseus.rect.right == SCREENWIDTH:
                #huidige_level += 1
                #reset_level()
                #start_time_level = 0
                gevecht_gewonnen = True
    Theseus.draw(screen)
    Theseus.beweging(map_data)
    Theseus.draw_healthbar(screen)
    
    if Theseus.health <= 0:
        Theseus.alive = False 
    
    
    if not Theseus.alive:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 80)# lettertype en grootte
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))#Zet tekst om naar afbeelding (True -> gladde randen)
        text_rect = game_over_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2))#rechthoek van game over afbeelding in het midden van afbeelding zetten
        screen.blit(game_over_text, text_rect)#tekent afbeelding op scherm
        font = pygame.font.SysFont(None, 40)
        play_again_text = font.render("press 'r' to play again", True, (255, 255, 255))#Zet tekst om naar afbeelding (True -> gladde randen)
        text_rect = game_over_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 4))#rechthoek van game over afbeelding in het midden van afbeelding zetten
        screen.blit(play_again_text, text_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            huidige_level = 1
            reset_level() 
            
    #if huidige_level == 3:
        #als de speler level 3 wint dan wordt een flag ingevoerd die zegt dat hij het gevecht heeft gewonnen
        #if vijand.health < 1 and Theseus.health > 0:
            #gevecht_gewonnen = True 
    
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
                   
