# -*- coding: utf-8 -*-
"""
This module contains the classes for Board and Node objects
"""
from itertools import product
import logging


class Board(object):
    """
    A board is a representation of a text file, and contains a matrix of Node objects
    :param board:
    """

    def __init__(self, board):
        """
        Initialize the board by creating the matrix
        """
        self.matrix = self.make_matrix(board)
        self.graph = self.make_graph(self.matrix)

    @staticmethod
    def make_matrix(board):
        """
        This function returns a matrix of Nodes based on an input string
        :param board:
        """

        # Create the initial character matrix
        matrix = [list(line) for line in board.split('\n')]

        # Transform to Node matrix
        for y in xrange(len(matrix)):
            for x in xrange(len(matrix[y])):
                matrix[y][x] = Node(x=x, y=y, c=matrix[y][x])

        return matrix

    @staticmethod
    def make_graph(matrix):
        """
        Create a dictionary of the nodes in the board matrix
        :param matrix: A two dimensional list of Node objects
        """

        graph = {}

        top = 0
        left = 0
        right = len(matrix[0]) - 1
        bottom = len(matrix) - 1

        logging.debug('Creating graph: %d,%d,%d,%d' % (left, top, right, bottom))

        for y in xrange(top, bottom):
            for x in xrange(left, right):
                graph[matrix[y][x]] = []
                for i, j in product([-1, 0, 1], [-1, 0, 1]):
                    if x == 0 and y == 0:
                        continue
                    if not (left <= x + i < right):
                        continue
                    if not (top <= y + j < bottom):
                        continue
                    if (abs(i) + abs(j) > 1):
                        continue
                    if not matrix[y+j][x+i].walkable:
                        continue

                    graph[matrix[y][x]].append(matrix[y+j][x+i])

        return graph

    def update_manhattan_distance(self):
        """
        This method will update manhattan distance on all Nodes
        """
        end = self.get_goal()
        for y in self.matrix:
            for x in y:
                x.h = Node.manhattan(x, end)


    def get_start(self):
        """
        Returns coordinates for the starting node
        """

        return self.get_point('A')

    def get_goal(self):
        """
        Returns coordinates for det goal node
        """

        return self.get_point('B')

    def get_point(self, node):
        """
        This function returns the x and y coordinates for a given node
        :param node: An instance of Node
        """
        for y in xrange(len(self.matrix)):
            for x in xrange(len(self.matrix[y])):
                if self.matrix[y][x].c == node:
                    return self.matrix[y][x]


class Node(object):
    """
    A Node is a representation of a tile on the game grid
    :param h: Distance from this node to goal node
    :param parent: A list of parents to this node used for traversal
    :param x: The X-coordinate of this node
    :param y: The Y-coordinate of this node
    :param c: The character used in the text file to represent this node
    """

    def __init__(self, h=0, parent=None, x=None, y=None, c=None):
        """
        Initialize a Node with the given values, set some inferrable values
        at start.
        """

        # Distance from node to goal node. Using Manhattan to get this value
        self.h = h

        # Movment cost from one node to another node. Values given i exercise
        self.g = 0

        # Cost to move to this node
        self.arc_cost = 0

        # F-value is G+H
        self.f = self.g + self.h

        # The previous node visited before this one
        self.parent = parent

        # x coordinate
        self.x = x

        # y coordinate
        self.y = y

        # Char represented in the map, '.', '#', A or B
        self.c = c

        self.walkable = True

        # Is the node walkable
        if self.c == '#':
            self.walkable = False
            self.color = 'black'

        # Add some colors to other states aswell
        elif self.c == '.':
            self.color = 'green'
            self.arc_cost = 1
        elif self.c == 'A':
            self.color = 'pink'
        elif self.c == 'B':
            self.color = 'red'

        else:

            # Establish weights and colors
            if self.c == 'w':
                self.arc_cost = 100
                self.color = 'blue'
            elif self.c == 'm':
                self.arc_cost = 50
                self.color = 'grey'
            elif self.c == 'f':
                self.arc_cost = 10
                self.color = 'green'
            elif self.c == 'g':
                self.arc_cost = 5
                self.color = 'lime green'
            elif self.c == 'r':
                self.arc_cost = 1
                self.color = 'brown'

    def update(self, new_g=0):
        """
        Update the F-value based on the G and H values
        """
        self.g = new_g
        self.f = self.g + self.h

    def __eq__(self, other):
        """
        Comparable function
        """

        return self.f == other.f

    def __lt__(self, other):
        """
        Compareble function
        """

        return self.f < other.f

    def __gt__(self, other):
        """
        Comparable function
        """

        return self.f > other.f

    @staticmethod
    def manhattan(start, end):
        """
        :param start: THe instance of the start node
        :param end: The instance of the end node
        :return: Returning the h value for a given node
        """

        xd = abs(end.x - start.x)
        yd = abs(end.y - start.y)

        return abs(xd) + abs(yd)

    def __unicode__(self):
        return 'Node %d,%d (%s)' % (self.x, self.y, self.color)

    def __repr__(self):
        return 'Node %d,%d (%s)' % (self.x, self.y, self.color)

    def __str__(self):
        return 'Node %d,%d (%s)' % (self.x, self.y, self.color)
