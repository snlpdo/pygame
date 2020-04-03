import pygame
from engine import Jeu

"""
Ce module ne s'occupe que de la partie graphique (dessiner le plateau, les pièce) 
et de l'interaction avec l'utilisateur (gestion de la souris et/ou du clavier)
"""

# Constantes utiles
WIDTH = 150
HEIGHT = 150
BLANC = (255,255,255)
NOIR = (0,0,0)

# Démarrer la bibliothèque
pygame.init()

# Création du jeu
jeu = Jeu()

# Définir la taille de la fenêtre en pixels
screen = pygame.display.set_mode((WIDTH,HEIGHT))

##################################################
# Préparer les images d'arrière plan et les pièces
bg = pygame.Surface((WIDTH,HEIGHT))
bg.fill(BLANC)
pygame.draw.line(bg, NOIR, (0,HEIGHT/3), (WIDTH,HEIGHT/3), 3)
pygame.draw.line(bg, NOIR, (0,2*HEIGHT/3), (WIDTH,2*HEIGHT/3), 3)
pygame.draw.line(bg, NOIR, (WIDTH/3,0), (WIDTH/3,HEIGHT), 3)
pygame.draw.line(bg, NOIR, (2*WIDTH/3,0), (2*WIDTH/3,HEIGHT), 3)

w = WIDTH/3-4
h = HEIGHT/3-4
croix = pygame.Surface((w,h))
croix.fill(BLANC)
pygame.draw.line(croix, NOIR, (w/4, h/4), (3*w/4, 3*h/4), 3)
pygame.draw.line(croix, NOIR, (w/4, 3*h/4), (3*w/4, h/4), 3)

cercle = pygame.Surface((w,h))
cercle.fill(BLANC)
pygame.draw.circle(cercle, NOIR, (int(w//2), int(h//2)), int(3*w//8), 3)
####################################################

# Horloge pour contrôler le fps
clock = pygame.time.Clock()

# Boucle principale
continuer = True
while continuer:
  # Gestion des évènements
  # (comme la fermeture de la fenêtre)
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      continuer = False
    elif e.type == pygame.MOUSEBUTTONUP:
      position = e.pos
      colonne = int(position[0]//(WIDTH/3))
      ligne = int(position[1]//(HEIGHT/3))
      jeu.maj(colonne, ligne)

  ##############################
  # Mises à jour des propriétés
  # du contenu
  
  
  #########################
  # Dessin du contenu
  screen.blit(bg, (0,0))
  for i in range(len(jeu.plateau)):
    for j in range(len(jeu.plateau[i])):
      if jeu.plateau[i][j]==1: # une croix
        screen.blit(croix, (j*WIDTH/3+2, i*HEIGHT/3+2))
      elif jeu.plateau[i][j]==2: # un cercle
        screen.blit(cercle, (j*WIDTH/3+2, i*HEIGHT/3+2))
  
  #########################  
  # raffraichir l'affichage
  pygame.display.flip()

  # fps: ici 30 image par seconde
  clock.tick(30)

# Terminer l'application
pygame.quit()
quit()
