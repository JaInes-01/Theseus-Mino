import pygame
import random 

rijen = 25 #aantal rijen van het doolhof (dus in feite de hoogte van het doolhof)
kolommen = 33 #aantal kolommen van het doolhof (breedte)
blokjesgrootte = 30 #de grootte van één vierkant in het doolhof

def teleport_speler(speler, draad_locaties, draad_cooldowns):
    # Bereken op welke rij en kolom de speler zich nu bevindt
    huidige_locatie = (speler.rect.y // blokjesgrootte, speler.rect.x // blokjesgrootte)

    # Controleer of de speler op een draad staat én of deze draad nog niet in cooldown zit
    if draad_cooldowns.get(huidige_locatie, 0) == 0 and len(draad_locaties) > 1:
        # Kies een andere draad als bestemming
        mogelijke_bestemmingen = [loc for loc in draad_locaties if loc != huidige_locatie]

        # Alleen teleporteren als er ten minste één andere draad beschikbaar is
        if mogelijke_bestemmingen:
            # Kies willekeurig een van de andere draadlocaties als nieuwe positie
            nieuwe_locatie = random.choice(mogelijke_bestemmingen)
            # Verplaats de speler naar de nieuwe locatie
            speler.rect.x = nieuwe_locatie[1] * blokjesgrootte    # Zet x-positie (kolom)
            speler.rect.y = nieuwe_locatie[0] * blokjesgrootte    # Zet y-positie (rij)

            # Stel een cooldown in op zowel de huidige als de nieuwe draadlocatie,
            # zodat de speler niet meteen terug kan teleporteren
            draad_cooldowns[huidige_locatie] = 100
            draad_cooldowns[nieuwe_locatie] = 100
