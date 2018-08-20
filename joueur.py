class Joueur():
	nb = 0

	def __init__(self):
		self.provisoire = []
		self.chevalet = [[None for i in range(9)]]
		self.score = 0

		Joueur.nb += 1
		self.num = Joueur.nb
