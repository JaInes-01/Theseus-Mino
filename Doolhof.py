import random # voor willekeurige keuzes (zoals het genereren van posities)
import pygame


# Scherm en algemene instellingen
schermbreedte = 1000
schermhoogte = 800
scherm = pygame.display.set_mode([schermbreedte, schermhoogte]) #maakt het scherm met de opgegeven breedte en hoogte 

 # Maakt een klokobject dat bepaalt hoe vaak het scherm ververst wordt
clock = pygame.time.Clock() #deze clock regelt hoe vaak het scherm ververst wordt 

# Zet de naam van het venster bovenin het spel
pygame.display.set_caption("Slaying the Minotaur") #weergeeft de naam van het spel in de (kleine) tekstbalk

# Instellingen voor het doolhof: aantal rijen, kolommen en de grootte van elk blokje
rijen = 25 #aantal rijen van het doolhof (dus in feite de hoogte van het doolhof)
kolommen = 33 #aantal kolommen van het doolhof (breedte)
blokjesgrootte = 30 #de grootte van één vierkant in het doolhof

# Startpositie voor het genereren van het doolhof
start_x = 1
start_y = 1

# Lege lijst die straks het volledige doolhof gaat bevatten
doolhof = [] # een lege lijst waar we telkens een "rij" in het doolhof aan gaan toevoegen 

# Richtingen waarin het doolhof algoritme mag bouwen (2 stappen per keer)
richtingen = [(0,-2), (2,0), (0,2), (-2,0)] #de 4 beweegopties

# Richtingen voor pad zoeken met A* (1 stap per keer)
a_star_richtingen = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 1-step moves


# Laad de afbeelding van een muursteen en pas het aan zodat het in het doolhofblok past
steen = pygame.image.load("steen.png")
steen = pygame.transform.scale(steen, (blokjesgrootte, blokjesgrootte))  # de afbeelding van schaal aanpassen zodat het overeenkomt met de grootte van een blokje

# Laad de draad-afbeelding en schaal deze
DraadVanAriadne = pygame.image.load("DraadAriadne.png")  
DraadVanAriadne= pygame.transform.scale(DraadVanAriadne, (blokjesgrootte, blokjesgrootte))  

# Laad de sleutel-afbeelding en bepaal waar deze ligt in het doolho
Sleutel = pygame.image.load("sleutel1.png")
Sleutel = pygame.transform.scale(Sleutel, (blokjesgrootte, blokjesgrootte))  
sleutel_locatie = (9, 17)

# Startpositie van de speler bij ingang van het doolhof
start_x_speler = 0
start_y_speler = 1

# Moeilijkheidsgraad is nog niet gekozen (wordt mogelijk later aangepast)
moeilijkheid = None

for y in range(rijen):                      # Herhaal voor elke rij in het doolhof
    rij = []                                # Maak een nieuwe lege lijst voor deze rij
    for x in range(kolommen):               # Herhaal voor elk kolom-element in de rij
        rij.append('X')                     # Voeg een 'X' toe om een muur te maken
    doolhof.append(rij)                     # Voeg de rij met muren toe aan de doolhof

def random_pos():                           # Functie om een willekeurige niet-muurpositie te kiezen
    while True:                             # Blijf herhalen tot een geldige positie is gevonden
        x = random.randint(12, 20)          # Kies een willekeurige x tussen 12 en 20
        y = random.randint(1, 20)           # Kies een willekeurige y tussen 1 en 20
        if doolhof[x][y] != 'X':            # Controleer of deze positie GEEN muur is
                return(x,y)                 # Als het geen muur is, geef dan deze positie terug
            
def kies_draadlocaties(aantal):            # Functie om een aantal draadlocaties te kiezen
    locaties = []                          # Maak een lege lijst om locaties in op te slaan
    while len(locaties) < aantal:          # Blijf zoeken tot we genoeg draadlocaties hebben
        x = random.randint(1, kolommen - 2)  # Kies een willekeurige x binnen grenzen (niet rand)
        y = random.randint(1, rijen - 2)     # Kies een willekeurige y binnen grenzen (niet rand)
        if doolhof[y][x] == " " and (y, x) not in locaties:  # Alleen als het pad is en nog geen draad daar ligt
            locaties.append((y, x))        # Voeg de geldige locatie toe aan de lijst
    return locaties                        # Geef de lijst met draadlocaties terug


#genereren vh doolhof (nu dus de paden eraan toevoegen):
def generate_doolhof(x, y):                # Functie om paden te maken in het doolhof
    doolhof[y][x] = " "                    # Verander de huidige muur in een pad
    random.shuffle(richtingen)            # Schud de richtingen om willekeurig te kiezen

    for dx, dy in richtingen:             # Loop door alle richtingen (dx, dy)
        nx, ny = x + dx, y + dy           # Bepaal nieuwe x en y (2 stappen verder)
        if 1 <= nx < kolommen-1 and 1 <= ny < rijen-1 and doolhof[ny][nx] == 'X':  # Check: binnen doolhof en nog muur
            doolhof[y+dy//2][x+dx//2] = " "  # Verwijder tussenliggende muur (maak pad ertussen)
            generate_doolhof(nx,ny)         # Herhaal vanaf de nieuwe positie


generate_doolhof(1,1) # doolhof genereren vanaf punt (1,1)

if moeilijkheid == "easy":                 # Als de moeilijkheid op "easy" staat
        aantal_draden = 5                  # Gebruik dan 5 draadlocaties
else:                                      # Anders (medium/hard/etc.)
    aantal_draden = 3                      # Gebruik dan 3 draadlocaties

draad_locaties = kies_draadlocaties(aantal_draden)  # Kies de draadlocaties op basis van moeilijkheid 


doolhof[1][0] = " "   #ingang

# Functie om het doolhof te tekenen
def teken_doolhof(scherm, blokjesgrootte, doolhof, draad_locaties, sleutel_locatie):  # Functie om doolhof te tekenen
    for y in range(rijen):                # Ga door elke rij
        for x in range(kolommen):         # Ga door elke kolom in de rij
            if doolhof[y][x] == "X":      # Als het een muur is
                scherm.blit(steen, (x*blokjesgrootte, y*blokjesgrootte))  # Teken de steen op die plek
            if (y, x) in draad_locaties:  # Als hier een draad ligt
                scherm.blit(DraadVanAriadne, (x*blokjesgrootte, y*blokjesgrootte))  # Teken draad

    if sleutel_locatie is not None:       # Als er een sleutelpositie is ingesteld
        ry, rx = sleutel_locatie          # Haal rijen en kolommen op van de sleutel
        scherm.blit(Sleutel, (rx*blokjesgrootte, ry*blokjesgrootte))  # Teken sleutel op juiste plek
   f sleutel_locatie is not None:  # Als er een sleutelpositie bestaat
    ry, rx = sleutel_locatie     # Haal de y (rij) en x (kolom) coördinaten op
    scherm.blit(Sleutel, (rx*blokjesgrootte, ry*blokjesgrootte))  # Teken de sleutel op het scherm


# Doolhofgeneratie met A* controle op bereikbaarheid
def genereer_doolhof_met_bereikbaarheid(uitgang_pos):  # Genereer een doolhof dat gecontroleerd wordt op bereikbaarheid
    while True:                            # Blijf proberen tot een geldig doolhof is gegenereerd
        doolhof.clear()                    # Maak het doolhof leeg

        for y in range(rijen):             # Voor elke rij
            rij = ['X' for _ in range(kolommen)]  # Maak een rij gevuld met muren
            doolhof.append(rij)            # Voeg de rij toe aan het doolhof

        generate_doolhof(1, 1)             # Genereer paden in het doolhof vanaf (1,1)

        speler_pos = (start_y_speler, start_x_speler)  # Stel startpositie van de speler in
        draad_locaties = kies_draadlocaties()          # Kies draadlocaties

        if alles_verbonden(doolhof, speler_pos, uitgang_pos, sleutel_locatie, draad_locaties):  
            # Als alles bereikbaar is vanaf de speler
            return doolhof                # Geef het doolhof terug

def a_star(doolhof, start, doel):        # A* algoritme om het kortste pad te vinden van start naar doel
    open_list = []                       # Lijst van knopen die nog geëvalueerd moeten worden
    closed_list = set()                  # Set van knopen die al geëvalueerd zijn
    came_from = {}                       # Dict om te onthouden waar we vandaan kwamen

    def get_neighbors(node):            # Hulpfunctie om buren op te halen
        x, y = node
        neighbors = []
        for dx, dy in a_star_richtingen:  
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(doolhof[0]) and 0 <= ny < len(doolhof) and doolhof[ny][nx] != "X":
                neighbors.append((nx, ny))  # Alleen als het geen muur is
        return neighbors

    def heuristic(a, b):                # Heuristiekfunctie: Manhattan afstand
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    g_scores = {start: 0}               # Afstand van start naar knoop
    f_scores = {start: heuristic(start, doel)}  # Totale kosten: g + h
    open_list.append((start, f_scores[start]))  # Voeg startknoop toe aan open lijst

    while open_list:                    # Zolang er knopen te evalueren zijn
        current = min(open_list, key=lambda x: f_scores[x[0]])[0]  # Knoop met laagste f_score
        open_list = [item for item in open_list if item[0] != current]  # Verwijder uit open lijst

        if current == doel:             # Als doel is bereikt
            path = []                   # Bouw het pad terug
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)          # Voeg start toe aan pad
            return path[::-1]           # Geef omgekeerd pad terug (van start naar doel)

        closed_list.add(current)       # Voeg toe aan gesloten lijst

        for neighbor in get_neighbors(current):  # Voor elke buur
            if neighbor in closed_list:
                continue                # Sla over als al bezocht

            tentative_g_score = g_scores[current] + 1  # Kosten tot nu toe + stap

            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = g_scores[neighbor] + heuristic(neighbor, doel)

                if neighbor not in [item[0] for item in open_list]:  # Als nog niet in open lijst
                    open_list.append((neighbor, f_scores[neighbor]))  # Voeg toe aan open lijst

    return []  # Geen pad gevonden

# Controleer of de speler alles kan bereiken
def controleer_pad(doolhof, start, doel):   # Controleer of er een pad is tussen start en doel
    pad = a_star(doolhof, start, doel)      # Gebruik A* om pad te zoeken
    return bool(pad)                        # Geef True terug als pad bestaat

def alles_verbonden(doolhof, speler_pos, uitgang_pos, sleutel_pos, draad_locaties):
    return (controleer_pad(doolhof, speler_pos, uitgang_pos) and # Bereik uitgang
            controleer_pad(doolhof, speler_pos,) and             # Bereik sleutel
            controleer_pad(doolhof, speler_pos, sleutel_pos) and # Bereik alle draden
            all(controleer_pad(doolhof, speler_pos, draad) for draad in draad_locaties))  # Controleer ALLE draden
