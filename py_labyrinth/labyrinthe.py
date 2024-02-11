#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""Module containing Labyrinthe class"""

import time
import sys
import os
import re
import random
from collections import OrderedDict

windoorVal = 'U'
doorVal = '.'
wallVal = 'O'
end_line = '\n'
obstacles = [wallVal, end_line]
magicables = [wallVal, doorVal]
spell_walltodoor = 'p'
spell_doortowall = 'm'
mappingMoves = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'o': (0, -1)}
patternMoves = '^[n,s,e,o][0-9]{,1}$'
pattern_spell_direction = '^[m,p][n,s,e,o]$'
timeSleep = .8


class Labyrinthe:

    """Labyrinthe class representation"""

    def __init__(self, carteStr, player1):
        self.grid = self.strToCoordVal(carteStr)
        self.player = self.startPlayer(self, player1)

    def strToCoordVal(chaine):
        """Transform a map/string into usable dict grid"""
        x, y = 0, 0
        coords = {}
        for c in chaine:
            if c == '\n':
                x += 1
                y = 0
            coords[x, y] = c
            y += 1
        return coords

    def validMapForLabytinth(chaine):
        charsValidMap = list()
        for c in obstacles:
            charsValidMap.extend(c)
        charsValidMap.extend((doorVal, windoorVal, ' ', 'X'))
        try:
            for e in chaine:
                if e not in charsValidMap:
                    raise ValueError('cette carte contient \
au moins un caractère invalide : \'{}\''.format(e))
        except ValueError as error:
            print('[Erreur]. {}'.format(error))
            return False
        return True

    def startPlayer(self, player):
        """Init player coords
        from map grid if already there or random on grid"""
        if player.x == 0 and player.y == 0:  # init
            print('init')
            if player.sign in list(self.grid.values()):  # X already on map
                Xidx = list(self.grid.values()).index(player.sign)
                robotCoord = list(self.grid.keys())[Xidx]
            else:  # random position
                emptyPlaces = [idx for idx, val in enumerate(self.grid.values()) if val == ' ']
                robotCoord = list(self.grid.keys())[random.choice(emptyPlaces)]
        player.x = robotCoord[0]
        player.y = robotCoord[1]

        self.grid[tuple([player.x, player.y])] = player.sign  # put on map
        return player

    def moveRobot(self, command):
        """Move robot in a specific direction and check given command"""
        try:
            message_error = "- Déplacement : n, s, e ou o avec \
éventuellement un nombre de cases \n\
- Magie sur porte ou mur : 'm' murer ou 'p' percer \
avec la direction (n, s, e ou o)"

            expected_patterns = [patternMoves, pattern_spell_direction]
            self.inputCheckPatterns(command, expected_patterns, message_error)

            if self.inputCheckPatterns(command, expected_patterns, message_error) == patternMoves:
                self.tryDirectionJump(tuple([self.player.x, self.player.y]), command)
            elif self.inputCheckPatterns(command, expected_patterns, message_error) == pattern_spell_direction:
                self.try_spell_direction(tuple([self.player.x, self.player.y]), command)

        except ValueError as error:
            print("La commande saisie est invalide.\n{}".format(error))
            time.sleep(timeSleep*3)

    def tryDirectionJump(self, coord, directionJump):
        """Try to move a thing in a specific direction,
            managing obstacles"""
        direction = directionJump[0]
        try:
            jump = int(directionJump[1])
        except IndexError:
            jump = 1

        try:
            print('Essai de mouvement...')
            originalCoord = coord
            for i in range(jump):
                self.canMoveNearby(coord, direction)

                # moving position attempt
                nextCoords = tuple([sum(x) for x in zip(coord, mappingMoves[direction])])

                # manage y position for first line map
                if (nextCoords[0] == 0):
                    nextCoords = self.manage_map_fisrtline(nextCoords)

                if self.grid[nextCoords] == doorVal:
                    print('. porte traversée')
                    time.sleep(.2)
                    nextCoords = tuple([sum(x) for x in zip(nextCoords, mappingMoves[direction])])

                    if nextCoords not in self.grid or self.grid[nextCoords] == end_line:
                        self.message_end()

                elif self.grid[nextCoords] == windoorVal:
                    self.message_win()

                print('. 1 pas')
                time.sleep(.2)
                self.grid[coord] = ' '
                self.grid[nextCoords] = self.player.sign
                self.player.x = nextCoords[0]
                self.player.y = nextCoords[1]
                coord = nextCoords  # step done

        except ValueError as error:
            print('Oups : {}'.format(error))
            time.sleep(timeSleep)
            self.grid[coord] = ' '
            self.grid[originalCoord] = self.player.sign
            self.player.x = originalCoord[0]
            self.player.y = originalCoord[1]

    def canMoveNearby(self, coord, direction):
        """Can it move 1 step nearby ?"""
        # sum robot coords + direction to get nearbyCoords
        nearbyCoords = tuple([sum(x) for x in zip(coord, mappingMoves[direction])])

        # manage y position for first line map
        if (nearbyCoords[0] == 0):
            nearbyCoords = self.manage_map_fisrtline(nearbyCoords)

        if self.grid[nearbyCoords] in obstacles:
            raise ValueError('obstacle sur votre chemin \n\
-> tentez un autre mouvement')

    def try_spell_direction(self, coord, spell_direction):
        """Try to modify an obstacle in a specific direction"""
        try:
            print('Essai de pouvoir magique...')
            self.try_magic_nearby(coord, spell_direction)
        except ValueError as error:
            print('Oups : {}'.format(error))
            time.sleep(timeSleep)

    def try_magic_nearby(self, coord, spell_direction):
        """Try magic spell nearby"""
        spell = spell_direction[0]
        direction = spell_direction[1]
        # sum robot coords + direction to get nearbyCoords
        nearbyCoords = tuple([sum(x) for x in zip(coord, mappingMoves[direction])])
        nearby_coords_val = self.grid[nearbyCoords]
        self.can_magic_nearby(nearby_coords_val)

        # manage y position for first line map
        if (nearbyCoords[0] == 0):
            nearbyCoords = self.manage_map_fisrtline(nearbyCoords)

        # manage spell
        if nearby_coords_val == wallVal and spell == spell_walltodoor:
            self.grid[nearbyCoords] = doorVal
        elif nearby_coords_val == doorVal and spell == spell_doortowall:
            self.grid[nearbyCoords] = wallVal
        else:
            raise ValueError('commande magique non permise ici\n\
-> tentez autre chose')
        time.sleep(timeSleep)

    def manage_map_fisrtline(nearbyCoords):
        """manage y position for first line map
        as no offset by /n"""
        firstline_coords = tuple([nearbyCoords[0], nearbyCoords[1] - 1])
        return firstline_coords

    def can_magic_nearby(self, nearby_coords_val):
        """Can it magic nearby ?"""
        if nearby_coords_val not in magicables:
            raise ValueError('pas de magie possible ici\n\
-> tentez autre chose')

    def inputCheckPatterns(given, expected_patterns, message):
        errors = 0
        for i, expected_ptern in enumerate(expected_patterns):
            patternCompiled = re.compile(expected_ptern)
            if not re.match(patternCompiled, given):
                errors += 1
            else:
                matched_ptern = expected_ptern

        if errors == len(expected_patterns):
            raise ValueError(message)
            return False
        return matched_ptern

    def inputCheckPattern(given, expectedPattern, message):
        patternCompiled = re.compile(expectedPattern)
        if not re.match(patternCompiled, given):
            raise ValueError(message)
            return False
        return True

    def message_win():
        os.system("clear")
        print('*********************************')
        print('*            Bravo !            *')
        print('*   Vous avez réussi à sortir   *')
        print('*********************************')
        # TODO rejouer ?
        time.sleep(1)
        sys.exit()

    def message_end():
        os.system("clear")
        print('x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
        print('x      Fin de la partie...      x')
        print('x  Vous êtes tombé de la carte  x')
        print('x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
        # TODO rejouer ?
        time.sleep(1)
        sys.exit()

    def __repr__(self):
        """Labyrinth sorted representation"""
        strMap = ''
        # sort tuples of the grid by first coord
        sortedGrid = OrderedDict(sorted(self.grid.items(), key=lambda t: t[0]))
        for key, value in sortedGrid.items():
            strMap += (value)
        return strMap

    strToCoordVal = staticmethod(strToCoordVal)
    validMapForLabytinth = staticmethod(validMapForLabytinth)
    startPlayer = staticmethod(startPlayer)
    inputCheckPattern = staticmethod(inputCheckPattern)
    inputCheckPatterns = staticmethod(inputCheckPatterns)
    message_end = staticmethod(message_end)
    manage_map_fisrtline = staticmethod(manage_map_fisrtline)
