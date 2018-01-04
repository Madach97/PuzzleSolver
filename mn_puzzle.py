from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self,other):
        """
        Return if this mn puzzle is equal to the other

        @param MNPuzzle self: this puzzle
        @param Any other: object to compare with
        @rtype: bool

        >>> m1 = MNPuzzle((("*","2"), ("3","4")),(("3","2"), ("*","4")))
        >>> m2 = MNPuzzle((("*","2"), ("3","4")),(("3","2"), ("*","4")))
        >>> m3 = MNPuzzle((("*","2"), ("3","4")),(("3","2"), ("4","*")))
        >>> m1 == m2
        True
        >>> m2 == m3
        False
        """
        return (type(self) == type(other) and self.from_grid == other.from_grid and
                self.to_grid == other.to_grid and self.m == other.m and
                self.n == other.n)

    def __str__(self):
        """
        String representation of this mn puzzle

        @param MNPuzzle self: this puzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> gr = MNPuzzle( start_grid, target_grid)
        >>> print(gr)
        * 2 3   1 2 3
        1 4 5   4 5 *

        """
        # doctest above is creating issues with \n character, so I have tested
        # it by printing it to the screen and inspecting if it prints properly

        s = ""
        for i in range(len(self.from_grid)):
            for j in range(len(self.from_grid[0])):
                s += self.from_grid[i][j] + " "

            s += "\t"

            for j in range((len(self.to_grid[0]))):
                s += self.to_grid[i][j] + " "

            s += "\n"

        return s

    def extensions(self):
        """
        Overrides Puzzle.extensions()

        Return valid extensions of mnpuzzle. Legal extensions are configurations
        that can be reached by swapping one symbol to the left, right, above,
        or below "*" with "*"

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> gr = MNPuzzle( start_grid, target_grid)
        >>> extends = gr.extensions()
        >>> t1 = (("1", "2", "3"),("*", "4", "5"))
        >>> t2 = (("2", "*", "3"),("1", "4", "5"))
        >>> extends[0] == MNPuzzle(t1 , target_grid)
        True
        >>> extends[1] == MNPuzzle(t2 , target_grid)
        True
        """

        new_configs = []
        for i in range(len(self.from_grid)):
            for j in range(len(self.from_grid[0])):
                if self.from_grid[i][j] == "*":
                    # the present position is a space

                    if i - 1 >= 0 and not (self.from_grid[i-1][j] == "*"):
                        # there is a position above it and it has a symbol
                        new_grid = []
                        sym = self.from_grid[i-1][j]
                        # copy contents of tuple(tuple) to a list[list]
                        for row in range(len(self.from_grid)):
                            new_grid.append([])
                            for col in range(len(self.from_grid[i])):
                                new_grid[row].append(self.from_grid[row][col])

                        new_grid[i][j] = sym
                        new_grid[i-1][j] = "*"
                        temp = []
                        # convert each row of grid to a tuple and store in temp.
                        # i.e convert from list[list] to list[tuple]
                        for row in new_grid:
                            temp.append(tuple(row))

                        # append the puzzle with this new grid into a list
                        # and convert the list[tuple] to a tuple(tuple)
                        new_configs.append(MNPuzzle(tuple(temp), self.to_grid))

                    if i + 1 < len(self.from_grid) and not (self.from_grid[i+1][j] == "*"):
                        # there is a position below it and it has a symbol
                        new_grid = []
                        sym = self.from_grid[i+1][j]

                        for row in range(len(self.from_grid)):
                            new_grid.append([])
                            for col in range(len(self.from_grid[i])):
                                new_grid[row].append(self.from_grid[row][col])

                        new_grid[i][j] = sym
                        new_grid[i+1][j] = "*"
                        temp = []

                        for row in new_grid:
                            temp.append(tuple(row))
                        new_configs.append(MNPuzzle(tuple(temp), self.to_grid))

                    if j - 1 >= 0 and not (self.from_grid[i][j-1] == "*"):
                        # there is a position to the left of it and it has a
                        # symbol
                        new_grid = []
                        sym = self.from_grid[i][j-1]
                        for row in range(len(self.from_grid)):
                            new_grid.append([])
                            for col in range(len(self.from_grid[i])):
                                new_grid[row].append(self.from_grid[row][col])

                        new_grid[i][j] = sym
                        new_grid[i][j-1] = "*"
                        temp = []
                        for row in new_grid:
                            temp.append(tuple(row))
                        new_configs.append(MNPuzzle(tuple(temp), self.to_grid))

                    if j + 1 < len(self.from_grid[i]) and not (self.from_grid[i][j+1] == "*"):
                        # there is a position to the right of it and it has a
                        # symbol
                        new_grid = []
                        sym = self.from_grid[i][j+1]
                        for row in range(len(self.from_grid)):
                            new_grid.append([])
                            for col in range(len(self.from_grid[i])):
                                new_grid[row].append(self.from_grid[row][col])

                        new_grid[i][j] = sym
                        new_grid[i][j+1] = "*"
                        temp = []
                        for row in new_grid:
                            temp.append(tuple(row))
                        new_configs.append(MNPuzzle(tuple(temp), self.to_grid))

        return new_configs

    def is_solved(self):
        """
        Overrides Puzzle.is_solved()

        Return whether a puzzle is solved. A configuration is solved when the
        from_grid is the same as to_grid

        @param MNPuzzle self: This mn puzzle
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> gr = MNPuzzle( start_grid, target_grid)
        >>> gr.is_solved()
        False
        >>> s = (("1", "2", "3"), ("4", "5", "*"))
        >>> gr1 = MNPuzzle( s, target_grid)
        >>> gr1.is_solved()
        True
        """
        return self.from_grid == self.to_grid


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
