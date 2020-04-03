"""
Ce module s'occupe du fonction interne du jeu.
Il ne doit surtout pas supposer qu'il existe une interface
graphique.
"""

class Jeu:

  def __init__(self):
    # Contenu des cellules:
    # 0: case vide
    # 1: croix
    # 2: cercle
    self.plateau = [
      [0,0,0],
      [0,0,0],
      [0,0,0],
    ]

    # 2 joueurs 1 (croix) et 2 (cercle)
    self.joueur = 1
    self.fin = (False, 0)

  def maj(self, c, l):
    """
    Prendre en compte un coup sur la cellule
    de coordonnées c (colonne) et l (ligne)
    """
    # Vérifier que la case est libre
    if self.plateau[l][c]!=0:
      return
    else:
      self.plateau[l][c] = self.joueur

    # Victoire ?
    self.fin = self.victoire()

    # Passer au joueur suivant
    self.joueur= 2 - (self.joueur-1)

  def victoire(self):
        """
        Vérifier si un joueur a gagné
        """
        
        # variable locale (plus rapide)
        p  = self.plateau 
        
        # Vérification des lignes et colonnes
        for i in range(3):
            if p[i][0]!=0 and p[i][0]==p[i][1]==p[i][2]:
                return (True, p[i][0])
            if p[0][i]!=0 and p[0][i]==p[1][i]==p[2][i]:
                return (True, p[0][i])
        # Vérifier les diagonales
        if p[0][0]!=0 and p[0][0]==p[1][1]==p[2][2]:
            return (True, p[0][0])
        if p[2][0]!=0 and p[2][0]==p[1][1]==p[0][2]:
            return (True, p[2][0])
        return (False, 0)