"""
Ce module s'occupe du fonction interne du jeu.
Il ne doit surtout pas supposer qu'il existe une interface
graphique.
"""
from threading import Thread
import sys
import socket
import random

class Jeu():

    def __init__(self):
        ########################
        # Analyser la ligne de commande
        # pour savoir s'il s'agit du mode serveur ou client
        if len(sys.argv)==2 and sys.argv[1]=="client":
            self.serveur = False
            print("Mode client")
        else:
            self.serveur = True
            print("Mode serveur")
            
        # Mise en place de la communication serveur-client
        if self.serveur:
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listen_socket.bind( ('', 7175) ) # 
            listen_socket.listen(1) # 1 seul client
            print("Attente du client...")
            self.local_socket, remote_socket = listen_socket.accept()
            print("Connecté avec", remote_socket)
            
            # Le serveur choisir le premier joueur en l'envoie au client
            if random.random()>0.5:
                self.joueur = 1
                message = "2"
            else:
                self.joueur = 2
                message = "1"
            b_message = bytes(message, 'ascii')
            self.local_socket.sendall(b_message)
        else:
            self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.local_socket.connect(('127.0.0.1', 7175))

            # Une fois connecté
            remote_socket = self.local_socket.getpeername()
            print("Connecté avec", remote_socket)
            
            # Réception du numéro de joueur
            b_reception = self.local_socket.recv(1)
            reception = b_reception.decode('ascii')
            self.joueur = int(reception)
        
        if self.joueur==1:
            self.mon_tour = True
        else:
            self.mon_tour = False
            
        self.reception = Reception(self)
        self.reception.start()

        # Contenu des cellules:
        # 0: case vide
        # 1: croix
        # 2: cercle
        self.plateau = [
          [0,0,0],
          [0,0,0],
          [0,0,0],
        ]
        self.fin = (False, 0)


    def maj(self, c, l):
        """
        Prendre en compte un coup sur la cellule
        de coordonnées c (colonne) et l (ligne)
        """
    
        # Vérifier que la case est libre
        if self.plateau[l][c]!=0:
            return
        else:
            if self.mon_tour:
                self.plateau[l][c] = self.joueur
            else:
                self.plateau[l][c] = 2-(self.joueur-1)
            # envoyer le message
            message = str(c) + str(l)
            b_message = bytes(message, 'ascii')
            self.local_socket.sendall(b_message)
            
        # Victoire ?
        self.fin = self.victoire()
        if self.fin[0]:
            self.mon_tour = False
        else: # Passer au joueur suivant
            self.mon_tour = not self.mon_tour
    
    def victoire(self):
        """
        Vérifier si un joueur a gagné
        """
        
        p  = self.plateau
        
        # Vérification des lignes et colonnes
        for i in range(3):
            if p[i][0]!=0 and p[i][0]==p[i][1]==p[i][2]:
                return (True, p[i][0])
            if p[0][i]!=0 and p[0][i]==p[1][i]==p[2][i]:
                return (True, p[0][i])
        # Vérifier les diagonales
        if p[0][0]!=0 and p[0][0]==p[1][1]==p[2][2]:
            return (True, p[0][0])
        if p[2][0]!=0 and p[2][0]==p[1][1]==p[0][2]:
            return (True, p[2][0])
        return (False, 0)
class Reception(Thread):
    def __init__(self,j):
        Thread.__init__(self)
        self.continuer = True
        self.jeu = j
    
    def stop(self):
        self.continuer = False
        
    def run(self):
        # Réception en continu
        while self.continuer:
            b_reception = self.jeu.local_socket.recv(2)
            recu = b_reception.decode('ascii')
            self.jeu.maj(int(recu[0]), int(recu[1]))