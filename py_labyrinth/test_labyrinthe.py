#!/usr/bin/python3
# -*-coding:Utf-8 -*

import unittest
from labyrinthe import Labyrinthe

class TestLabyrinthe(unittest.TestCase):

    """Test case for labyrinth"""

    def test_validMapForLabytinth(self):
        """Test if given string can become a valid labyrinth"""
        chaineGood = 'OOOO\nO .U\nOOOO'
        chaineBad = 'abcdO\nO .U\nOOOO'
        self.assertTrue(Labyrinthe.validMapForLabytinth(chaineGood))
        self.assertFalse(Labyrinthe.validMapForLabytinth(chaineBad))

    def test_strToCoordVal(self):
        """Test string to labyrinth dict coords transformation"""
        chaine = 'OOOO\nO .U\nOOOO'
        grid = Labyrinthe.strToCoordVal(chaine)
        expected = {(0, 1): 'O', (1, 2): ' ', (0, 0): 'O', (1, 1): 'O', (2, 1): 'O', (0, 2): 'O', (2, 0): '\n', (1, 3): '.', (2, 3): 'O', (1, 4): 'U', (2, 2): 'O', (2, 4): 'O', (1, 0): '\n', (0, 3): 'O'}
        self.assertEqual(grid, expected)
