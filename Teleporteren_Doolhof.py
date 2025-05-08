import pygame
import random 

rijen = 25 #aantal rijen van het doolhof (dus in feite de hoogte van het doolhof)
kolommen = 33 #aantal kolommen van het doolhof (breedte)
blokjesgrootte = 30 #de grootte van één vierkant in het doolhof

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
