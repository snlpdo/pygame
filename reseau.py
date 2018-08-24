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
            ss.bind( ("192.168.43.16", 7175) )
            ss.listen(args.nombre_joueurs-1) 
            
            # Connexion avec client (1 seul pour le moment)
            self.sock, dist_sock = ss.accept()

        elif args.client: # Mode client
            print("\n=== Mode réseau (client)===")
            print("Connexion au serveur "+args.client)

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect( (args.client, 7175))

    def demarrer_ecoute(self, jeu, plateau):
        # Lancer thread d'écoute
        self.reception = Reception(self.sock, jeu, plateau)
        self.reception.start()

    def envoyer(self, param, valeur):
        message = param + '=' + valeur
        self.sock.sendall(bytes(message, 'ascii'))

    def envoyer_multiple(self, params, valeurs):
        message = ''
        for i in range(len(params)):
            message += params[i] + '=' + valeurs[i]
            if i<len(params)-1:
                message += '&'
        self.sock.sendall(bytes(message, 'ascii'))

    def recevoir(self, nbBytes):
        message = self.sock.recv(nbBytes).decode('ascii').split('=')
        return message

    def reception_multiple(self):
        return self.sock.recv(1024).decode('ascii').split('&')

class Reception(Thread):
    def __init__(self, socket, jeu, plateau):
        Thread.__init__(self)
        self.socket = socket
        self.continuer = True
        self.jeu = jeu
        self.plateau = plateau
        self.socket.settimeout(5) # 5s

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
                elif message[0]=='fin':
                    self.jeu.terminer_partie()
                    self.continuer = False

    def stop(self):
        self.continuer = False
