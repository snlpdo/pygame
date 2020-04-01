import pygame

BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
NOIR = (0,0,0)

class Page0():
    def __init__(self,largeur,hauteur):
        self.next_page_idx = 0
        self.largeur = largeur
        self.hauteur = hauteur

        police = pygame.font.SysFont('caladea', 40)
        police_mini = pygame.font.SysFont('caladea', 20)

        # Préparer le titre de la page
        self.titre = police_mini.render("Page d'accueil", True, BLEU)

        # Préparer les menus
        self.menu_idx = 0
        self.menu = []
        self.menu_selected = []
        self.rect = []
        liste = ["Jouer", "Configurer", "Quitter"]
        nb_menu = len(liste)
        for i in range(nb_menu):
            rendu = police.render(liste[i], True, BLEU)
            self.menu.append(rendu)
            self.menu_selected.append(police.render(liste[i], True, ROUGE))
            self.rect.append(rendu.get_rect(center=(largeur/2,(i+1)*hauteur/(nb_menu+1))))

        # Prochaine page pour chaque menu
        self.next_page = [2, 1, -1]
    
    def start(self):
        pygame.display.set_caption("Menu principal")
        pygame.display.set_mode((self.largeur, self.hauteur))
    
    def update(self,s):
        self.next_page_idx = 0
        nb_menu = len(self.menu)

        ###################
        # Gestion des évènements
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.next_page_idx = -1
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.menu_idx += 1
                    if self.menu_idx>=nb_menu:
                        self.menu_idx = 0
                elif e.key == pygame.K_UP:
                    self.menu_idx -= 1
                    if self.menu_idx<0:
                        self.menu_idx = nb_menu-1
                elif e.key == pygame.K_RETURN:
                    self.next_page_idx = self.next_page[self.menu_idx]
            elif e.type == pygame.MOUSEMOTION:
                position = e.pos
                for i in range(nb_menu):
                    if self.rect[i].collidepoint(position):
                        self.menu_idx = i
            elif e.type == pygame.MOUSEBUTTONUP:
                position = e.pos
                for i in range(nb_menu):
                    if self.rect[i].collidepoint(position):
                        self.next_page_idx = self.next_page[i]

        #########################
        # Dessin du contenu
        s.fill(NOIR)
        s.blit(self.titre, (10,10))

          # Les menus
        for i in range(nb_menu):
            if self.menu_idx==i: # si sélectionné
                s.blit(self.menu_selected[i], self.rect[i])
            else: # sinon
                s.blit(self.menu[i], self.rect[i])
