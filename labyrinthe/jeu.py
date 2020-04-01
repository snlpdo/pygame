import pygame
from personnage import Personnage

BLEU = (0, 0, 255)
BLANC = (255,255,255)
NOIR = (0,0,0)
VERT = (0,255,0)
PLATEAU = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
  [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
  [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
  [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
  [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
CELL_SZ = 40

class Jeu():
    def __init__(self):
        self.next_page_idx = 2

        police_mini = pygame.font.SysFont('caladea', 20)
        self.titre = police_mini.render("Jeu (Esc pour sortir)", True, BLEU)
        police = pygame.font.SysFont('caladea', 80)
        self.victoire = police.render("GAGNÉ !", True, VERT)
        
        self.mes_sprites = pygame.sprite.Group()
        self.p = Personnage(PLATEAU, CELL_SZ)
        self.mes_sprites.add(self.p)
        
    def start(self):
        pygame.display.set_caption("Labyrinthe")
        self.width = CELL_SZ*len(PLATEAU[0])
        self.height = CELL_SZ*len(PLATEAU)
        pygame.display.set_mode((self.width,self.height))
    
    def update(self,s):
        self.next_page_idx = 2

        ###################
        # Gestion des évènements
        for e in pygame.event.get():
            if e.type == pygame.QUIT: # Fermer la fenêtre
                self.next_page_idx = -1
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: # Revenir au menu principal
                    self.next_page_idx = 0
                    
        #########################
        # Mise à jour
        self.mes_sprites.update()

        #########################
        # Dessin du contenu
        s.fill(BLANC)

        # Dessiner le plateau
        for i in range(len(PLATEAU)):
            for j in range(len(PLATEAU[i])):
                if PLATEAU[i][j]==1: # Mur
                    pygame.draw.rect(s, NOIR, (CELL_SZ*j, CELL_SZ*i, CELL_SZ, CELL_SZ))
                else: # Vide
                    pygame.draw.rect(s, BLANC, (CELL_SZ*j, CELL_SZ*i, CELL_SZ, CELL_SZ))
        
        # Afficher un texte
        s.blit(self.titre, (5,5))
        
        # Personnage
        self.mes_sprites.draw(s)
        
        if self.p.gagne:
            w = self.victoire.get_width()
            h = self.victoire.get_height()
            s.blit(self.victoire, (self.width/2-w/2,self.height/2-h/2))
            
