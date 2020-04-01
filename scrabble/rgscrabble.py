#!/usr/bin/env python3

# À faire:
#  - Fenêtre graphique lors du démarrage réseau
#
# Bugs connus:

import sys
import pygame
import argparse
import sys

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
        'monojoueur ou multijoueurs, en local ou en réseau (uniquement 2 joueurs).')
    parser.add_argument('-i', '--input', 
        help='Charger une partie sauvegardée.')
    parser.add_argument('-nb', '--nombre_joueurs', type=int, 
        help='Nombre de participants au jeu.', default=1)
    parser.add_argument('--serveur', help='Démarrer le jeu en réseau en mode serveur'+
        ' Le nombre de participant doit être supérieur à 1 dans cette situation.',
        action="store_true")
    parser.add_argument('--client', action='store_true',
        help="Se connecter au serveur (autodétection).")
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
    if args.client:
        if args.input!=None:
            sys.stderr.write("\nErreur: le client n'a pas le droit de charger "+
                "une partie sauvegardée\n\n")
            quit()

    # Mode réseau
    if args.serveur or args.client:
        args.nombre_joueurs = 2 # pour le moment
        reseau = Reseau(args)
    else:
        reseau = None

    # Initialisation de la fenêtre et de pygame
    if reseau != None:
        titre = 'Scrabble réseau - ' + args.pseudo
        if args.serveur: 
            titre += ' (serveur)'
        elif args.client: 
            titre += ' (client)'
    else:
        titre = 'Scrabble (local)'
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(titre)

    # Création du plateau
    plateau = Plateau(screen, Jeu.grille_bonus)

    # Création du jeu
    jeu = Jeu(args, reseau)
    # mémoriser les éventuelles lettres posées sur le plateau
    plateau.memoriser(jeu.joueurs[0])

    # Contenu des chevalets
    jeu.debuter_partie(reseau, plateau)

    #####################
    # Boucle principale #
    #####################
    continuer = True
    clock = pygame.time.Clock()
    while continuer:
        # Gestion des évènements
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Fermeture de la fenêtre
                continuer = False
                if reseau!=None: reseau.reception.stop()
            elif event.type == pygame.KEYUP:
                if plateau.edition_joker==None:
                    if event.key == pygame.K_v: # Capture console
                        print(jeu)
                    elif event.key == pygame.K_s: # Sauvegarde fichier
                        if not(args.client):
                            filename = jeu.sauvegarder()
                            plateau.set_message('Sauvegarde dans '+filename, 'info')
                    elif jeu.partie_finie:
                        continuer = False
                else: # Édition joker
                    res = plateau.editer_joker(event.key)
                    if res[0] and reseau != None:
                        reseau.envoyer('joker', str(jeu.joueur_local)+res[1])
            elif not(jeu.partie_finie) and event.type == pygame.MOUSEBUTTONDOWN \
              or event.type == pygame.MOUSEMOTION \
              or event.type == pygame.MOUSEBUTTONUP: 

                res = plateau.handle_mouse_click(event, jeu)
                if res != None: 
                    ############################
                    # Déplacement d'une lettre #
                    ############################
                    src = res[0].pos # cellule initiale
                    dst = res[1] # cellule finale
                    result = jeu.deplacer_piece(jeu.joueur_local, dst, res[0])
                    if result and reseau!=None:
                        reseau.envoyer('move', src + ',' + dst)

        # Afficher le plateau (arrière-plan, chevalet, lettre en mouvement, 
        # statistiques)
        plateau.draw(jeu)
        
        # Message d'information termporaire
        plateau.afficher_message()

        if not(jeu.partie_finie): #### Partie en cours ####

            # Comptabiliser le score actuel du coup en cours
            total_points, mots, points = jeu.verifier_positionnement()

            # Bouton de validation (affichant les points)
            plateau.afficher_bouton(total_points, jeu, jeu.local_is_playing())

            ###################
            # Valider un coup #
            ###################
            if plateau.button.is_clicked():
                # Vérifier si le coup est valide
                result = jeu.valider(jeu.joueur_local)

                if not(result[0]): # Coup non valide
                    plateau.set_message(result[1])

                else: # Coup valide
                    plateau.set_message(result[1], 'info')
                    plateau.memoriser(jeu.joueurs[jeu.joueur_actuel-1])
                    tirage = jeu.completer_chevalet(jeu.joueur_actuel)
                    if reseau!=None:
                        if tirage=="##FIN##": # fin de la partie
                            reseau.envoyer_multiple(['detail_coup', 'validation', 'tirage', 'fin'], 
                                [result[1], '', ''.join(tirage), ''])
                            reseau.reception.stop()
                        else: # coup classique
                            reseau.envoyer_multiple(['detail_coup', 'validation', 'tirage'], 
                                [result[1], '', ''.join(tirage)])
                    else:
                        jeu.joueur_local = jeu.joueur_actuel
        
        else: #### Partie finie ####
            plateau.afficher_fin(screen, jeu)

        # Mettre à jour l'écran
        pygame.display.flip()

        # Contrôle du rafraichissement des images
        clock.tick(fps)

    pygame.quit()
    quit()

if __name__ == '__main__': main()
