#!/usr/bin/python3
# -*-coding:Utf-8 -*

import unittest
from game import roboc


class TestRoboc(unittest.TestCase):

    """Test case for client"""

    def test_valid_map_choice(self):
        map_list = ['1', '2', '3']
        self.assertFalse(roboc.valid_map_choice('k', map_list))
        self.assertFalse(roboc.valid_map_choice('9', map_list))
        self.assertTrue(roboc.valid_map_choice('2', map_list))
