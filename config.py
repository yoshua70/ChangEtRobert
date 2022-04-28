import configparser

parser = configparser.ConfigParser()
parser.read("setup.ini")


def getDefaultNodePort():
    return int(parser['local']['Port'])


def getDefaultNodeName():
    return parser['local']['Nom']


def getDefaultNextNode():
    return (parser['voisin']['IP'], int(parser['voisin']['Port']))
