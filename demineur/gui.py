#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 1.1 - 22 décembre 2019
Version 2.0 - 2 février 2019

Interface graphique minimale pour le jeu du démineur.

- La taille de la matrice plateau fixe les dimensions de la grille de jeu
(ici 5x4 mais elles peuvent modifiées). 

- La fonction clic_joueur est automatiquement appelée dès que le joueur fait
un clic gauche ou droit sur une case du plateau. 

- La variable fin_du_jeu permet d'autoriser/empêcher le joueur de cliquer
sur le plateau (utile en fin de partie). 

@author: R. Grosbois, NSI Vizille
"""

import pygame
import demineur

# Constantes pour le fonctionnement du jeu
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255,0,0)
GRIS_FONCE = (100, 100, 100)
GRIS_MOYEN = (175, 175, 175)
GRIS_CLAIR = (225, 225, 225)
CELL_SZ = 50

pygame.font.init()
FONT_GRAND = pygame.font.SysFont('comicsans', 50, True, False)
FONT = pygame.font.SysFont('comicsans', 30, False, False)
FONT_MINI = pygame.font.SysFont('comicsans', 20, False, False)

def clic_joueur(case, bouton, plateau, voisinage):
    """
    Fonction appelée lorsque le joueur clique sur une case du plateau.

    case: nom de la cellule (exemple: 'B2')
    bouton: 1 pour creuser, 3 basculer entre non jouée/mine certaine/incertaine
    """

    perdu = demineur.gestion_coup(case, bouton, plateau, voisinage)

    return perdu

def dessiner_plateau(plateau, mine, drapeau, fenetre):
    '''
    Fonction pour dessiner le contenu de plateau dans le fenêtre pygame.
    '''
    fenetre.fill(BLANC)
    
    for i in range(len(plateau)):
        # Légende des lignes
        #if i!=0 and i!=len(plateau)-1:
        #    texte = FONT.render(chr(ord('1')+(i-1)), True, NOIR)
        #    largeur = texte.get_width()
        #    hauteur = texte.get_height()
        #    fenetre.blit(texte, (3*CELL_SZ/4-largeur/2,
        #                     CELL_SZ*i+CELL_SZ/2-hauteur/2))

        for j in range(len(plateau[i])):
            # légende des colonnes
            #if i == 0 and j!=0 and j!=len(plateau)-1:
            #    texte = FONT.render(chr(ord('A')+(j-1)), True, NOIR)
            #    largeur = texte.get_width()
            #    hauteur = texte.get_height()
            #    fenetre.blit(texte, (CELL_SZ*j+CELL_SZ/2-largeur/2,
            #                         3*CELL_SZ/4-hauteur/2))

            ########################
            # Contenu des cellules #
            ########################
            #print(f"plateau[{i}][{j}]={plateau[i][j]}")
            if i==0 or i==(len(plateau)-1) or j==0 or j==(len(plateau[0])-1):
                continue
            
            x = j*CELL_SZ
            y = i*CELL_SZ
            if plateau[i][j] == -1:  # Mine présente
                pygame.draw.rect(fenetre, GRIS_FONCE,
                                 (x+2, y+2, CELL_SZ-4, CELL_SZ-4), 0)
                fenetre.blit(mine, (x, y))
            elif 0 <= plateau[i][j] <= 8:  # case dévoilée: nombre de mines alentour
                pygame.draw.rect(fenetre, GRIS_CLAIR,
                                 (x+2, y+2, CELL_SZ-4, CELL_SZ-4), 0)
                texte = FONT.render(chr(ord('0') + plateau[i][j]), True, NOIR)
                largeur = texte.get_width()
                hauteur = texte.get_height()
                if plateau[i][j] != 0:
                    #print(' text'+ chr(ord('0') + plateau[i][j]))
                    fenetre.blit(texte, (CELL_SZ*(j)+CELL_SZ/2-largeur/2,
                                         CELL_SZ*(i)+CELL_SZ/2-hauteur/2))
            elif 10 <= plateau[i][j] <= 12:  # case non dévoilée
                pygame.draw.rect(fenetre, GRIS_MOYEN,
                                 (x+2, y+2, CELL_SZ-4, CELL_SZ-4), 0)
                if 11 <= plateau[i][j] <= 12:  # Mine certaine
                    fenetre.blit(drapeau, (x, y))
                if plateau[i][j] == 12:  # Mine incertaine
                    texte = FONT_MINI.render('?', True, NOIR)
                    fenetre.blit(texte, (x+.6*CELL_SZ, y+.6*CELL_SZ))


def main():
    '''
    Fonction principale.
    '''

    # Démarrer la bibliothèque
    pygame.init()

    voisinage, plateau = demineur.init(8,8,10)
    
    # Créer l'image du drapeau
    drapeau = pygame.Surface((CELL_SZ, CELL_SZ), pygame.SRCALPHA, 32)
    pygame.draw.line(drapeau, NOIR, (.25*CELL_SZ, .2*CELL_SZ),
                     (.25*CELL_SZ, .8*CELL_SZ), 5)
    pygame.draw.polygon(drapeau, NOIR, [(.25*CELL_SZ, .2*CELL_SZ),
                                        (.75*CELL_SZ, .4*CELL_SZ),
                                        (.25*CELL_SZ, .6*CELL_SZ)])

    # Créer l'image de la mine
    mine = pygame.Surface((CELL_SZ, CELL_SZ), pygame.SRCALPHA, 32)
    pygame.draw.ellipse(mine, NOIR,
                        [0.3*CELL_SZ, 0.3*CELL_SZ, 0.4*CELL_SZ, 0.4*CELL_SZ])
    pygame.draw.line(mine, NOIR,
                     (0.5*CELL_SZ-1, 0.25*CELL_SZ),
                     (0.5*CELL_SZ-1, 0.75*CELL_SZ), 3)
    pygame.draw.line(mine, NOIR,
                     (0.3*CELL_SZ, 0.3*CELL_SZ),
                     (0.7*CELL_SZ, 0.7*CELL_SZ), 4)
    pygame.draw.line(mine, NOIR,
                     (0.7*CELL_SZ, 0.3*CELL_SZ),
                     (0.3*CELL_SZ, 0.7*CELL_SZ), 4)

    # Définir la fenêtre
    n_lignes = len(plateau)
    n_colonnes = len(plateau[0])
    width = n_colonnes*CELL_SZ
    height = n_lignes*CELL_SZ
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Démineur")

    # Mettre à True lorsque la partie est finie
    # pour empêcher le joueur de cliquer sur le plateau
    fin_du_jeu = False
    message_gagne = FONT_GRAND.render('GAGNÉ !', True, ROUGE)
    message_perdu = FONT_GRAND.render('PERDU !', True, ROUGE)

    # Horloge pour contrôler le fps
    clock = pygame.time.Clock()

    dessiner_plateau(plateau, mine, drapeau, screen)

    # Boucle principale
    continuer = True
    while continuer:
        # Gestion des évènements
        # (comme la fermeture de la fenêtre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            elif event.type == pygame.MOUSEBUTTONUP and not fin_du_jeu:
                x = int(event.pos[0]//CELL_SZ)-1
                y = int(event.pos[1]//CELL_SZ)-1
                button = event.button

                if (0 <= x < (n_colonnes-2)) and (0 <= y < (n_lignes-2)) and (button == 1 or button == 3):
                    # Identification de la colonne
                    col = chr(ord('A') + x)
                    # Identification de la ligne
                    ligne = chr(ord('1') + y)

                    fin_du_jeu = clic_joueur(col+ligne, event.button, plateau, voisinage)
                    dessiner_plateau(plateau, mine, drapeau, screen)
                    if fin_du_jeu:
                        message_fin = message_perdu
                    elif demineur.partie_gagnee(plateau, voisinage):
                        message_fin = message_gagne
                        fin_du_jeu = True

        #########################
        # Instructions          #
        # de mise à jour de la  #
        # fenètre               #
        #########################
        #dessiner_plateau(plateau, mine, drapeau, screen)
        if fin_du_jeu:
            w = message_fin.get_width()
            h = message_fin.get_height()
            screen.blit(message_fin, (width/2-w/2,height/2-h/2))

        # raffraichir l'affichage
        pygame.display.flip()

        # fps: ici 30 image par seconde
        clock.tick(30)

    # Terminer l'application
    pygame.quit()


if __name__ == "__main__":
    main()
