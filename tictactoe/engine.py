"""
Ce module s'occupe du fonction interne du jeu.
Il ne doit surtout pas supposer qu'il existe une interface
graphique.
"""

# Contenu des cellules:
# 0: case vide
# 1: croix
# 2: cercle
plateau = [
  [0,0,0],
  [0,0,0],
  [0,0,0],
]

# 2 joueurs 1 (croix) et 2 (cercle)
joueur = 1

def maj(c, l):
	"""
	Prendre en compte un coup sur la cellule
	de coordonnées c (colonne) et l (ligne)
	"""
	# Pour pouvoir modifier la variable joueur dans la fonction
	global joueur

	# Vérifier que la case est libre
	if plateau[l][c]!=0:
		return
	else:
		plateau[l][c]=joueur

	# Passer au joueur suivant
	if joueur==1:
		joueur=2
	else:
		joueur=1

