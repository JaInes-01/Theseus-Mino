import pygame
import random 

schermbreedte = 1000
schermhoogte = 800
scherm = pygame.display.set_mode([schermbreedte, schermhoogte]) #maakt het scherm met de opgegeven breedte en hoogte 
clock = pygame.time.Clock() #deze clock regelt hoe vaak het scherm ververst wordt 
pygame.display.set_caption("Slaying the Minotaur") #weergeeft de naam van het spel in de (kleine) tekstbalk


#onderdelen doolhof:
rijen = 21 #aantal rijen van het doolhof (dus in feite de hoogte van het doolhof)
kolommen = 21 #aantal kolommen van het doolhof (breedte)
blokjesgrootte = 30 #de grootte van één vierkant in het doolhof
      
start_x = 1
start_y = 1

# de stenen laden (zodat we stenen muur krijgen ipv witte blokjes):
steen = pygame.image.load("steen.png")
steen = pygame.transform.scale(steen, (blokjesgrootte, blokjesgrootte))  # de afbeelding van schaal aanpassen zodat het overeenkomt met de grootte van een blokje

# De draad van Ariadne toevoegen:
DraadVanAriadne = pygame.image.load("DraadAriadne.png")  
DraadVanAriadne= pygame.transform.scale(DraadVanAriadne, (blokjesgrootte, blokjesgrootte))  
draad_locaties = [(4, 8), (2, 16), (11, 3), (15, 13)]  # Hier geef je de vaste locaties aan


#Sleutel toevoegen: 
Sleutel = pygame.image.load("sleutel1.png")
Sleutel = pygame.transform.scale(Sleutel, (blokjesgrootte, blokjesgrootte))  
sleutel_locatie = (9, 17)

draad_cooldowns = {draad: 0 for draad in draad_locaties}  # Initieer cooldowns voor alle draden

def teleport_speler(speler, draad_locaties, draad_cooldowns):
    huidige_locatie = (speler.rect.y // blokjesgrootte, speler.rect.x // blokjesgrootte)

    # Controleer of de speler op een draad staat én of deze draad nog niet in cooldown zit
    if draad_cooldowns.get(huidige_locatie, 0) == 0 and len(draad_locaties) > 1:
        # Kies een andere draad als bestemming
        mogelijke_bestemmingen = [loc for loc in draad_locaties if loc != huidige_locatie]

        if mogelijke_bestemmingen:
            nieuwe_locatie = random.choice(mogelijke_bestemmingen)
            speler.rect.x = nieuwe_locatie[1] * blokjesgrootte
            speler.rect.y = nieuwe_locatie[0] * blokjesgrootte

            # Cooldowns instellen zodat speler niet meteen terug teleporteert
            draad_cooldowns[huidige_locatie] = 100
            draad_cooldowns[nieuwe_locatie] = 100
