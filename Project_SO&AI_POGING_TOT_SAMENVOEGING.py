# modules en initialisaties:  
import pygame # Pygame bibliotheek laden 
import sys
import random
from Minotaurus_Doolhof import Minotaurus 
from Speler_Doolhof import *
from Button_Doolhof import Button
from Doolhof import *
from Teleporteren_Doolhof import teleport_speler

#samenvoeging van de twee delen
from Fight_MainCode import reset_level, game_run, intro, niveau1, niveau2, niveau3, Zwaard, stenen, levels, intro_duur, intro_start, speler_intro, Minotaurus_intro, Fight_intro, SCREENWIDTH, SCREENHEIGHT
huidige_level = 1
vijanden = []
background = pygame.image.load("background_fight.png")
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
intro_background = pygame.image.load("intro_fight.png")
intro_background = pygame.transform.scale(intro_background, (SCREENWIDTH, SCREENHEIGHT))
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()
fps = 30




pygame.init() #pygame initialiseren

# de stenen laden (zodat we stenen muur krijgen ipv witte blokjes):
steen = pygame.image.load("steen.png")
steen = pygame.transform.scale(steen, (blokjesgrootte, blokjesgrootte))  # de afbeelding van schaal aanpassen zodat het overeenkomt met de grootte van een blokje

# De draad van Ariadne toevoegen:
DraadVanAriadne = pygame.image.load("DraadAriadne.png")  
DraadVanAriadne= pygame.transform.scale(DraadVanAriadne, (blokjesgrootte, blokjesgrootte))  
draad_locaties = kies_draadlocaties()


#Sleutel toevoegen: 
Sleutel = pygame.image.load("sleutel1.png")
Sleutel = pygame.transform.scale(Sleutel, (blokjesgrootte, blokjesgrootte))  
sleutel_locatie = (9, 17)




#start van de vijand:
start_x_vijand = random_pos()[0]
start_y_vijand = random_pos()[1]


minotaurus = Minotaurus(start_x_vijand * blokjesgrootte , start_y_vijand * blokjesgrootte ,snelheid = 15)


#startpunt voor aanmaak speler: 
start_x_speler = 0
start_y_speler = 1

# Speler aanmaken met een afbeelding (pas het pad naar je afbeelding aan)
speler = Speler(start_x_speler * blokjesgrootte , start_y_speler * blokjesgrootte , 'speler.png', 22, 22, 5, 5) #beginpositie wordt bepaald door start_x en start_y te verm met de blokjesgrootte om de speler op de jusite plek in het doolhof te krijgen (dus als start_x = 1 en blokjesgrootte = 30, dan start de speler op 30 pixels van de linkerrand), speler.png geeft de bestandsnaam voor de afbeelding van de speler --> deze wordt door 24, 24 geschaald naar 24 op 24 pixels; 5, 5 geeft de snelheid van de speler aan (dus de speler beweegt telkens 5 pixels als er op de pijltjes degrukt wordt)

draad_cooldowns = {draad: 0 for draad in draad_locaties}  # Initieer cooldowns voor alle draden


def check_botsing(speler, minotaurus):
    return speler.rect.colliderect(minotaurus.rect)

       
def get_font(size):
    return pygame.font.Font(None, size)


# dingen in de inventaris toevoegen: 
def check_item_opname(speler):
    global sleutel_locatie, draad_locaties
    speler_locatie = (speler.rect.y // blokjesgrootte, speler.rect.x // blokjesgrootte) # hier berekenen we in welke cel van het doolhof de speler zich bevindt in grid-coord (speler.rect.x en speler.rect.y) --> dit doen we door te delen door blokjesgrootte waardoor de grid-coord van de speler bepaald worden 
    deur_frames = [pygame.transform.scale(pygame.image.load(f"deur{i}.png"), (200, 300)) for i in range(1, 8)]  # Voor de animatie van de deur
    
    # Controleer of de speler de schatkist oppakt:
    if speler_locatie == sleutel_locatie: #als de locatie van de speler en de sleutel gelijk is aan elkaar dan,
        speler.pak_item("sleutel") #pakt de speler het item op en voegt deze toe aan zijn inventaris mbv pak_item()
        
        doolhof[23][32] = ' ' #hierdoor wordt de uitgang zichtbaar
        
        
        Uitgang_open_tekst = get_font(75).render("You opened the exit!", True, (0,0,0) )
        Uitgang_open_rect = Uitgang_open_tekst.get_rect(center=(316, 420))
        
        sleutel_locatie = None # De sleutel is opgepakt, dus verwijder de sleutel van het scherm
        
        # om de deuren te laten verschijnen doen we dit met een for-loop:
        for frame in deur_frames:
            teken_doolhof() # we tekenen eerst nog eens het doolhof en de speler zodat we gaan bruin scherm als achtergrond hebben
            speler.draw(scherm)
            scherm.blit(frame, (225, 70))  # Teken het frame van de deuranimatie op positie (225, 70)
            scherm.blit(Uitgang_open_tekst, Uitgang_open_rect)  # hiermee tekenen we de tekst op het scherm
            pygame.display.update()  # Werkt het scherm bij
            pygame.time.delay(200) #hoe lang een frame op het scherm zichtbaar blijft 
    
    # Controleer de draad
  
    if speler_locatie in draad_locaties:
        speler.pak_item("draad")  # Pak de draad
        teleport_speler(speler, draad_locaties, draad_cooldowns)



# de button image aanpassen:
button_surface = pygame.image.load('PLAYQUIT.png')
button_surface = pygame.transform.scale(button_surface,(200,75))

# Achtergrond hoofdmenu:
achtergrond_afbeelding = pygame.image.load("HoofdmenuAchtergrond.png")  
achtergrond_afbeelding = pygame.transform.scale(achtergrond_afbeelding, (schermbreedte, schermhoogte))  

def hoofdmenu(): 
    running = True  # Variabele om de loop te controleren
    while running:
        scherm.blit(achtergrond_afbeelding, (0, 0))  # Teken de afbeelding op positie (0, 0)

        Positie_cursor = pygame.mouse.get_pos()
        Menu_tekst = get_font(75).render("Slaying The Minotaur", True, (255, 255, 255) )
        Menu_rect = Menu_tekst.get_rect(center=(500, 300))

        # Knoppen
        PLAY_button = Button(button_surface, (500, 410), "PLAY", get_font(50), 'Green', 'White')
        EXIT_button = Button(button_surface, (500, 505), "EXIT", get_font(50), 'Green', 'White')

        scherm.blit(Menu_tekst, Menu_rect)

        for button in [PLAY_button, EXIT_button]:
            button.changeColor(Positie_cursor)
            button.update(scherm)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # wanneer je op het kruisje drukt
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: #hier gaan we kijken op welke knop er gedrukt wordt
                if PLAY_button.CheckForInput(Positie_cursor):
                    game_over(False)
                    start_x_speler = 0
                    start_y_speler = 1
                    spelen()  # Start de functie spelen()
                if EXIT_button.CheckForInput(Positie_cursor):
                    pygame.quit()
                hoofdmenu()
        
        pygame.display.update()  # Scherm bijwerken na elke frame

botsing_afbeelding = pygame.image.load("botsing.png")  # Zorg ervoor dat je een afbeelding hebt met deze naam
botsing_afbeelding = pygame.transform.scale(botsing_afbeelding, (schermbreedte, schermhoogte))

gamestate = "doolhof" 
def game_over(flag):
    # restart knop toevoegen en dan functie restart definieren en dan functie aanroepen als je op restart drukt 
    flag
    running = True
    while running and flag:
        scherm.blit(botsing_afbeelding, (0, 0)) 
        
        
        
        Positie_cursor = pygame.mouse.get_pos()
        RESTART_button = Button(button_surface, (500, 550), "RESTART", get_font(50), 'Green', 'White')  # Create RESTART button
        EXIT_button = Button(button_surface, (500, 650), "EXIT", get_font(50), 'Green', 'White')

        for button in [RESTART_button, EXIT_button]:  # Handle both buttons in the same loop
            button.changeColor(Positie_cursor)
            button.update(scherm)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Function to reset everything in the game to start fresh
                def reset_game():
                    global speler, minotaurus
                    # Reset player position to starting point
                    speler.rect.x = start_x_speler * blokjesgrootte  # Set player X position
                    speler.rect.y = start_y_speler * blokjesgrootte  # Set player Y position
                    # Reset minotaur position to a new random location
                    start_x_vijand = random_pos()[0]  # Generate random X for minotaur
                    start_y_vijand = random_pos()[1]  # Generate random Y for minotaur
                    minotaurus.rect.x = start_x_vijand * blokjesgrootte  # Set minotaur X position
                    minotaurus.rect.y = start_y_vijand * blokjesgrootte  # Set minotaur Y position
                
                if RESTART_button.CheckForInput(Positie_cursor):  # If RESTART button is clicked
                    reset_game()  # Reset player and minotaur positions
                    running = False  # Exit the game over screen
                    gamestate = "doolhof"  # Start a new game immediately
                    return  # Exit the function
                    
                if EXIT_button.CheckForInput(Positie_cursor):  # If EXIT button is clicked
                    reset_game()  # Still reset positions before exiting
                    running = False  # Exit the game over screen
                    hoofdmenu()  # Return to the main menu instead
                    return  # Exit the function
        
        pygame.display.update()  # Scherm bijwerken na elke frame


def gevecht_loop():
    global gamestate
    intro_start = time.time()
    intro_duur = 3  # seconden
    
    # Eerst de intro tonen
    while time.time() - intro_start < intro_duur:
        screen.blit(background, (0, 0))
        intro()  # Tekent intro op het scherm
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    # Dan het gevecht starten
    reset_level()
    running = True
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        game_run(levels)  # Roep de gevechtsfase aan

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Als speler dood is, terug naar hoofdmenu
        if not Theseus.alive:
            pygame.time.delay(1000)
            game_over(True)
            return
        
        # Als vijand dood is, terug naar doolhof (optioneel: volgend level)
        if hasattr(levels[huidige_level]["vijand"], "health"):
            if levels[huidige_level]["vijand"].health <= 0:
                pygame.time.delay(2000)
                gamestate = "maze"
                spelen()
                return

        pygame.display.flip()
        
gamestate = "doolhof"
def spelen(): #scherm om te spelen
    global doolhof
    reset_level()
    running = True
    while running:
        clock.tick(20) #hiermee wordt de game beperkt tot max 20 frames per seconde, zodat de beweging stabiel en niet te snel gebeurt 
        scherm.fill((206,204,184))  # Maak het scherm bruin, hiermee wordt elke oude loop overschreven 
        
        
        # Speler doen bewegen: 
        keys = pygame.key.get_pressed() # hiermee verzamelen we een overxzicht van welke toetsen gedrukt zijn (heb ik uit de les gehaald)
        if keys[pygame.K_UP]: # dus als we op het pijltje naar boven drukken, dan zal de speler in de negatieve y-richting bewegen met snelheid y 
            speler.move(0, -speler.snelheid_y)
            if speler.check_collision(doolhof):  # Na elke beweging wordt er gecontroleerd of er geen botsing is tussen de speler en de muur, is dit zo dan wordt de beweging onmiddelijk ongedaan gemaakt waardoor de speler op het pad blijft
                speler.move(0, speler.snelheid_y)
            check_item_opname(speler) #hiermee roepen we de functie op die controleert of de speler zich op hetzelfde punt bevindt als één van de items
        if keys[pygame.K_DOWN]:
            speler.move(0, speler.snelheid_y)
            if speler.check_collision(doolhof):
                speler.move(0, -speler.snelheid_y)
            check_item_opname(speler)
        if keys[pygame.K_LEFT]:
            speler.move(-speler.snelheid_x, 0)
            if speler.check_collision(doolhof):
                speler.move(speler.snelheid_x, 0)
            check_item_opname(speler)
        if keys[pygame.K_RIGHT]:
            speler.move(speler.snelheid_x, 0)
            if speler.check_collision(doolhof):
                speler.move(-speler.snelheid_x, 0)
            check_item_opname(speler)
    
        # Beweging Minotaurus
        minotaurus.should_move = True 
        minotaurus.update(speler)  # Update the Minotaur's movement
        
        if speler.teleport_cooldown > 0:
            speler.teleport_cooldown -= 1  # Verminder cooldown
            
        for draad in draad_cooldowns:
            if draad_cooldowns[draad] > 0:
                draad_cooldowns[draad] -= 1  # Verminder cooldown geleidelijk

        
        # Controleer op botsing
        if check_botsing(speler, minotaurus):
            global gamestate
            gamestate = "gevecht"
            return
            #game_over(True)  # Ga naar het game over scherm
        
       

        # Teken alles
        teken_doolhof()
        speler.draw(scherm)
        minotaurus.draw(scherm)
        # Controleer of het spel gesloten moet worden (heb ik ook uit de les gehaald vlgm laatste WPO)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # Update het scherm
        pygame.display.flip()


def main():
    global gamestate
    while True:
        if gamestate == "doolhof":
            spelen()  # Call the labyrinth function
        elif gamestate == "gevecht":
            gevecht_loop()  # Call the fight function
# Start the game
main()
# Stop Pygame
pygame.quit()