import threading
from typing import Tuple
import uuid
import socket
from time import sleep
from communication import receive, send
from config import getDefaultNextNode, getDefaultNodeName, getDefaultNodePort


CHOICE_YES = ["Y", 'y', 'Yes', 'yes', 'O', 'o', 'Oui', 'oui']
CHOICE_NO = ["N", 'N', 'No', 'no', 'Non', 'non']


class Node():
    def __init__(self) -> None:
        self.uid = uuid.uuid1()
        self.participant = False
        self.leader = None
        self.name = getDefaultNodeName()
        self.ip = socket.gethostbyname(socket.gethostname() + ".local")
        self.port = getDefaultNodePort()
        self.addr = (self.ip, self.port)
        self.next = getDefaultNextNode()

    def __str__(self) -> str:
        return f"[{self.name}] {self.uid}\n{self.addr}"

    def getUid(self) -> uuid.UUID:
        return self.uid

    def getIp(self) -> str:
        return self.ip

    def getPort(self) -> int:
        return self.port

    def setPort(self, port: int) -> None:
        self.port = port

    def getAddr(self) -> Tuple[str, int]:
        return (self.getIp(), self.getPort())

    def getName(self) -> str:
        return self.name

    def setName(self, name: str) -> None:
        self.name = name

    def getLeader(self) -> str:
        return self.leader

    def setLeader(self, leader: str) -> None:
        self.leader = leader

    def getParticipant(self) -> bool:
        return self.participant

    def setParticipant(self, participant: bool) -> None:
        self.participant = participant

    def getNextNode(self) -> Tuple[str, int]:
        return self.next

    def setNextNode(self, next: Tuple[str, int]) -> None:
        self.next = next

    def showConfig(self) -> None:
        print("\nLa configuration par défaut du noeud est la suivante :")
        print(f"\tAdresse : {self.getIp()}")
        print(f"\tPort : {self.getPort()}")
        print(f"\tNom : {self.getName()}")
        print(f"\tNoeud suivant : {self.getNextNode()}")
        print("\n")

    def config(self) -> None:
        print("\n[CONFIGURATION] ⚙️ début de la configuration du noeud...")

        self.setName(input("Entrez un nom pour le noeud : "))

        print("Vous devez maintenant choisir un numéro de port, veuillez vous assurer que le port choisi est disponible.")
        self.setPort(int(input("Entrez un numéro de port : ")))

        nextIp = input("Entrez l'ip du noeud suivant : ")
        nextPort = int(input("Entrez le port du noeud suivant : "))
        self.setNextNode((nextIp, nextPort))

        print("Récapitulatif de la configuration :")
        self.showConfig()

        choixConfig = input("Accepter la configuration ? Oui(O)/non(n)")

        if choixConfig in CHOICE_YES:
            print("\n[CONFIGURATION] validation de la configuration...")
        else:
            self.config()

        print("\n")

    def listen(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(self.getAddr())

        server.listen()
        print(
            f"[LISTENING] le serveur est installé sur {self.addr[0]}:{self.addr[1]}")

        while True:
            conn, addr = server.accept()
            msg = receive(conn, addr, self.getNextNode())

            sleep(2)

            if msg:
                if msg == '!DISCONNECTED':
                    print("[ARRET] ...")
                    exit()
                msg_header = msg.split(" ")[0].strip("[]")
                msg_sender = msg.split(" ")[1].strip("[]")
                msg_body = msg.split(" ")[2]

                if msg_header == 'ELECTED':
                    self.setLeader(int(msg_body))
                    self.setParticipant(False)
                    if self.getUid().int == int(msg_body):
                        send("!DISCONNECTED", self.getNextNode())
                    send(msg, self.getNextNode())
                elif msg_header == 'ELECTION':
                    self.setParticipant(True)

                    if self.getUid().int > int(msg_body):
                        print(
                            f"[MESSAGE] De: {msg_sender} Contenu: {msg_body}")
                        print("L'uid reçu est inférieur à l'uid du noeud.")
                        print("Envoie de l'uid du noeud à la place de l'uid reçu.")
                        send(
                            f"[ELECTION] [{self.getName()}] {str(self.getUid().int)}", self.getNextNode())
                    elif self.getUid().int < int(msg_body):
                        print(
                            f"[MESSAGE] De: {msg_sender} Contenu: {msg_body}")
                        print("L'uid reçu est supérieur à l'uid du noeud.")
                        print("Transfert du message reçu.")
                        send(msg, self.getNextNode())
                    else:
                        print(
                            f"[MESSAGE] De: {msg_sender} Contenu: {msg_body}")
                        print("L'uid reçu est identique à l'uid du noeud.")
                        print("🏆 Le noeud est élu !")
                        send(
                            f"[ELECTED] [{self.getName()}] {str(self.getUid().int)}", self.getNextNode())
                else:
                    pass

    def start(self) -> None:
        print("[DEMARRAGE] ⚡ démarrage du noeud...")
        print("[CONFIGURATION] 🔌 configuration du noeud...")
        self.showConfig()

        choixConfig = input("Accepter la configuration ? Oui(O)/non(n)")

        if choixConfig in CHOICE_YES:
            print("[CONFIGURATION] validation de la configuration...")
        else:
            self.config()

        choixElection = input("[ELECTION] Démarrer l'élection ? Oui(O)/non(n)")

        if choixElection in CHOICE_YES:
            thread = threading.Thread(target=self.listen)
            thread.start()
            print("[ELECTION] ⚙️ ...")
            sleep(5)
            send(f"[ELECTION] [{self.name}] {str(self.uid.int)}", self.next)
        else:
            print("[ELECTION] en attente de réception d'un message...")
            thread = threading.Thread(target=self.listen)
            thread.start()
