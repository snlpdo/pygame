#!/usr/bin/env python3

# À faire:
#  - pseudo des joueurs dans l'affichage des scores
#  - Gestion de la lettre cachée du joker
#  - Vérification des mots dans un dictionnaire
#  - Fin du jeu
#  - réseau: 
#      * démarrer le serveur sur toutes les adresses IPv4
#      * détection automatique du serveur

import sys
import pygame
import argparse

from plateau import Plateau
from lettre import * 
from jeu import *
from reseau import Reseau

# Dimension de la fenetre
WIDTH, HEIGHT = 850, 950

fps = 30

def cli_setup():
    """ Définir et analyser la ligne de commande. """

    parser = argparse.ArgumentParser(description='Jeu de Scrabble graphique, '+
        'monojoueur ou multijoueurs, en local ou en réseau.')
    parser.add_argument('-i', '--input', 
        help='Charger une sauvegarde de partie')
    parser.add_argument('-nb', '--nombre_joueurs', type=int, 
        help='Nombre de participants au jeu.', default=1)
    parser.add_argument('--serveur', help='Démarrer le jeu en réseau en mode serveur'+
        ' Le nombre de participant doit être supérieur à 1 dans cette situation.',
        action="store_true")
    parser.add_argument('--client', 
        help="Se connecter au serveur dont l'adresse IPv4 est fournie.")
    parser.add_argument('--pseudo', help='Nom à utiliser pour la partie. Pour une, '+
        'partie multijoueur en mode local, un numéro distinct est ajouté pour participant.',
        default='Joueur')
    
    return parser.parse_args()

#######################
# Programme principal #
#######################
def main():
    # Ligne de commande
    args = cli_setup() 

    # Mode réseau ?
    if args.serveur or args.client:
        args.nombre_joueurs = 2 # pour le moment
        reseau = Reseau(args)
        titre = 'Scrabble réseau - ' + args.pseudo
    else:
        reseau = None
        titre = 'Scrabble local'

    # Initialisation de la fenêtre et de pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(titre)

    # Création du plateau
    plateau = Plateau(screen, Jeu.grille_bonus)

    # Création du jeu
    jeu = Jeu(args, plateau, reseau)

    # Contenu des chevalets
    if reseau != None: 
        # En mode réseau, il ne faut tirer au sort que les lettres du joueur local
        # et les envoyer à l'adversaire
        for i in range(2): # Action en 2 temps
            if i==0 and reseau.premier_joueur or i==1 and not(reseau.premier_joueur):
                # Tirer au sort le chevalet 
                tirage = jeu.tirer_au_sort(i+1, False)
                # Envoyer à l'adversaire
                reseau.envoyer('tirage' , ''.join(tirage))
            else:
                # Récupérer le tirage de l'adversaire
                param, tirage = reseau.recevoir(128)
                if param != 'tirage':
                    print("Reçu paramètre "+param+" au lieu de tirage")
                    quit()
                jeu.affecter_tirage(i+1, tirage, False)
        reseau.ecouter_reception(jeu, plateau)
    else: # Tirer au sort le chevalet de tous les joueurs
        for i in range(len(jeu.joueurs)):
            jeu.tirer_au_sort(i+1, False)

    #####################
    # Boucle principale #
    #####################
    continuer = True
    piece_deplacee = None
    clock = pygame.time.Clock()
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
                    plateau.set_message('Sauvegarde dans '+filename, 'info')
            elif event.type == pygame.MOUSEBUTTONDOWN \
              or event.type == pygame.MOUSEMOTION \
              or event.type == pygame.MOUSEBUTTONUP: 
                piece_deplacee = plateau.handle_mouse_click(event, jeu, reseau)

        # Afficher le plateau (arrière-plan, chevalet, lettre en mouvement, 
        # statistiques)
        plateau.draw(jeu)
        
        # Bouton de validation
        plateau.afficher_bouton(jeu.compter_points(), 
            jeu.joueur_local==jeu.joueur_actuel)

        # Clic de validation ?
        if plateau.button.is_clicked():
            result = jeu.validation(jeu.joueur_local)
            if not(result[0]): # Coup non valide
                plateau.set_message(result[1])
            elif result[1]!="": # Coup valide
                plateau.set_message(result[1], 'info')
                plateau.validation(jeu.joueurs[jeu.joueur_actuel-1])
                tirage = jeu.tirer_au_sort(jeu.joueur_actuel)
                if reseau!=None:
                    reseau.envoyer_multiple(['message', 'validation', 'tirage'], 
                        [result[1], '', ''.join(tirage)])

        # Message d'information termporaire
        plateau.afficher_message()

        # Mettre à jour l'écran
        pygame.display.flip()

        # Contrôle du rafraichissement des images
        clock.tick(fps)

    pygame.quit()
    quit()

if __name__ == '__main__': main()
