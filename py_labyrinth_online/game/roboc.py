#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Labyrinth game"""

import os
import sys
from game.carte import Carte
from game.labyrinthe import Labyrinthe

DIR_CARTES = "{}/cartes".format(os.path.dirname(__file__))
MSG_MAP = "Quelle No de carte pour jouer ?"
MSG_MOVE =  "quelle commande au robot (n,s,e,o) ?\n'exit' pour quitter\n"


def mapsLoad():
    """
    Load maps list
    :return:
    """
    cartes = []
    for nom_fichier in os.listdir(DIR_CARTES):
        if nom_fichier.endswith(".txt"):
            chemin = os.path.join(DIR_CARTES, nom_fichier)
            nom_carte = nom_fichier[:-3].lower()

            with open(chemin, "r") as fichier:
                contenu = fichier.read()
                nom_carte = Carte(nom_carte, contenu)
        cartes.append(nom_carte)
    return cartes


def maps_list(cartes):
    """Display maps list"""
    # cartes = mapsLoad()
    print("Labyrinthes existants :")
    for i, carte in enumerate(cartes):
        print("  {} - {}".format(i + 1, carte.nom))


def valid_map_choice(choice, given_choices):
    """Check input given to choose a map
    ('int' in a range of maps expected)"""
    try:
        choice = int(choice)
    except ValueError:
        print("'{}' n'est pas dans la liste. Entrez un chiffre".format(choice))
        return False
    try:
        choice = int(choice)-1
        if choice not in range(0, len(given_choices)):
            raise IndexError("Cartes possibles de 1 à {}".format(len(given_choices)))
    except IndexError as error:
        print("Choix invalide. {}".format(error))
        return False
    return True


def server_selectmap():
    """select map on server side
    :return: Carte
    """
    # Choix de la carte
    cartes = mapsLoad()
    maps_list(cartes)
    map_choice = input(MSG_MAP)
    map_is_playable = [False, False]

    # Check given choice and map integrity
    while map_is_playable != [True, True]:
        if valid_map_choice(map_choice, cartes):
            map_is_playable = [True, False]
            if Labyrinthe.validmap_labyrinth(cartes[int(map_choice) - 1].content):
                map_is_playable[1] = True
        else:
            map_is_playable[0] = False

        if False in map_is_playable:
            map_choice = input(MSG_MAP)

    map_to_play = cartes[int(map_choice) - 1]

    return map_to_play


def init_game(map_to_play):
    return Labyrinthe(map_to_play.content)


def add_player_to_game(game, player_id):
    game.add_player(player_id)


def manage_players_addition(game, player_id):
    # print(repr(game.players))
    if player_id not in game.players:
        add_player_to_game(game, player_id)

def main():
    """Main code for single player game"""
    # Choix de la carte
    cartes = mapsLoad()
    maps_list(cartes)
    map_choice = input(MSG_MAP)
    map_is_playable = [False, False]

    # Check given choice and map integrity
    while map_is_playable != [True, True]:
        if valid_map_choice(map_choice, cartes):
            map_is_playable = [True, False]
            if Labyrinthe.validmap_labyrinth(cartes[int(map_choice)-1].content):
                map_is_playable[1] = True
        else:
            map_is_playable[0] = False

        if False in map_is_playable:
            map_choice = input(MSG_MAP)

    map_to_play = cartes[int(map_choice)-1]

    game = Labyrinthe(map_to_play.content)
    game.add_player('standalone')

    # Debut du jeu
    input_player = ''
    while input_player != 'exit':
        os.system("cls" if os.name == "nt" else "clear")
        print(game)
        input_player = input("Joueur 1 : {}".format(MSG_MOVE))

        # 'exit' quitter la partie en cours
        if input_player is 'exit':
            sys.exit(0)
        else:
            game.move_robot(input_player, 'standalone', 3)


if __name__ == '__main__':
    main()

    manage_players_addition = staticmethod(manage_players_addition)
    add_player_to_game = staticmethod(add_player_to_game)