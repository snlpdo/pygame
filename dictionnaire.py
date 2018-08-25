class Dictionnaire():
	def __init__(self):
		fichier = open('dictionnaire-fr.txt', 'r')
		self.mots = fichier.readlines()
		continuer = True
		fichier.close()

	def valide(self, mot):
		mot += '\n'	
		if mot in self.mots:
			return True
		else:
		 	return False

if __name__ == '__main__':
	dico = Dictionnaire()

	while True:
		mot = input('Mot à vérifier: ')

		if dico.valide(mot):
			print("le mot", mot, "existe")
		else:
			print("le mot", mot, "n'existe pas")

