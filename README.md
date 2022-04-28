# Configuration

Le fichier de configuration contient deux sections : _local_ et _voisin_.
- local : permet de définir certains paramètres pour le noeud. Ces paramètres sont les suivants :
  - Port : le port sur lequel le noeud doit écouter les messages.
  - Nom : le nom du noeud. Il permet de rendre les messages plus lisibles au lieu d'utiliser l'uuid des noeuds.
- voisin : ce sont les paramètres du noeud voisin. On y retrouve les paramètres suivants :
  - IP : l'adresse IP du noeud voisin
  - Port : le port sur lequel envoyer les messages

Le module config.py contient des fonctions qui permettent de récupérer les valeurs par défaut des différents paramètres.
