import random
import time

from joueur import *
from lettre import *
from reseau import Reseau

LIGNES = "ABCDEFGHIJKLMNO"

class Jeu():

	grille_bonus = [
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

	def __init__(self, args, plateau, reseau):
		""" Contruire un nouveau jeu original ou chargé depuis un fichier de 
		sauvegarde. """

		self.grille = [ ["" for x in range(15)] for y in range(15)] # Grille vide
		self.pioche = Lettre.get_pioche() # Pioche globale

		self.joueur_actuel = 1
		self.joueur_local = 1

		if reseau!=None and not(reseau.premier_joueur):
			self.joueur_local=2

		if args.input==None or reseau!=None: # Nouvelle partie
			self.tour_jeu = 1
			self.joueurs = [Joueur() for i in range(args.nombre_joueurs)]
		else:
			########################################
			# Charger une partie depuis un fichier #
			########################################
			input = open(args.input, "r")

			# Numéro de tour du jeu
			self.tour_jeu = int(input.readline())

			# Nombre de joueurs
			nb_joueurs = int(input.readline()) 
			self.joueurs = [Joueur() for i in range(nb_joueurs)]

			# Joueur dont c'est le tour
			self.joueur_actuel = int(input.readline())

			# Contenu de la grille: créer les lettres correspondantes,
			# les enlever de la pioche et les affecter arbitrairement
			# au premier joueur (pour validation plateau)
			for i in range(15): 
				ligne = input.readline()
				for j in range(15):
					if ligne[j] == ' ': # cellule vide
						self.grille[i][j] = ''
					else: # cellule occupée
						lettre = self.creer_lettre(ligne[j])
						# Placer la lettre sur le jeu
						self.grille[i][j] = lettre.char 
						lettre.pos = self.get_cell_name(j, i)
						# L'attribuer arbitrairement au 1er joueur
						self.joueurs[0].provisoire.append(lettre)
			# validation plateau des lettres déjà posées
			plateau.validation(self.joueurs[0])

			# Scores et chevalets des joueurs
			for joueur in self.joueurs:
				# lecture du score
				joueur.score = int(input.readline())
				
				# lecture des lettres du chevalet: créer les lettres
				# correspondantes, les enlever de la pioche et les placer
				# sur le chevalet
				ligne = input.readline()
				for j in range(len(ligne)-1): # ne pas lire \n
					lettre = self.creer_lettre(ligne[j])
					lettre.pos = 'Q' + str(j+4) # ajouter sur le chevalet
					joueur.chevalet[0][j] = lettre

			input.close()

	def creer_lettre(self, c):
		""" Créer l'objet Lettre correspondant au caractère c et enlever
		cette lettre de la pioche. """

		# Joker
		if c=='?': c=' '

		# Supprimer de la pioche
		del self.pioche[self.pioche.index(c)]

		return Lettre(c)


	def sauvegarder(self):
		""" Sauvegarder la partie courant dans un fichier avec dénomé en 
		fonction de l'horodate du moment."""

		# Nom du fichier
		filename = time.strftime("%Y%m%d-%H%M.sav", time.gmtime())

		out = open(filename, 'w')

		# tour de jeu
		out.write(str(self.tour_jeu)+'\n')

		# Nombre de joueurs
		out.write(str(len(self.joueurs)) + '\n')

		# Joueur courant
		out.write(str(self.joueur_actuel) + '\n')

		# Grille
		for i in range(15):
			for j in range(15):
				if self.grille[i][j] == '':
					out.write(' ')
				elif self.grille[i][j]== ' ':
					out.write('?')
				else:	
					out.write(str(self.grille[i][j]))
			out.write('\n')

		# Chaque joueur: score puis chevalet + lettres placées
		for j in self.joueurs:
			out.write(str(j.score)+'\n')
			for l in j.chevalet[0]:
				if l!=None: 
					if l.char==' ': out.write('?')
					else: out.write(l.char)
			for l in j.provisoire:
				if l!=None: 
					if l.char==' ': out.write('?')
					else: out.write(l.char)
			out.write('\n')

		out.write('\n')
		out.close()

		return filename

	def tirer_au_sort(self, jnum, incr_tour=True):
		""" Tirer au sort les lettres d'un joueur spécifique. """

		tirage = [] # mémoire du tirage

		# joueur concerné
		joueur = self.joueurs[jnum-1] 
		joueur.provisoire = [] # Supprimer les pièces en attente

		# Nombre pièces initiales sur le chevalet
		compte = self.taille_chevalet(joueur)

		# Remplir le chevalet
		while compte<7 and len(self.pioche)>0:
			# Retirer une lettre de la pioche
			random.shuffle(self.pioche)
			c = self.pioche.pop() 

			# Créer la lettre 
			lettre = Lettre(c)

			# Mémoriser progressivement le tirage
			tirage.append(c) 

			# Ajouter au chevalet
			self.ajouter_chevalet(joueur, lettre)

			# Comptabiliser le nombre de lettre sur le chevalet
			compte = self.taille_chevalet(joueur)

		# Tour suivant
		if incr_tour:
			self.tour_jeu += 1
			self.joueur_actuel += 1
			if self.joueur_actuel>len(self.joueurs): self.joueur_actuel=1

		return tirage

	def taille_chevalet(self, joueur):
		""" Comptabiliser le nombre de cases occupées sur le chevalet
		du joueur. """

		nombre = 0
		for l in joueur.chevalet[0]:
			if l!=None: nombre += 1
		return nombre

	def ajouter_chevalet(self, joueur, lettre):
		""" Poser une lettre sur la première case libre du chevalet du joueur """		

		# Trouver la première case vide
		i=0
		while joueur.chevalet[0][i]!=None: i += 1

		# Poser la lettre à cette place
		lettre.pos = 'Q' + str(i+4)
		joueur.chevalet[0][i] = lettre

		# Comptabiliser le nombre de lettre sur le chevalet
		compte = self.taille_chevalet(joueur)

	def affecter_tirage(self, jnum, tirage, incr_tour=True):
		""" Attribuer le résultat d'un tirage au chevalet d'un joueur. """

		joueur = self.joueurs[jnum-1] 
		joueur.provisoire = [] # Supprimer les pièces en attente

		for c in tirage:
			self.ajouter_chevalet(joueur, self.creer_lettre(c))

		# Tour suivant
		if incr_tour:
			self.tour_jeu += 1
			self.joueur_actuel += 1
			if self.joueur_actuel>len(self.joueurs): self.joueur_actuel=1

	def __str__(self):
		""" État actuel du jeu dans une chaîne de caractères """

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

		# Score et chevalet de chaque joueur
		for j in self.joueurs:
			s += '\nJoueur '+ str(j.num) +', score: ' + str(j.score) + '\n'
			s += '   ' + '-'*(2+len(j.chevalet[0])) + '\n'
			s += '   |'
			for i in range(len(j.chevalet[0])):
				if j.chevalet[0][i]==None:
					s += ' '
				else:
					s += j.chevalet[0][i].char
			s += '|\n'
			s += '   ' + '-'*(2+len(j.chevalet[0])) + '\n'

		# Joueur courant:
		s += '\n Joueur courant: ' + str(self.joueur_actuel)

		return s

	def get_cell_name(self, x, y):
		""" Fournir le label d'une cellule à partir de ses 
		coordonnées/indexes (x,y)"""

		return LIGNES[y] + str(x+1)

	def get_cell_info(self, jnum, cell_name):
		""" Fournir les coordonnées et l'état d'une cellule visible (grille ou
		chevalet du joueur courant) depuis son label. """ 

		if cell_name[0]=='Q': # Chevalet du joueur courant
			joueur = self.joueurs[jnum-1]
			i = 0
			j = int(cell_name[1:])-4
			if joueur.chevalet[i][j]==None:
				return (joueur.chevalet, (j,i), False)
			else:
				return (joueur.chevalet, (j, i), True)
		else: # zone de jeu
			i = LIGNES.index(cell_name[0])
			j = int(cell_name[1:])-1
			if self.grille[i][j] == "":
				return (self.grille, (j,i), False)
			else:
				return (self.grille, (j, i), True)

	def free_cell(self, jnum, cell_name):
		""" Réinitialisation une cellule visible (grille ou 
		chevalet du joueur courant)"""

		if cell_name[0]=='Q': # zone de chevalet
			i = 0
			j = int(cell_name[1:])-4
			self.joueurs[jnum-1].chevalet[i][j]=None
		else: # zone de jeu
			i = LIGNES.index(cell_name[0])
			j = int(cell_name[1:])-1
			self.grille[i][j] == ""

	def deplacer_piece(self, jnum, destination, piece, force=False):
		""" Déplacer une pièce sur le jeur (grille ou
		chevalet du joueur courant). """

		dst_zone, dst_idx, dst_busy = self.get_cell_info(jnum, destination)
		src_zone, src_idx, src_busy = self.get_cell_info(jnum, piece.pos)

		joueur = self.joueurs[jnum-1]

		if src_zone==joueur.chevalet and dst_zone==self.grille: # Chevalet vers grille
			if not(force) and self.joueur_local != self.joueur_actuel:
				return False

			if dst_busy: return False # destination occupée

			self.free_cell(jnum, piece.pos) # libérer ancienne place

			# Nouvelle piece en placement provisoire
			joueur.chevalet[src_idx[1]][src_idx[0]] = None
			self.grille[dst_idx[1]][dst_idx[0]] = piece.char
			joueur.provisoire.append(piece)
		elif src_zone==self.grille and dst_zone==joueur.chevalet: # Grille vers chevalet
			if not(force) and self.joueur_local != self.joueur_actuel:
				return False

			if dst_busy: return False # destination occupée

			self.free_cell(jnum, piece.pos) # libérer ancienne place

			# Déplacement de la grille vers la zone de chevalet
			self.grille[src_idx[1]][src_idx[0]] = ""
			del joueur.provisoire[joueur.provisoire.index(piece)]
			joueur.chevalet[dst_idx[1]][dst_idx[0]] = piece
		elif src_zone==joueur.chevalet and dst_zone==joueur.chevalet: # Dans le chevalet
			if dst_busy: # Échange des contenus
				joueur.chevalet[src_idx[1]][src_idx[0]].pos, joueur.chevalet[dst_idx[1]][dst_idx[0]].pos = \
				  joueur.chevalet[dst_idx[1]][dst_idx[0]].pos, joueur.chevalet[src_idx[1]][src_idx[0]].pos
				joueur.chevalet[src_idx[1]][src_idx[0]], joueur.chevalet[dst_idx[1]][dst_idx[0]] = \
				  joueur.chevalet[dst_idx[1]][dst_idx[0]], joueur.chevalet[src_idx[1]][src_idx[0]]
			else:
				self.free_cell(jnum, piece.pos) # libérer ancienne place
				joueur.chevalet[src_idx[1]][src_idx[0]] = None
				joueur.chevalet[dst_idx[1]][dst_idx[0]] = piece
		else: # Déplacement dans la grille
			if not(force) and self.joueur_local != self.joueur_actuel:
				return False

			if dst_busy: return False # destination occupée

			self.free_cell(jnum, piece.pos) # libérer ancienne place

			self.grille[src_idx[1]][src_idx[0]] = ""
			self.grille[dst_idx[1]][dst_idx[0]] = piece.char
		
		piece.pos = destination
		return True

	def __dir_principale(self, jnum):
		joueur = self.joueurs[jnum-1]

		# Déterminer la direction principale
		x, y = 0,0
		horizontal = True
		vertical = True
		xmin, xmax, ymin, ymax =15, 0, 15, 0
		for i in range(len(joueur.provisoire)):
			zone, c, b = self.get_cell_info(jnum, joueur.provisoire[i].pos)
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

		return (horizontal, vertical, xmin, ymin, xmax, ymax)

	def compter_points(self):
		joueur = self.joueurs[self.joueur_actuel-1]

		if len(joueur.provisoire)==0: return 0 # aucune lettre

		# Direction principale
		horizontal, vertical, xmin, ymin, xmax, ymax = self.__dir_principale(self.joueur_actuel)
		if not(horizontal) and not(vertical): # Mot invalide
			return 0
		if horizontal and vertical: # 1 seule lettre posée
			# Trouver l'orientation grâce au contexte
			if (xmin>0 and self.grille[ymin][xmin-1]!='') or (xmin<14 and self.grille[ymin][xmin+1]!=''):
				horizontal = True
			elif (ymin>0 and self.grille[ymin-1][xmin]!='') or (ymin<14 and self.grille[ymin+1][xmin]!=''):
				vertical = True
			else:
				return 0
			
		# Vérifier la position du mot
		if self.tour_jeu == 1:
			positionOK = False
			for p in joueur.provisoire:
				if p.pos == "H8":
					positionOK = True
			if not(positionOK):
				return 0

		total = 0
		if horizontal:
			res = self.identifier_mot_horizontal(xmin,ymin, joueur)
		else:
			res = self.identifier_mot_vertical(xmin,ymin, joueur)
		total += res[1]

		# Identifier les mots perpendiculaires supplémentaires
		for l in joueur.provisoire:
			zone, c, busy = self.get_cell_info(self.joueur_actuel, l.pos)
			if horizontal:
				res = self.identifier_mot_vertical(c[0], c[1], joueur)
			else:
				res = self.identifier_mot_horizontal(c[0], c[1], joueur)
			if res[1] != 0:
				total += res[1]

		scrabble = len(joueur.provisoire)==7
		if scrabble: 
			total.score += 50

		return total


	def validation(self, jnum):
		""" Vérifier que le coup du joueur courant est valide.
		Actuellement, aucune vérification du/des mot(s) dans
		une dictionnaire n'est réalisée. """

		joueur = self.joueurs[jnum-1]

		# Vérifier qu'une pièce a été posée
		if len(joueur.provisoire)==0:
			return (False, "Aucune pièce n'a été placée sur le jeu")

		# Déterminer la direction principale
		horizontal, vertical, xmin, ymin, xmax, ymax = self.__dir_principale(jnum)
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
			for p in joueur.provisoire:
				if p.pos == "H8":
					positionOK = True
			if not(positionOK):
				return (False, "Le premier mot ne passe pas par la case H8")

		msg = ''
		if horizontal:
			res = self.identifier_mot_horizontal(xmin,ymin, joueur)
		else:
			res = self.identifier_mot_vertical(xmin,ymin, joueur)
		joueur.score += res[1]
		msg += res[0]+' : '+ str(res[1]) + ' points'

		# Identifier les mots perpendiculaires supplémentaires
		for l in joueur.provisoire:
			zone, c, busy = self.get_cell_info(jnum, l.pos)
			if horizontal:
				res = self.identifier_mot_vertical(c[0], c[1], joueur)
			else:
				res = self.identifier_mot_horizontal(c[0], c[1], joueur)
			if res[1] != 0:
				joueur.score += res[1]
				msg += ', ' + res[0]+' : '+ str(res[1]) + ' points'

		scrabble = len(joueur.provisoire)==7
		if scrabble: 
			joueur.score += 50
			msg = 'SCRABBLE (50 points): ' + msg

		return (True, msg)

	def identifier_mot_horizontal(self, x, y, joueur):
		""" Identifier un mot horizontal créé par le joueur
		courant à partir d'une position donnée. """

		# Extension à gauche
		xmin = x
		while xmin>=0 and self.grille[y][xmin]!="": xmin -= 1
		xmin += 1 
		# Extension à droite
		xmax = x
		while xmax>=0 and self.grille[y][xmax]!="": xmax += 1
		xmax -= 1

		# Ne pas considérer les mots d'une seule lettre
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
			for l in joueur.provisoire:
				if l.pos == cell_name:
					nouvelle_lettre = True
					break
			if nouvelle_lettre: # prendre en compte le bonus
				bonus_lettre, bm = self.get_bonus(x, y)
				bonus_mot *= bm
			points += point_lettre * bonus_lettre
		points *= bonus_mot

		return (''.join(mot), points)

	def identifier_mot_vertical(self, x, y, joueur):
		""" Identifier un mot vertical créé par le joueur courant
		à partir d'une position donnée. """

		# Extension à gauche
		ymin = y
		while ymin>=0 and self.grille[ymin][x]!='': ymin -= 1
		ymin += 1 
		# Extension à droite
		ymax = y
		while ymax>=0 and self.grille[ymax][x]!='': ymax += 1
		ymax -= 1

		# Ne pas considérer les mots d'une seule lettre
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
			for l in joueur.provisoire:
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
		""" Indiquer les bonus multiplicatifs pour la lettre ou
		pour le mot entier d'une cellule donnée. """

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

