import random 
import pygame

schermbreedte = 1000
schermhoogte = 800
scherm = pygame.display.set_mode([schermbreedte, schermhoogte]) #maakt het scherm met de opgegeven breedte en hoogte 
clock = pygame.time.Clock() #deze clock regelt hoe vaak het scherm ververst wordt 
pygame.display.set_caption("Slaying the Minotaur") #weergeeft de naam van het spel in de (kleine) tekstbalk


rijen = 25 #aantal rijen van het doolhof (dus in feite de hoogte van het doolhof)
kolommen = 33 #aantal kolommen van het doolhof (breedte)
blokjesgrootte = 30 #de grootte van één vierkant in het doolhof
      
start_x = 1
start_y = 1

doolhof = [] # een lege lijst waar we telkens een "rij" in het doolhof aan gaan toevoegen 

richtingen = [(0,-2), (2,0), (0,2), (-2,0)] #de 4 beweegopties
a_star_richtingen = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 1-step moves


# de stenen laden (zodat we stenen muur krijgen ipv witte blokjes):
steen = pygame.image.load("steen.png")
steen = pygame.transform.scale(steen, (blokjesgrootte, blokjesgrootte))  # de afbeelding van schaal aanpassen zodat het overeenkomt met de grootte van een blokje

# De draad van Ariadne toevoegen:
DraadVanAriadne = pygame.image.load("DraadAriadne.png")  
DraadVanAriadne= pygame.transform.scale(DraadVanAriadne, (blokjesgrootte, blokjesgrootte))  
#draad_locaties = [(4, 8), (2, 16), (11, 3), (15, 13)]  # Hier geef je de vaste locaties aan


#Sleutel toevoegen: 
Sleutel = pygame.image.load("sleutel1.png")
Sleutel = pygame.transform.scale(Sleutel, (blokjesgrootte, blokjesgrootte))  
sleutel_locatie = (9, 17)

start_x_speler = 0
start_y_speler = 1

for y in range(rijen):
    rij = [] #een nieuwe rij aanmaken
    for x in range(kolommen):
        rij.append('X') #voeg een muur "X" toe (hierdoor gaan er dus muren ontstaan)
    doolhof.append(rij) #nu voegen we dus de nieuwe rij toe aan de lijst "doolhof"

def random_pos():
    while True:
        x = random.randint(12, 20)
        y = random.randint(1, 20)
        if doolhof[x][y] != 'X': 
                return(x,y)
            
def kies_draadlocaties(aantal=4):
    locaties = []
    while len(locaties) < aantal:
        x = random.randint(1, kolommen - 2)
        y = random.randint(1, rijen - 2)
        if doolhof[y][x] == " " and (y, x) not in locaties:
            locaties.append((y, x))
    return locaties


#genereren vh doolhof (nu dus de paden eraan toevoegen):
def generate_doolhof(x, y): #deze functie gaat dus muren in paden veranderen 
    doolhof[y][x] = " "  # Maakt van muur een pad, vandaar gewoon een spatie 
    random.shuffle(richtingen)  # Willekeurige richtingen proberen
    
    for dx, dy in richtingen: # dx en dy komen uit de lijst "richtingen"
        nx, ny = x + dx, y + dy #nx en ny zijn de volgende cel in deze richting
        if 1 <= nx < kolommen-1 and 1 <= ny < rijen-1 and doolhof[ny][nx] == 'X': # we controleren hier of de nieuwe positie nog binnen het doolhof is en of het nog een muur is --> is dit zo dan kunnen we daar nog een pad van maken 
            doolhof[y+dy//2][x+dx//2] = " " #dit zorgt voor een verbinding tussen de muren, verwijdert tussenliggende muur (maakt pad)
            generate_doolhof(nx,ny)

generate_doolhof(1,1) # doolhof genereren vanaf punt (1,1)
draad_locaties = kies_draadlocaties()

doolhof[1][0] = " "   #ingang

# Functie om het doolhof te tekenen
def teken_doolhof():
    for y in range(rijen):
        for x in range(kolommen):
            karakter = doolhof[y][x]
            scherm_x = start_x + (x * blokjesgrootte)
            scherm_y = start_y + (y * blokjesgrootte)
            
            if karakter == "X":
                scherm.blit(steen, (scherm_x, scherm_y))
                
            if (y, x) in draad_locaties:  # Controleer of deze locatie een draad is
                scherm.blit(DraadVanAriadne, (scherm_x, scherm_y))

            if (y, x) == sleutel_locatie:
                scherm.blit(Sleutel, (scherm_x, scherm_y))

# Doolhofgeneratie met A* controle op bereikbaarheid
def genereer_doolhof_met_bereikbaarheid(uitgang_pos):
    while True:
        doolhof.clear()
        for y in range(rijen):
            rij = ['X' for _ in range(kolommen)]
            doolhof.append(rij)

        # Gebruik DFS of een willekeurige generatietechniek om paden te maken
        generate_doolhof(1, 1)  # Hier moet je je originele doolhofgeneratie code aanroepen
        

        # Controleer de verbinding van alles:
        speler_pos = (start_y_speler, start_x_speler)
        #uitgang_pos = (33,25)
        sleutel_pos = (9, 17)
        draad_locaties = kies_draadlocaties()

        if alles_verbonden(doolhof, speler_pos, uitgang_pos, sleutel_pos, draad_locaties):
            return doolhof  # Als alles bereikbaar is, retourneer het doolhof

def a_star(doolhof, start, doel):
    open_list = []  # The list of nodes to be evaluated
    closed_list = set()  # The list of nodes already evaluated
    came_from = {}  # To reconstruct the path

    # Directions for movement: left, right, down, up (4 directions)

    def get_neighbors(node):
        x, y = node
        neighbors = []
        for dx, dy in a_star_richtingen:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(doolhof[0]) and 0 <= ny < len(doolhof) and doolhof[ny][nx] != "X":
                neighbors.append((nx, ny))
        return neighbors

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    g_scores = {start: 0}
    f_scores = {start: heuristic(start, doel)}
    f_scores[start] = heuristic(start, doel)
    open_list.append((start, f_scores[start]))  # Voeg start node toe met de berekende f_score

    while open_list:
        # Get the node with the lowest f_score from open_list
        current = min(open_list, key=lambda x: f_scores[x[0]])[0]
        open_list = [item for item in open_list if item[0] != current]  # Remove current from open_list
        
        if current == doel:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)  # Add the start node to the path
            return path[::-1]  # Reverse the path to start -> goal

        closed_list.add(current)  # Move current node from open_list to closed_list

        ######### PROBLEM
        #print(current)
        for neighbor in get_neighbors(current):
            if neighbor in closed_list:

                continue  # Ignore the neighbor which is already evaluated

            tentative_g_score = g_scores[current] + 1  # Assume the movement cost is 1

            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                # This path to the neighbor is better than any previous one
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = g_scores[neighbor] + heuristic(neighbor, doel)

                # If the neighbor is not in the open list, add it
                if neighbor not in [item[0] for item in open_list]:
                    open_list.append((neighbor, f_scores[neighbor]))

    return []  # No path found


# Controleer of de speler alles kan bereiken
def controleer_pad(doolhof, start, doel):
    pad = a_star(doolhof, start, doel)
    return bool(pad)  # True als er een pad is

def alles_verbonden(doolhof, speler_pos, uitgang_pos, sleutel_pos, draad_locaties):
    return (controleer_pad(doolhof, speler_pos, uitgang_pos) and
            controleer_pad(doolhof, speler_pos,) and
            controleer_pad(doolhof, speler_pos, sleutel_pos) and
            all(controleer_pad(doolhof, speler_pos, draad) for draad in draad_locaties))  # Controleer ALLE draden
