import pygame
from engine import Jeu

"""
Tic Tac Toe en mode réseau.

Pour lancer le serveur:
    python gui serveur
    
Pour lancer le client:
    python gui client
"""


# Constantes utiles
WIDTH = 150
HEIGHT = 150
BLANC = (255,255,255)
NOIR = (0,0,0)

def titre():
    if jeu.serveur:
        joueur = "Serveur"
    else:
        joueur = "Client"
        
    if jeu.mon_tour:
        pygame.display.set_caption(joueur +" - À vous")
    else:
        pygame.display.set_caption(joueur + " - attendre")

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

titre()

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
      
      if jeu.mon_tour:
          jeu.maj(colonne, ligne)

  ##############################
  # Mises à jour des propriétés
  # du contenu
  if jeu.fin[0]:
      if jeu.fin[1]==jeu.joueur:
          pygame.display.set_caption("Gagné !")
      else:
          pygame.display.set_caption("Perdu !")
  else:
      titre()
  
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

  avous = jeu.mon_tour
# Terminer l'application
pygame.quit()

