import pygame
from Doolhof import a_star, doolhof

blokjesgrootte = 30  #De grootte (in pixels) van één vakje in het doolhof

# Klasse voor de Minotaurus, een vijand die de speler volgt
class Minotaurus:
    def __init__(self, x, y, snelheid = 100):
        self.x = x  # Startpositie x (in pixels)
        self.y = y    # Startpositie y (in pixels)
        self.rect = pygame.Rect(x, y, blokjesgrootte, blokjesgrootte)  # Rechthoek voor botsing en positie
        self.should_move = False  # Vlag om te bepalen of de Minotaurus moet bewegen (optioneel gebruik)
        self.snelheid = snelheid # Hoe vaak de Minotaurus beweegt (hoe lager, hoe sneller)
        self._frame_teller = 0 # Teller om beweging te vertragen

        
    def move_towards_player(self, speler):
        # Bepaal de huidige tegelpositie van de Minotaurus
        minotaurus_pos = (self.rect.x // blokjesgrootte, self.rect.y// blokjesgrootte)
        # Bepaal de tegelpositie van de speler
        speler_pos = (speler.rect.x // blokjesgrootte, speler.rect.y  // blokjesgrootte)
        
        # Bereken het pad van de Minotaurus naar de speler met A*
        path = a_star(doolhof, minotaurus_pos, speler_pos)
        
        # Als er een geldig pad is met minstens één stap richting de speler
        if path and len(path) > 1:
            next_step = path[1] # De volgende stap op het pad (index 0 is huidige positie)
             
            # Zet de Minotaurus op die volgende positie
            self.x, self.y = next_step[0] * blokjesgrootte , next_step[1] * blokjesgrootte 
            self.rect.topleft = (self.x, self.y) # Werk de rechthoek bij

    def update(self, speler):
        """ Update the Minotaur’s behavior """
        # Determineer of de Minotaurus zou moeten bewegen
        # Tel frames om beweging te vertragen volgens 'snelheid'
        self._frame_teller += 1
        # Als de teller de snelheid bereikt, mag hij bewegen
        if self._frame_teller >= self.snelheid:
            self._frame_teller = 0 # Reset teller
            self.move_towards_player(speler)# Verplaats richting spele
    
    def draw(self, screen):
        # Laad de afbeelding van de Minotaurus
        minotaurus_afbeelding = pygame.image.load("minotaurus.png")
       
        # Schaal de afbeelding zodat hij past binnen één vakje
        minotaurus_afbeelding = pygame.transform.scale(minotaurus_afbeelding, (blokjesgrootte, blokjesgrootte))
       
        # Teken de afbeelding op het scherm op de huidige positie
        screen.blit(minotaurus_afbeelding, (self.rect.x, self.rect.y))
