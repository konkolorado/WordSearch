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
    ws = BaseWordSearch("grids/grid3.txt")

    ws.find_word("Q")
    ws.find_word("ZSE")
    ws.find_word("C")


def main():
    test_load_csv()
    test_str_()
    test_find_word()

if __name__ == '__main__':
    main()
