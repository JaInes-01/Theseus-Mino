from Speler_Doolhof import *
from Button_Doolhof import Button
from Doolhof import *
from Teleporteren_Doolhof import teleport_speler
import time 
import Fight_MainCode
from Objecten import * 

# Vervolgens initialiseren we pygame: 
pygame.init() 

fps = 30


# de stenen laden (zodat we stenen muur krijgen ipv witte blokjes):
steen = pygame.image.load("steen.png")
steen = pygame.transform.scale(steen, (blokjesgrootte, blokjesgrootte))  # de afbeelding van schaal aanpassen zodat het overeenkomt met de grootte van een blokje

# Voor verder gebruik bepalen we de startposities (x, y) van de minotaurus (vijand). Dit doen we door voor zowel x als y de functie random_pos() op te roepen voor positie [0] en positie [1]:
start_x_vijand = random_pos()[0]
start_y_vijand = random_pos()[1]

# We definiëren ook de minotaurus adhv de functie Minotaurus() uit de module Minotaurus_Doolhof. Met als input de startpositie van de minotaurus, en de snelheid van de minotaurus (gelijk aan 15): 
minotaurus = Minotaurus(start_x_vijand * blokjesgrootte , start_y_vijand * blokjesgrootte ,snelheid = 15)
# de blokjesgrootte converteert grid-coord naar pixels


# Hier bepalen we de startpostie van de speler (deze liggen vast aangezien we willen dat de speler telkens op dezelfde plek begint): 
start_x_speler = 0
start_y_speler = 1

# We definiëren de speler met de Speler() functie uit de Speler_Doolhof module. Ook hier hebben we als input de startpositie van de speler genomen, het png-bestand, 
speler = Speler_Doolhof(start_x_speler * blokjesgrootte , start_y_speler * blokjesgrootte , 'speler.png', 22, 22, 5, 5) 
#--> beginpositie wordt bepaald door start_x en start_y te verm met de blokjesgrootte om de speler op de jusite plek in het doolhof te krijgen (dus als start_x = 1 en blokjesgrootte = 30, dan start de speler op 30 pixels van de linkerrand), speler.png geeft de bestandsnaam voor de afbeelding van de speler --> deze wordt door 24, 24 geschaald naar 24 op 24 pixels; 5, 5 geeft de snelheid van de speler aan (dus de speler beweegt telkens 5 pixels als er op de pijltjes degrukt wordt)

# We initiëren cooldowns, zodat de speler niet meteen kan teleporteren (om spel moeilijker te maken)
draad_cooldowns = {draad: 0 for draad in draad_locaties} #Het houdt bij wanneer de een draad laatst gebruikt is waardoor het teleporteren niet omiddelijk lukt 

# de button image aanpassen:
button_surface = pygame.image.load('PLAYQUIT.png')
button_surface = pygame.transform.scale(button_surface,(200,75))

# Achtergrond hoofdmenu:
achtergrond_afbeelding = pygame.image.load("HoofdmenuAchtergrond.png")  
achtergrond_afbeelding = pygame.transform.scale(achtergrond_afbeelding, (schermbreedte, schermhoogte))  

botsing_afbeelding = pygame.image.load("botsing.png")  # Zorg ervoor dat je een afbeelding hebt met deze naam
botsing_afbeelding = pygame.transform.scale(botsing_afbeelding, (schermbreedte, schermhoogte))

gewonnen_afbeelding = pygame.image.load("YouWon.png")  # Zorg ervoor dat je een afbeelding hebt met deze naam
gewonnen_afbeelding = pygame.transform.scale(gewonnen_afbeelding, (schermbreedte, schermhoogte))

# Globale variabelen voor het bewaren van de staat van het doolhof
voormalig_doolhof = None
voormalige_speler_x = None
voormalige_speler_y = None
voormalige_inventory = None

# Hiermee checken we of er een botsing is tussen de speler en de minotaurus: 
def check_botsing(speler, minotaurus):
    return speler.rect.colliderect(minotaurus.rect)
# zowel de speler als de minotaurus hebben een rechthoek (rect) die gebruikt wordt om een object in het spel visueel te representeren. Hierdoor kunnen we controleren of er een overlap (botsing) is tussen de speler en de minotaurus met colliderect (geeft True als ze elkaar raken en anders False)

# Met deze functie wordt het een lettertype ingevoerd met als input een bepaalde grootte:
def get_font(size):
    return pygame.font.Font(None, size)

def check_item_opname(speler):
    global sleutel_locatie
    speler_locatie = (speler.rect.y // blokjesgrootte, speler.rect.x // blokjesgrootte) # hier berekenen we in welke cel van het doolhof de speler zich bevindt in grid-coord (speler.rect.x en speler.rect.y) --> dit doen we door te delen door blokjesgrootte waardoor de grid-coord van de speler bepaald worden 
    deur_frames = [pygame.transform.scale(pygame.image.load(f"deur{i}.png"), (200, 300)) for i in range(1, 8)]  # Voor de animatie van de deur
    
    # Controleer of de speler de schatkist oppakt:
    if speler_locatie == sleutel_locatie: #als de locatie van de speler en de sleutel gelijk is aan elkaar dan,
        speler.pak_item("sleutel") #pakt de speler het item op en voegt deze toe aan zijn inventaris mbv pak_item()
        
        doolhof[23][32] = ' ' # hierdoor wordt de uitgang zichtbaar eens de speler de sleutel te pakken heeft
        
        # Hiermee wordt er een tekst op het scherm getoond als de speler de sleutel heeft: 
        Uitgang_open_tekst = get_font(75).render("You opened the exit!", True, (0,0,0) )
        Uitgang_open_rect = Uitgang_open_tekst.get_rect(center=(500, 500))
        
        # sleutel_locatie = None # De sleutel is opgepakt, dus verwijder de sleutel van het scherm (er is geen locatie meer)
        sleutel_locatie = None
        
        # om de deuren te laten verschijnen doen we dit met een for-loop:
        for frame in deur_frames:
            teken_doolhof(scherm, blokjesgrootte, doolhof, draad_locaties, sleutel_locatie) # we tekenen eerst nog eens het doolhof en de speler zodat we gaan bruin scherm als achtergrond hebben
            speler.draw(scherm)
            scherm.blit(frame, (400, 150))  # Teken het frame van de deuranimatie op positie (400, 150)
            scherm.blit(Uitgang_open_tekst, Uitgang_open_rect)  # hiermee tekenen we de tekst op het scherm
            pygame.display.update()  # Werkt het scherm bij
            pygame.time.delay(200) #hoe lang een frame op het scherm zichtbaar blijft 

def starten_met_moeilijkheid(moeilijkheidsgraad):
    global moeilijkheid, draad_locaties, minotaurus
    moeilijkheid = moeilijkheidsgraad
    
    # Bepaal het aantal draden op basis van de moeilijkheidsgraad
    if moeilijkheid == "easy":
        aantal_draden = 5
        minotaurus_snelheid = 15  # Langzaam
    elif moeilijkheid == "medium":
        aantal_draden = 4
        minotaurus_snelheid = 10  # Gemiddeld
    else:  # hard
        aantal_draden = 3
        minotaurus_snelheid = 5  # Snel

    # Genereer de dradenlocaties en sla ze op
    draad_locaties = kies_draadlocaties(aantal_draden)
    
    # Reset de minotaurus met de nieuwe snelheid
    start_x_vijand = random_pos()[0]
    start_y_vijand = random_pos()[1]
    minotaurus = Minotaurus(start_x_vijand * blokjesgrootte, start_y_vijand * blokjesgrootte, snelheid=minotaurus_snelheid)

    game_over(False)
    gewonnen(False)
    reset_game()
    spelen()


# Function to reset everything in the game to start fresh
def reset_game():
    global speler, minotaurus, sleutel_locatie
    # Reset player position to starting point
    speler.rect.x = start_x_speler * blokjesgrootte  # Set player X position
    speler.rect.y = start_y_speler * blokjesgrootte  # Set player Y position
    # Reset minotaur position to a new random location
    start_x_vijand = random_pos()[0]  # Generate random X for minotaur
    start_y_vijand = random_pos()[1]  # Generate random Y for minotaur
    minotaurus.rect.x = start_x_vijand * blokjesgrootte  # Set minotaur X position
    minotaurus.rect.y = start_y_vijand * blokjesgrootte  # Set minotaur Y position
    # Reset sleutel en uitgang
    sleutel_locatie = (9, 17)  # of waar je de sleutel oorspronkelijk had
    doolhof[23][32] = 'X'  # Zorg dat dit de originele waarde is vóórdat de uitgang zichtbaar werd

    # Leeg eventueel ook de inventaris van de speler
    speler.inventaris.clear()
    



def sla_doolhof_staat_op():
    global voormalig_doolhof, voormalige_speler_x, voormalige_speler_y, voormalige_inventory
    voormalig_doolhof = [rij[:] for rij in doolhof]  # Kopie van het doolhof maken
    voormalige_speler_x = speler.rect.x
    voormalige_speler_y = speler.rect.y
    voormalige_inventory = speler.inventaris[:]  # Kopie van de inventaris
    
def herstel_doolhof_staat():
    global doolhof, speler
    if voormalig_doolhof is not None:
        doolhof = [rij[:] for rij in voormalig_doolhof]  # Herstel de oude structuur
        speler.rect.x = voormalige_speler_x  # Zet speler terug op oude positie
        speler.rect.y = voormalige_speler_y
        speler.inventaris = voormalige_inventory[:]  # Herstel de inventaris



def hoofdmenu(): 
    running = True  # Variabele om de loop te controleren
    while running:
        scherm.blit(achtergrond_afbeelding, (0, 0))  # Teken de afbeelding op positie (0, 0)

        Positie_cursor = pygame.mouse.get_pos()
        Menu_tekst = get_font(75).render("Slaying The Minotaur", True, (255, 255, 255) )
        Menu_rect = Menu_tekst.get_rect(center=(500, 300))

        # Knoppen
        EASY_button = Button(button_surface, (500, 410), "EASY", get_font(50), 'Green', 'White')
        MEDIUM_button = Button(button_surface, (500, 510), "MEDIUM", get_font(50), 'Yellow', 'White')
        HARD_button = Button(button_surface, (500, 610), "HARD", get_font(50), 'Red', 'White')
        EXIT_button = Button(button_surface, (500, 710), "EXIT", get_font(50), 'Green', 'White')
        

        scherm.blit(Menu_tekst, Menu_rect)

        for button in [EASY_button, MEDIUM_button, HARD_button, EXIT_button]:
            button.changeColor(Positie_cursor)
            button.update(scherm)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # wanneer je op het kruisje drukt
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: #hier gaan we kijken op welke knop er gedrukt wordt
                if EASY_button.CheckForInput(Positie_cursor):
                    starten_met_moeilijkheid("easy")
                if MEDIUM_button.CheckForInput(Positie_cursor):
                    starten_met_moeilijkheid("medium")
                if HARD_button.CheckForInput(Positie_cursor):
                    starten_met_moeilijkheid("hard")
                if EXIT_button.CheckForInput(Positie_cursor):
                    pygame.quit()
                hoofdmenu()
        
        pygame.display.update()  # Scherm bijwerken na elke frame

def game_over(flag):
    # restart knop toevoegen en dan functie restart definieren en dan functie aanroepen als je op restart drukt 
    flag
    running = True
    while running and flag:
        scherm.blit(botsing_afbeelding, (0, 0)) 
        
        Positie_cursor = pygame.mouse.get_pos()
        RESTART_button = Button(button_surface, (350, 750), "RESTART", get_font(50), 'Green', 'White')  # Create RESTART button
        EXIT_button = Button(button_surface, (650, 750), "EXIT", get_font(50), 'Green', 'White')

        for button in [RESTART_button, EXIT_button]:  # Handle both buttons in the same loop
            button.changeColor(Positie_cursor)
            button.update(scherm)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if RESTART_button.CheckForInput(Positie_cursor):  # If RESTART button is clicked
                    reset_game()  # Reset player and minotaur positions
                    running = False  # Exit the game over screen
                    spelen()  # Start a new game immediately
                    return  # Exit the function
                    
                if EXIT_button.CheckForInput(Positie_cursor):  # If EXIT button is clicked
                    reset_game()  # Still reset positions before exiting
                    running = False  # Exit the game over screen
                    hoofdmenu()  # Return to the main menu instead
                    return  # Exit the function
        
        pygame.display.update()  # Scherm bijwerken na elke frame

def gevecht_loop():
    huidige_level = 1
    intro = Fight_MainCode.Intro()
    
    while True:
        
        clock.tick(fps)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
                # skip or end intro
                intro.finished = True
                
        resultaat = Fight_MainCode.game_run(Fight_MainCode.levels)

        intro.run(Fight_MainCode.screen)
        if time.time() - intro.anim_start >= intro.anim_duur:
            intro.displayed = True
            font = pygame.font.SysFont(None, 40)
            game_over_text = font.render("Press 'P' to start", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2))
            Fight_MainCode.screen.blit(game_over_text, text_rect)# draws its frames
        if intro.finished:
            break        # exit intro loop
        pygame.display.flip()

    # --- 2) ACTUAL FIGHT ---
    Fight_MainCode.reset_level()
    fight_running = True
    while fight_running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        # draw fight frame
        Fight_MainCode.game_run(Fight_MainCode.levels)
        pygame.display.flip()

        # end conditions:
        vijand = Fight_MainCode.levels[huidige_level]["vijand"]
        all_dead = isinstance(vijand, list) and all(v.health <= 0 for v in vijand)
        
        if not Fight_MainCode.Theseus.alive:
            game_over(True)
        
        if resultaat == "gevecht_gewonnen":
            fight_running = False 
            pygame.quit
            herstel_doolhof_staat()  # Breng speler terug naar het doolhof
            spelen()  # Ga terug naar het doolhof
            return
            
            

def gewonnen(flag):
    flag 
    running = True
    while running and flag:
        scherm.blit(gewonnen_afbeelding, (0, 0)) 
        
        Positie_cursor = pygame.mouse.get_pos()
        RESTART_button = Button(button_surface, (350, 750), "RESTART", get_font(50), 'Green', 'White')  # Create RESTART button
        EXIT_button = Button(button_surface, (650, 750), "EXIT", get_font(50), 'Green', 'White')

        for button in [RESTART_button, EXIT_button]:  # Handle both buttons in the same loop
            button.changeColor(Positie_cursor)
            button.update(scherm)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                
                if RESTART_button.CheckForInput(Positie_cursor):  # If RESTART button is clicked
                    reset_game()  # Reset player and minotaur positions
                    running = False  # Exit the game over screen
                    spelen()  # Start a new game immediately
                    return  # Exit the function
                    
                if EXIT_button.CheckForInput(Positie_cursor):  # If EXIT button is clicked
                    reset_game()  # Still reset positions before exiting
                    running = False  # Exit the game over screen
                    hoofdmenu()  # Return to the main menu instead
                    return  # Exit the function
        
        pygame.display.update()  # Scherm bijwerken na elke frame

def spelen(): #scherm om te spelen
    global doolhof, moeilijkheid
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
        
        speler_locatie = (speler.rect.y//blokjesgrootte, speler.rect.x//blokjesgrootte)
        if keys[pygame.K_t] and speler_locatie in draad_locaties: 
            teleport_speler(speler, draad_locaties, draad_cooldowns)
        
        # Beweging Minotaurus
        minotaurus.should_move = True 
        minotaurus.update(speler)  # Update the Minotaur's movement
        
        
        if speler.teleport_cooldown > 0:
            speler.teleport_cooldown -= 1  # Verminder cooldown
            
        for draad in draad_cooldowns:
            if draad_cooldowns[draad] > 0:
                draad_cooldowns[draad] -= 1  # Verminder cooldown geleidelijk

        
        if check_botsing(speler, minotaurus):
            sla_doolhof_staat_op()  # Bewaar de spelstatus
            gevecht_loop()


        # Teken alles
        teken_doolhof(scherm, blokjesgrootte, doolhof, draad_locaties, sleutel_locatie)
        speler.draw(scherm)
        minotaurus.draw(scherm)
        # Controleer of het spel gesloten moet worden (heb ik ook uit de les gehaald vlgm laatste WPO)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
        # Update het scherm
        pygame.display.flip()

hoofdmenu()
# Stop Pygame
pygame.quit()
