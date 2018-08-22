import pygame

FOREGROUND = (0,0,0)
BACKGROUND = (212, 208, 200)
CONTOUR_DESSUS = (235, 235, 235)
CONTOUR_DESSOUS = (0,0,0) 

class Button():

	def __init__(self, orig, text='Valider'):
		# Texte
		font = pygame.font.SysFont('comicsans', 36)
		self.text = font.render(text, True, FOREGROUND)

		self.subtext = None

		self.bx0 = orig[0]
		self.by0 = orig[1]
		self.bw = self.text.get_width()+20
		self.bh = self.text.get_height()*2
		self.pressed = False
		self.action = False

	def draw(self, screen):
	    """ Dessiner le bouton de validation (affichage différent
	    selon que le bouton soit appuyé ou non) et vérifier s'il est appuyé """

	    pygame.draw.rect(screen, BACKGROUND, (self.bx0, self.by0, self.bw, self.bh))

	    # Texte
	    if self.subtext!=None:
		    screen.blit(self.text, (self.bx0+10, self.by0+5))
		    screen.blit(self.subtext, (self.bx0 + self.bw/2 - self.subtext.get_width()/2, 
		    	self.by0+5 + self.text.get_height()))
	    else:
	    	screen.blit(self.text, (self.bx0+10, self.by0+self.bh/2-self.text.get_height()/2))

	    # Contours
	    if self.pressed:
	        pygame.draw.lines(screen, CONTOUR_DESSOUS, False, 
	            [(self.bx0, self.by0+self.bh), (self.bx0, self.by0), 
	            (self.bx0+self.bw, self.by0)], 2)
	        pygame.draw.lines(screen, CONTOUR_DESSUS, False, 
	            [(self.bx0, self.by0+self.bh), (self.bx0+self.bw, self.by0+self.bh), 
	            (self.bx0+self.bw, self.by0)], 2)
	    else:
	        pygame.draw.lines(screen, CONTOUR_DESSUS, False, 
	          [(self.bx0, self.by0+self.bh), (self.bx0, self.by0), 
	          (self.bx0+self.bw, self.by0)], 2)
	        pygame.draw.lines(screen, CONTOUR_DESSOUS, False, 
	          [(self.bx0, self.by0+self.bh), (self.bx0+self.bw, self.by0+self.bh), 
	          (self.bx0+self.bw, self.by0)], 2)

	def set_subtext(self, text):
		if text!=None:
			font = pygame.font.SysFont('comicsans', 14)
			self.subtext = font.render(text, True, FOREGROUND)
		else:
			self.subtext = None

	def is_clicked(self):
		""" Vérifier si l'évènement bouton cliqué est survenu. """

		if self.action:
		    self.action = False
		    return True
		return False

	def check_mouse_click(self, mouse_event):
	    """ Vérifier si l'évènement souris correspond à un clic sur le bouton"""

	    pos = mouse_event.pos
	    if (self.bx0 <= pos[0] <self.bx0+self.bw) and (self.by0 <= pos[1] <self.by0+self.bh):
	        if mouse_event.type==pygame.MOUSEBUTTONDOWN:
	            self.pressed = True
	        else:
	            self.pressed = False
	            self.action = True
