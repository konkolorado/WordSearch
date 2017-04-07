import random

import numpy as np

from BaseWordSearch import BaseWordSearch

def test_load_csv():
    print("Testing loading csv...", end='')
    np.testing.assert_array_equal(BaseWordSearch("grids/grid1.txt").grid, \
        [['Q', 'W', 'E', 'R'], ['A', 'S', 'D', 'F']])

    np.testing.assert_array_equal(BaseWordSearch("grids/grid2.txt").grid, \
        [['Q', 'A'], ['W', 'S'], ['E', 'D'], ['R', 'F']])

    np.testing.assert_array_equal(BaseWordSearch("grids/grid3.txt").grid, \
        [['Q', 'W', 'E'], ['A', 'S', 'D'], ['Z', 'X', 'C']])

    print("Done")

def test_str_():
    # NOTE: Sorry, too lazy to break these assertion lines up
    print("Testing str representations of grid... ", end='')

    ws = BaseWordSearch("grids/grid1.txt")
    assert repr(ws.__str__()) == \
        repr('rows\nQWER\nASDF\ncols\nQA\nWS\nED\nRF\ndiag_down\nA\nQS\nWD\nEF\nR\ndiag_up\nQ\nAW\nSE\nDR\nF')

    ws = BaseWordSearch("grids/grid2.txt")
    assert repr(ws.__str__()) == \
        repr('rows\nQA\nWS\nED\nRF\ncols\nQWER\nASDF\ndiag_down\nR\nEF\nWD\nQS\nA\ndiag_up\nQ\nWA\nES\nRD\nF')

    ws = BaseWordSearch("grids/grid3.txt")
    assert repr(ws.__str__()) == \
        repr('rows\nQWE\nASD\nZXC\ncols\nQAZ\nWSX\nEDC\ndiag_down\nZ\nAX\nQSC\nWD\nE\ndiag_up\nQ\nAW\nZSE\nXD\nC')

    print("Done")

def test_find_word():
    print("Testing find word... ", end='')
    ws = BaseWordSearch("grids/grid1.txt")
    assert ws.find_word("QWER") == [((0, 0), (0, 4))]
    assert ws.find_word("QWE") == [((0, 0), (0, 3))]
    assert ws.find_word("QW") == [((0, 0), (0, 2))]
    assert ws.find_word("Q") == [((0, 0), (0, 1)), ((0, 0), \
        (1, 0)), ((0, 0), (1, 1)), ((0, 0), (-1, 1))]
    assert ws.find_word("ASDF") == [((1, 0), (1, 4))]
    assert ws.find_word("ASD") == [((1, 0), (1, 3))]
    assert ws.find_word("QA") == [((0, 0), (2, 0))]
    assert ws.find_word("A") == [((1, 0), (1, 1)), ((1, 0), \
        (2, 0)), ((1, 0), (2, 1)), ((1, 0), (0, 1))]
    assert ws.find_word("RF") == [((0, 3), (2, 3))]
    assert ws.find_word("R") == [((0, 3), (0, 4)), ((0, 3), \
        (1, 3)), ((0, 3), (1, 4)), ((0, 3), (-1, 4))]
    assert ws.find_word("F") == [((1, 3), (1, 4)), ((1, 3), \
        (2, 3)), ((1, 3), (2, 4)), ((1, 3), (0, 4))]
    assert ws.find_word("QS") == [((0, 0), (2, 2))]
    assert ws.find_word("AW") == [((1, 0), (-1, 2))]

    ws = BaseWordSearch("grids/grid2.txt")
    assert ws.find_word("QA") == [((0, 0), (0, 2))]
    assert ws.find_word("RF") == [((3, 0), (3, 2))]
    assert ws.find_word("Q") == [((0, 0), (0, 1)), ((0, 0), \
        (1, 0)), ((0, 0), (1, 1)), ((0, 0), (-1, 1))]
    assert ws.find_word("F") == [((3, 1), (3, 2)), ((3, 1), \
        (4, 1)), ((3, 1), (4, 2)), ((3, 1), (2, 2))]
    assert ws.find_word("QWER") == [((0, 0), (4, 0))]
    assert ws.find_word("ER") == [((2, 0), (4, 0))]
    assert ws.find_word("WER") == [((1, 0), (4, 0))]
    assert ws.find_word("QSF") == []
    assert ws.find_word("QS") == [((0, 0), (2, 2))]
    assert ws.find_word("EF") == [((2, 0), (4, 2))]
    assert ws.find_word("WA") == [((1, 0), (-1, 2))]

    ws = BaseWordSearch("grids/grid3.txt")
    assert ws.find_word("QAZ") == [((0, 0), (3, 0))]
    assert ws.find_word("AZ") == [((1, 0), (3, 0))]
    assert ws.find_word("QSC") == [((0, 0), (3, 3))]
    assert ws.find_word("SC") == [((1, 1), (3, 3))]
    assert ws.find_word("WE") == [((0, 1), (0, 3))]
    assert ws.find_word("ZSE") == [((2, 0), (-1, 3))]
    assert ws.find_word("SE") == [((1, 1), (-1, 3))]
    assert ws.find_word("AS") == [((1, 0), (1, 2))]
    assert ws.find_word("AW") == [((1, 0), (-1, 2))]
    assert ws.find_word("X") == [((2, 1), (2, 2)), ((2, 1), \
        (3, 1)), ((2, 1), (3, 2)), ((2, 1), (1, 2))]
    assert ws.find_word("ZXC") == [((2, 0), (2, 3))]

    print("Done")

def test_build_string_from_coords():
    print("Testing build string from coords...", end="")

    ws = BaseWordSearch("grids/grid1.txt")
    words = gen_random_strings_from_letters("QWERASDF")
    w_i = 0
    for results in ws.find_words(words):
        for coord in results:
            assert ws.build_string_from_coords(coord) == words[w_i]
        w_i += 1

    ws = BaseWordSearch("grids/grid2.txt")
    words = gen_random_strings_from_letters("QWERASDF")
    w_i = 0
    for results in ws.find_words(words):
        for coord in results:
            assert ws.build_string_from_coords(coord) == words[w_i]
        w_i += 1

    ws = BaseWordSearch("grids/grid3.txt")
    words = gen_random_strings_from_letters("QWEASDZXC")
    w_i = 0
    for results in ws.find_words(words):
        for coord in results:
            assert ws.build_string_from_coords(coord) == words[w_i]
        w_i += 1

    print("Done")

def gen_random_strings_from_letters(letters):
    letters += " "
    words = []
    for i in range(100):
        words.append(gen_random_string(letters))
    return words

def gen_random_string(letters):
    s = ""
    char = random.choice(letters)
    while char != " ":
        s += char
        char = random.choice(letters)
    return s

def test_show_board():
    print("Testing show board...", end='')
    ws = BaseWordSearch("grids/grid1.txt")
    ws.find_words(["QWER", "E", "QS", "ED"])
    assert repr(ws.show_board(True)) == repr('q w e r \nA s d F ')

    ws = BaseWordSearch("grids/grid2.txt")
    ws.find_words(["QWER", "QS", "ED", "Z"])
    assert repr(ws.show_board(True)) == repr('q A \nw s \ne d \nr F ')

    ws = BaseWordSearch("grids/grid3.txt")
    ws.find_words(["ZSE", "QS", "ED", "C"])
    assert repr(ws.show_board(True)) == repr('q W e \nA s d \nz X c ')

    print("Done")

def main():
    test_load_csv()
    test_str_()
    test_find_word()
    test_build_string_from_coords()
    test_show_board()

if __name__ == '__main__':
    main()
