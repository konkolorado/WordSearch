"""
Implements key word search functionality
TODO
- Implement find_first_occurence or find_all_occurence
"""
import sys

import numpy as np

from SuffixTreeEfficient import SuffixTreeEfficient

class BaseWordSearch(object):

    def __init__(self, filename):
        self.grid = self._load_csv(filename)
        self.board = self.grid.copy()
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.suffix_trees = self._make_suffix_trees_from_grid()

    def __str__(self):
        # display self.text for all suffix trees
        s = ""
        for _type in self.suffix_trees:
            s = s + _type + "\n"
            for tree in self.suffix_trees[_type]:
                endchar = len(tree.text) - 1
                s = s + tree.text[:endchar] + "\n"

        endchar = len(s) - 1 # To chop off trailing newline
        return s[:endchar]

    def show_board(self, silent=False):
        """
        Display search results from all found words so far.
        Lowercased letters are letter which have been matched against.
        Can be run in silent mode to simply return the string
        representation of the board
        """
        s = ""
        for i in range(self.rows):
            for j in range(self.cols):
                s += self.board[i][j] + " "
            if i != self.rows - 1:
                s += "\n"
        if not silent:
            print(repr(s))
        return s

    def _load_csv(self, filename):
        grid = []
        infile = open(filename)
        for line in infile:
            line = line.strip().split(',')
            grid.append(line)
        infile.close()
        return np.array(grid)

    def _tree_setup(self, string):
        """
        Creates and initializes a SuffixTreeEfficient object given a
        string. Returns the object
        """
        st = SuffixTreeEfficient(string)
        st.create_suffix_tree()
        return st

    def _make_suffix_trees_from_grid(self):
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])
        rows = self._make_suffix_trees_from_rows(num_rows)
        cols = self._make_suffix_trees_from_cols(num_cols)
        diag_down = self._make_suffix_trees_from_diags_down(num_rows, num_cols)
        diag_up = self._make_suffix_trees_from_diags_up(num_rows, num_cols)
        return {"rows": rows, "cols": cols, "diag_down": diag_down, "diag_up": diag_up}

    def _make_suffix_trees_from_rows(self, num_rows):
        trees = []
        for i in range(num_rows):
            s = ''.join(self.grid[i])
            trees.append(self._tree_setup(s))
        return trees

    def _make_suffix_trees_from_cols(self, num_cols):
        trees = []
        grid_copy = self.grid.T
        for i in range(num_cols):
            s = ''.join(grid_copy[i])
            trees.append(self._tree_setup(s))
        return trees

    def _make_suffix_trees_from_diags_down(self, num_rows, num_cols):
        return self._diags_down(num_rows, num_cols)

    def _make_suffix_trees_from_diags_up(self, num_rows, num_cols):
        return self._diags_up(num_rows, num_cols)

    def _diags_down(self, num_rows, num_cols):
        trees = []
        for i in range(num_rows-1, -1, -1):
            diag = self._trace_diagonal_down_from(num_rows, num_cols, i, 0)
            trees.append(self._tree_setup(diag))
        for i in range(1, num_cols):
            diag = self._trace_diagonal_down_from(num_rows, num_cols, 0, i)
            trees.append(self._tree_setup(diag))
        return trees

    def _diags_up(self, num_rows, num_cols):
        trees = []
        for i in range(num_rows):
            diag = self._trace_diagonal_up_from(num_rows, num_cols, i, 0)
            trees.append(self._tree_setup(diag))
        for i in range(1, num_cols):
            diag = self._trace_diagonal_up_from(num_rows, num_cols, num_rows-1, i)
            trees.append(self._tree_setup(diag))
        return trees

    def _trace_diagonal_up_from(self, max_row, max_col, row, col):
        letters = []
        while row >= 0 and col < max_col:
            letters.append(self.grid[row][col])
            row -= 1
            col += 1
        return ''.join(letters)

    def _trace_diagonal_down_from(self, max_row, max_col, row, col):
        letters = []
        while row < max_row and col < max_col:
            letters.append(self.grid[row][col])
            row += 1
            col += 1
        return ''.join(letters)

    def find_word(self, word):
        """
        Looks for a given word in the grid. Returns a list of tuples,
        containing information about where the word begins and ends.
        The first item in the tuple is the word's beginning location,
        the second is the word's end location"
        """
        loc_info = []
        for tree_type in self.suffix_trees:
            for i, tree in enumerate(self.suffix_trees[tree_type]):
                result = tree.find_pattern(word)
                if result == []:
                    continue

                if tree_type == "rows":
                    for r in result:
                        beginning = (i, r)
                        end = (i, r + len(word))
                        loc_info.append( (beginning, end) )

                elif tree_type == "cols":
                    for r in result:
                        beginning = (r, i)
                        end = (r + len(word), i)
                        loc_info.append( (beginning, end) )

                elif tree_type == "diag_down":
                    row, col = self._diag_down_grid_loc_from_index(i)
                    for r in result:
                        coords = self._diag_down_get_coords(word, row, col, r)
                        loc_info.append( coords )

                elif tree_type == "diag_up":
                    row, col = self._diag_up_grid_loc_from_index(i)
                    for r in result:
                        coords = self._diag_up_get_coords(word, row, col, r)
                        loc_info.append( coords )

        self._update_board(loc_info)
        return loc_info

    def _diag_down_grid_loc_from_index(self, i):
        """
        Given an index (index in the diag_down suffix array), returns
        the corresponding grid row,col pair location where the match
        begins.
        """
        main_diag_pos = self.rows - 1
        if i < main_diag_pos:
            row = self.rows - i - 1
            col = 0
        elif i > main_diag_pos:
            row = 0
            col = i - main_diag_pos
        else:
            row = 0
            col = 0
        return row, col

    def _diag_down_get_coords(self, word, row, col, depth):
        """
        Given the location where the string occurs in the grid and
        the location in the down suffix array where the string begins,
        returns the word's beginning and end coordinates in the grid
        """
        beg_r, beg_c = self._diag_down_move_n(row, col, depth)
        end_r, end_c = self._diag_down_move_n(beg_r, beg_c, len(word))
        beginning = (beg_r, beg_c)
        end = (end_r, end_c)
        return beginning, end

    def _diag_up_get_coords(self, word, row, col, depth):
        """
        Given the location where the string occurs in the grid and
        the location in the up suffix array where the string begins,
        returns the word's beginning and end coordinates in the grid
        """
        beg_r, beg_c = self._diag_up_move_n(row, col, depth)
        end_r, end_c = self._diag_up_move_n(beg_r, beg_c, len(word))
        beginning = (beg_r, beg_c)
        end = (end_r, end_c)
        return beginning, end

    def _diag_up_grid_loc_from_index(self, i):
        """
        Given an index (index in the diag_up suffix array), returns
        the corresponding grid row,col pair location where the match
        begins.
        """
        main_diag_pos = self.rows - 1
        if i < main_diag_pos:
            row = i
            col = 0
        elif i > main_diag_pos:
            row = self.rows - 1
            col = i - main_diag_pos
        else:
            row = self.rows - 1
            col = 0
        return row, col

    def _diag_down_move_n(self, row, col, depth):
        """
        On a diagonal, moves the row, col variables depth positions
        down the diagonal
        """
        cur_row = row
        cur_col = col
        for i in range(depth):
            cur_row += 1
            cur_col += 1
        return cur_row, cur_col

    def _diag_up_move_n(self, row, col, depth):
        """
        On a diagonal, moves the row, col variables depth positions
        down the diagonal
        """
        cur_row = row
        cur_col = col
        for i in range(depth):
            cur_row -= 1
            cur_col += 1
        return cur_row, cur_col

    def find_words(self, words):
        self.locations = []
        for w in words:
            self.locations.append(self.find_word(w))
        return self.locations

    def build_string_from_coords(self, coords):
        """
        Given a coords tuple (the begining coords for a string and
        the end coords for a string), returns the found string
        """
        if self._in_row(coords):
            return self._recover_from_row(coords)
        elif self._in_col(coords):
            return self._recover_from_col(coords)
        elif self._in_diag_down(coords):
            return self._recover_from_diag_down(coords)
        elif self._in_diag_up(coords):
            return self._recover_from_diag_up(coords)
        else:
            return ""

    def _in_row(self, coords):
        """
        Returns true if a given coords is contained within a row
        """
        beg_row = coords[0][0]
        end_row = coords[1][0]
        return beg_row == end_row

    def _recover_from_row(self, coords):
        """
        Returns a string from the coords specified built with the grid
        """
        beg_row, beg_col = coords[0]
        end_row, end_col = coords[1]
        length = end_col - beg_col
        pattern = ""
        for i in range(length):
            pattern += self.grid[beg_row][beg_col]
            beg_col += 1
        return pattern

    def _in_col(self, coords):
        """
        Returns true if a given coords is contained within a column
        """
        beg_col = coords[0][1]
        end_col = coords[1][1]
        return beg_col == end_col

    def _recover_from_col(self, coords):
        """
        Returns a string from the coords specified built with the grid
        """
        beg_row, beg_col = coords[0]
        end_row, end_col = coords[1]
        length = end_row - beg_row
        pattern = ""
        for i in range(length):
            pattern += self.grid[beg_row][beg_col]
            beg_row += 1
        return pattern

    def _in_diag_down(self, coords):
        """
        Returns true if given coords are contained in a downwards
        diagonal
        """
        beg_row, beg_col = coords[0]
        end_row, end_col = coords[1]
        return beg_row < end_row and beg_col < end_col

    def _recover_from_diag_down(self, coords):
        """
        Returns a string spanning the coords specified built from
        the grid
        """
        beg_row, beg_col = coords[0]
        end_row, end_col = coords[1]
        length = end_row - beg_row
        pattern = ""
        for i in range(length):
            pattern += self.grid[beg_row][beg_col]
            beg_row += 1
            beg_col += 1
        return pattern

    def _in_diag_up(self, coords):
        """
        Returns true if given coords are contained in an upwards
        diagonal
        """
        beg_row, beg_col = coords[0]
        end_row, end_col = coords[1]
        return beg_row > end_row and beg_col < end_col

    def _recover_from_diag_up(self, coords):
        """
        Returns a string spanning the coords specified built from
        the grid
        """
        beg_row, beg_col = coords[0]
        end_row, end_col = coords[1]
        length = end_col - beg_col
        pattern = ""
        for i in range(length):
            pattern += self.grid[beg_row][beg_col]
            beg_row -= 1
            beg_col += 1
        return pattern

    def _update_board(self, loc_info):
        """
        Given a list of coordinates, finds which characters in the
        board the coordinates correspond to and lowercases them
        """
        for coord in loc_info:
            if self._in_row(coord):
                self._lowercase_in_row(coord)
            elif self._in_col(coord):
                self._lowercase_in_col(coord)
            elif self._in_diag_down(coord):
                self._lowercase_in_diag_down(coord)
            elif self._in_diag_up(coord):
                self._lowercase_in_diag_up(coord)
            else:
                sys.exit()

    def _lowercase_in_row(self, coord):
        beg_row, beg_col = coord[0]
        end_row, end_col = coord[1]
        length = end_col - beg_col
        for i in range(length):
            self.board[beg_row][beg_col] = self.board[beg_row][beg_col].lower()
            beg_col += 1

    def _lowercase_in_col(self, coord):
        beg_row, beg_col = coord[0]
        end_row, end_col = coord[1]
        length = end_row - beg_row

        for i in range(length):
            self.board[beg_row][beg_col] = self.board[beg_row][beg_col].lower()
            beg_row += 1

    def _lowercase_in_diag_down(self, coord):
        beg_row, beg_col = coord[0]
        end_row, end_col = coord[1]
        length = end_row - beg_row
        for i in range(length):
            self.board[beg_row][beg_col] = self.board[beg_row][beg_col].lower()
            beg_row += 1
            beg_col += 1

    def _lowercase_in_diag_up(self, coord):
        beg_row, beg_col = coord[0]
        end_row, end_col = coord[1]
        length = end_col - beg_col
        for i in range(length):
            self.board[beg_row][beg_col] = self.board[beg_row][beg_col].lower()
            beg_row -= 1
            beg_col += 1
