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

            # Initier le dialogue
            start_comm = True

        elif args.client: # Mode client
            print("\n=== Mode réseau (client)===")
            print("Connexion au serveur "+args.client)

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect( (args.client, 7175))

            # Attendre l'initiation du dialogue par le serveur
            start_comm = False
    
        # Dialogue initial (4 étapes):
        # 1) Envoi du pseudo du serveur
        # 2) Envoi du pseudo du client
        # 3) Envoi d'un nombre tiré au sort par le réseau
        # 4) Envoi d'un nombre tiré au sort par le client
        for i in range(4):
            if i==0 and start_comm or i==1 and not(start_comm):
                # envoi pseudo local
                self.envoyer('pseudo', args.pseudo)

            elif i==1 and start_comm or i==0 and not(start_comm):
                # réception pseudo distant
                param, self.remote_pseudo = self.recevoir(128)
                if param!='pseudo':
                    print('Reçu paramètre ' + param + ' au lieu de pseudo')
                    quit()

            elif i==2 and start_comm or i==3 and not(start_comm):
                # envoi random local
                local_rand = random.random()
                self.envoyer('priority', str(local_rand))

            elif i==3 and start_comm or i==2 and not(start_comm):
                # réception random distant
                param, remote_rand = self.recevoir(128)
                if param != 'priority' : 
                    print('Reçu paramètre '+param+' au lieu de priority')
                    quit()
                remote_rand = float(remote_rand)

        # Détermination du 1er joueur (nombre tiré au sort le plus grand)
        if local_rand > remote_rand:
            self.premier_joueur = True
            if self.remote_pseudo==args.pseudo:
                args.pseudo += '1'
                self.remote_pseudo += '2'
            print('Je joue en premier')
        else:
            self.premier_joueur = False
            if self.remote_pseudo==args.pseudo:
                args.pseudo += '2'
                self.remote_pseudo += '1'
            print('Je joue en second')
        print("Connecté avec", self.remote_pseudo, self.sock.getpeername())

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

    def ecouter_reception(self, jeu, plateau):
        self.reception = Reception(self.sock, jeu, plateau)
        self.reception.start()

class Reception(Thread):
    def __init__(self, socket, jeu, plateau):
        Thread.__init__(self)
        self.socket = socket
        self.continuer = True
        self.jeu = jeu
        self.plateau = plateau
        self.socket.settimeout(2) # 2s

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
