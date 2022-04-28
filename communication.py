import socket
from typing import Tuple

HEADER = 1024
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = "!DISCONNECTED"


def receive(conn, addr, nextNode=socket.gethostbyname(socket.gethostname() + ".local")) -> str:
    """Fonction pour recevoir un message au travers d'un socket TCP/IP.

    Args:
        conn (socket): Un socket représentant une nouvelle connexion avec le client
        addr (Tuple[str, int]): Adresse de la machine client
        nextNode (str): Adresse ou envoyer un éventuel message

    Returns:
        str: Le message envoyé par le client
    """
    connected = True

    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg:
            # print(f"[{addr}] {msg}")
            if msg == DISCONNECTED_MESSAGE:
                print("[DECONNEXION] ...")
                connected = False
                send("!DISCONNECTED", nextNode)
            conn.close()

            return msg
    conn.close()


def send(msg: str, recv: Tuple[str, int]):
    """Envoie un message au travers d'un socket TCP/IP.

    Args:
        msg (str): Le message à envoyer
        recv (Tuple[str, int]): L'adresse et le port du destinataire
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(recv)

    message = msg.encode(FORMAT)
    client.send(message)
