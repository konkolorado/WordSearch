"""
Efficient construction of a SuffixTree for a string
Builds a suffix tree from suffix array in linear time
Can build a suffix tree from scratch in S*log(S) time
"""

from SuffixArrayEfficient import SuffixArrayEfficient
from SuffixTreeNode import SuffixTreeNode

class SuffixTreeEfficient(object):
    def __init__(self, text, terminal="$"):
        self.text = text + terminal
        self.suffix_array = SuffixArrayEfficient(text).build_suffix_array()
        self.lcp_array = self._compute_lcp_array()

    def __str__(self):
        return "Text:" + self.text + "\nSuffixArray:" + str(self.suffix_array)

    def _invert_suffix_array(self, order):
        pos = [0] * len(order)
        for i in range(len(order)):
            pos[order[i]] = i
        return pos

    def _lcp_of_suffixes(self, S, i, j, equal):
        lcp = max(0, equal)
        while i + lcp < len(S) and j + lcp < len(S):
            if S[i+lcp] == S[j+lcp]:
                lcp += 1
            else:
                break
        return lcp

    def _compute_lcp_array(self):
        """
        Computes the least common prefixes among all suffixes. For each
        number at location i in the array, this represents the number of
        common characters in a prefix between suffix at position i and
        suffix at position i + 1.
        For example
        - suffix array = [$, a$, aa$, bb$, bbb$]
        - lcp array = [0, 1, 0, 2]
        """
        lcp_arr = [0] * (len(self.text) - 1)
        lcp = 0
        pos_in_order = self._invert_suffix_array(self.suffix_array)
        suffix = self.suffix_array[0]
        for i in range(len(self.text)):
            order_index = pos_in_order[suffix]
            if order_index == len(self.text) - 1:
                lcp = 0
                suffix = (suffix + 1) % len(self.text)
                continue
            next_suffix = self.suffix_array[order_index + 1]
            lcp = self._lcp_of_suffixes(self.text, suffix, next_suffix, lcp-1)
            lcp_arr[order_index] = lcp
            suffix = (suffix + 1) % len(self.text)
        return lcp_arr

    def _new_leaf(self, node, S, suffix):
        leaf = SuffixTreeNode(node,
                len(S) - suffix,
                suffix + node.string_depth,
                len(S) - 1
                )
        node.children[S[leaf.edge_start]] = leaf
        return leaf

    def _break_edge(self, node, S, start, offset):
        start_char = S[start]
        mid_char = S[start + offset]
        mid_node = SuffixTreeNode(node,
                    node.string_depth + offset,
                    start,
                    start + offset - 1
                    )
        mid_node.children[mid_char] = node.children[start_char]
        node.children[start_char].parent = mid_node
        node.children[start_char].edge_start = start + offset
        node.children[start_char] = mid_node
        return mid_node

    def _make_suffix_tree_from_suffix_array(self, S, order, lcp_arr):
        root = SuffixTreeNode(None, 0, -1, -1)
        lcp_prev = 0
        curr_node = root
        for i in range(len(S)):
            suffix = order[i]
            #print("suffix:", suffix)
            while curr_node.string_depth > lcp_prev:
                curr_node = curr_node.parent
            if curr_node.string_depth == lcp_prev:
                curr_node = self._new_leaf(curr_node, S, suffix)
                curr_node.occurs = suffix
            else:
                edge_start = order[i-1] + curr_node.string_depth
                offset = lcp_prev - curr_node.string_depth
                mid_node = self._break_edge(curr_node, S, edge_start, offset)
                #mid_node.occurs = suffix
                curr_node = self._new_leaf(mid_node, S, suffix)
                curr_node.occurs=suffix
            if i < len(S)-1:
                lcp_prev = lcp_arr[i]
        return root

    def create_suffix_tree(self):
        lcp_array = self._compute_lcp_array()
        self.root = self._make_suffix_tree_from_suffix_array(self.text, \
                self.suffix_array, lcp_array)

    def display_tree(self):
        """
        Displays the suffix tree labels level by level. The furthest left
        is level 0 the next furthest left is level 1 etc. The children of
        a given label are signified by a change in level (indentation).
        Returns the displayed string
        """
        s = self._display_tree_recursive("", self.root)
        length = len(s) - 2 # remove the trailing newline char
        return s[:length]

    def _display_tree_recursive(self, string, curr, space=''):
        for child in curr.children:
            start = curr.children[child].edge_start
            end = curr.children[child].edge_end
            string += space + self.text[start:end+1] + "\n"
            string = self._display_tree_recursive(string, curr.children[child], space+"\t")
        return string

    def find_patterns(self, patterns):
        locations = []
        for pattern in patterns:
            locations.append(self.find_pattern(pattern))
        return locations

    def find_pattern(self, pattern):
        """
        Traverses the suffix tree to find if a given pattern
        can be matched. If so, returns a list of indices where it
        occurs
        """
        curr_node = self.root
        curr_char_pos = 0
        updated = True
        while curr_char_pos < len(pattern) and updated:
            updated = False
            for child in curr_node.children.keys():
                child_node = curr_node.children[child]
                edge_label = self.text[child_node.edge_start:child_node.edge_end+1]
                edge_label_len = child_node.edge_end - child_node.edge_start + 1

                # Check if pattern contains the full edge label
                if pattern[curr_char_pos:curr_char_pos+edge_label_len] == edge_label:
                    curr_char_pos += edge_label_len
                    curr_node = child_node
                    updated = True
                    break

                # Check if edge label contains the pattern
                elif edge_label.startswith(pattern[curr_char_pos:]):
                    curr_char_pos = len(pattern)
                    curr_node = child_node
                    updated = True
                    break

            # We have completed the pattern, now return where the pattern
            # occurs in the original text
            if curr_char_pos == len(pattern):
                # Not a leaf node, all children of node contain pattern
                if curr_node.occurs == None:
                    locations = []
                    self._explore_leaves(curr_node, locations)
                else:
                    locations = [curr_node.occurs]
                return locations
        return []

    def _explore_leaves(self, node, locations):
        """
        Explores a down thru to the leaves from a given node,
        appending where the suffix at the leaf occurs in the
        string to locations
        """
        for child in node.children.keys():
            if node.children[child].occurs != None:
                locations.append(node.children[child].occurs)
            else:
                self._explore_leaves(node.children[child], locations)
