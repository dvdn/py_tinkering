#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""This module is for Player class"""


class Player:

    """Player Objet with position, sign & name"""

    def __init__(self, coords=(0, 0), sign='X', name='robot'):
        self.x = coords[0]
        self.y = coords[1]
        self.sign = sign
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

