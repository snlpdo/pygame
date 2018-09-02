from threading import Thread
import random
import socket
import struct
import time

from lettre import *

class Reseau():
    def __init__(self, args):
        if args.serveur: # Mode serveur     
            print("\n=== Mode réseau (serveur)===")

            balise = Balise('rgscrabble')
            balise.start()

            print("Attente de connexion...")
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ss.bind( ('', 7175) )
            ss.listen(args.nombre_joueurs-1) # 1 seul client pour le moment
            self.sock, dist_sock = ss.accept()
            print('Client connecté')
            balise.stop()

        elif args.client: # Mode client
            print('\n=== Mode réseau (client)===')

            ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ss.bind(('224.1.1.1', 7175))
            mreq = struct.pack("4sl", socket.inet_aton('224.1.1.1'), socket.INADDR_ANY)
            ss.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            received = False
            while not(received):
                message, address = ss.recvfrom(128)
                message = message.decode('ascii')
                if 'rgscrabble' in message:
                    print('Balise reçue')
                    received = True

            print('Connexion au serveur ')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect( (address[0], 7175))
            print('Connecté au serveur')

    def init_communication(self, args, jeu):
        """ Communication initiale entre le serveur et le client
        pour partager les informations de départ du jeu. """

        for i in range(4):
            # Envoi pseudo
            if i==0 and args.serveur or i==1 and not(args.serveur): 
                self.envoyer('pseudo', args.pseudo)

            # Réception pseudo
            elif i==1 and args.serveur or i==0 and not(args.serveur): 
                param, remote_pseudo = self.recevoir()
                if param!='pseudo':
                    print('Reçu paramètre ' + param + ' au lieu de pseudo')
                    quit()

            # Envoi nombre aléatoire
            elif i==2 and args.serveur or i==3 and not(args.serveur): 
                if args.serveur and args.input: # Pour le serveur
                    if jeu.local_is_playing():
                        local_rand = 1.5 # prise de la main par le serveur
                    else:
                        local_rand = -0.5 # prise de la main par l'adversaire
                else: # Pour le client
                    local_rand = random.random() # prise de la main aléatoire
                self.envoyer('priority', str(local_rand))

            # Réception nombre aléatoire
            elif i==3 and args.serveur or i==2 and not(args.serveur): 
                param, remote_rand = self.recevoir()
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
            jokers = ""
            if len(jeu.jokers)>=1:
                jokers += jeu.jokers[0].joker_char
            if len(jeu.jokers)>=2:
                jokers += jeu.jokers[1].joker_char
            num_adversaire = (jeu.joueur_local%2)+1
            ch1 = [ l.char for l in jeu.joueurs[0].chevalet[0] if l!=None ]
            ch2 = [ l.char for l in jeu.joueurs[1].chevalet[0] if l!=None ]

            self.envoyer_multiple(['grille', 'jokers', 'numero', 'ch1', 'ch2', 
                'sc1', 'sc2', 'tour'], 
                [''.join(msg), jokers, str(num_adversaire),''.join(ch1),''.join(ch2), 
                 str(jeu.joueurs[0].score), str(jeu.joueurs[1].score), 
                 str(jeu.tour_jeu)])

            # attendre l'ack du client
            self.recevoir() 

        else: # client
            # Réception de la grille, du numéro de joueur à utiliser, des chevalets,
            # des scores et du numéro de tour de jeu
            messages = self.recevoir_multiple()

            for message in messages:
                message = message.split('=')

                if message[0]=='grille':
                    rgrille = message[1]
                    for idx in range(15*15):
                        j = idx%15
                        i = idx//15
                        if rgrille[idx]==' ':
                            jeu.grille[i][j] = ''
                        else:
                            jeu.grille[i][j] = rgrille[idx]

                        if jeu.grille[i][j] != '': # affecter au 1er joueur
                            lettre = jeu.creer_lettre(jeu.grille[i][j])
                            lettre.pos = jeu.get_cell_name(j, i)
                            # L'attribuer arbitrairement au 1er joueur
                            jeu.joueurs[0].provisoire.append(lettre)
                            if rgrille[idx]=='?':
                                jeu.jokers.append(lettre)

                elif message[0]=='jokers': # ĺe numéro du joueur local
                    if len(message[1])>=1:
                        jeu.jokers[0].joker_char = message[1][0]
                    if len(message[1])>=2:
                        jeu.jokers[1].joker_char = message[1][0]
                    num_adversaire = (jeu.joueur_local%2)+1

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
        jeu.get_local_player().pseudo = args.pseudo
        jeu.joueurs[num_adversaire-1].pseudo = remote_pseudo

        # Déterminer le 1er joueur (tirage au sort le plus grand)
        if local_rand > remote_rand:
            jeu.joueur_actuel = jeu.joueur_local
        else:
            jeu.joueur_actuel = (jeu.joueur_local%2)+1

        # Modifier les pseudos si identiques
        if jeu.get_local_player().pseudo==jeu.joueurs[num_adversaire-1].pseudo:
            jeu.joueurs[0].pseudo += '1'
            jeu.joueurs[1].pseudo += '2'

    def demarrer_ecoute(self, jeu, plateau):
        """ Lancer le thread d'écoute et d'analyse continue. """

        self.reception = Reception(self, jeu, plateau)
        self.reception.start()

    def envoyer(self, param, valeur):
        """ Envoyer un message de la forme <param>=<valeur> à un pair. Le
        message est précédé d'un en-tête de 2 octets qui indique le nombre d'octets
        qui suivent. """

        message = bytes(param + '=' + valeur, 'ascii')
        l = len(message).to_bytes(2, byteorder='big')
        self.sock.sendall(l+message)
        print('[->'+str(len(message))+']', message)

    def envoyer_multiple(self, params, valeurs):
        """ Envoyer plusieurs messages de la forme <param>=<valeur>
        concaténés par '&' à un pair. Ces messages sont précédés d'un en-tête 
        de 2 octets qui indique le nombre d'octets qui suivent. """

        message = ''
        for i in range(len(params)):
            message += params[i] + '=' + valeurs[i]
            if i<len(params)-1:
                message += '&'
        message = bytes(message, 'ascii')
        l = len(message).to_bytes(2, byteorder='big')
        self.sock.sendall(l+message)
        print('[->'+str(len(message))+']', message)

    def recevoir(self):
        """ Récupérer un message au format <param>=<valeur> auprès du pair. 
        Le message est précédé d'un en-tête de 2 octets indiquant le nombre
        d'octets qui suivent. """

        nbBytes = int.from_bytes(self.sock.recv(2), 'big')
        message = self.sock.recv(nbBytes).decode('ascii').split('=')
        print('[<-'+str(nbBytes)+']', message)
        return message

    def recevoir_multiple(self):
        """ Récupérer plusieurs messages au format <param>=<valeur> concaténés
        par un '&' auprès du pair. 
        Ces messages sont précédés d'un en-tête de 2 octets indiquant le nombre
        d'octets qui suivent. """

        nbBytes = int.from_bytes(self.sock.recv(2), 'big')
        message = self.sock.recv(nbBytes).decode('ascii').split('&')
        print('[<-'+str(nbBytes)+']', message)
        return message

class Balise(Thread):
    def __init__(self, message):
        Thread.__init__(self)
        self.message = message
        self.continuer = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        while self.continuer:
            print("Émission balise")
            sock.sendto(bytes(self.message, 'ascii'), ('224.1.1.1', 7175))
            time.sleep(1) # 1s

    def stop(self):
        self.continuer = False


class Reception(Thread):
    def __init__(self, reseau, jeu, plateau):
        Thread.__init__(self)
        self.reseau = reseau
        self.continuer = True
        self.jeu = jeu
        self.plateau = plateau
        self.reseau.sock.settimeout(3) # 3s

    def run(self):
        while self.continuer:
            messages = []
            try:
                messages = self.reseau.recevoir_multiple()
            except socket.timeout: # timeout
                pass
            except:
                raise

            # numéro de joueur de l'adversaire
            if self.jeu.joueur_local==1:
                joueur_num = 2
            else:
                joueur_num = 1

            for message in messages:
                message = message.split('=')

                if message[0]=='move': # Déplacer une pièce

                    # Identifier les cases de départ et d'arrivée
                    move = message[1].split(',')
                    src = move[0]
                    dst = move[1]

                    # Récupérer la pièce concernée
                    if src[0]=='Q': # pièce depuis le chevalet
                        piece = self.jeu.joueurs[joueur_num-1].chevalet[0][int(src[1:])-4]
                    else: # pièce déjà sur le plateau
                        for l in self.jeu.joueurs[joueur_num-1].provisoire:
                            if l.pos == src:
                                piece = l
                                break

                    # Effectuer le déplacement
                    self.jeu.deplacer_piece(joueur_num, dst, piece, True)

                elif message[0]=='validation': # Valider le coup en cours
                    self.jeu.valider(joueur_num)
                    self.plateau.memoriser(self.jeu.joueurs[joueur_num-1])

                elif message[0]=='tirage': # Tirage au sort de l'adversaire (un coup a été joué)
                    # Ne pas prendre en compte les tirages vides (quand plus aucune lettre
                    # dans la pioche) ou la fin de partie 
                    if len(message[1])>0 and message[1][0]!="#" or message[1]=='':
                        self.jeu.affecter_tirage(self.jeu.joueur_actuel, message[1], True)

                elif message[0]=='detail_coup': # Détail du coup joué
                    nom = self.jeu.joueurs[self.jeu.joueur_actuel-1].pseudo
                    self.plateau.set_message(nom+' a fait ' + message[1], 'info', infinite=True)

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
