# modules en initialisaties:  
import pygame # Pygame bibliotheek laden 
import sys
pygame.init() #pygame initialiseren

# het speelveld aanmaken: 
schermbreedte = 632
schermhoogte = 632
scherm = pygame.display.set_mode([schermbreedte, schermhoogte]) #maakt het scherm met de opgegeven breedte en hoogte 
clock = pygame.time.Clock() #deze clock regelt hoe vaak het scherm ververst wordt 
pygame.display.set_caption("Slaying the Minotaur") #weergeeft de naam van het spel in de (kleine) tekstbalk

#onderdelen doolhof:
rijen = 21 #aantal rijen van het doolhof (dus in feite de hoogte van het doolhof)
kolommen = 21 #aantal kolommen van het doolhof (breedte)
blokjesgrootte = 30 #de grootte van één vierkant in het doolhof

richtingen = [(0,-2), (2,0), (0,2), (-2,0)] #de 4 beweegopties

# Doolhof van level 1: 
    
Doolhof_Level1 = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X','X','X','X','X','X','X','X','X', 'X'], [' ', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X'], ['X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X','X',' ','X',' ','X','X','X',' ', 'X'], ['X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ','X',' ',' ',' ','X',' ',' ',' ', 'X'], ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ','X','X','X','X','X',' ','X',' ', 'X'], ['X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ',' ',' ',' ',' ','X',' ','X',' ', 'X'], ['X', ' ', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X', 'X','X','X','X',' ','X',' ','X',' ', 'X'], ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ',' ',' ',' ',' ',' ',' ','X',' ', 'X'], ['X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ','X','X','X','X','X','X','X',' ', 'X'], ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ','X',' ',' ',' ',' ',' ','X',' ', 'X'], ['X', ' ', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X', ' ','X',' ','X','X','X','X','X',' ', 'X'], ['X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', ' ',' ',' ','X',' ',' ',' ',' ',' ', 'X'], ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X','X','X','X','X','X','X','X',' ', 'X'], ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X', ' ',' ',' ',' ',' ',' ',' ','X',' ', 'X'], ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ','X','X','X',' ','X','X','X',' ', 'X'], ['X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ','X',' ','X',' ','X',' ','X',' ', 'X'], ['X', ' ', 'X', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X','X',' ','X','X','X',' ','X',' ', 'X'], ['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ','X',' ',' ',' ','X',' ','X',' ', 'X'], ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ','X','X','X',' ','X',' ','X',' ', 'X'], ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ',' ',' ',' ',' ',' ',' ','X',' ', 'X'], ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X','X','X','X','X','X','X','X','X', 'X']]

#startpunt voor aanmaak doolhof: 
rijen = len(Doolhof_Level1)
kolommen = len(Doolhof_Level1)
start_x = 1
start_y = 1

# de stenen laden (zodat we stenen muur krijgen ipv witte blokjes):
steen = pygame.image.load("steen.png")
steen = pygame.transform.scale(steen, (blokjesgrootte, blokjesgrootte))  # de afbeelding van schaal aanpassen zodat het overeenkomt met de grootte van een blokje

# De draad van Ariadne toevoegen:
DraadVanAriadne = pygame.image.load("DraadAriadne.png")  
DraadVanAriadne= pygame.transform.scale(DraadVanAriadne, (blokjesgrootte, blokjesgrootte))  
draad_locatie = (11, 3)

# Zwaard toevoegen: 
Zwaard = pygame.image.load("zwaard2.png")
Zwaard = pygame.transform.scale(Zwaard, (blokjesgrootte, blokjesgrootte))  
zwaard_locatie = (15, 13)

# Sleutel toevoegen: 
Sleutel = pygame.image.load("sleutel1.png")
Sleutel = pygame.transform.scale(Sleutel, (blokjesgrootte, blokjesgrootte))  
sleutel_locatie = (9, 17)

# class speler aanmaken:
class Speler:
    def __init__(self, x, y, afbeelding_pad, breedte, hoogte, snelheid_x, snelheid_y): #hiermee gaan we de afbeelding laden, de schaal en beginpositie instellen
        self.x = x
        self.y = y
        self.afbeelding = pygame.image.load('speler.png')  # Laadt de afbeelding
        self.afbeelding = pygame.transform.scale(self.afbeelding, (breedte, hoogte))  # Pas de grootte van de afbeelding aan
        self.breedte = breedte
        self.hoogte = hoogte
        self.snelheid_x = snelheid_x #hoe snel de speler in de x-richting beweegt
        self.snelheid_y = snelheid_y #hoe snel de speler in de y-richting beweegt
        self.rect = pygame.Rect(x, y, breedte, hoogte) # maakt een rechthoek aan die we kunnen gebruiken voor botsing en beweging --> legt de positie en grootte van de speler vast 
        
        # nu moeten we een inventaris toevoegen voor wanneer de speler dingen op pakt onderweg: 
        self.inventaris = []  # Lege lijst om items bij te houden
    
    # de speler tekenen:
    def draw(self, screen):
        screen.blit(self.afbeelding, (self.rect.x, self.rect.y))  # hiermee wordt de afbeelding (dus de speler) getekend: met screen.blit() wordt de spelerafbeelding op het scherm getekend, met gebruik van de positie die in self.rect staat --> hierdoor komt de speler op de juiste plek terecht

    # de speler laten bewegen:
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # nakijken of er geen "botsing" is tussen de speler en de muur:
    def check_collision(self, doolhof):
        speler_rect = self.rect #het vierkant van de speler
        for y in range(rijen):
            for x in range(kolommen):
                if Doolhof_Level1[y][x] == "X": #als het blokje gelijk is aan een muur, dan
                    pixel_x = start_x + (x * blokjesgrootte) # hiermee berekenen we de positie op het scherm in pixels van de muur op positie (x, y) in het doolhof
                    pixel_y = start_y + (y * blokjesgrootte)
                    
                    muur_rect = pygame.Rect(pixel_x, pixel_y, blokjesgrootte, blokjesgrootte) #de rechthoek van de muur maken 
                    if speler_rect.colliderect(muur_rect):
                        return True  # Er is een botsing met een muur
        return False
    
    # functie om dingen toe te voegen aan de inventaris:
    def pak_item(self, item):
        if item not in self.inventaris: #als het item nog niet in de inventaris zit ga je deze toevoegen 
            self.inventaris.append(item)
            print(f"{item} is toegevoegd aan de inventaris!")

# Speler aanmaken met een afbeelding (pas het pad naar je afbeelding aan)
speler = Speler(start_x * blokjesgrootte, start_y * blokjesgrootte, 'speler.png', 22, 22, 5, 5) #beginpositie wordt bepaald door start_x en start_y te verm met de blokjesgrootte om de speler op de jusite plek in het doolhof te krijgen (dus als start_x = 1 en blokjesgrootte = 30, dan start de speler op 30 pixels van de linkerrand), speler.png geeft de bestandsnaam voor de afbeelding van de speler --> deze wordt door 24, 24 geschaald naar 24 op 24 pixels; 5, 5 geeft de snelheid van de speler aan (dus de speler beweegt telkens 5 pixels als er op de pijltjes degrukt wordt)

# Button class aanmaken:
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        if self.image is None: 
            self.image = self.text
        
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        
    def CheckForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# Functie om het doolhof te tekenen
def teken_doolhof():
    for y in range(rijen):
        for x in range(kolommen):
            karakter = Doolhof_Level1[y][x] # we halen ofwel 'X' ofwel ' ' op voor elke cel
            scherm_x = start_x + (x * blokjesgrootte) # hiermee wordt de pixelpositie op het scherm van het huidige blokje bepaald
            scherm_y = start_y + (y * blokjesgrootte)
            if karakter == "X":  # als het karakter een muur is 
                scherm.blit(steen, (scherm_x, scherm_y))  # hier wordt de steen getekend 
                
            # Op het huidige blokje de draad zetten: 
            if (y, x) == draad_locatie:
                scherm.blit(DraadVanAriadne, (scherm_x, scherm_y))
                
            # Op het huidige blokje het zwaard zetten: 
            if (y, x) == zwaard_locatie:
                scherm.blit(Zwaard, (scherm_x, scherm_y))
                
            # Op het huidige blokje de sleutel zetten: 
            if (y, x) == sleutel_locatie:
                scherm.blit(Sleutel, (scherm_x, scherm_y))
        
def get_font(size):
    return pygame.font.Font(None, size)

# dingen in de inventaris toevoegen: 
def check_item_opname(speler):
    global zwaard_locatie, sleutel_locatie, draad_locatie
    speler_locatie = (speler.rect.y // blokjesgrootte, speler.rect.x // blokjesgrootte) # hier berekenen we in welke cel van het doolhof de speler zich bevindt in grid-coord (speler.rect.x en speler.rect.y) --> dit doen we door te delen door blokjesgrootte waardoor de grid-coord van de speler bepaald worden 
    deur_frames = [
    pygame.transform.scale(pygame.image.load(f"deur{i}.png"), (200, 300)) for i in range(1, 8)]  # Voor de animatie van de deur
    # Controleer of de speler het zwaard oppakt: 
    if speler_locatie == zwaard_locatie: #als de locatie van de speler en het zwaard gelijk is aan elkaar dan,
        speler.pak_item("zwaard") #pakt de speler het item op en voegt deze toe aan zijn inventaris mbv pak_item()
         
        zwaard_locatie = None  # Het zwaard is opgepakt, dus verwijder het zwaard van het scherm
    
    # Controleer de schatkist
    if speler_locatie == sleutel_locatie:
        speler.pak_item("sleutel")
        
        Doolhof_Level1[19][20] = ' ' #hierdoor wordt de uitgang zichtbaar
        
        Uitgang_open_tekst = get_font(75).render("You opened the exit!", True, (0,0,0) )
        Uitgang_open_rect = Uitgang_open_tekst.get_rect(center=(316, 420))
        
        sleutel_locatie = None
        
        # om de deuren te laten verschijnen doen we dit met een for-loop:
        for frame in deur_frames:
            teken_doolhof() # we tekenen eerst nog eens het doolhof en de speler zodat we gaan bruin scherm als achtergrond hebben
            speler.draw(scherm)
            scherm.blit(frame, (225, 70))  # Teken het frame van de deuranimatie op positie (225, 70)
            scherm.blit(Uitgang_open_tekst, Uitgang_open_rect)  # hiermee tekenen we de tekst op het scherm
            pygame.display.update()  # Werkt het scherm bij
            pygame.time.delay(200) #hoe lang een frame op het scherm zichtbaar blijft 
    
    # Controleer de draad
    if speler_locatie == draad_locatie:
        speler.pak_item("draad")
    
        draad_locatie = None



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
        Menu_rect = Menu_tekst.get_rect(center=(316, 150))

        # Knoppen
        PLAY_button = Button(button_surface, (316, 340), "PLAY", get_font(50), 'Green', 'White')
        EXIT_button = Button(button_surface, (316, 440), "EXIT", get_font(50), 'Green', 'White')

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
                    spelen()  # Start de functie spelen()
                if EXIT_button.CheckForInput(Positie_cursor):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()  # Scherm bijwerken na elke frame


def spelen(): #scherm om te spelen
    running = True
    while running:
        clock.tick(20) #hiermee wordt de game beperkt tot max 20 frames per seconde, zodat de beweging stabiel en niet te snel gebeurt 
        scherm.fill((206,204,184))  # Maak het scherm bruin, hiermee wordt elke oude loop overschreven 
    
        # Speler doen bewegen: 
        keys = pygame.key.get_pressed() # hiermee verzamelen we een overxzicht van welke toetsen gedrukt zijn (heb ik uit de les gehaald)
        if keys[pygame.K_UP]: # dus als we op het pijltje naar boven drukken, dan zal de speler in de negatieve y-richting bewegen met snelheid y 
            speler.move(0, -speler.snelheid_y)
            if speler.check_collision(Doolhof_Level1):  # Na elke beweging wordt er gecontroleerd of er geen botsing is tussen de speler en de muur, is dit zo dan wordt de beweging onmiddelijk ongedaan gemaakt waardoor de speler op het pad blijft
                speler.move(0, speler.snelheid_y)
            check_item_opname(speler) #hiermee roepen we de functie op die controleert of de speler zich op hetzelfde punt bevindt als één van de items
        if keys[pygame.K_DOWN]:
            speler.move(0, speler.snelheid_y)
            if speler.check_collision(Doolhof_Level1):
                speler.move(0, -speler.snelheid_y)
            check_item_opname(speler)
        if keys[pygame.K_LEFT]:
            speler.move(-speler.snelheid_x, 0)
            if speler.check_collision(Doolhof_Level1):
                speler.move(speler.snelheid_x, 0)
            check_item_opname(speler)
        if keys[pygame.K_RIGHT]:
            speler.move(speler.snelheid_x, 0)
            if speler.check_collision(Doolhof_Level1):
                speler.move(-speler.snelheid_x, 0)
            check_item_opname(speler)
    
        # Teken het doolhof en de speler
        teken_doolhof()
        speler.draw(scherm)
    
        # Controleer of het spel gesloten moet worden (heb ik ook uit de les gehaald vlgm laatste WPO)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # Update het scherm
        pygame.display.flip()

hoofdmenu()
# Stop Pygame
pygame.quit()
