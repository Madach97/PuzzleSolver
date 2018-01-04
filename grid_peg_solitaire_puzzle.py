from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __str__(self):
        """
        String representation of Grid Peg Solitaire puzzle

        @type self: GridPegSolitairePuzzle
        @rtype: String

        >>> grid = []
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", ".", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(gpsp)
        * * * * *
        * * * * *
        * * * * *
        * * . * *
        * * * * *

        """
        # doctest above is creating issues with \n character, so I have tested
        # it by printing it to the screen and inspecting if it prints properly

        s = ""
        for row in self._marker:
            for x in row:
                s += x + " "
            s += "\n"
        return s

    def __eq__(self, other):
        """
        Checks if two GridPegSolitairePuzzles are the same

        @type self: GridPegSolitairePuzzle
        @type other: Any
        @rtype: bool

        >>> grid1 = []
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> grid1.append([".", ".", "*", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = []
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> grid2.append([".", ".", "*", "*", "*"])
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp1 == gpsp2
        True
        >>> grid3 = []
        >>> grid3.append(["*", "*", ".", "*", "*"])
        >>> grid3.append(["*", "*", ".", "*", "*"])
        >>> grid3.append(["*", "*", "*", "*", "*"])
        >>> grid3.append(["*", "*", "*", "*", "*"])
        >>> grid3.append(["*", "*", "*", "*", "*"])
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> grid4 = []
        >>> grid4.append(["*", "*", "*", "*", "*"])
        >>> grid4.append(["*", "*", "*", "*", "*"])
        >>> grid4.append(["*", "*", "*", "*", "*"])
        >>> grid4.append(["*", "*", ".", "*", "*"])
        >>> grid4.append(["*", "*", ".", "*", "*"])
        >>> gpsp4 = GridPegSolitairePuzzle(grid4, {"*", ".", "#"})
        >>> gpsp3 ==  gpsp4
        False
        """
        return (type(self) == type(other) and self._marker == other._marker and
                self._marker_set == other._marker_set)

    def extensions(self):
        """
        Overrides Puzzle.extensions()

        Return valid extensions of GridPegSolitaire Puzzle. A legal extension
        consists of all configurations that can be reached by
        making a single jump from this configuration

        @param GridPegSolitairePuzzle self: This GridPegSolitaire puzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid = []
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", ".", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> extends = gpsp.extensions()
        >>> grid1 = []
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> grid1.append([".", ".", "*", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = []
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> grid2.append(["*", "*", "*", ".", "."])
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> grid3 = []
        >>> grid3.append(["*", "*", ".", "*", "*"])
        >>> grid3.append(["*", "*", ".", "*", "*"])
        >>> grid3.append(["*", "*", "*", "*", "*"])
        >>> grid3.append(["*", "*", "*", "*", "*"])
        >>> grid3.append(["*", "*", "*", "*", "*"])
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> grid4 = []
        >>> grid4.append(["*", "*", "*", "*", "*"])
        >>> grid4.append(["*", "*", "*", "*", "*"])
        >>> grid4.append(["*", "*", "*", "*", "*"])
        >>> grid4.append(["*", "*", ".", "*", "*"])
        >>> grid4.append(["*", "*", ".", "*", "*"])
        >>> gpsp4 = GridPegSolitairePuzzle(grid4, {"*", ".", "#"})
        >>> extends[1] == gpsp1
        True
        >>> extends[0] == gpsp2
        True
        >>> extends[2] == gpsp3
        True
        >>> extends[3] == gpsp4
        True
        """

        new_configs = []
        # to save typing
        m = [x for x in self._marker]

        for row in range(len(m)):
            for col in range(len(m[row])):

                if m[row][col] == ".":
                    if (col + 2 < len(m[row]) and m[row][col + 2] == "*" and
                        m[row][col + 1] == "*"):
                        # jump to the left
                        new_marker = m[:]
                        new_marker[row] = (m[row][: col] + ["*"] + ["."] +
                                           ["."] + m[row][col + 3:])
                        puz = GridPegSolitairePuzzle(new_marker,
                                                     self._marker_set)
                        new_configs.append(puz)

                    if (col - 2 >= 0 and m[row][col - 2] == "*" and
                        m[row][col - 1] == "*"):
                        # jump to the right
                        new_marker = m[:]
                        new_marker[row] = (m[row][: col - 2] + ["."] + ["."] +
                                           ["*"] + m[row][col + 1:])

                        puz = GridPegSolitairePuzzle(new_marker,
                                                     self._marker_set)
                        new_configs.append(puz)

                    if (row - 2 >= 0 and m[row - 2][col] == "*" and
                                m[row - 1][col] == "*"):
                        # jump down
                        new_marker = []

                        # copy contents of m into new_marker
                        for i in range(len(m)):
                            new_marker.append([])
                            for item in m[i]:
                                new_marker[i].append(item)

                        new_marker[row - 2][col] = "."
                        new_marker[row - 1][col] = "."
                        new_marker[row][col] = "*"
                        puz = GridPegSolitairePuzzle(new_marker,
                                                     self._marker_set)
                        new_configs.append(puz)

                    if (row + 2 < len(m) and m[row + 2][col] == "*" and
                                m[row + 1][col] == "*"):
                        # jump up

                        new_marker = []
                        for i in range(len(m)):
                            new_marker.append([])
                            for item in m[i]:
                                new_marker[i].append(item)

                        new_marker[row + 2][col] = "."
                        new_marker[row + 1][col] = "."
                        new_marker[row][col] = "*"
                        puz = GridPegSolitairePuzzle(new_marker,
                                                     self._marker_set)
                        new_configs.append(puz)

        return new_configs

    def is_solved(self):
        """
        Overrides Puzzle.is_solved()

        Returns if it has reached solved configuration. A configuration is
        solved when there is exactly one "*" left

        @param GridPegSolitairePuzzle self: This GridPegSolitaire puzzle
        @rtype : bool

        >>> grid = []
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", "*", "*", "*"])
        >>> grid.append(["*", "*", ".", "*", "*"])
        >>> grid.append(["*", "*", ".", "*", "*"])
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.is_solved()
        False
        >>> grid2 = []
        >>> grid2.append([".", ".", ".", ".", "."])
        >>> grid2.append([".", ".", ".", ".", "."])
        >>> grid2.append([".", ".", ".", ".", "."])
        >>> grid2.append([".", ".", ".", "*", "."])
        >>> grid2.append([".", ".", ".", ".", "."])
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2.is_solved()
        True
        >>> grid3 = []
        >>> grid3.append([".", ".", ".", ".", "."])
        >>> grid3.append([".", ".", ".", ".", "."])
        >>> grid3.append([".", ".", ".", ".", "."])
        >>> grid3.append([".", ".", ".", "*", "."])
        >>> grid3.append([".", "*", ".", ".", "."])
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> gpsp3.is_solved()
        False

        """
        i = 0
        for row in self._marker:
            for x in row:
                if x == "*":
                    i += 1
                    if i > 1:
                        return False
        return True

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
