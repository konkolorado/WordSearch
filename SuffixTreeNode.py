"""
Node definition for use with the SuffixTreeEfficient class
"""

class SuffixTreeNode(object):
    def __init__(self, parent, string_depth, edge_start, edge_end):
        self.parent = parent
        self.children = {}
        self.string_depth = string_depth
        self.edge_start = edge_start
        self.edge_end = edge_end
        self.occurs = None

    def __str__(self):
        return "Depth: " + str(self.string_depth) + \
            " Edge start: " + str(self.edge_start) + \
            " Edge end: " + str(self.edge_end) + \
            " Children: " + str(self.children)
