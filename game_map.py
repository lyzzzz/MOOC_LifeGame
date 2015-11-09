# -*- coding: utf-8 -*-
#
# @author lyzzzz

import random
import sys


class GameMap(object):
    
    MAX_MAP_SIZE = 100

    CELL_ALIVE = 1
    CELL_DEAD = 0
    CELL_WALL = -1
    POSSIBILITY_WALL = 0.2

    def __init__(self, rows, cols):
        """Inits GameMap with row and column count."""
        assert isinstance(rows, int)
        assert isinstance(cols, int)
        assert 0 < rows <= self.MAX_MAP_SIZE
        assert 0 < cols <= self.MAX_MAP_SIZE
        self.size = (rows, cols, )
        self.cells = [[0 for col in range(cols)] for row in range(rows)]

    @property
    def rows(self):
        return self.size[0]

    @property
    def cols(self):
        return self.size[1]

    def reset(self, possibility=0.5):
        """Reset the map with random data.

        Args:
            possibility: possibility of life cell
        """
        num_alive = (int)(possibility * 10)
        num_wall = (int)(self.POSSIBILITY_WALL * 10)
        num_dead = 10 - num_alive - num_wall
        temp = [self.CELL_ALIVE for _a in range(num_alive)] + [self.CELL_DEAD for _b in range(num_dead)] + \
            [self.CELL_WALL for _c in range(num_wall)]

        self.cells = [[temp[random.randint(0, 9)] for col in range(self.cols)] for row in range(self.rows)]

    def set(self, row, col, val):
        """Set specific cell in the map."""
        self.cells[row][col] = val

    def get_neighbor_count(self, row, col):
        """Get count of neighbors in specific cell.

        Args:
            row: row number
            col: column number

        Returns:
            Count of live neighbor cells

            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
            "up_left": (-1, -1),
            "up_right": (-1, 1),
            "down_left": (1, -1),
        """
        DIRECTION = {
            "up": (-1, 0),
            "up2": (-2, 0),
            "down": (1, 0),
            "down2": (2, 0),
            "left": (0, -1),
            "left2": (0, -2),
            "right": (0, 1),
            "right2": (0, 2),
        }

        counter = 0
        for dire in DIRECTION:
            trow = (row + DIRECTION[dire][0]) % self.rows
            tcol = (col + DIRECTION[dire][1]) % self.cols
            if self.cells[trow][tcol] == GameMap.CELL_ALIVE:
                counter += 1
        return counter

    def get_neighbor_count_map(self):
        """Get count of neighbors of every cell in the map.

        Returns:
            A grid contains every cell's neighbor count.
        """
        return [[self.get_neighbor_count(row, col) for col in range(self.cols)] for row in range(self.rows)]

    def print_map(self, cell_maps=None, sep=' ', fd=sys.stdout):
        """Print the map to target file descriptor

        Args:
            cell_maps: mapping from cell value to a string that will be displayed.
            sep: separator between cells of the same row.
            fd: file descriptor, default standard output
        """
        if not cell_maps:
            cell_maps = ['0', '1', '-1']
        assert isinstance(cell_maps, list) or isinstance(cell_maps, dict)
        assert isinstance(sep, str)
        for row in self.cells:
            m = map(lambda cell: cell_maps[cell], row)
            print(sep.join(m), file=fd)
            #print(sep.join(map(lambda cell: cell_maps[cell], row)), file=fd)
