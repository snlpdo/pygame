import random

from lettre import *

LIGNES = "ABCDEFGHIJKLMNO"

class Jeu():

	def __init__(self):
		self.grille_bonus = [
	         ["MT","  ","  ","LD","  ","  ","  ","MT","  ","  ","  ","LD","  ","  ","MT"],
	         ["  ","MD","  ","  ","  ","LT","  ","  ","  ","LT","  ","  ","  ","MD","  "],
	         ["  ","  ","MD","  ","  ","  ","LD","  ","LD","  ","  ","  ","MD","  ","  "],
	         ["LD","  ","  ","MD","  ","  ","  ","LD","  ","  ","  ","MD","  ","  ","LD"],
	         ["  ","  ","  ","  ","MD","  ","  ","  ","  ","  ","MD","  ","  ","  ","  "],
	         ["  ","LT","  ","  ","  ","LT","  ","  ","  ","LT","  ","  ","  ","LT","  "],
	         ["  ","  ","LD","  ","  ","  ","LD","  ","LD","  ","  ","  ","LD","  ","  "],
	         ["MT","  ","  ","LD","  ","  ","  ","DP","  ","  ","  ","LD","  ","  ","MT"],
	         ["  ","  ","LD","  ","  ","  ","LD","  ","LD","  ","  ","  ","LD","  ","  "],
	         ["  ","LT","  ","  ","  ","LT","  ","  ","  ","LT","  ","  ","  ","LT","  "],
	         ["  ","  ","  ","  ","MD","  ","  ","  ","  ","  ","MD","  ","  ","  ","  "],
	         ["LD","  ","  ","MD","  ","  ","  ","LD","  ","  ","  ","MD","  ","  ","LD"],
	         ["  ","  ","MD","  ","  ","  ","LD","  ","LD","  ","  ","  ","MD","  ","  "],
	         ["  ","MD","  ","  ","  ","LT","  ","  ","  ","LT","  ","  ","  ","MD","  "],
	         ["MT","  ","  ","LD","  ","  ","  ","MT","  ","  ","  ","LD","  ","  ","MT"]]
		self.grille = [ ["" for x in range(15)] for y in range(15)]
		self.pioche = Lettre.get_pioche()
		self.chevalet = [[None for i in range(9)]]
		self.provisoire = []
		self.score = 0
		self.tour_jeu = 0

	def tirage_au_sort(self):
		# Supprimer les pièces en attente
		self.provisoire = []

		# Compter le nombre pièces initiale sur le chevalet
		compte = 0
		for l in self.chevalet[0]:
			if l!=None: compte += 1

		# Remplir le chevalet
		while compte<7:
			random.shuffle(self.pioche)
			c = self.pioche.pop()
			lettre = Lettre(c)

			i=0
			while self.chevalet[0][i]!=None: i += 1
			lettre.pos = 'Q' + str(i+4)
			self.chevalet[0][i] = lettre

			compte = 0
			for l in self.chevalet[0]:
				if l!=None: compte += 1

		# Début du tour de jeu suivant
		self.tour_jeu += 1

	def __str__(self):
		s = ' '
		for i in range(15):
			if i<9:
				s += '  '
			else:
				s += ' 1'
		s += '\n'

		s += ' '
		for i in range(15):
			if i<9:
				s += ' ' + str(i+1)
			else:
				s += ' ' + str(i+1-10)
		s += '\n ' + '-'*31 + '\n'
		for i in range(len(self.grille)):
			s += LIGNES[i] + "|"
			for j in range(len(self.grille[i])):
				if self.grille[i][j]=="":
					s += ' |'
				else:
					s += self.grille[i][j] + '|'
			s += '\n ' + '-'*31 + '\n'
		s += '\n'

		s += '   ' + '-'*(2+len(self.chevalet[0])) + '\n'
		s += '   |'
		for i in range(len(self.chevalet[0])):
			if self.chevalet[0][i]==None:
				s += ' '
			else:
				s += self.chevalet[0][i].char
		s += '|\n'
		s += '   ' + '-'*(2+len(self.chevalet[0])) + '\n'

		s += '\nScore: ' + self.score
		return s

	def get_cell_name(self, x, y):
		return LIGNES[y] + str(x+1)

	def get_cell_info(self, cell_name):
		if cell_name[0]=='Q': # zone de chevalet
			i = 0
			j = int(cell_name[1:])-4
			if self.chevalet[i][j]==None:
				return (self.chevalet, (j,i), False)
			else:
				return (self.chevalet, (j, i), True)
		else: # zone de jeu
			i = LIGNES.index(cell_name[0])
			j = int(cell_name[1:])-1
			if self.grille[i][j] == "":
				return (self.grille, (j,i), False)
			else:
				return (self.grille, (j, i), True)

	def free_cell(self, cell_name):
		if cell_name[0]=='Q': # zone de chevalet
			i = 0
			j = int(cell_name[1:])-4
			self.chevalet[i][j]=None
		else: # zone de jeu
			i = LIGNES.index(cell_name[0])
			j = int(cell_name[1:])-1
			self.grille[i][j] == ""

	def deplacement(self, destination, piece):
		dst_zone, dst_idx, busy = self.get_cell_info(destination)

		if busy: # destination invalide
			return False

		src_zone, src_idx, busy = self.get_cell_info(piece.pos)

		# libérer l'ancienne position
		self.free_cell(piece.pos)
		if src_zone==self.chevalet and dst_zone==self.grille:
			# Nouvelle piece en placement provisoire
			self.chevalet[src_idx[1]][src_idx[0]] = None
			self.grille[dst_idx[1]][dst_idx[0]] = piece.char
			self.provisoire.append(piece)
		elif src_zone==self.grille and dst_zone==self.chevalet:
			# Déplacement de la grille vers la zone de chevalet
			self.grille[src_idx[1]][src_idx[0]] = ""
			del self.provisoire[self.provisoire.index(piece)]
			self.chevalet[dst_idx[1]][dst_idx[0]] = piece
		elif src_zone==self.chevalet and dst_zone==self.chevalet:
			# Déplacement dans la zone de chevalet
			self.chevalet[src_idx[1]][src_idx[0]] = None
			self.chevalet[dst_idx[1]][dst_idx[0]] = piece
		else: # Déplacement dans la grille
			self.grille[src_idx[1]][src_idx[0]] = ""
			self.grille[dst_idx[1]][dst_idx[0]] = piece.char
		piece.pos = destination

		return True

	def validation(self):
		msg = ""

		# Vérifier qu'une pièce a été posée
		if len(self.provisoire)==0:
			return (False, "Aucune pièce n'a été placée sur le jeu")

		# Déterminer la direction principale
		x, y = 0,0
		horizontal = True
		vertical = True
		xmin, xmax, ymin, ymax =15, 0, 15, 0
		for i in range(len(self.provisoire)):
			zone, c, b = self.get_cell_info(self.provisoire[i].pos)
			if i==0:
				x, y = c[0], c[1]
				xmin, xmax, ymin, ymax = x, x, y, y
			else:
				if c[0]!=x:
					vertical = False
					if c[0]<xmin: xmin=c[0]
					if c[0]>xmax: xmax=c[0]
				if c[1]!=y:
					horizontal = False
					if c[1]<ymin: ymin=c[1]
					if c[1]>ymax: ymax=c[1]
		if not(horizontal) and not(vertical): # Mot invalide
			return (False, "Le nouveau mot n'est ni vertical ni horizontal")
		if horizontal and vertical: # 1 seule lettre posée
			# Trouver l'orientation grâce au contexte
			if (xmin>0 and self.grille[ymin][xmin-1]!='') or (xmin<14 and self.grille[ymin][xmin+1]!=''):
				horizontal = True
			elif (ymin>0 and self.grille[ymin-1][xmin]!='') or (ymin<14 and self.grille[ymin+1][xmin]!=''):
				vertical = True
			else:
				return (False, "La lettre en " + self.get_cell_name(xmin, ymin) + ' ne peut être isolée')
		
		# Vérifier la position du mot
		if self.tour_jeu == 1:
			positionOK = False
			for p in self.provisoire:
				if p.pos == "H8":
					positionOK = True
			if not(positionOK):
				return (False, "Le premier mot ne passe pas par la case H8")

		if horizontal:
			msg_h = ''

			res = self.identifier_mot_horizontal(xmin,ymin)
			self.score += res[1]
			msg_h += res[0]+' : '+ str(res[1]) + ' points'

			# Identifier les mots verticaux supplémentaires
			for l in self.provisoire:
				zone, c, busy = self.get_cell_info(l.pos)
				res = self.identifier_mot_vertical(c[0], c[1])
				if res[1] != 0:
					self.score += res[1]
					msg_h += ', ' + res[0]+' : '+ str(res[1]) + ' points'

			return (True, msg_h)


		elif vertical:
			msg_v = ''

			res = self.identifier_mot_vertical(xmin,ymin)
			self.score += res[1]
			msg_v += res[0]+' : '+ str(res[1]) + ' points'

			# Identifier les mots verticaux supplémentaires
			for l in self.provisoire:
				zone, c, busy = self.get_cell_info(l.pos)
				res = self.identifier_mot_horizontal(c[0], c[1])
				if res[1] != 0:
					self.score += res[1]
					msg_v += ', ' + res[0]+' : '+ str(res[1]) + ' points'

			return (True, msg_v)

		else:
			return (False, 'Direction de placement non reconnue')

		scrabble = len(self.provisoire)==7

		return (True, msg)

	def identifier_mot_horizontal(self, x, y):
		# Extension à gauche
		xmin = x
		while xmin>=0 and self.grille[y][xmin]!="": xmin -= 1
		xmin += 1 
		# Extension à droite
		xmax = x
		while xmax>=0 and self.grille[y][xmax]!="": xmax += 1
		xmax -= 1

		# Mot d'une lettre (ne pas considérer)
		if xmin == xmax: return ('', 0)

		for x in range(xmin, xmax+1):
			if self.grille[y][x]=='':
				return (False, "Le mot ne doit pas comporter d'espace")

		# Lire le mot et comptabiliser les points
		mot = [' ' for x in range(xmin, xmax+1)]
		points = 0
		bonus_mot = 1
		for x in range(xmin, xmax+1):
			bonus_lettre = 1

			cell_name = self.get_cell_name(x, y)
			mot[x-xmin] = self.grille[y][x]
			
			point_lettre = (Lettre.alphabet[str(mot[x-xmin])])[1]

			nouvelle_lettre = False
			for l in self.provisoire:
				if l.pos == cell_name:
					nouvelle_lettre = True
					break
			if nouvelle_lettre: # prendre en compte le bonus
				bonus_lettre, bm = self.get_bonus(x, y)
				bonus_mot *= bm
			points += point_lettre * bonus_lettre
		points *= bonus_mot

		return (''.join(mot), points)

	def identifier_mot_vertical(self, x, y):
		# Extension à gauche
		ymin = y
		while ymin>=0 and self.grille[ymin][x]!='': ymin -= 1
		ymin += 1 
		# Extension à droite
		ymax = y
		while ymax>=0 and self.grille[ymax][x]!='': ymax += 1
		ymax -= 1

		# Mot d'une lettre (ne pas considérer)
		if ymin == ymax: return ('', 0)

		for y in range(ymin, ymax+1):
			if self.grille[y][x]=='':
				return (False, "Le mot ne doit pas comporter d'espace")

		# Lire le mot et comptabiliser les points
		mot = [' ' for y in range(ymin, ymax+1)]
		points = 0
		bonus_mot = 1
		for y in range(ymin, ymax+1):
			bonus_lettre = 1

			cell_name = self.get_cell_name(x, y)
			mot[y-ymin] = self.grille[y][x]

			point_lettre = (Lettre.alphabet[str(mot[y-ymin])])[1]

			nouvelle_lettre = False
			for l in self.provisoire:
				if l.pos == cell_name:
					nouvelle_lettre = True
					break
			if nouvelle_lettre: # prendre en compte le bonus
				bonus_lettre, bm = self.get_bonus(x, y)
				bonus_mot *= bm
			points += point_lettre * bonus_lettre
		points *= bonus_mot

		return (''.join(mot), points)

	def get_bonus(self, x, y):
		bonus_lettre, bonus_mot = 1, 1

		if self.grille_bonus[y][x]=="MT":
			bonus_mot *= 3
		elif self.grille_bonus[y][x]=="MD" or self.grille_bonus[x][y]=="DP":
			bonus_mot *= 2
		elif self.grille_bonus[y][x]=="LT":
			bonus_lettre *= 3
		elif self.grille_bonus[y][x]=="LD":
			bonus_lettre *= 2
		return (bonus_lettre, bonus_mot)

