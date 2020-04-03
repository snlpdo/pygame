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

		# Passer au joueur suivant
		self.joueur= 2 - (self.joueur-1)