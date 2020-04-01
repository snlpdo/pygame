#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 1.0 - 2 février 2019

Moteur du jeu de démineur

@author: R. Grosbois, NSI Vizille
"""
import random

def init(n_col=5, n_lignes=4,nb_mines=3):
    '''
    Initialiser les 3 tableaux pour le jeu.

    Chaque tableau a 2 colonnes et 2 lignes de plus pour gérer les effets
    de bords (mais aucune mine ne se trouve sur ces bords).
    '''

    # Nombre de mine par cellule (aléatoires), nb_mines en tout
    # 0: pas de mine
    # 1: 1 mine 
    mines = [[ 0 for j in range(n_col+2)] for i in range(n_lignes+2)]
    pos = [i for i in range(n_col*n_lignes)]
    random.shuffle(pos)
    for i in range(nb_mines):
        index = pos.pop()
        ligne = index//n_col
        colonne = index%n_col
        mines[ligne+1][colonne+1] = 1
        
    # Nombre de mines voisines par cellule:
    # - valeurs possibles: 0 à 8
    # - valeur pour cellule contenant une mine: 9
    voisinage = [[ 9 for j in range(n_col+2)] for i in range(n_lignes+2)]  
    for i in range(1,n_lignes+1):
        for j in range(1,n_col+1):
            if mines[i][j]==0:
                somme = 0
                somme += mines[i-1][j-1]
                somme += mines[i-1][j]
                somme += mines[i-1][j+1]
                somme += mines[i][j-1]
                somme += mines[i][j+1]
                somme += mines[i+1][j-1]
                somme += mines[i+1][j]
                somme += mines[i+1][j+1]
                voisinage[i][j] = somme

    # Contenu de chaque cellule à afficher:
    # -1: mine dévoilée (partie perdue)
    # 0 à 8 : Nombre de mines voisine (cellule jouée)
    # 10: cellule non jouée
    # 11: drapeau pour mine certaine
    # 12: drapeau pour mine incertaine
    plateau = [[ 10 for j in range(n_col+2)] for i in range(n_lignes+2)]

    return voisinage, plateau
    
def gestion_coup(position, commande, plateau, voisinage):
    '''
    La position est fournie au format '<col><ligne>' (ex: H4) et
    la commande vaut:
        - 1 pour creuser
        - 20 pour supprimer une annotation
        - 21 pour annoter avec une certitude (drapeau)
        - 22 pour annoter avec une incertitude
        - 3 pour basculer l'annotation entre successivement 
          non joué/drapeau/incertain 
    
    Cette fonction revoit True si la partie est perdue, False sinon
    '''
    position = position.upper()
    # Retrouver les indices de colonnes et lignes
    i = ord(position[1])-ord('1')+1
    j = ord(position[0])-ord('A')+1
    
    if commande==1: # creuser
        # Impossible si case jouée ou annotée
        if plateau[i][j] != 10:
            return False
        if voisinage[i][j]==9: # mine présente
            plateau[i][j]=-1
            return True # Partie perdue
        else: # pas de mine
            plateau[i][j]=voisinage[i][j]
            if plateau[i][j]==0:
                propagation_zero(i,j,plateau,voisinage)
    elif commande==20: # supprimer annotation
        # Seulement si case non jouée
        if plateau[i][j]<10:
            return False
        else:
            plateau[i][j] = 10
    elif commande==21: # poser un drapeau
        # Seulement si case non jouée
        if plateau[i][j]<10:
            return False
        else:
            plateau[i][j] = 11
    elif commande==22: # indiquer une incertitude
        # Seulement si case non jouée
        if plateau[i][j]<10:
            return False
        else:
            plateau[i][j] = 12
    elif commande==3: # basculer
        # Seulement si case non jouée
        if plateau[i][j]<10:
            return False
        elif plateau[i][j]==10:
            plateau[i][j] = 11
        elif plateau[i][j]==11:
            plateau[i][j] = 12
        elif plateau[i][j]==12:
            plateau[i][j] = 10
    return False

def propagation_zero(i,j,p,v):
    '''
    Algorithme récursif de propagation du 0 
    (0 mines dans le voisinage)
    '''
    p[i][j]=0
    # Dévoiler le nombre de mines de chaque voisin non annoté
    if p[i-1][j-1]<11 and v[i-1][j-1]!=0: 
        p[i-1][j-1] = v[i-1][j-1]
    if p[i-1][j]<11 and v[i-1][j]!=0: 
        p[i-1][j] = v[i-1][j]
    if p[i-1][j+1]<11 and v[i-1][j+1]!=0: 
        p[i-1][j+1] = v[i-1][j+1]
    if p[i][j-1]<11 and v[i][j-1]!=0: 
        p[i][j-1] = v[i][j-1]
    if p[i][j+1]<11 and v[i][j+1]!=0: 
        p[i][j+1] = v[i][j+1]
    if p[i+1][j-1]<11 and v[i+1][j-1]!=0: 
        p[i+1][j-1] = v[i+1][j-1]
    if p[i+1][j]<11 and v[i+1][j]!=0: 
        p[i+1][j] = v[i+1][j]
    if p[i+1][j+1]<11 and v[i+1][j+1]!=0: 
        p[i+1][j+1] = v[i+1][j+1]

    # Propagation récursive
    if v[i-1][j-1]==0 and p[i-1][j-1]!=0: 
        propagation_zero(i-1,j-1,p,v)
    if v[i-1][j]==0 and p[i-1][j]!=0: 
        propagation_zero(i-1,j,p,v)
    if v[i-1][j+1]==0 and p[i-1][j+1]!=0: 
        propagation_zero(i-1,j+1,p,v)
    if v[i][j-1]==0 and p[i][j-1]!=0: 
        propagation_zero(i,j-1,p,v)
    if v[i][j+1]==0 and p[i][j+1]!=0: 
        propagation_zero(i,j+1,p,v)
    if v[i+1][j-1]==0 and p[i+1][j-1]!=0: 
        propagation_zero(i+1,j-1,p,v)
    if v[i+1][j]==0 and p[i+1][j]!=0: 
        propagation_zero(i+1,j,p,v)
    if v[i+1][j+1]==0 and p[i-1][j+1]!=0: 
        propagation_zero(i+1,j+1,p,v)

def partie_gagnee(p,e):
    '''
    Une partie est gagnée lorsque:
        - toutes les cases ont été jouées ou annotées.
        - toutes les mines sont annotées par un drapeau.
    '''
    # Toutes les cases ont été jouées ?
    for i in range(len(p)-2):
        for j in range(len(p[i])-2):
            if p[i+1][j+1]==10:
                return False
            
    # Toutes les mines ont été annotées
    for i in range(len(p)-2):
        for j in range(len([i])-2):
            if e[i+1][j+1]==1 and p[i+1][j+1]!=11:
                return False
    return True

