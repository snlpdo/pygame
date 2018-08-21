#!/usr/bin/env python3

import sys
import pygame
import argparse
import socket

from plateau import Plateau
from lettre import * 
from jeu import *
from reseau import Reseau

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
    parser.add_argument('--serveur', help='Lancer un serveur de Scrabble en réseau.'+
        ' Il faut spécifier un nombre de joueur supérieur à 1 dans cette situation.',
        action="store_true")
    parser.add_argument('--client', 
        help="Se connecter au serveur avec l'adresse IPv4 fournie")
    parser.add_argument('--pseudo', help='Nom à utiliser pour une partie réseau')
    args = parser.parse_args()

    # Déterminer le nombre de joueurs
    if args.nombre_joueurs==None:
        args.nombre_joueurs=1

    # Mode serveur 
    reseau = None
    if args.serveur:
        # Pseudo local
        if args.pseudo==None: args.pseudo = 'master'
        
        print("\n=== Mode réseau (serveur)===")
        print("Attente de connexion...")
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ss.bind( (socket.gethostname(), 7175) )
        ss.listen(1) 
        
        # Connexion avec client
        sock, dist_sock = ss.accept()
        reseau = Reseau(sock, args.pseudo, True)

    elif args.client:
        # Pseudo local
        if args.pseudo==None: args.pseudo = 'client'

        print("\nMode réseau (client)")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connexion avec serveur
        sock.connect( (args.client, 7175))
        reseau = Reseau(sock, args.pseudo, False)

    # Initialisation de la fenêtre et de pygame
    pygame.init()
    screen = pygame.display.set_mode((w_width, w_height))
    if reseau == None:
        titre = 'Scrabble local'
    else: titre = 'Scrabble réseau - ' + args.pseudo
    pygame.display.set_caption(titre)
    clock = pygame.time.Clock()

    # Création du plateau
    plateau = Plateau(screen.get_size(), Jeu.grille_bonus)

    # Création du jeu
    if reseau!=None: args.nombre_joueurs = 2 # pour le moment

    if args.input!=None: # Chargement d'un fichier
        jeu = Jeu(args.nombre_joueurs, plateau, args.input, reseau)
        for j in jeu.joueurs: # valider les lettre déjà posées
            plateau.validation(j)
    else: # Nouveau jeu
        jeu = Jeu(args.nombre_joueurs, None, None, reseau)

    # Tirage au sort du contenu des chevalets
    if reseau != None: 
        for i in range(2):
            if i==0 and reseau.premier_joueur or i==1 and not(reseau.premier_joueur):
                # Tirer au sort le chevalet local et l'envoyer
                tirage = jeu.tirer_au_sort(i+1, False)
                reseau.envoyer('tirage' , ''.join(tirage))
            else:
                # récupérer le tirage au sort de l'adversaire et le prendre en compte
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
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                # Début de déplacement ?
                piece_deplacee = plateau.start_move(event.pos, jeu)
                # Appui sur le bouton
                if piece_deplacee == None:
                    plateau.check_button(event.pos, True)
            elif event.type == pygame.MOUSEMOTION: 
                if piece_deplacee != None: # Déplacement en cours
                    plateau.continue_move(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP: 
                if piece_deplacee != None: # Fin de déplacement
                    src = piece_deplacee.pos
                    dst = plateau.get_cell_name(event.pos)
                    
                    if dst!=None:
                        result = jeu.deplacer_piece(jeu.joueur_local, dst, piece_deplacee)
                        if result and reseau!=None:
                            reseau.envoyer('move', src + ',' + dst)
                    plateau.end_move()
                    piece_deplacee = None
                else:
                    plateau.check_button(event.pos, False)
                
        # Afficher l'image du plateau
        screen.blit(plateau.img, (0,0))

        # Afficher les lettres sur le chevalet du joueur local
        plateau.afficher_lettres_chevalet(screen, jeu)

        # Afficher les lettres en placement
        # provisoire du joueur actuel
        plateau.afficher_lettres_provisoires(screen, jeu)

        # Afficher la lettre en cours de déplacement
        if piece_deplacee != None: 
            plateau.draw_move(screen)

        # Mettre à jour l'affichage des statistique
        plateau.afficher_stat(screen, jeu)

        # Bouton de validation
        if plateau.bouton_validation(screen):
            result = jeu.validation(jeu.joueur_local)
            if not(result[0]): # Coup non valide
                set_message(result[1], 3)
            elif result[1]!="": # Coup valide
                set_message(result[1], 3, "info")
                plateau.validation(jeu.joueurs[jeu.joueur_actuel-1])
                tirage = jeu.tirer_au_sort(jeu.joueur_actuel)
                if reseau!=None:
                    reseau.envoyer('validation', '')
                    reseau.envoyer('tirage' , ''.join(tirage))

        # Message d'information ponctuel
        update_message(screen, plateau)

        # Mettre à jour l'écran
        pygame.display.flip()

        # Contrôle du rafraichissement des images
        clock.tick(fps)

    pygame.quit()
    quit()

if __name__ == '__main__': main()
