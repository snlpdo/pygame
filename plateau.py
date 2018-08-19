import pygame
from math import cos, sin, pi
from lettre import *

# Couleurs
NOIR = (0,0,0)
VERT = (0, 123, 0)
ROSE = (255, 182, 193)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 215)
CYAN = (50,200,200)
BLANC = (255, 255, 255)
LIGHTGRAY = (212, 208, 200)

TOP_MARGIN, RIGHT_MARGIN, BOTTOM_MARGIN, LEFT_MARGIN = 60, 50, 150, 50
LEGENDE_SEP = 15
LEGENDE_SIZE = 25
LIGNES = "ABCDEFGHIJKLMNOPQ"

NB_ROWS, NB_COLS = 15, 15

class Plateau():

    def __init__(self, size, bonus):
        """ Construit un plateau aux bonnes dimensions qui fait
        apparaître les différentes cases bonus. 

        INPUT:
        size: largeur et hauteur du plateau 
        bonus: tableau 15x15 indiquant la position des cases bonus.
        """

        self.wCell, self.hCell = 0, 0 # dimension d'une cellule
        self.x0, self.y0 = 0, 0 # origine du quadrillage
        self.tx0, self.ty0 = 0, 0 # origine du chevalet
        self.size = size
        self.img = self.__creer_image(bonus)
        self.piece_a_deplacer = None

        # Bouton de validation
        font = pygame.font.SysFont('comicsans', 36)
        self.text_button = font.render('Valider', True, NOIR)
        self.button_checked = False

        # Font
        self.bx0 = LEFT_MARGIN + 13*self.wCell
        self.by0 = TOP_MARGIN + 16*self.hCell + 5
        self.bw = self.text_button.get_width()+20
        self.bh = self.text_button.get_height()+10
        self.button_pressed = False
        self.button_action = False


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

    def afficher_joueur(self, screen, chevalet, en_attente):
        """ Dessine les pièces du joueur:
        - celles dans le chevalet.
        - celles sur le plateau en attente de validation.

        INPUT:
        - écran contenant le plateau
        - liste 2D contenant les pièces sur le chevalet
          (la pièce en court de déplacement ne sera pas prise en compte).
        - file contenant les pièces posées sur le jeu mais pas encore
          validées.
        """ 

        for l in chevalet:
            if l != None and l != self.piece_a_deplacer:
                if l.img == None:
                    l.creer_image((self.wCell, self.hCell))
                screen.blit(l.img, self.get_cell_orig(l.pos))
        for l in en_attente:
            if l != self.piece_a_deplacer:
                if l.img == None:
                    l.creer_image((self.wCell, self.hCell))
                screen.blit(l.img, self.get_cell_orig(l.pos))

    def validation(self, en_attente):
        # Enregistrer les pièces placées dans l'image de fond
        for l in en_attente:
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
    
    def can_move(self, pos, chevalet, en_attente):
        """ Indique si la position indiquée correspond à une case contenant pièce
            pouvant se déplacer """
        
        cellName =  self.get_cell_name(pos)
        if cellName!=None:
            # Rechercher si pièce valide
            for t in chevalet:
                if t!=None and t.pos == cellName:
                    return (True, t)
            for t in en_attente:
                if t.pos == cellName:
                    return (True, t)
        return (False, None)

    def start_move(self, pos, chevalet, en_attente):
        result = self.can_move(pos, chevalet, en_attente)
        if result[0]: # Début de déplacement
            self.piece_a_deplacer = result[1]
            self.piece_a_deplacer_pos = pos
            self.piece_a_deplacer_delta = ((pos[0]-LEFT_MARGIN)%self.wCell, (pos[1]-LEFT_MARGIN)%self.hCell)
        return result[1]

    def continue_move(self, pos):
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

    def draw_move(self, screen):
        pos = (self.piece_a_deplacer_pos[0]-self.piece_a_deplacer_delta[0],
            self.piece_a_deplacer_pos[1]-self.piece_a_deplacer_delta[1])
        screen.blit(self.piece_a_deplacer.img, pos)

    def end_move(self):
        self.piece_a_deplacer = None

    def afficher_stat(self, screen, jeu):
        # État de la pioche
        font = pygame.font.SysFont('comicsans', 24)
        s = 'Tour: ' + str(jeu.tour_jeu) 
        if len(jeu.pioche)>1:
            s += ' (' + str(len(jeu.pioche)) + ' lettres restantes)'
        else:
            s += ' (' + str(len(jeu.pioche)) + ' lettre restante'
        text = font.render(s , True, NOIR)
        screen.blit(text, (20, 5))

        # Score du joueur
        font2 = pygame.font.SysFont('comicsans', 36)
        s = 'Score : ' + str(jeu.score)
        text = font2.render(s, True, NOIR)
        screen.blit(text, (25, TOP_MARGIN + 16*self.hCell + 10))

    def bouton_validation(self, screen):
        pygame.draw.rect(screen, LIGHTGRAY, (self.bx0, self.by0, self.bw, self.bh))

        # Texte
        screen.blit(self.text_button, (self.bx0+10, self.by0+5))

        # Contours
        if self.button_pressed:
            pygame.draw.lines(screen, NOIR, False, 
                [(self.bx0, self.by0+self.bh), (self.bx0, self.by0), 
                (self.bx0+self.bw, self.by0)], 2)
            pygame.draw.lines(screen, (235, 235, 235), False, 
                [(self.bx0, self.by0+self.bh), (self.bx0+self.bw, self.by0+self.bh), 
                (self.bx0+self.bw, self.by0)], 2)
        else:
            pygame.draw.lines(screen, (235, 235, 235), False, 
              [(self.bx0, self.by0+self.bh), (self.bx0, self.by0), 
              (self.bx0+self.bw, self.by0)], 2)
            pygame.draw.lines(screen, NOIR, False, 
              [(self.bx0, self.by0+self.bh), (self.bx0+self.bw, self.by0+self.bh), 
              (self.bx0+self.bw, self.by0)], 2)

        if self.button_action:
            self.button_action = False
            return True
        return False

    def check_button(self,pos, startEvent):
        if (self.bx0 <= pos[0] <self.bx0+self.bw) and (self.by0 <= pos[1] <self.by0+self.bh):
            if startEvent:
                self.button_pressed = True
            else:
                self.button_pressed = False
                self.button_action = True

    def print_status(self, screen, message, type="error"):
        font = pygame.font.SysFont('comicsans', 20)
        if type=="error":
            text = font.render(message, True, ROUGE)
        else:
            text = font.render(message, True, NOIR)
        screen.blit(text, (LEFT_MARGIN, TOP_MARGIN + 17*self.hCell+10))
