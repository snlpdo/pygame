import pygame

class Lettre():
    alphabet = {
        "A": (9, 1),
        "B": (2, 3),
        "C": (2, 3),
        "D": (3, 2),
        "E": (15, 1),
        "F": (2, 4),
        "G": (2, 2),
        "H": (2, 4),
        "I": (8, 1),
        "J": (1, 8),
        "K": (1, 10),
        "L": (5, 1),
        "M": (3, 2),
        "N": (6, 1),
        "O": (6, 1),
        "P": (2, 3),
        "Q": (1, 8),
        "R": (6, 1),
        "S": (6, 1),
        "T": (6, 1),
        "U": (6, 1),
        "V": (2, 4),
        "W": (1, 10),
        "X": (1, 10),
        "Y": (1, 10),
        "Z": (1, 10),
        " ": (2, 0)
        }
    
    def get_pioche():
        """ Génère et retourne la pioche initiale constituée
        de toutes les lettres de l'alphabet en respectant leurs
        occurrences. """

        pioche = []
        for key,val in Lettre.alphabet.items():
            for i in range(val[0]):
                pioche.append(key)
        return pioche

    def __init__(self, c):
        """ Construire une Lettre correspondant à un caractère sans
        image ni position initiales."""

        self.char = c
        self.img = None
        self.pos = None

    def __str__(self):
        """ Description du contenu de la Lettre """

        return "'" + self.char + "', pos: " + self.pos

    def creer_image(self, size):
        """ Créer l'image correspondant à la lettre:
        - font blanc (légèrement plus petit que la taille de la cellule).
        - affichage caractère au centre
        - affichage du nombre de points correspondants en bas à droite

        INPUT:
        size: dimension de l'image (celle d'une cellule)
        """
        w, h = size[0], size[1]
        self.img = pygame.Surface((w,h))

        pygame.draw.rect(self.img, (255, 255, 255), (2, 2, w-4, h-4))
        policeG = pygame.font.SysFont('comicsans', 30)
        policeP = pygame.font.SysFont('comicsans', 14)
    
        text = policeG.render(self.char, True, (0,0,0))
        self.img.blit(text, (w/2-text.get_width()/2, h/2-text.get_height()/2))
        val = Lettre.alphabet[self.char]
        if val[1]!=0:
            text2 = policeP.render(str(val[1]), True, (0,0,0))
            self.img.blit(text2, (6.8*w/8-text.get_width()/2,
                                7*h/8-text.get_height()/2))
