#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Labyrinth game"""

import os
import sys
from carte import Carte
from backup import Backup
from labyrinthe import Labyrinthe
from player import Player


dirCartes = "cartes"


def mapsLoad():
    cartes = []
    """Load maps list"""
    for nom_fichier in os.listdir(dirCartes):
        if nom_fichier.endswith(".txt"):
            chemin = os.path.join(dirCartes, nom_fichier)
            nom_carte = nom_fichier[:-3].lower()

            with open(chemin, "r") as fichier:
                contenu = fichier.read()
                nom_carte = Carte(nom_carte, contenu)
        cartes.append(nom_carte)
    return cartes


def mapsList(cartes):
    """Display maps list"""
    cartes = mapsLoad()
    print("Labyrinthes existants :")
    for i, carte in enumerate(cartes):
        print("  {} - {}".format(i + 1, carte.nom))


def validMapChoice(choice, givenChoices):
    """Check input given to choose a map
    ('int' in a range of maps expected)"""
    try:
        choice = int(choice)
    except:
        print("Entrez un chiffre")
        return False
    try:
        choice = int(choice)-1
        if choice not in range(0, len(givenChoices)):
            raise IndexError("Cartes possibles de 1 à {}".format(len(givenChoices)))
    except IndexError as error:
        print("Choix invalide. {}".format(error))
        return False
    return True


def main():
    """Main code of the game"""
    replay = 'n'
    # Si il y a une partie sauvegardée
    if Backup.exists():
        replay = input("Continuer dernière partie o/n?")
        while replay not in ['o', 'n']:
            replay = input("entrez 'o' pour oui / 'n' pour non :")
        if replay == 'o':
            game = Backup.restore()

    if replay != 'o':
        # Choix de la carte
        cartes = mapsLoad()
        mapsList(cartes)
        question = "Quelle No de carte pour jouer ?"
        mapChoice = input(question)
        mapIsPlayable = [False, False]

        # Check given choice and map integrity
        while mapIsPlayable != [True, True]:
            if validMapChoice(mapChoice, cartes):
                mapIsPlayable = [True, False]
                if Labyrinthe.validMapForLabytinth(cartes[int(mapChoice)-1].content):
                    mapIsPlayable[1] = True
            else:
                mapIsPlayable[0] = False

            if False in mapIsPlayable:
                mapChoice = input(question)

        mapToPlay = cartes[int(mapChoice)-1]
        player1 = Player()

        game = Labyrinthe(mapToPlay.content, player1)

    # Debut du jeu
    inputPlayer = ''
    while inputPlayer != 'Q':
        os.system("clear")
        print(game)
        inputPlayer = input('\nQuelle commande au robot (n,s,e,o) ?\n\
\'Q\' pour sauvergarder partie et quitter\n')
        # Si 'Q ou q' entré, sauvegarde et quitter la partie en cours
        if inputPlayer in ['Q', 'q']:
            Backup.save(game)
            sys.exit(0)
        else:
            game.moveRobot(inputPlayer)


if __name__ == '__main__':
    main()
