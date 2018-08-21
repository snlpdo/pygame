from threading import Thread
import random

class Reseau():
    def __init__(self, socket, local_pseudo, start_comm):
        self.sock = socket
        self.peer_name = socket.getpeername()

        # Négociation initiale (6 étapes)
        for i in range(6):
            if i==0 and start_comm or i==1 and not(start_comm):
                # envoi pseudo local
                self.envoyer('pseudo', local_pseudo)

            elif i==1 and start_comm or i==0 and not(start_comm):
                # réception pseudo distant
                param, self.remote_pseudo = self.recevoir(128)
                if param!='pseudo':
                    print("Reçu paramètre "+param+" au lieu de pseudo")
                    quit()

            elif i==2: 
                print("Connecté avec", self.remote_pseudo, self.peer_name)

            elif i==3 and start_comm or i==4 and not(start_comm):
                # envoi random local
                local_rand = random.random()
                self.envoyer('priority', str(local_rand))

            elif i==4 and start_comm or i==3 and not(start_comm):
                # réception random distant
                param, remote_rand = self.recevoir(128)
                if param != 'priority' : 
                    print("Reçu paramètre "+param+" au lieu de priority")
                    quit()
                remote_rand = float(remote_rand)

            elif i==5:
                # détermination du 1er joueur
                if local_rand > remote_rand:
                    self.premier_joueur = True
                    print('Je joue en premier')
                else:
                    self.premier_joueur = False
                    print('Je joue en second')

    def envoyer(self, param, valeur):
        message = param + '=' + valeur
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

    def run(self):
        while True:
            message = self.socket.recv(1024).decode('ascii').split('=')

            # numéro de joueur de l'adversaire
            if self.jeu.joueur_local==1:
                joueur_num = 2
            else:
                joueur_num = 1

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
                result = self.jeu.validation(joueur_num)
                self.plateau.validation(self.jeu.joueurs[joueur_num-1])
            elif message[0]=='tirage':
                self.jeu.affecter_tirage(self.jeu.joueur_actuel, message[1], True)

    def stop(self):
        self.continer = False
