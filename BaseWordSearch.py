"""
Implements key word search functionality
"""
import sys

import numpy as np

from SuffixTreeEfficient import SuffixTreeEfficient

class BaseWordSearch(object):

    def __init__(self, filename):
        self.grid = self._load_csv(filename)
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
                if result != []:
                    if tree_type == "rows":
                        continue
                        for r in result:
                            beginning = (i, r)
                            end = (i + len(word), r)
                            loc_info.append( (beginning, end) )

                    elif tree_type == "cols":
                        continue
                        for r in result:
                            beginning = (r, i)
                            end = (r , i + len(word))
                            loc_info.append( (beginning, end) )

                    elif tree_type == "diag_down":
                        continue
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
                        for r in result:
                            beg_r, beg_c = self._diag_down_move_n(row, col, r)
                            end_r, end_c = self._diag_down_move_n(beg_r, beg_c, len(word))
                            beginning = (beg_r, beg_c)
                            end = (end_r, end_c)
                            loc_info.append( (beginning, end) )

                    elif tree_type == "diag_up":
                        row, col = self._diag_up_grid_loc_from_index(i)
                        for r in result:
                            beg_r, beg_c = self._diag_up_move_n(row, col, r)
                            end_r, end_c = self._diag_up_move_n(beg_r, beg_c, len(word))
                            beginning = (beg_r, beg_c)
                            end = (end_r, end_c)
                            loc_info.append( (beginning, end) )
                            print(beginning, end)
        return loc_info

    def _diag_down_grid_loc_from_index(self, i):
        """
        Given an index (index in the diag_down suffix array), returns
        the corresponding grid row,col pair location where the match
        begins.
        """
        return ()

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
        return [[]]
