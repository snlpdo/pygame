import random
import time
import pygame

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

    def __init__(self, args, reseau):
        """ Contruire un nouveau jeu original ou chargé depuis un fichier de 
        sauvegarde. """

        # Pioche commune
        self.pioche = Lettre.get_pioche()

        # Valeur par défaut
        self.grille = [ ["" for x in range(15)] for y in range(15)] # Grille vide
        self.joueur_local = 1
        self.joueur_actuel = 1 
        self.partie_finie = False
        self.tour_jeu = 1

        # Charger un fichier ?
        if args.input!=None: 
            self.__charger_fichier(args, reseau)
        else: # créer uniquement les joueurs
            self.joueurs = [Joueur() for i in range(args.nombre_joueurs)]
            for i, joueur in enumerate(self.joueurs):
                joueur.pseudo = args.pseudo + str(i+1)

        # Partie réseau ?
        if reseau!=None:
            for i in range(4):
                # Envoi pseudo
                if i==0 and args.serveur or i==1 and not(args.serveur): 
                    reseau.envoyer('pseudo', args.pseudo)

                # Réception pseudo
                elif i==1 and args.serveur or i==0 and not(args.serveur): 
                    param, remote_pseudo = reseau.recevoir(128)
                    if param!='pseudo':
                        print('Reçu paramètre ' + param + ' au lieu de pseudo')
                        quit()

                # Envoi nombre aléatoire
                elif i==2 and args.serveur or i==3 and not(args.serveur): 
                    if args.serveur and args.input: # Pour le serveur
                        if self.joueur_actuel==self.joueur_local:
                            local_rand = 1.5 # prise de la main par le serveur
                        else:
                            local_rand = -0.5 # prise de la main par l'adversaire
                    else: # Pour le client
                        local_rand = random.random() # prise de la main aléatoire
                    reseau.envoyer('priority', str(local_rand))

                # Réception nombre aléatoire
                elif i==3 and args.serveur or i==2 and not(args.serveur): 
                    param, remote_rand = reseau.recevoir(128)
                    if param != 'priority' : 
                        print('Reçu paramètre '+param+' au lieu de priority')
                        quit()
                    remote_rand = float(remote_rand)

            if args.serveur: 
                # Envoi de:
                # - la grille, 
                # - le numéro de joueur de l'adversaire
                # - des chevalets des 2 joueurs (dans l'ordre)
                # - des scores des 2 joueurs (dans l'ordre)
                # - du numéro de tour de jeu
                msg = []
                for i in range(15):
                    for j in range(15):
                        if self.grille[i][j]=='':
                            msg.append(' ')
                        elif self.grille[i][j]==' ':
                            msg.append('?')
                        else:
                            msg.append(self.grille[i][j])
                num_adversaire = (self.joueur_local%2)+1
                ch1 = [ l.char for l in self.joueurs[0].chevalet[0] if l!=None ]
                ch2 = [ l.char for l in self.joueurs[1].chevalet[0] if l!=None ]

                reseau.envoyer_multiple(['grille', 'numero', 'ch1', 'ch2', 
                    'sc1', 'sc2', 'tour'], 
                    [''.join(msg), str(num_adversaire),''.join(ch1),''.join(ch2), 
                     str(self.joueurs[0].score), str(self.joueurs[1].score), 
                     str(self.tour_jeu)])

                reseau.recevoir(64) # attendre l'ack du client

            else: # client
                # Réception de la grille et du numéro de joueur à utiliser
                messages = reseau.reception_multiple()

                for message in messages:
                    message = message.split('=')

                    if message[0]=='grille':
                        rgrille = message[1]
                        for idx in range(15*15):
                            j = idx%15
                            i = idx//15
                            if rgrille[idx]=='?':
                                self.grille[i][j] = ' '
                            elif rgrille[idx]==' ':
                                self.grille[i][j] = ''
                            else:
                                self.grille[i][j] = rgrille[idx]

                            if self.grille[i][j] != '': # affecter au 1er joueur
                                lettre = self.creer_lettre(self.grille[i][j])
                                lettre.pos = self.get_cell_name(j, i)
                                # L'attribuer arbitrairement au 1er joueur
                                self.joueurs[0].provisoire.append(lettre)

                    elif message[0]=='numero': # ĺe numéro du joueur local
                        self.joueur_local = int(message[1])
                        num_adversaire = (self.joueur_local%2)+1

                    elif message[0][:2]=='ch': # Un chevalet
                        num = int(message[0][2:])
                        for i, l in enumerate(message[1]):
                            lettre = self.creer_lettre(l)
                            lettre.pos = 'Q' + str(4+i)
                            self.joueurs[num-1].chevalet[0][i] = lettre

                    elif message[0][:2]=='sc': # Un score
                        num = int(message[0][2:])
                        self.joueurs[num-1].score = int(message[1])

                    elif message[0]=='tour':
                        self.tour_jeu = int(message[1])

                reseau.envoyer('PRET', '')

            # Modification des pseudos
            self.joueurs[self.joueur_local-1].pseudo = args.pseudo
            self.joueurs[num_adversaire-1].pseudo = remote_pseudo

            # Détermination du 1er joueur (tirage au sort le plus grand)
            if local_rand > remote_rand:
                self.joueur_actuel = self.joueur_local
                print('Je joue en premier')
            else:
                self.joueur_actuel = (self.joueur_local%2)+1
                print('Je joue en second')

            if self.joueurs[self.joueur_local-1].pseudo==self.joueurs[num_adversaire-1].pseudo:
                self.joueurs[0].pseudo += '1'
                self.joueurs[1].pseudo += '2'

    def debuter_partie(self, reseau, plateau):
        if reseau != None: 
            reseau.demarrer_ecoute(self, plateau)

            # En mode réseau, il ne faut tirer au sort que les lettres du joueur local
            # et les envoyer à l'adversaire
            for i in range(2): # Action en 2 temps
                if i==0 and self.joueur_actuel==self.joueur_local \
                  or i==1 and not(self.joueur_actuel==self.joueur_local):
                    # Tirer au sort le chevalet 
                    tirage = self.completer_chevalet(i+1, False)
                    # Envoyer à l'adversaire
                    reseau.envoyer('tirage' , ''.join(tirage))
                else:
                    # Récupérer le tirage de l'adversaire
                    param, tirage = reseau.recevoir(128)
                    if param != 'tirage':
                        print("Reçu paramètre "+param+" au lieu de tirage")
                        quit()
                    self.affecter_tirage(i+1, tirage, False)
        else: # Completer le chevalet de tous les joueurs
            for i in range(len(self.joueurs)):
                self.completer_chevalet(i+1, False)

    def __charger_fichier(self, args, reseau):
        """ Charger une partie depuis un fichier. """
 
        # ouvrir le fichier
        input = open(args.input, "r") 

        # Numéro de tour du jeu
        self.tour_jeu = int(input.readline())

        # Nombre de joueurs
        nb_joueurs = int(input.readline())
        self.joueurs = [Joueur() for i in range(nb_joueurs)]
        if reseau!=None and nb_joueurs!=2:
            print('Nombre de joueurs ({}) invalide en mode réseau'.format(nb_joueurs))
            jeu.partie_finie = True
            pygame.quit()
            quit()

        # Numéro du joueur dont c'est le tour
        self.joueur_actuel = int(input.readline())

        # Numéro du joueur local
        self.joueur_local = int(input.readline())
        if reseau==None:
            self.joueur_local = self.joueur_actuel

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

        # Pseudos, scores et chevalets des joueurs
        for joueur in self.joueurs:
            joueur.pseudo = input.readline().rstrip()

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

        # Joueur local
        out.write(str(self.joueur_local) + '\n')

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
            out.write(j.pseudo+'\n')
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

    def creer_lettre(self, c):
        """ Créer l'objet Lettre correspondant au caractère c et enlever
        cette lettre de la pioche. """

        # Joker
        if c=='?': c=' '

        # Supprimer de la pioche
        del self.pioche[self.pioche.index(c)]

        return Lettre(c)

    def terminer_partie(self):
        # Décrémenter tous les scores avec les lettres restantes
        for j in self.joueurs:
            for l in j.chevalet[0]:
                if l!=None: j.score -= (Lettre.alphabet[l.char])[1]
        self.partie_finie = True

    def completer_chevalet(self, jnum, incr_tour=True):
        """ Tirer au sort les lettres d'un joueur spécifique. """

        tirage = [] # mémoire du tirage

        # joueur concerné
        joueur = self.joueurs[jnum-1] 
        joueur.provisoire = [] # Supprimer les pièces en attente

        # Nombre pièces initiales sur le chevalet
        compte = self.taille_chevalet(joueur)

        # Vérifier si la partie est finie
        if compte==0 and len(self.pioche)==0: # Fin
            self.terminer_partie()
            return "##FIN##"

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
                elif self.grille[i][j]==' ':
                    s += '?|'
                else:
                    s += self.grille[i][j] + '|'
            s += '\n ' + '-'*31 + '\n'
        s += '\n'

        # Score et chevalet de chaque joueur
        for j in self.joueurs:
            s += '\n' + j.pseudo +', score: ' + str(j.score) + '\n'
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
            self.joueurs[jnum-1].chevalet[i][j] = None
        else: # zone de jeu
            i = LIGNES.index(cell_name[0])
            j = int(cell_name[1:])-1
            self.grille[i][j] == ''

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

    def __dir_principale_horizontale(self, jnum):
        """ Identifier la direction selon laquelle le joueur a placé
        ses lettres. """

        joueur = self.joueurs[jnum-1] # joueur à considérer

        # Déterminer les coordonnées de la ligne englobant les lettres
        x, y = 0,0
        xmin, xmax, ymin, ymax =15, 0, 15, 0
        for i, lettre in enumerate(joueur.provisoire):
            zone, c, b = self.get_cell_info(jnum, lettre.pos)
            if i==0: # valeurs initiales
                x, y = c[0], c[1]
                xmin, xmax, ymin, ymax = x, x, y, y

            if c[0]!=x: # Nouvelle valeur de x
                if c[0]<xmin: xmin=c[0]
                if c[0]>xmax: xmax=c[0]
            if c[1]!=y: # Nouvelle valeur de y
                if c[1]<ymin: ymin=c[1]
                if c[1]>ymax: ymax=c[1]

        if xmin==xmax and ymin!=ymax: # vertical
            return (False, xmin,xmax,ymin,ymax)
        elif xmin!=xmax and ymin==ymax: # horizontal
            return (True, xmin,xmax,ymin,ymax)
        elif xmin!=xmax and ymin!=ymax: # invalide (lettres non juxtaposées)
            return (None, xmin,xmax,ymin,ymax)
        else: # 1 seule lettre posée
            # Trouver l'orientation grâce au contexte
            if (xmin>0 and self.grille[ymin][xmin-1]!='') or (xmin<14 and self.grille[ymin][xmin+1]!=''):
                # Lettre à gauche ou à droite sur le jeu: horizontal
                return (True, xmin,xmax,ymin,ymax)
            elif (ymin>0 and self.grille[ymin-1][xmin]!='') or (ymin<14 and self.grille[ymin+1][xmin]!=''):
                # Lettre au dessous ou au dessus sur le jeu: vertical
                return (False, xmin,xmax,ymin,ymax)
            else:
                return (None, xmin,xmax,ymin,ymax) # invalide (lettre isolée)

    def verifier(self):
        joueur = self.joueurs[self.joueur_actuel-1]

        if len(joueur.provisoire)==0: return (0, 'Aucune lettre') # aucune lettre

        # Direction principale
        mot_principal_horizontal,xmin,xmax,ymin,ymax = self.__dir_principale_horizontale(self.joueur_actuel)
        if mot_principal_horizontal == None:
            return (0, 'Coup invalide')

        # Comptabiliser les points
        total = 0
        mots = []
        if mot_principal_horizontal:
            # Vérifier le mot principal horizontal
            res = self.identifier_mot(True,xmin,xmax,ymin,ymax,joueur)
            if res[0]==0: return (0, res[1])
            total += res[0]
            mots = [res[1]]

            # Vérifier l'existance de mots secondaires 
            for l in joueur.provisoire:
                zone, c, busy = self.get_cell_info(self.joueur_actuel, l.pos)
                res = self.identifier_mot(False,c[0],c[0],c[1],c[1],joueur)
                total += res[0]
                if res[0] != 0: mots.append(res[1])

        else: # Vérifier le mot principal vertical
            res = self.identifier_mot(False,xmin,xmax,ymin,ymax,joueur)
            if res[0]==0: return (0, res[1])
            total += res[0]
            mots = [res[1]]

            # Vérifier l'existance de mots secondaires 
            for l in joueur.provisoire:
                zone, c, busy = self.get_cell_info(self.joueur_actuel, l.pos)
                res = self.identifier_mot(True,c[0],c[0],c[1],c[1],joueur)
                total += res[0]
                if res[0] != 0: mots.append(res[1])

        if self.tour_jeu == 1: # Le premier mot doit recouvrir la case H8
            positionOK = False
            for p in joueur.provisoire:
                if p.pos == "H8": positionOK = True
            if not(positionOK):
                return (0, "Le premier mot doit recouvrir la case H8")
        else: # Le mot ne doit pas être isolé
            if len(mots)==1 and len(mots[0])==len(joueur.provisoire):
              return (0, "Le mot ne peut être isolé du reste du jeu")

        # Détection d'un scrabble
        scrabble = len(joueur.provisoire)==7
        if scrabble: total += 50

        return (total, ','.join(mots))

    def valider(self, jnum):
        score, info = self.verifier()

        if score==0: # Coup invalide
            return (False, info) 
        else: # OK
            joueur = self.joueurs[jnum-1]
            joueur.score += score
            return (True, 'mot(s): ' + info)

    def identifier_mot(self, horizontal, xmin, xmax, ymin, ymax, joueur):
        """ Identifier un mot selon une direction et un rectangle donnés. """

        mot = []
        points = 0
        bonus_mot = 1 # valeur par défaut
        if horizontal: # Mot horizontal
            # Étendre à gauche
            while xmin>=0 and self.grille[ymin][xmin]!='': xmin-=1
            xmin += 1
            # Étendre à droite
            while xmax<15 and self.grille[ymin][xmax]!='': xmax+=1
            xmax -= 1

            # Mot d'une lettre
            if xmin==xmax: return (0, "Mot d'une seule lettre.")

            # Lire le mot et compter les points
            for x in range(xmin,xmax+1):
                c = self.grille[ymin][x] 
                if c=='': return (0,"Mot avec un espace")

                mot.append(c)

                points_lettre = (Lettre.alphabet[c])[1]

                cell_name = self.get_cell_name(x, ymin)
                lettre_provisoire = False
                for l in joueur.provisoire:
                    if l.pos == cell_name:
                        lettre_provisoire = True
                        break

                bonus_lettre = 1
                if lettre_provisoire: # prendre en compte le bonus
                    bonus_lettre, bm = self.get_bonus(x, ymin)
                    bonus_mot *= bm
                points += points_lettre * bonus_lettre
        else: # Mot vertical
            # Étendre en haut
            while ymin>=0 and self.grille[ymin][xmin]!='': ymin-=1
            ymin += 1
            # Étendre à droite
            while ymax<15 and self.grille[ymax][xmin]!='': ymax+=1
            ymax -= 1

            # Mot d'une lettre
            if ymin==ymax: return (0, "Mot d'une seule lettre.")

            # Lire le mot et compter les points
            for y in range(ymin,ymax+1):
                c = self.grille[y][xmin] 
                if c=='': return (0,"Mot avec un espace")

                mot.append(c)

                points_lettre = (Lettre.alphabet[c])[1]

                cell_name = self.get_cell_name(xmin, y)
                lettre_provisoire = False
                for l in joueur.provisoire:
                    if l.pos == cell_name:
                        lettre_provisoire = True
                        break

                bonus_lettre = 1
                if lettre_provisoire: # prendre en compte le bonus
                    bonus_lettre, bm = self.get_bonus(xmin, y)
                    bonus_mot *= bm
                points += points_lettre * bonus_lettre

        points *= bonus_mot
        return (points,  ''.join(mot))

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

    def vainqueur(self):
        id_max = 0
        for i in range(len(self.joueurs)):
            if self.joueurs[i].score > self.joueurs[id_max].score:
                id_max = i
        return id_max+1

