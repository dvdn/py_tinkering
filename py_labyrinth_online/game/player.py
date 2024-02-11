#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""This module is for Player class"""


class Player:

    players_number = 0

    def __init__(self, coords=(0, 0), name='robot'):
        self.x = coords[0]
        self.y = coords[1]
        self.sign = self.manage_players_sign()
        self.name = name

    def __setattr__(self, attr, val):
        """Special method used when player.nom_attr = val_attr is asked.
        Check for coordinates type"""
        if attr in ['x', 'y']:
            try:
                object.__setattr__(self, attr, int(val))
            except ValueError:
                print('Player coordinates must be numbers')
        else:
            object.__setattr__(self, attr, val)

    @staticmethod
    def manage_players_sign():
        """Players counter, 9 maximum allowed
        :return: counter
        """
        if Player.players_number < 9:
            Player.players_number += 1
        else:
            raise Warning('You reached the maximum players allowed for the game')
        return str(Player.players_number)
