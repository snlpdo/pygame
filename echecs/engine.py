plateau = [
  [ 'tn', 'cn', 'fn', 'dn', 'rn', 'fn', 'cn', 'tn' ],
  [ 'pn', 'pn', 'pn', 'pn', 'pn', 'pn', 'pn', 'pn' ],
  [ '', '', '', '', '', '', '', '' ],  
  [ '', '', '', '', '', '', '', '' ],  
  [ '', '', '', '', '', '', '', '' ],  
  [ '', '', '', '', '', '', '', '' ],  
  [ 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb' ],
  [ 'tb', 'cb', 'fb', 'db', 'rb', 'fb', 'cb', 'tb' ]
]

def valider_coup(depart, arrivee, blanc):
	if depart==None or arrivee==None:
		return "Case de départ ou d'arrivée invalide"

	j = ord(depart[0])-ord('A')
	i = 7-(ord(depart[1])-ord('1'))
	if plateau[i][j]=='': 
		return "Case de départ vide"
	elif (plateau[i][j][1]=='n' and blanc) or (plateau[i][j][1]=='b' and not blanc):
		return "La pièce ne vous appartient pas"

	j2 = ord(arrivee[0])-ord('A')
	i2 = 7-(ord(arrivee[1])-ord('1'))

	# à faire, vérifier que le déplacement soit valide

	plateau[i2][j2] = plateau[i][j]
	plateau[i][j] = ''
	
