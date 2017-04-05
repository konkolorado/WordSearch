# python3
import sys

"""
Contains source code for efficiently creating a Suffix Array
for a long string. For a string S, this builds a Suffix Array
in time O( |S| log(s) ) using O(|S|) memory
"""

class SuffixArrayEfficient(object):

    def __init__(self, text, terminal="$", custom_alpha=False):
        """
        Alphabet must be in order such that the smallest value
        character is furthest left in the string and values
        continue increasing as we progress right
        """
        self.text = text + terminal
        if not custom_alpha:
            self.alpha = terminal + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        else:
            self.alpha = self._get_custom_alpha()

    def __str__(self):
        return "Suffix Array for text:" + self.text

    def _get_custom_alpha(self):
        """
        Gets a custom character set from the user via command line
        """
        print("Please enter your custom alphabet set:")
        return ''.join(list(set(input(""))))

    def build_suffix_array(self):
        """
        Build suffix array of the string text and
        return a list result of the same length as the text
        such that the value result[i] is the index (0-based)
        in text where the i-th lexicographically smallest
        suffix of text starts.
        """
        order = self._sort_characters()
        classes = self._compute_character_classes(order)
        L = 1
        while L < len(self.text):
            order = self._sort_characters_doubled(L, order, classes)
            classes = self._update_classes(order, classes, L)
            L = 2 * L
        return order

    def _sort_characters(self):
        """
        Returns a list containing mappings of letter index to its position
        in a sorted list
        For example
        - Suppose we return order = [1, 2, 0]
        - Suppose our original text = "DBC"
        - What this order means is that the character in index 1 will
        be located at index 0 of the sorted character array
        - The character at index 2 will be located at index 1 of the sorted
        array
        - The character at index 0 will be located at index 2 of sorted array
        - If we look at the sorted array of our original text, ["B", "C", "D"]
        this is true
        """
        order = [0] * len(self.alpha)
        count = {letter: 0 for letter in self.alpha}

        # Store the count of each unique letter in the text
        for i in range(0, len(self.text)):
            if self.text[i] in count:
                count[self.text[i]] += 1
            else:
                count[self.text[i]] = 0

        # Modify count so that it stores the element at each index stores
        # the sum of previous counts
        for i, letter in enumerate(self.alpha):
            if i == 0:
                continue
            count[letter] = count[letter] + count[self.alpha[i-1]]

        # Copy resulting location to output list
        for i in range(len(self.text)-1, -1, -1):
            c = self.text[i]
            count[c] = count[c] - 1
            order[count[c]] = i

        return order[:len(self.text)]

    def _compute_character_classes(self, order):
        """
        A character class's value is the number of cyclic shifts that
        are smaller than the current class. So, if the current class's
        value is 2, it means there are 2 cyclic shifts smaller than it
        For example
        - Suppose text = "ABABAA$"
        - Suppose order = [6,0,2,4,5,1,3]
        - Our initial classes = [-, -, -, -, -, -, -]
        - Class 0 is assigned to the smallest value in order
            text[6] = "$"
            So, classes = [-, -, -, -, -, -, 0]
        - Class 1 is assigned to the next smallest value in order
            text[0] = "A"
            So, classes = [1, -, -, -, -, -, 0]
        - Class 1 is assigned to the next smallest value in order
          because text[2] == text[0]
            classes = [1, -, 1, -, -, -, 0]
        ...
        - Class 2 is assigned to the next smallest value in order
          because text[1] != text[5]
            classes = [1, 2, 1, -, 1, 1, 0]
        - Class 2 is assigned to the next smallest value in order
          because text[3] == text[1]
            classes = [1, 2, 1, 2, 1, 1, 0]
        """
        classes = [0] * len(self.text)
        classes[order[0]] = 0
        for i in range(1, len(self.text)):
            if self.text[order[i]] != self.text[order[i-1]]:
                classes[order[i]] = classes[order[i-1]] + 1
            else:
                classes[order[i]] = classes[order[i-1]]
        return classes

    def _sort_characters_doubled(self, L, order, classes):
        """
        Given a string S, size L, order array and class array, this
        procedure will sort suffixes by their first half, and do so
        stabley so that if their first halves are the same, they
        preserve the order they were in from the second half
        """
        count, new_order = [0] * len(self.text), [0] * len(self.text)
        for i in range(0, len(self.text)):
            count[classes[i]] = count[classes[i]] + 1
        for i in range(1, len(self.text)):
            count[i] = count[i] + count[i-1]
        for i in range(len(self.text)-1, -1, -1):
            start = (order[i] - L + len(self.text)) % len(self.text)
            cl = classes[start]
            count[cl] = count[cl] - 1
            new_order[count[cl]] = start

        return new_order

    def _update_classes(self, new_order, old_classes, L):
        """
        Given a new_order array, previous classes array, and size L of
        cyclic shifts, returns an array of equivalence classes of the
        doubled cyclic shifts
        """
        n = len(new_order)
        new_class = [0] * n
        new_class[new_order[0]] = 0
        for i in range(1, n):
            cur = new_order[i]
            cur_mid = (cur + L) % n
            prev = new_order[i-1]
            prev_mid = (prev + L) % n
            if old_classes[cur] != old_classes[prev] or \
                    old_classes[cur_mid] != old_classes[prev_mid]:
                new_class[cur] = new_class[prev] + 1
            else:
                new_class[cur] = new_class[prev]

        return new_class
