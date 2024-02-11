#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""


class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""

    def __init__(self, nom, chaine):
        self.nom = nom
        self.content = chaine

    def __repr__(self):
        return "<Carte {}>".format(self.nom)


