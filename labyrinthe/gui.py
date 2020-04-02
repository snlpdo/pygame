#!/usr/bin/env python3

import pygame
from page0 import Page0
from page1 import Page1
from jeu import Jeu

FPS = 30

# Démarrer la bibliothèque
pygame.init()

# Définir la taille de la fenêtre en pixels
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gestion des menus")

# Horloge pour contrôler le fps
clock = pygame.time.Clock()

# Initialisation des pages
pages = [ Page0(WIDTH, HEIGHT), Page1(WIDTH, HEIGHT), Jeu()]
page_idx = 0
prev_page_idx = 0

# Boucle principale
continuer = True
while continuer:
  # Lancer uniquement la bonne page
  if prev_page_idx!=page_idx: # Chargement si nouvelle page
      prev_page_idx = page_idx
      pages[page_idx].start()
      
  pages[page_idx].update(screen)
  
  
  # Identifier la page suivante
  page_idx = pages[page_idx].next_page_idx
  if page_idx==-1:
    continuer = False
  
  #########################  
  # raffraichir l'affichage
  pygame.display.flip()

  # fps: ici 30 image par seconde
  clock.tick(FPS)

# Terminer l'application
pygame.quit()