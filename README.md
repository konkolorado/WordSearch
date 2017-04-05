A repository for efficiently finding patterns within a letter grid.
The base word search game simple uses suffix trees to find patterns
within each row and can easily be extended to support:
- Backwards word matching (up, down, and diagonally)
- Next row/column word matching (when at the end of the row or column,
    continue searching to match a pattern on the next row or column)
- Torus word matching (when at the end of the row or column, return to
    the beginning of the row or column to continue trying to match)

Input Format
- Input should be provided as a csv file containing letters on each row
- An n x m matrix should have characters in each cell
- Easiest for use with English standard alphabetic characters
