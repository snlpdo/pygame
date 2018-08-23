import pygame
from math import cos, sin, pi

from lettre import *
from joueur import *
from button import Button

# Couleurs
NOIR = (0,0,0)
VERT = (0, 123, 0)
ROSE = (255, 182, 193)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 215)
CYAN = (50,200,200)
BLANC = (255, 255, 255)

TOP_MARGIN, RIGHT_MARGIN, BOTTOM_MARGIN, LEFT_MARGIN = 60, 50, 150, 50
LEGENDE_SEP = 15
LEGENDE_SIZE = 25
LIGNES = "ABCDEFGHIJKLMNOPQ"

NB_ROWS, NB_COLS = 15, 15

class Plateau():
    def __init__(self, screen, bonus):
        """ Construire un plateau aux bonnes dimensions en faisant
        apparaître les différentes cases bonus. 

        INPUT:
        screen: écran utilisé
        bonus: tableau 15x15 indiquant la position des cases bonus.
        """

        self.screen = screen

        self.wCell, self.hCell = 0, 0 # dimension d'une cellule
        self.x0, self.y0 = 0, 0 # origine du quadrillage
        self.tx0, self.ty0 = 0, 0 # origine du chevalet
        self.size = self.screen.get_size()
        self.img = self.__creer_image(bonus)
        self.piece_a_deplacer = None

        # Message temporaire
        self.message = ""
        self.msg_time_count = 0
        self.msg_type = "error"

        # Bouton de validation
        self.button = Button((LEFT_MARGIN + 13*self.wCell, 
            TOP_MARGIN + 16*self.hCell + 5))

    def __draw_bonus_cell(self, type_case, img, area):
        """ Dessine la case bonus appropriée sur une zone spécifique
        de l'image de fond du plateau. 

        INPUT:
        type_case: chaîne indiquant le type de bonus
        img: image de fond du plateau sur laquelle dessiner
        area: emplacement sur l'image où dessiner la case
        """

        x0, y0, w, h = area[0], area[1], area[2], area[3]
        t = .15*w, .1*w
        police = pygame.font.SysFont('comicsans', 12)
        
        if type_case=="DP":
            pygame.draw.rect(img, ROSE, area)
            r = [.4*w, .25*w] # 2 rayons
            poly = [[x0+w/2+r[i%2]*cos(i*pi/8),
                     y0+h/2+r[i%2]*sin(i*pi/8)] for i in range(16)]
            pygame.draw.polygon(img, NOIR, poly)
        elif type_case=="MD":
            pygame.draw.rect(img, ROSE, area)
            for dx in (w/2-w/4,w/2,w/2+w/4):
                for dy in (-t[0], h):
                    pygame.draw.rect(img, ROSE, (x0+dx-t[1]/2, y0+dy, t[1], t[0]))
                    pygame.draw.rect(img, ROSE, (x0+dy, y0+dx-t[1]/2, t[0], t[1]))
            text1 = police.render('MOT', True, NOIR)
            text2 = police.render('COMPTE', True, NOIR)
            text3 = police.render('DOUBLE', True, NOIR)
            img.blit(text1, (x0+w/2-text1.get_width()/2, y0+h/4-text1.get_height()/2))
            img.blit(text2, (x0+w/2-text2.get_width()/2, y0+h/2-text2.get_height()/2))
            img.blit(text3, (x0+w/2-text3.get_width()/2, y0+3*h/4-text3.get_height()/2))
        elif type_case=="MT":
            pygame.draw.rect(img, ROUGE, area)
            for dx in (w/2-w/4,w/2,w/2+w/4):
                for dy in (-t[0], h):
                    pygame.draw.rect(img, ROUGE, (x0+dx-t[1]/2, y0+dy, t[1], t[0]))
                    pygame.draw.rect(img, ROUGE, (x0+dy, y0+dx-t[1]/2, t[0], t[1]))
            text1 = police.render('MOT', True, NOIR)
            text2 = police.render('COMPTE', True, NOIR)
            text3 = police.render('TRIPLE', True, NOIR)
            img.blit(text1, (x0+w/2-text1.get_width()/2, y0+h/4-text1.get_height()/2))
            img.blit(text2, (x0+w/2-text2.get_width()/2, y0+h/2-text2.get_height()/2))
            img.blit(text3, (x0+w/2-text3.get_width()/2, y0+3*h/4-text3.get_height()/2))
        elif type_case=="LD":
            pygame.draw.rect(img, CYAN, area)
            for dx in (w/2-w/4,w/2,w/2+w/4):
                for dy in (-t[0], h):
                    pygame.draw.rect(img, CYAN, (x0+dx-t[1]/2, y0+dy, t[1], t[0]))
                    pygame.draw.rect(img, CYAN, (x0+dy, y0+dx-t[1]/2, t[0], t[1]))
            text1 = police.render('LETTRE', True, NOIR)
            text2 = police.render('COMPTE', True, NOIR)
            text3 = police.render('DOUBLE', True, NOIR)
            img.blit(text1, (x0+w/2-text1.get_width()/2, y0+h/4-text1.get_height()/2))
            img.blit(text2, (x0+w/2-text2.get_width()/2, y0+h/2-text2.get_height()/2))
            img.blit(text3, (x0+w/2-text3.get_width()/2, y0+3*h/4-text3.get_height()/2))
        elif type_case=="LT":
            pygame.draw.rect(img, BLEU, area)
            for dx in (w/2-w/4,w/2,w/2+w/4):
                for dy in (-t[0], h):
                    pygame.draw.rect(img, BLEU, (x0+dx-t[1]/2, y0+dy, t[1], t[0]))
                    pygame.draw.rect(img, BLEU, (x0+dy, y0+dx-t[1]/2, t[0], t[1]))
            text1 = police.render('LETTRE', True, NOIR)
            text2 = police.render('COMPTE', True, NOIR)
            text3 = police.render('TRIPLE', True, NOIR)
            img.blit(text1, (x0+w/2-text1.get_width()/2, y0+h/4-text1.get_height()/2))
            img.blit(text2, (x0+w/2-text2.get_width()/2, y0+h/2-text2.get_height()/2))
            img.blit(text3, (x0+w/2-text3.get_width()/2, y0+3*h/4-text3.get_height()/2))
            
    def __creer_image(self, bonus):
        """ Créé l'image de fond du plateau aux bonnes dimensions. Cette image
        contient initialement:
        * un arrière-plan blanc,
        * le quadrillage noir du jeu sur fond vert,
        * les légendes des lignes et colonnes,
        * les images des différentes cases bonus,
        * un chevalet pour le joueur (9 cases noires sur fond vert).

        INPUT:
        bonus: tableau 2D 15x15 indiquant la position des différentes cases bonus.
        """

        # Image aux bonnes dimensions
        b = pygame.Surface(self.size)
        b = b.convert()

        # Arrière-plan 
        b.fill(BLANC)

        # Dimension des cellules
        w, h = (self.size[0]-LEFT_MARGIN-RIGHT_MARGIN)//NB_COLS,\
               (self.size[1]-TOP_MARGIN-BOTTOM_MARGIN)//NB_ROWS

        # Plateau vert
        pygame.draw.rect(b, VERT, (LEFT_MARGIN, TOP_MARGIN, NB_COLS*w, NB_ROWS*h))

        # Cases spéciales
        y0 = TOP_MARGIN
        for i in range(NB_ROWS):
            x0 = LEFT_MARGIN
            for j in range(NB_COLS):
                self.__draw_bonus_cell(bonus[i][j],b,(x0, y0, w, h))
                x0 += w
            y0 += h

        # Légendes
        police = pygame.font.SysFont('comicsans', LEGENDE_SIZE)
        i = TOP_MARGIN + h//2
        j1 = LEFT_MARGIN - LEGENDE_SEP
        j2 = LEFT_MARGIN + NB_COLS*w + LEGENDE_SEP
        for idx in range(NB_ROWS):
            text = police.render(LIGNES[idx], True, NOIR)
            b.blit(text, (j1-text.get_width()/2, i-text.get_height()/2))
            b.blit(text, (j2-text.get_width()/2, i-text.get_height()/2))
            i += h
        i1 = TOP_MARGIN - LEGENDE_SEP
        i2 = TOP_MARGIN + NB_ROWS*h + LEGENDE_SEP
        j = LEFT_MARGIN + w//2
        for n in range(1,16):
            text = police.render(str(n), True, NOIR)
            b.blit(text, (j-text.get_width()/2, i1-text.get_height()/2))
            b.blit(text, (j-text.get_width()/2, i2-text.get_height()/2))
            j += w

        # Quadrillage noir
        for i in range(NB_ROWS):
            for j in range(NB_COLS):
                pygame.draw.rect(b, NOIR, (LEFT_MARGIN+w*i,TOP_MARGIN+h*j,w,h), 2)

        # Zone pour le joueur
        pygame.draw.rect(b, VERT, (LEFT_MARGIN+3*w-5,TOP_MARGIN+16*h-5,9*w+10,h+10))
        for i in range(9):
            pygame.draw.rect(b, NOIR, (LEFT_MARGIN+(3+i)*w,TOP_MARGIN+16*h,w,h), 2)

        # Mise à jour des attributs        
        self.wCell = w
        self.hCell = h
        self.x0 = LEFT_MARGIN
        self.y0 = TOP_MARGIN
        self.tx0 = LEFT_MARGIN+3*w
        self.ty0 = TOP_MARGIN+16*h

        return b

    def draw(self, jeu):
        """ Afficher le contenu du plateau: 
        - Arrière-plan
        - Chevalet du joueur local
        - Lettres sur le jeu en attente de validation
        - Lettre en cours de déplacement
        - État du jeu.
        """

        # Arrière-plan
        self.screen.blit(self.img, (0,0))

        # Lettres sur le chevalet du joueur local
        self.__afficher_lettres_chevalet(jeu)

        # Lettres du joueur actuel en placement provisoire
        self.__afficher_lettres_provisoires(jeu)

        # Lettre en cours de déplacement
        self.__afficher_deplacement()

        # Statistique
        self.__afficher_etat(jeu)

    def __afficher_lettres_chevalet(self, jeu):
        """ Dessiner les pièces du joueur local sur le chevalet
        en ajoutant un point bleu dans le coin supérieur gauche.
        """ 
        
        joueur = jeu.joueurs[jeu.joueur_local-1]

        font = pygame.font.SysFont('comicsans', 18)
        text = font.render(joueur.pseudo, True, NOIR)
        self.screen.blit(text, (LEFT_MARGIN+3*self.wCell,TOP_MARGIN+16*self.hCell-20))
        for l in joueur.chevalet[0]:
            if l != None and l != self.piece_a_deplacer:
                if l.img == None:
                    l.creer_image((self.wCell, self.hCell))
                x, y = self.get_cell_orig(l.pos)
                self.screen.blit(l.img, (x,y))
                pygame.draw.rect(self.screen, BLEU, (x+5,y+5, 5, 5))

    def __afficher_lettres_provisoires(self, jeu):
        """ Dessiner les pièces du joueur actuel en placement
        provisoire en ajoutant un point bleu ou rouge 
        dans le coin supérieur gauche selon qu'il s'agisse du joueur
        local ou non.
        """ 
        joueur = jeu.joueurs[jeu.joueur_actuel-1]

        for l in joueur.provisoire:
            if l != self.piece_a_deplacer:
                if l.img == None:
                    l.creer_image((self.wCell, self.hCell))
                x, y = self.get_cell_orig(l.pos)
                self.screen.blit(l.img, (x, y))
                if jeu.joueur_local == jeu.joueur_actuel:
                    couleur = BLEU
                else:
                    couleur = ROUGE
                pygame.draw.rect(self.screen, couleur, (x+5,y+5, 5, 5))

    def __afficher_etat(self, jeu):
        """ Afficher l'état du jeu (numéro du tour, nombre de lettres restantes,
        joueur dont c'est le tour) en haut de l'écran et les scores
        de tous les joueurs en bas de l'écran."""

        font = pygame.font.SysFont('comicsans', 24) # petite police
        fontG = pygame.font.SysFont('comicsans', 36) # grande police

        # Numéro du tour
        s = 'Tour: ' + str(jeu.tour_jeu) 

        # État de la pioche
        if len(jeu.pioche)>1:
            s += ' (' + str(len(jeu.pioche)) + ' lettres restantes)'
        else:
            s += ' (' + str(len(jeu.pioche)) + ' lettre restante)'

        # Joueur dont c'est le tour
        if jeu.joueur_local==jeu.joueur_actuel:
            s += ' - À vous de jouer ('+jeu.joueurs[jeu.joueur_actuel-1].pseudo+')'
        else:
            s += ' - À '+ jeu.joueurs[jeu.joueur_actuel-1].pseudo + ' de jouer'
        text = font.render(s , True, NOIR)
        self.screen.blit(text, (20, 5))

        # Scores des joueurs
        if len(jeu.joueurs)>1:
            s = 'Scores:'
        else:
            s = 'Score:'
        textT = fontG.render(s, True, NOIR)
        self.screen.blit(textT, (25, TOP_MARGIN + 15*self.hCell+25))

        for i, joueur in enumerate(jeu.joueurs):
            s = joueur.pseudo + '=' + str(joueur.score)
            if i==jeu.joueur_local-1:
                text = font.render(s, True, ROUGE)
            else:
                text = font.render(s, True, NOIR)
            self.screen.blit(text, (40, TOP_MARGIN + 15*self.hCell +25 + textT.get_height()+5 + i*20))

    def __afficher_deplacement(self):
        if self.piece_a_deplacer!=None:
            pos = (self.piece_a_deplacer_pos[0]-self.piece_a_deplacer_delta[0],
                self.piece_a_deplacer_pos[1]-self.piece_a_deplacer_delta[1])
            self.screen.blit(self.piece_a_deplacer.img, pos)

    def afficher_bouton(self, nb_points, visible):
        if visible:
            if nb_points!=0:
                if nb_points==1:
                    text = '(1 point)'
                else:
                    text = '(' + str(nb_points) + ' points)'
                self.button.set_subtext(text)
            else:
                self.button.set_subtext(None)
            self.button.draw(self.screen)

    def memoriser(self, joueur):
        """ Enregistrer dans l'image du plateau le coup joué par le joueur
        courant"""

        # Enregistrer les pièces placées dans l'image de fond
        for l in joueur.provisoire:
            if l.img == None:
                l.creer_image((self.wCell, self.hCell))
            self.img.blit(l.img, self.get_cell_orig(l.pos))

    def get_cell_orig(self, cell_name):
        """ Fournir les coordonnées du coin supérieur gauche d'une cellule"""

        colonne = int(cell_name[1:])-1
        ligne = LIGNES.find(cell_name[0])
        coord = (self.x0+colonne*self.wCell, self.y0+ligne*self.hCell)
        return coord

    def get_cell_name(self, pos):
        """ Indique le nom de la cellule correspondant à la position spécifiée.
            Retourne None si aucune cellule ne contient cette position. """
        
        if pos[0] >= LEFT_MARGIN and pos[1] >= TOP_MARGIN:
            colonne = int((pos[0]-LEFT_MARGIN)/self.wCell)
            ligne = int((pos[1]-TOP_MARGIN)/self.hCell)
            if colonne<NB_COLS and (ligne<NB_ROWS or ligne==NB_ROWS+1 and 3<=colonne<=11):
                return LIGNES[ligne] + str(colonne+1)
        return None
    
    def handle_mouse_click(self, mouse_event, jeu, reseau):
        if mouse_event.type == pygame.MOUSEBUTTONDOWN: 
            return self.__check_start_move(mouse_event, jeu, reseau) # Début ?
        elif mouse_event.type == pygame.MOUSEMOTION: 
            return self.__continue_move(mouse_event, jeu, reseau)
        elif mouse_event.type == pygame.MOUSEBUTTONUP: 
            return self.__end_move(mouse_event, jeu, reseau)

    def __check_cell(self, pos, jeu):
        """ Indique si la position indiquée correspond à une case contenant pièce
            pouvant se déplacer """
        joueur = jeu.joueurs[jeu.joueur_local-1]

        cell_name =  self.get_cell_name(pos)
        if cell_name!=None:
            # Rechercher si pièce valide
            for t in joueur.chevalet[0]:
                if t!=None and t.pos == cell_name:
                    return (True, t)
            for t in joueur.provisoire:
                if t.pos == cell_name:
                    return (True, t)
        return (False, None)

    def __check_start_move(self, mouse_event, jeu, reseau):
        pos = mouse_event.pos

        case_occupee, piece = self.__check_cell(pos, jeu)

        if case_occupee: # Début de déplacement
            self.piece_a_deplacer = piece
            self.piece_a_deplacer_pos = pos
            self.piece_a_deplacer_delta = ((pos[0]-LEFT_MARGIN)%self.wCell, 
                (pos[1]-LEFT_MARGIN)%self.hCell)
        else:
            self.piece_a_deplacer = None
            self.check_click_on_button(mouse_event)
        return self.piece_a_deplacer

    def __continue_move(self, mouse_event, jeu, reseau):
        if self.piece_a_deplacer!=None:
            pos = mouse_event.pos
            newpos = [pos[0], pos[1]]
            if pos[0] < 0:
                newpos[0] = 0
            elif pos[0] >= self.size[0]-self.wCell:
                newpos[0] = self.size[0]-self.wCell-1
            if pos[1] < 0:
                newpos[1] = 0
            elif pos[1] >= self.size[1]-self.hCell:
                newpos[1] = self.size[1]-self.hCell-1
            self.piece_a_deplacer_pos = tuple(newpos)
        return self.piece_a_deplacer

    def __end_move(self, mouse_event, jeu, reseau):
        if self.piece_a_deplacer!=None:
            src = self.piece_a_deplacer.pos
            dst = self.get_cell_name(mouse_event.pos)

            if dst!=None:
                result = jeu.deplacer_piece(jeu.joueur_local, dst, self.piece_a_deplacer)
                if result and reseau!=None:
                    reseau.envoyer('move', src + ',' + dst)

            self.piece_a_deplacer = None
        else:
            self.check_click_on_button(mouse_event)

        return self.piece_a_deplacer    

    def check_click_on_button(self, mouse_event):
        self.button.check_mouse_click(mouse_event)

    def set_message(self, m, mtype='error', fps=30, nb_sec=3):
        """ Définir le message à afficher en bas de la fenêtre, 
        en spécifiant sa durée d'affichage et son type. """

        self.message = m
        self.msg_time_count = nb_sec*fps
        self.msg_type = mtype

    def afficher_message(self):
        """ Mettre à jour l'affichage du message """

        if self.msg_time_count > 0:
            self.msg_time_count -= 1
            self.print_message()

    def print_message(self):
        """ Afficher un message d'information temporaire en bas
        de la fenêtre. Le type indiqué influence le format 
        d'affichage """

        font = pygame.font.SysFont('comicsans', 20)
        if self.msg_type=='error': # texte en rouge
            text = font.render(self.message, True, ROUGE)
        else: # texte en noir
            text = font.render(self.message, True, NOIR)
        self.screen.blit(text, (LEFT_MARGIN, TOP_MARGIN + 17*self.hCell+10))

    def afficher_fin(self, screen, jeu):
        """ Affichage de l'écran de fin. """

        v_idx = jeu.vainqueur()-1
        m_l1 = 'Victoire de ' + jeu.joueurs[v_idx].pseudo + ' ('+\
         str(jeu.joueurs[v_idx].score) +' points)'
        m_l2= 'Appuyer sur une touche pour quitter.'
        font = pygame.font.SysFont('comicsans', 48)
        text = font.render(m_l1, True, (255, 255, 0))
        font2 = pygame.font.SysFont('comicsans', 26)
        text2 = font2.render(m_l2, True, (255, 255, 0))

        width = screen.get_width()
        height = screen.get_height()
        pygame.draw.rect(screen, (0,0,0), (width/2 - text.get_width()/2 -10, 
            height/2 - text.get_height()-10, text.get_width()+20, 
            text.get_height() + text2.get_height() + 20 ))
        screen.blit(text, (width/2-text.get_width()/2, height/2-text.get_height()-2))
        screen.blit(text2, (width/2-text2.get_width()/2, height/2 + 2))
