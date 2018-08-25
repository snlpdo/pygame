from threading import Thread
import random
import socket

class Reseau():
    def __init__(self, args):
        if args.serveur: # Mode serveur         
            print("\n=== Mode réseau (serveur)===")
            print("Attente de connexion...")

            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ss.bind( ("192.168.1.43", 7175) )
            ss.listen(args.nombre_joueurs-1) 
            
            # Connexion avec client (1 seul pour le moment)
            self.sock, dist_sock = ss.accept()
            print("Client connecté")

        elif args.client: # Mode client
            print("\n=== Mode réseau (client)===")
            print("Connexion au serveur "+args.client)

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect( (args.client, 7175))
            print("Connecté au serveur")

    def init_communication(self, args, jeu):
        """ Communication initiale entre le serveur et le client
        pour partager les informations de départ du jeu. """

        for i in range(4):
            # Envoi pseudo
            if i==0 and args.serveur or i==1 and not(args.serveur): 
                self.envoyer('pseudo', args.pseudo)

            # Réception pseudo
            elif i==1 and args.serveur or i==0 and not(args.serveur): 
                param, remote_pseudo = self.recevoir(128)
                if param!='pseudo':
                    print('Reçu paramètre ' + param + ' au lieu de pseudo')
                    quit()

            # Envoi nombre aléatoire
            elif i==2 and args.serveur or i==3 and not(args.serveur): 
                if args.serveur and args.input: # Pour le serveur
                    if jeu.joueur_actuel==jeu.joueur_local:
                        local_rand = 1.5 # prise de la main par le serveur
                    else:
                        local_rand = -0.5 # prise de la main par l'adversaire
                else: # Pour le client
                    local_rand = random.random() # prise de la main aléatoire
                self.envoyer('priority', str(local_rand))

            # Réception nombre aléatoire
            elif i==3 and args.serveur or i==2 and not(args.serveur): 
                param, remote_rand = self.recevoir(128)
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
                    if jeu.grille[i][j]=='':
                        msg.append(' ')
                    elif jeu.grille[i][j]==' ':
                        msg.append('?')
                    else:
                        msg.append(jeu.grille[i][j])
            num_adversaire = (jeu.joueur_local%2)+1
            ch1 = [ l.char for l in jeu.joueurs[0].chevalet[0] if l!=None ]
            ch2 = [ l.char for l in jeu.joueurs[1].chevalet[0] if l!=None ]

            self.envoyer_multiple(['grille', 'numero', 'ch1', 'ch2', 
                'sc1', 'sc2', 'tour'], 
                [''.join(msg), str(num_adversaire),''.join(ch1),''.join(ch2), 
                 str(jeu.joueurs[0].score), str(jeu.joueurs[1].score), 
                 str(jeu.tour_jeu)])

            # attendre l'ack du client
            self.recevoir(64) 

        else: # client
            # Réception de la grille, du numéro de joueur à utiliser, des chevalets,
            # des scores et du numéro de tour de jeu
            messages = self.recevoir_multiple(1024)

            for message in messages:
                message = message.split('=')

                if message[0]=='grille':
                    rgrille = message[1]
                    for idx in range(15*15):
                        j = idx%15
                        i = idx//15
                        if rgrille[idx]=='?':
                            jeu.grille[i][j] = ' '
                        elif rgrille[idx]==' ':
                            jeu.grille[i][j] = ''
                        else:
                            jeu.grille[i][j] = rgrille[idx]

                        if jeu.grille[i][j] != '': # affecter au 1er joueur
                            lettre = jeu.creer_lettre(jeu.grille[i][j])
                            lettre.pos = jeu.get_cell_name(j, i)
                            # L'attribuer arbitrairement au 1er joueur
                            jeu.joueurs[0].provisoire.append(lettre)

                elif message[0]=='numero': # ĺe numéro du joueur local
                    jeu.joueur_local = int(message[1])
                    num_adversaire = (jeu.joueur_local%2)+1

                elif message[0][:2]=='ch': # Un chevalet
                    num = int(message[0][2:])
                    for i, l in enumerate(message[1]):
                        lettre = jeu.creer_lettre(l)
                        lettre.pos = 'Q' + str(4+i)
                        jeu.joueurs[num-1].chevalet[0][i] = lettre

                elif message[0][:2]=='sc': # Un score
                    num = int(message[0][2:])
                    jeu.joueurs[num-1].score = int(message[1])

                elif message[0]=='tour':
                    jeu.tour_jeu = int(message[1])

            self.envoyer('PRET', '')

        # Définir les pseudos
        jeu.joueurs[jeu.joueur_local-1].pseudo = args.pseudo
        jeu.joueurs[num_adversaire-1].pseudo = remote_pseudo

        # Déterminer le 1er joueur (tirage au sort le plus grand)
        if local_rand > remote_rand:
            jeu.joueur_actuel = jeu.joueur_local
        else:
            jeu.joueur_actuel = (jeu.joueur_local%2)+1

        # Modifier les pseudos si identiques
        if jeu.joueurs[jeu.joueur_local-1].pseudo==jeu.joueurs[num_adversaire-1].pseudo:
            jeu.joueurs[0].pseudo += '1'
            jeu.joueurs[1].pseudo += '2'

    def demarrer_ecoute(self, jeu, plateau):
        """ Lancer le thread d'écoute et d'analyse continue. """

        self.reception = Reception(self.sock, jeu, plateau)
        self.reception.start()

    def envoyer(self, param, valeur):
        """ Envoyer un message au pair d'un type donné. """

        message = param + '=' + valeur
        self.sock.sendall(bytes(message, 'ascii'))
        # print("[->]", message)

    def envoyer_multiple(self, params, valeurs):
        """ Envoyer plusieurs messages consécutifs au pair. """

        message = ''
        for i in range(len(params)):
            message += params[i] + '=' + valeurs[i]
            if i<len(params)-1:
                message += '&'
        self.sock.sendall(bytes(message, 'ascii'))
        # print("[->]", message)

    def recevoir(self, nbBytes):
        """ Récupérer un message de longueur données auprès du pair. """

        message = self.sock.recv(nbBytes).decode('ascii').split('=')
        # print("[<-]", message)
        return message

    def recevoir_multiple(self, nbBytes):
        message = self.sock.recv(nbBytes).decode('ascii').split('&')
        # print("[<-]", message)
        return message

class Reception(Thread):
    def __init__(self, socket, jeu, plateau):
        Thread.__init__(self)
        self.socket = socket
        self.continuer = True
        self.jeu = jeu
        self.plateau = plateau
        self.socket.settimeout(3) # 3s

    def run(self):
        while self.continuer:
            messages = []
            try:
                messages = self.socket.recv(1024).decode('ascii').split('&')
            except:
                pass # pour timeout

            # numéro de joueur de l'adversaire
            if self.jeu.joueur_local==1:
                joueur_num = 2
            else:
                joueur_num = 1

            for message in messages:
                message = message.split('=')

                if message[0]=='move':
                    move = message[1].split(',')
                    src = move[0]
                    dst = move[1]

                    if src[0]=='Q': # pièce depuis le chevalet
                        piece = self.jeu.joueurs[joueur_num-1].chevalet[0][int(src[1:])-4]
                    else: # pièce déjà sur le plateau
                        for l in self.jeu.joueurs[joueur_num-1].provisoire:
                            if l.pos == src:
                                piece = l
                                break
                    self.jeu.deplacer_piece(joueur_num, dst, piece, True)
                elif message[0]=='validation':
                    result = self.jeu.valider(joueur_num)
                    self.plateau.memoriser(self.jeu.joueurs[joueur_num-1])
                elif message[0]=='tirage':
                    self.jeu.affecter_tirage(self.jeu.joueur_actuel, message[1], True)
                elif message[0]=='message':
                    self.plateau.set_message(message[1], 'info')
                elif message[0]=='joker':
                    # Caractère
                    jnum = int(message[1][0])
                    char = message[1][1]
                    pos = message[1][2:]
                    # Trouver la lettre et l'éditer
                    joueur = self.jeu.joueurs[jnum-1]
                    lettre = None
                    if pos[0]=='Q': # lettre sur le chevalet
                        for l in joueur.chevalet[0]:
                            if l!=None and l.pos==pos:
                                lettre = l
                    else: # lettre en placement provisoire
                        for l in joueur.provisoire:
                            if l!=None and l.pos==pos:
                                lettre = l
                    lettre.joker_char = char
                    lettre.creer_image(lettre.img.get_size())
                elif message[0]=='fin':
                    self.jeu.terminer_partie()
                    self.continuer = False

    def stop(self):
        self.continuer = False
