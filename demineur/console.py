#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 1.0 - 2 février 2019

Jeu du démineur en mode console.

@author: R. Grosbois, NSI Vizille
"""
import demineur

#######################
# Fonctions générales #
#######################

#########################################
# Fonctions spécifiques pour la console #
#########################################

def dessiner_plateau(p):
    print("Plateau:")
    print('  ', end='')
    for j in range(len(p[0])-2):
        print(chr(ord('A')+j), end='')
    print()

    for i in range(len(p)):
        if i==0 or i==len(p)-1:
            print(' ',end='')
        else:
            print(chr(ord('1')+(i-1)),end='')
        for j in range(len(p[i])):
            
            if i==0 and (j==0 or j==len(p[i])-1) \
               or i==len(p)-1 and (j==0 or j==len(p[i])-1):
                print('+', end='')
            elif i==0 or i==len(p)-1:
                print('-', end='')
            elif j==0 or j==len(p[i])-1:
                print('|', end='')
            elif p[i][j]==-1: # Mine
                print('*', end='')
            elif 0<=p[i][j]<=8: # Joué (afficher le voisinage)
                if p[i][j]==0:
                    print(' ', end='')
                else:
                    print(str(p[i][j]), end='')
            elif p[i][j]==10: # Cases non jouée
                print('.', end='')
            elif p[i][j]==11: # Drapeau pour mine certaine
                print('d', end='')
            elif p[i][j]==12: # Drapeau pour mine probable
                print('?', end='')
        print()
        
def saisir_coup(index):
    commande = 1
    
    coup = input(f"Coup[{index}]: ").split(' ')
    cellule = coup[0]
    if len(coup)==2:
        if coup[1]=='n': # enlever l'annotation
            commande = 20
        elif coup[1]=='d': # drapeau
            commande = 21
        elif coup[1]=='?': # incertain
            commande = 22
        elif coup[1]=='t': # toggle
            commande = 3
        
    return (cellule, commande)

def main():
    # Nombre de mines
    #nb = int(input('Nombre de mines: '))    

    # Initialisation
    v, p = demineur.init()
    dessiner_plateau(p)
    
    # Démarrer le jeu
    nb_coups = 0
    continuer = True
    while continuer:
        nb_coups += 1
        pos,cmd = saisir_coup(nb_coups)
        perdu = demineur.gestion_coup(pos, cmd, p, v)
        dessiner_plateau(p)
        if perdu:
            print("PERDU", end=' ')
            continuer = False
        if demineur.partie_gagnee(p, v):
            print("GAGNË", end=' ')
            continuer = False
    
    print(f"en {nb_coups} coup(s).")

if __name__ == '__main__':
  main()
