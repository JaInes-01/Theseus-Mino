import pygame

rijen = 25 #aantal rijen van het doolhof (dus in feite de hoogte van het doolhof)
kolommen = 33 #aantal kolommen van het doolhof (breedte)
blokjesgrootte = 30 #de grootte van één vierkant in het doolhof

start_x = 1
start_y = 1

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
        self.teleport_cooldown = 0  # Tijd voordat de speler opnieuw kan teleporteren
        # nu moeten we een inventaris toevoegen voor wanneer de speler dingen op pakt onderweg: 
        self.inventaris = []  # Lege lijst om items bij te houden
    
    # de speler tekenen:
    def draw(self, screen):
        screen.blit(self.afbeelding, (self.rect.x, self.rect.y))  # hiermee wordt de afbeelding (dus de speler) getekend: met screen.blit() wordt de spelerafbeelding op het scherm getekend, met gebruik van de positie die in self.rect staat --> hierdoor komt de speler op de juiste plek terecht

    # de speler laten bewegen:
    def move(self, dx, dy):
        #print(f"Moving: dx={dx}, dy={dy}")
        self.rect.x += dx
        self.rect.y += dy
        
        self.x = self.rect.x
        self.y = self.rect.y
        
    # nakijken of er geen "botsing" is tussen de speler en de muur:
    def check_collision(self, doolhof):
        speler_rect = self.rect #het vierkant van de speler
        for y in range(rijen):
            for x in range(kolommen):
                if doolhof[y][x] == "X": #als het blokje gelijk is aan een muur, dan
                    pixel_x = x * blokjesgrootte
                    pixel_y = y * blokjesgrootte

                    
                    muur_rect = pygame.Rect(pixel_x, pixel_y, blokjesgrootte, blokjesgrootte) #de rechthoek van de muur maken 
                    if speler_rect.colliderect(muur_rect):
                        return True  # Er is een botsing met een muur
        return False

    # functie om dingen toe te voegen aan de inventaris:
    def pak_item(self, item):
        if item not in self.inventaris: #als het item nog niet in de inventaris zit ga je deze toevoegen 
            self.inventaris.append(item)
            print(f"{item} is toegevoegd aan de inventaris!")