import pygame
from Doolhof import a_star, doolhof

blokjesgrootte = 30 #de grootte van één vierkant in het doolhof

# Minotaurus die de speler volgt
class Minotaurus:
    def __init__(self, x, y, snelheid = 100):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, blokjesgrootte, blokjesgrootte)
        self.should_move = False  # A flag to control whether the Minotaur should move
        self.snelheid = snelheid
        self._frame_teller = 0
        
    def move_towards_player(self, speler):
        minotaurus_pos = (self.rect.x // blokjesgrootte, self.rect.y// blokjesgrootte)
        speler_pos = (speler.rect.x // blokjesgrootte, speler.rect.y  // blokjesgrootte)

        path = a_star(doolhof, minotaurus_pos, speler_pos)
        if path and len(path) > 1:
            next_step = path[1]  # Path[0] is de huidige positie, [1] is de volgende stap
            self.x, self.y = next_step[0] * blokjesgrootte , next_step[1] * blokjesgrootte 
            self.rect.topleft = (self.x, self.y)

    def update(self, speler):
        """ Update the Minotaur’s behavior """
        # Determine if Minotaur should move
        self._frame_teller += 1
        if self._frame_teller >= self.snelheid:
            self._frame_teller = 0
            self.move_towards_player(speler)
    
    def draw(self, screen):
        minotaurus_afbeelding = pygame.image.load("minotaurus.png")
        minotaurus_afbeelding = pygame.transform.scale(minotaurus_afbeelding, (blokjesgrootte, blokjesgrootte))
        screen.blit(minotaurus_afbeelding, (self.rect.x, self.rect.y))