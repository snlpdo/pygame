#!/usr/bin/env python3

import sys
import pygame
import argparse

from plateau import Plateau
from lettre import * 
from jeu import *

w_width, w_height = 850, 950

fps = 30
message = ""
msg_count = 0
msg_type = "error"

def set_message(m, nb_sec, mtype="error"):
    global message, msg_count, msg_type
    message = m
    msg_count = nb_sec*fps
    msg_type = mtype

def update_message(screen, plateau):
    global msg_count
    if msg_count >= 0:
        msg_count -= 1
        plateau.print_status(screen, message, msg_type)

def main():
    # Analyse de la ligne de commande
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', 
        help='Charger une sauvegarde de partie')
    parser.add_argument('-nb', '--nombre_joueurs', type=int, 
        help='Nombre de joueurs pour cette partie')
    args = parser.parse_args()

    # Initialisation
    pygame.init()
    screen = pygame.display.set_mode((w_width, w_height))
    pygame.display.set_caption('Scrabble')
    clock = pygame.time.Clock()

    plateau = Plateau(screen.get_size(), Jeu.grille_bonus)

    # Création du jeu
    if args.nombre_joueurs==None:
        args.nombre_joueurs=1

    if args.input!=None:
        jeu = Jeu(args.nombre_joueurs, plateau, args.input)
        for j in jeu.joueurs:
            plateau.validation(j)
    else:
        jeu = Jeu(args.nombre_joueurs)

    #####################
    # Boucle principale #
    #####################
    for i in range(len(jeu.joueurs)):
        jeu.tirage_au_sort(i+1, False)

    continuer = True
    piece_deplacee = None
    while continuer:
        # Gestion des évènements
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Fermeture de la fenêtre
                continuer = False
            elif event.type == pygame.KEYUP: 
                if event.key == pygame.K_v: # Capture console
                    print(jeu)
                elif event.key == pygame.K_s: # Sauvegarde fichier
                    filename = jeu.sauvegarder()
                    set_message('Sauvegarde dans '+filename, 2, 'info')
            elif event.type == pygame.MOUSEBUTTONDOWN: # Début de déplacement
                piece_deplacee = plateau.start_move(event.pos, jeu)
                if piece_deplacee == None:
                    plateau.check_button(event.pos, True)
            elif event.type == pygame.MOUSEMOTION: 
                if piece_deplacee != None: # Déplacement en cours
                    plateau.continue_move(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP: 
                if piece_deplacee != None: # Fin de déplacement
                    dst = plateau.get_cell_name(event.pos)
                    if dst!=None:
                        jeu.deplacer_piece(dst, piece_deplacee)
                    plateau.end_move()
                    piece_deplacee = None
                else:
                    plateau.check_button(event.pos, False)
                
        # Afficher l'image du plateau
        screen.blit(plateau.img, (0,0))

        # Afficher les lettres du joueur sur le chevalet et celles
        # en placement provisoire sur le plateau
        plateau.afficher_joueur_courant(screen, jeu)

        # Afficher la lettre en cours de déplacement
        if piece_deplacee != None:
            plateau.draw_move(screen)

        # Mettre à jour l'affichage des statistique
        plateau.afficher_stat(screen, jeu)

        # Bouton de validation
        if plateau.bouton_validation(screen):
            result = jeu.validation()
            if not(result[0]): # Coup non valide
                set_message(result[1], 3)
            elif result[1]!="": # Coup valide
                set_message(result[1], 3, "info")
                plateau.validation(jeu.joueurs[jeu.joueur_courant-1])
                jeu.tirage_au_sort(jeu.joueur_courant)

        update_message(screen, plateau)

        # Mettre à jour l'écran
        pygame.display.flip()

        # Contrôle du rafraichissement des images
        clock.tick(fps)

    pygame.quit()
    quit()

if __name__ == '__main__': main()
