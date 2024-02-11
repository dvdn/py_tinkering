#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""Module containing Labyrinthe class"""

import time
import sys
import os
import re
import random
from collections import OrderedDict
from game.player import Player

WINDOOR_VAL = 'U'
DOOR_VAL = '.'
WALL_VAL = 'O'
END_LINE = '\n'
OBSTACLES = [WALL_VAL, END_LINE, '1', '2', '3', '4', '5', '6', '7', '8', '9']
MAGICABLES = [WALL_VAL, DOOR_VAL]
SPELL_WALLTODOOR = 'p'
SPELL_DOORTOWALL = 'm'
MAPPING_MOVES = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'o': (0, -1)}
PATTERN_MOVES = '^[n,s,e,o][0-9]{,1}$'
PATTERN_SPELL_DIRECTION = '^[m,p][n,s,e,o]$'
TIME_SLEEP = .8

MSG_MOVE_INFO = "- Déplacement : n, s, e ou o avec \
éventuellement un nombre de cases \n\
- Magie sur porte ou mur : 'm' murer ou 'p' percer \
avec la direction (n, s, e ou o)"

MSG_END_INFO = 'x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x\
\nx      Fin de la partie...      x\
\nx  Vous êtes tombé de la carte  x\
\nx-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x'

MSG_WIN_INFO = '*********************************\
\n*            Bravo !            *\
\n*   Vous avez réussi à sortir   *\
\n*********************************'



class Labyrinthe:

    """Labyrinthe class representation"""

    def __init__(self, carte_str, players = None, status = 'running'):
        self.grid = self.str_to_coord_val(carte_str)
        if players is None:
            players = dict()
        self.players = players
        self.status = status # info to share with all players

    @staticmethod
    def str_to_coord_val(chaine):
        """
        Transform a map/string into usable dict grid
        :param chaine:
        :return:
        """
        x, y = 0, 0
        coords = {}
        for c in chaine:
            if c == '\n':
                x += 1
                y = 0
            coords[x, y] = c
            y += 1
        return coords

    def add_player(self, player_id):
        """
        Add player into game, max. 9 allowed
        :param player_id:
        :return:
        """
        try:
            player = Player(name=player_id)
            # no need to repeat 'self' at method call
            # https://stackoverflow.com/questions/23944657/typeerror-method-takes-1-positional-argument-but-2-were-given
            self.start_player(player)
            self.players[player_id] = player
        except Warning as warning:
            print('[Warning]. {}'.format(warning))

    def init_players(self, players_ids):
        for player_id in players_ids:
           self.add_player(player_id)

    @staticmethod
    def validmap_labyrinth(chaine):
        """
        Is it a valid string to be a map
        :param chaine:
        :return:
        """
        charsValidMap = list()
        for c in OBSTACLES:
            charsValidMap.extend(c)
        charsValidMap.extend((DOOR_VAL, WINDOOR_VAL, ' '))
        try:
            for e in chaine:
                if e not in charsValidMap:
                    raise ValueError('cette carte contient \
au moins un caractère invalide : \'{}\''.format(e))
        except ValueError as error:
            print('[Erreur]. {}'.format(error))
            return False
        return True

    def start_player(self, player):
        """
        Init player coords
        from map grid if already there or random on grid
        :param player:
        :return:
        """
        if player.x == 0 and player.y == 0:  # init
            # print(list(self.grid.values()))
            if player.sign in list(self.grid.values()):  # if it's sign already on map
                Xidx = list(self.grid.values()).index(player.sign)
                robot_coord = list(self.grid.keys())[Xidx]
            else:  # random position
                empty_areas = [idx for idx, val in enumerate(self.grid.values()) if val == ' ']
                robot_coord = list(self.grid.keys())[random.choice(empty_areas)]
        player.x = robot_coord[0]
        player.y = robot_coord[1]

        self.grid[tuple([player.x, player.y])] = player.sign  # put on map
        return player

    def move_robot(self, command, player_id, time_seconds=0):
        """Move robot in a specific direction and check given command"""
        player = self.players[player_id]
        try:
            expected_patterns = [PATTERN_MOVES, PATTERN_SPELL_DIRECTION]
            self.input_check_patterns(command, expected_patterns, MSG_MOVE_INFO)

            if self.input_check_patterns(command, expected_patterns, MSG_MOVE_INFO) == PATTERN_MOVES:
                self.try_direction_jump(tuple([player.x, player.y]), command, player)
            elif self.input_check_patterns(command, expected_patterns, MSG_MOVE_INFO) == PATTERN_SPELL_DIRECTION:
                self.try_spell_direction(tuple([player.x, player.y]), command)

        except ValueError as error:
            print("La commande saisie est invalide.\n{}".format(error))
            time.sleep(time_seconds)

    def try_direction_jump(self, coord, directionJump, player):
        """
        Try to move a thing in a specific direction, managing OBSTACLES
        :param coord:
        :param directionJump:
        :param player:
        :return:
        """
        direction = directionJump[0]
        try:
            jump = int(directionJump[1])
        except IndexError:
            jump = 1

        original_coord = coord
        try:
            print('Essai de mouvement...')
            for i in range(jump):
                self.can_move_nearby(coord, direction)

                # moving position attempt
                nextCoords = tuple([sum(x) for x in zip(coord, MAPPING_MOVES[direction])])

                # manage y position for first line map
                if (nextCoords[0] == 0):
                    nextCoords = self.manage_map_fisrtline(nextCoords)

                if self.grid[nextCoords] == DOOR_VAL:
                    print('. porte traversée')
                    time.sleep(.2)
                    nextCoords = tuple([sum(x) for x in zip(nextCoords, MAPPING_MOVES[direction])])

                    if nextCoords not in self.grid or self.grid[nextCoords] == END_LINE:
                        self.manage_end_of_game(MSG_END_INFO)

                elif self.grid[nextCoords] == WINDOOR_VAL:
                    self.manage_end_of_game(MSG_WIN_INFO)
                    raise UserWarning('**********************************\
\n*   Joueur {} a réussi à sortir   *\
\n**********************************'.format(player.sign))

                print('hop, ', end='')
                time.sleep(.2)
                self.grid[coord] = ' '
                self.grid[nextCoords] = player.sign
                player.x = nextCoords[0]
                player.y = nextCoords[1]
                coord = nextCoords  # step done
        except ValueError as error:
            print('\nOups : {}'.format(error))
            time.sleep(TIME_SLEEP)
            self.grid[coord] = ' '
            self.grid[original_coord] = player.sign
            player.x = original_coord[0]
            player.y = original_coord[1]
        else:
            print('ok')

    def can_move_nearby(self, coord, direction):
        """
        Can it move 1 step nearby ?
        :param coord:
        :param direction:
        :return:
        """
        # sum robot coords + direction to get nearby_coords
        nearby_coords = tuple([sum(x) for x in zip(coord, MAPPING_MOVES[direction])])

        # manage y position for first line map
        if (nearby_coords[0] == 0):
            nearby_coords = self.manage_map_fisrtline(nearby_coords)

        if self.grid[nearby_coords] in OBSTACLES:
            raise ValueError('obstacle sur votre chemin \n\
-> tentez un autre mouvement')

    def try_spell_direction(self, coord, spell_direction):
        """
        Try to modify an obstacle in a specific direction
        :param coord:
        :param spell_direction:
        :return:
        """
        try:
            print('Essai de pouvoir magique...')
            self.try_magic_nearby(coord, spell_direction)
        except ValueError as error:
            print('Oups : {}'.format(error))
            time.sleep(TIME_SLEEP)
        else:
            print('ok')

    def try_magic_nearby(self, coord, spell_direction):
        """
        Try magic spell nearby
        :param coord:
        :param spell_direction:
        :return:
        """
        spell = spell_direction[0]
        direction = spell_direction[1]
        # sum robot coords + direction to get nearby_coords
        nearby_coords = tuple([sum(x) for x in zip(coord, MAPPING_MOVES[direction])])
        nearby_coords_val = self.grid[nearby_coords]
        self.can_magic_nearby(nearby_coords_val)

        # manage y position for first line map
        if nearby_coords[0] == 0:
            nearby_coords = self.manage_map_fisrtline(nearby_coords)

        # manage spell
        if nearby_coords_val == WALL_VAL and spell == SPELL_WALLTODOOR:
            self.grid[nearby_coords] = DOOR_VAL
        elif nearby_coords_val == DOOR_VAL and spell == SPELL_DOORTOWALL:
            self.grid[nearby_coords] = WALL_VAL
        else:
            raise ValueError('commande magique non permise ici\n\
-> tentez autre chose')
        time.sleep(TIME_SLEEP)

    @staticmethod
    def manage_map_fisrtline(nearby_coords):
        """
        manage y position for first line map
        as no offset by /n
        :param nearby_coords:
        :return: tuple coordinates of first line
        """
        firstline_coords = tuple([nearby_coords[0], nearby_coords[1] - 1])
        return firstline_coords

    @staticmethod
    def can_magic_nearby(nearby_coords_val):
        """Can it magic nearby ?"""
        if nearby_coords_val not in MAGICABLES:
            raise ValueError('pas de magie possible ici\n\
-> tentez autre chose')

    @staticmethod
    def input_check_patterns(given, expected_patterns, message):
        errors = 0
        for i, expected_ptern in enumerate(expected_patterns):
            pattern_compiled = re.compile(expected_ptern)
            if not re.match(pattern_compiled, given):
                errors += 1
            else:
                matched_ptern = expected_ptern

        if errors == len(expected_patterns):
            raise ValueError(message)
        return matched_ptern

    def manage_end_of_game(self, msg):
        """
        Manage end of game if standalone or online
        :param msg:
        :return:
        """
        os.system("cls" if os.name == "nt" else "clear")
        print(msg)
        time.sleep(1)
        if len(self.players) == 1 and 'standalone' in self.players:
            sys.exit()

    def __repr__(self):
        """Labyrinth sorted representation"""
        str_map = ''
        # sort tuples of the grid by first coord
        sorted_grid = OrderedDict(sorted(self.grid.items(), key=lambda t: t[0]))
        for key, value in sorted_grid.items():
            str_map += (value)
        return str_map
