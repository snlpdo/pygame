#!/bin/env python3
import pygame
import pygame.freetype
import os
from engine import *

# Constantes utiles
CZ = 50
WIDTH, HEIGHT = CZ*10, CZ*11
BGCOLOR = (213, 166, 49)
BLANC = (255, 255, 255)
MARRON = (97,82,74)
NOIR = (0,0,0)
GRIS = (175, 175, 175)
ROUGE = (255,0,0)

pygame.init()

# Définir la taille de la fenêtre en pixels
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu d'échecs")

# Polices
police = pygame.freetype.SysFont('overpass', 30, True, False)
police_petite = pygame.freetype.SysFont('overpass', 20, True, False)
police_mini = pygame.freetype.SysFont('overpass', 14, True, False)

#####################################
# Création de l'image d'arrière plan
background = pygame.Surface((WIDTH,HEIGHT))
background.fill(BGCOLOR)
toggle = True
for i in range(8):
  text, r = police.render(str(8-i), NOIR)
  background.blit(text, (CZ/2-r.width/2, (i+1)*CZ+CZ/2-r.height/2))
  
  for j in range(8):
    if i==0:
      text, r = police.render(chr(j+ord('A')), NOIR)
      background.blit(text, ((j+1)*CZ+CZ/2-r.width/2, CZ/2-r.height/2))

    if toggle:
      pygame.draw.rect(background, BLANC, ((j+1)*CZ, (i+1)*CZ, CZ, CZ), 0)
    else:
      pygame.draw.rect(background, MARRON, ((j+1)*CZ, (i+1)*CZ, CZ, CZ), 0)
    toggle = not(toggle)
  toggle=not(toggle)

text,r = police_petite.render("Joueurs: ", NOIR)
background.blit(text, (CZ, 9*CZ+CZ/2-r.height/2))
text,r = police_mini.render("vers", NOIR)
pygame.draw.rect(background, GRIS, (6*CZ+CZ/2-r.width/2-5, 9*CZ+CZ/2-r.height/2-5, r.width+10, r.height+10))
background.blit(text, (6*CZ+CZ/2-r.width/2, 9*CZ+CZ/2-r.height/2))

pygame.draw.rect(background, BLANC, (5*CZ, 9*CZ+CZ/4, CZ, CZ/2), 0)
pygame.draw.rect(background, BLANC, (7*CZ, 9*CZ+CZ/4, CZ, CZ/2), 0)

background.convert()

#####################
# Charger les pièces
def charger(filename):
	img = pygame.image.load(os.path.join(curdir,'img', filename)).convert_alpha()
	return pygame.transform.scale(img, (CZ,CZ))

curdir = os.getcwd()
image_tn = charger('tour_noire.png')
image_cn = charger('cavalier_noir.png')
image_dn = charger('dame_noire.png')
image_rn = charger('roi_noir.png')
image_fn = charger('fou_noir.png')
image_pn = charger('pion_noir.png')
image_tb = charger('tour_blanche.png')
image_cb = charger('cavalier_blanc.png')
image_db = charger('dame_blanche.png')
image_rb = charger('roi_blanc.png')
image_fb = charger('fou_blanc.png')
image_pb = charger('pion_blanc.png')

# Horloge pour contrôler le fps
clock = pygame.time.Clock()
fps = 30
temps = 0

#############
# Gestion des déplacements
dep = None
fin = None
def case(pos):
	colonne = int(pos[0]/CZ)-1
	ligne = int(pos[1]/CZ)-1
	if ligne<0 or ligne>7 or colonne<0 or colonne>7:
		return None
	return chr(colonne+ord('A')) + str(8-ligne)

text_joueur_blanc,rect_blanc = police_petite.render("blancs", NOIR)
text_joueur_noir,rect_noir = police_petite.render("noirs", NOIR)
text_erreur = None
tour_blanc = True

#####################
# Boucle principale #
#####################
continuer = True
while continuer:
  # Gestion des évènements
  # (comme la fermeture de la fenêtre)
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      continuer = False
    elif e.type == pygame.MOUSEBUTTONUP:
    	if e.button==1: # case de départ
    		dep = case(e.pos)
    		if dep!=None:
    			text_dep,r = police_petite.render(dep, NOIR)
    			text_erreur=None
    	elif e.button==3: # case d'arrivée
    		fin = case(e.pos)
    		if fin!=None:
    			text_fin,r = police_petite.render(fin, NOIR)
    			text_erreur=None
    	elif e.button==2: # Validation
    		res = valider_coup(dep, fin, tour_blanc)
    		if res==None:
	    		dep = None
	    		fin = None
	    		text_erreur = None
	    		tour_blanc = not(tour_blanc)
	    	else:
	    		text_erreur, r_erreur = police_mini.render(res, ROUGE)

  # Arrière plan
  screen.blit(background, (0,0))
  # pièces de l'échiquier
  for i in range(len(plateau)):
  	for j in range(len(plateau[i])):
  		if plateau[i][j]=='tn':
  			screen.blit(image_tn, ((j+1)*CZ, (i+1)*CZ))
  		elif plateau[i][j]=='cn':
  			screen.blit(image_cn, ((j+1)*CZ, (i+1)*CZ))
  		elif plateau[i][j]=='fn':
  			screen.blit(image_fn, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='dn':
  			screen.blit(image_dn, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='rn':
  			screen.blit(image_rn, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='pn':
  			screen.blit(image_pn, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='pb':
  			screen.blit(image_pb, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='rb':
  			screen.blit(image_rb, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='db':
  			screen.blit(image_db, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='fb':
  			screen.blit(image_fb, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='cb':
  			screen.blit(image_cb, ((j+1)*CZ, (i+1)*CZ))	
  		elif plateau[i][j]=='tb':
  			screen.blit(image_tb, ((j+1)*CZ, (i+1)*CZ))	

  # Éléments de déplacement
  if dep!=None:
  	screen.blit(text_dep, (5*CZ+CZ/4, 9*CZ+CZ/3))
  if fin!=None:
  	screen.blit(text_fin, (7*CZ+CZ/4, 9*CZ+CZ/3))

  # Joueur courant
  if tour_blanc:
  	screen.blit(text_joueur_blanc, (3*CZ, 9*CZ+CZ/2-rect_blanc.height/2))
  else:
  	screen.blit(text_joueur_noir, (3*CZ, 9*CZ+CZ/2-rect_blanc.height/2))

  # Erreur ?
  if text_erreur!=None:
  	screen.blit(text_erreur, (2*CZ, 10*CZ+CZ/2-r_erreur.height/2))  	

  # raffraichir l'affichage
  pygame.display.flip()

  # fps: ici 30 image par seconde
  clock.tick(fps)

# Terminer l'application
pygame.quit()
quit()
