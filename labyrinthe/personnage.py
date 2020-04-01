import pygame

ROUGE = (255,0,0)
DELTA = 5

HAUT = 0
DROITE = 1
BAS = 2
GAUCHE = 3
AUCUN = -1

class Personnage(pygame.sprite.Sprite):
    
    def __init__(self, plateau, cell_sz):
        pygame.sprite.Sprite.__init__(self)
        self.plateau = plateau
        self.cz = cell_sz
        
        self.image = pygame.Surface([10,10])
        self.image.fill(ROUGE)
        
        self.rect = self.image.get_rect()
        
        self.dx = DELTA
        self.dy = 0
        
        self.gagne = False
        self.etat = 0
        self.direction = DROITE
        self.mur_suivi = AUCUN
        self.rect.left = cell_sz
        self.rect.top = 11.5*cell_sz
        
    def pledge(self):
        # Détection de murs
        mur = [0,0,0,0] # haut, droite, bas, gauche

        # Mur à droite ?
        c = int((self.rect.right)//self.cz)
        l1 = int(self.rect.top//self.cz)
        l2 = int((self.rect.bottom-1)//self.cz)
        if self.plateau[l1][c]==1 or  self.plateau[l2][c]==1:
            self.rect.right = c*self.cz
            mur[DROITE]=1
            
        # Mur à gauche ?
        c = int((self.rect.left-1)//self.cz)
        l1 = int(self.rect.top//self.cz)
        l2 = int((self.rect.bottom-1)//self.cz)
        if self.plateau[l1][c]==1 or self.plateau[l2][c]==1:
            self.rect.left = (c+1)*self.cz
            mur[GAUCHE]=1
            
        # Détecter un mur en bas
        c1 = int(self.rect.left//self.cz)
        c2 = int((self.rect.right-1)//self.cz)
        l = int(self.rect.bottom//self.cz)
        if self.plateau[l][c1]==1 or self.plateau[l][c2]==1:
            self.rect.bottom = l*self.cz
            mur[BAS]=1

        # Détecter un mur en haut
        c1 = int(self.rect.left//self.cz)
        c2 = int((self.rect.right-1)//self.cz)
        l = int((self.rect.top-1)//self.cz)
        if self.plateau[l][c1]==1 or self.plateau[l][c2]==1:
            self.rect.top = (l+1)*self.cz
            mur[HAUT] = 1
        
        if self.etat==0: # aller tout droit (jusqu'à trouver un mur)
            if self.direction==DROITE and mur[DROITE]==1:
                self.direction=BAS
                self.etat += 1
                #print(self.etat)
                self.mur_suivi = DROITE
            elif self.direction==BAS and mur[BAS]==1:
                self.direction=GAUCHE
                self.etat += 1
                #print(self.etat)
                self.mur_suivi = BAS
            elif self.direction==GAUCHE and mur[GAUCHE]==1:
                self.direction=HAUT
                self.etat += 1
                #print(self.etat)
                self.mur_suivi = GAUCHE
            elif self.direction==HAUT and mur[HAUT]==1:
                self.direction=DROITE
                self.etat += 1
                #print(self.etat)
                self.mur_suivi = HAUT
        else:
            if self.direction==DROITE:
                if self.mur_suivi==HAUT:
                    if mur[HAUT]==0:
                        self.direction = HAUT
                        self.mur_suivi = GAUCHE
                        self.etat -= 1
                        print(self.etat)
                        colonne = int((self.rect.left)//self.cz)
                        self.rect.left = colonne * self.cz
                    elif mur[DROITE]==1:
                        self.direction = BAS
                        self.mur_suivi = DROITE
                        self.etat += 1
                        print(self.etat)
                else: # mur suivi en bas
                    if mur[BAS]==0:
                        self.direction = BAS
                        self.mur_suivi = GAUCHE
                        self.etat += 1
                        print(self.etat)
                        colonne = int((self.rect.left)//self.cz)
                        self.rect.left=colonne * self.cz
                    elif mur[DROITE]==1:
                        self.direction = HAUT
                        self.mur_suivi = DROITE
                        self.etat -= 1
                        print(self.etat)
            elif self.direction==HAUT:
                if self.mur_suivi==DROITE:
                    if mur[DROITE]==0: # plus de mur à droite
                        self.direction = DROITE
                        self.mur_suivi = BAS
                        self.etat += 1
                        print(self.etat)
                        ligne = int((self.rect.top)//self.cz)
                        self.rect.top = ligne*self.cz
                    elif mur[HAUT]==1:
                        self.direction = GAUCHE
                        self.mur_suivi = HAUT
                        self.etat -= 1
                        print(self.etat)
                else: # mur suivi à gauche
                    if mur[GAUCHE]==0: # plus de mur à gauche
                        self.direction = GAUCHE
                        self.mur_suivi = BAS
                        self.etat -= 1
                        print(self.etat)
                        ligne = int(self.rect.bottom//self.cz)
                        self.rect.bottom = ligne*self.cz
                    elif mur[HAUT]==1:
                        self.direction = DROITE
                        self.mur_suivi = HAUT
                        self.etat += 1
                        print(self.etat)
            elif self.direction==GAUCHE:
                if self.mur_suivi==BAS:
                    if mur[BAS]==0: # plus de mur en bas
                        self.direction = BAS
                        self.mur_suivi = DROITE
                        self.etat -= 1
                        print(self.etat)
                        colonne = int(self.rect.right//self.cz)
                        self.rect.right = colonne * self.cz
                    elif mur[GAUCHE]==1:
                        self.direction = HAUT
                        self.mur_suivi = GAUCHE
                        self.etat += 1
                        print(self.etat)
                else: # mur suivi en HAUT
                    if mur[HAUT]==0: # plus de mur en haut
                        self.direction = HAUT
                        self.mur_suivi = DROITE
                        self.etat += 1
                        print(self.etat)
                    elif mur[GAUCHE]==1:
                        self.direction = BAS
                        self.mur_suivi = GAUCHE
                        self.etat -= 1
                        #print(self.etat)
            elif self.direction==BAS:
                if self.mur_suivi==GAUCHE:
                    if mur[GAUCHE]==0: # plus de mur à gauche
                        self.direction = GAUCHE
                        self.mur_suivi = HAUT
                        self.etat += 1
                        print(self.etat)
                        ligne = int((self.rect.top)//self.cz)
                        self.rect.top = ligne*self.cz                        
                    elif mur[BAS]==1: 
                        self.direction = DROITE
                        self.mur_suivi = BAS
                        self.etat -= 1
                        print(self.etat)
                else: # mur suivi à DROITE
                    if mur[DROITE]==0: # plus de mur à droite
                        self.direction = DROITE
                        self.mur_suivi = HAUT
                        self.etat -= 1
                        print(self.etat)
                        ligne = int((self.rect.top)//self.cz)
                        self.rect.top = ligne*self.cz                        
                    elif mur[BAS]==1: 
                        self.direction = GAUCHE
                        self.mur_suivi = BAS
                        self.etat += 1
                        print(self.etat)
            
        
    def update(self):
        """
        Déplacement du personnage dans le labyrinthe selon
        l'algorithme de Pledge
        """
        
        # Sortie du labyrinthe ?
        height = self.cz * len(self.plateau)
        width = self.cz * len(self.plateau[0])
        if self.rect.left<1 or self.rect.right>=width or self.rect.top<1 or self.rect.bottom>=height:
            self.gagne = True
        
        if not self.gagne:
            self.pledge()
            
            if self.direction==DROITE:
                self.rect.centerx += DELTA
            elif self.direction==GAUCHE:
                self.rect.centerx -= DELTA
            elif self.direction==BAS:
                self.rect.centery += DELTA
            elif self.direction==HAUT:
                self.rect.centery -= DELTA
            
        
        
        
        
