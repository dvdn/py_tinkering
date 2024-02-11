#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Class to manage game backup"""

import labyrinthe
import pickle
import os.path

filename = 'game.sav'


class Backup:

    def save(labyrinthe):
        with open(filename, 'wb') as fichier:
            data = pickle.Pickler(fichier)
            data.dump(labyrinthe)

    def restore():
        with open(filename, 'rb') as fichier:
            getData = pickle.Unpickler(fichier)
            return getData.load()

    def exists():
        return os.path.isfile(filename)

    if __name__ == '__main__':
        # save('test')
        print(restore())
