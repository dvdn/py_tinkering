#!/usr/bin/python3
# -*-coding:Utf-8 -*

import unittest
from game.labyrinthe import Labyrinthe

from contextlib import redirect_stdout
import io

VALID_CHAINE = 'OOOO\nO .U\nOOOO'

class TestLabyrinthe(unittest.TestCase):

    """Test case for labyrinth maps."""

    def test_validmap_labyrinth(self):
        """Test if given string can become a valid labyrinth"""
        chaineBad = 'abcdO\nO .U\nOOOO'
        self.assertTrue(Labyrinthe.validmap_labyrinth(VALID_CHAINE))
        self.assertFalse(Labyrinthe.validmap_labyrinth(chaineBad))

    def test_str_to_coord_val(self):
        """Test string to labyrinth dict coords transformation"""
        grid = Labyrinthe.str_to_coord_val(VALID_CHAINE)
        expected = {(0, 1): 'O', (1, 2): ' ', (0, 0): 'O', (1, 1): 'O', (2, 1): 'O', (0, 2): 'O', (2, 0): '\n', (1, 3): '.', (2, 3): 'O', (1, 4): 'U', (2, 2): 'O', (2, 4): 'O', (1, 0): '\n', (0, 3): 'O'}
        self.assertEqual(grid, expected)

    def test_can_move_nearby(self):
        """Test movement"""
        game = Labyrinthe(carte_str=VALID_CHAINE)
        # invalid move
        with self.assertRaises(ValueError):
            Labyrinthe.can_move_nearby(game, (0, 0), 's')
        # valid move returns nothing
        self.assertIsNone(Labyrinthe.can_move_nearby(game, (0, 2), 's'))

    def test_try_magic_nearby(self):
        """Test movement"""
        game = Labyrinthe(carte_str=VALID_CHAINE)
        # invalid
        with self.assertRaises(ValueError):
            Labyrinthe.try_magic_nearby(game, (0, 2), 'ps')
        # valid spell
        self.assertIsNone(Labyrinthe.try_magic_nearby(game, (1, 1), 'pn'))

    def test_try_direction_jump(self):
        """Test different movements"""
        game = Labyrinthe(carte_str=VALID_CHAINE)
        game.add_player('standalone')
        player1 = game.players['standalone']
        player1_coords = tuple([player1.x, player1.y])
        # display game
        # print('\n{}'.format(game))

        # invalid
        with self.assertRaises(ValueError):
            game.try_direction_jump(player1_coords, 'ss', player1)

        # valid obstacle
        self.assertIsNone(game.try_direction_jump(player1_coords, 'o2', player1))

        # valid spell, then move out of map, end of game (for standalone)
        game.try_magic_nearby(player1_coords, 'ps')
        with self.assertRaises(SystemExit):
            self.assertIsNone(game.try_direction_jump(player1_coords, 's', player1))