"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle, seen=set()):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @type seen: set
    @rtype: PuzzleNode

    # for the doctest below, the test prints the node on the console. I felt it
    # would be easier to see and inspect the output rather than construct a node
    # with the same sequence of solutions to compare it with and return if it is
    # the same as the node.

    >>> from sudoku_puzzle import SudokuPuzzle
    >>> grid1 = ["A", "B", "C", "D"]
    >>> grid1 += ["D", "C", "B", "A"]
    >>> grid1 += ["*", "D", "*", "*"]
    >>> grid1 += ["*", "*", "*", "*"]
    >>> s1 = SudokuPuzzle(4, grid1, {"A", "B", "C", "D"})
    >>> node = depth_first_solve(s1)
    >>> print(node)
    >>> from word_ladder_puzzle import WordLadderPuzzle
    >>> w2 = WordLadderPuzzle("same", "cost", {"case", "same", "some", "rome", "rose", "rost", "cost"})
    >>> node = depth_first_solve(w2)
    >>> print(node)

    """
    if puzzle is None or str(puzzle) in seen:
        return None

    seen.add(str(puzzle))

    if puzzle.is_solved():
        return PuzzleNode(puzzle)

    else:
        extensions = puzzle.extensions()
        for x in extensions:
            node = depth_first_solve(x, seen)
            if node:
                main_node = PuzzleNode(puzzle)
                node.parent = main_node
                main_node.children.append(node)
                return main_node
    return None


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode

    # for the doctest below, the test prints the node on the console. I felt it
    # would be easier to see and inspect the output rather than construct a node
    # with the same sequence of solutions to compare it with and return if it is
    # the same as the node.

    >>> from sudoku_puzzle import SudokuPuzzle
    >>> grid1 = ["A", "B", "C", "D"]
    >>> grid1 += ["D", "C", "B", "A"]
    >>> grid1 += ["*", "D", "*", "*"]
    >>> grid1 += ["*", "*", "*", "*"]
    >>> s1 = SudokuPuzzle(4, grid1, {"A", "B", "C", "D"})
    >>> node = breadth_first_solve(s1)
    >>> print(node)
    >>> from word_ladder_puzzle import WordLadderPuzzle
    >>> word_set = {"case", "same", "some", "rome", "rose", "rost", "cost"}
    >>> w2 = WordLadderPuzzle("same", "cost", word_set)
    >>> node2 =  breadth_first_solve(w2)
    >>> print(node2)

    """
    def get_children(puznode):

        children = []
        extension = puznode.puzzle.extensions()
        for config in extension:
            children.append(PuzzleNode(config, None, puznode))
        return children

    seen = set()
    q = deque([PuzzleNode(puzzle)])
    while q:
        puznode = q.popleft()
        seen.add(str(puznode))
        if puznode.puzzle.is_solved():
            # if this node is solved, trace back to its parent node
            # in case puznode does not have a parent, it is its parent
            parent = puznode

            # if it has a parent, trace back to it
            while puznode.parent:
                parent = puznode.parent
                parent.children = [puznode]
                puznode = parent  # to find the grandparent

            return parent
        else:
            children = get_children(puznode)
            for child in children:
                if str(child) not in seen:
                    q.append(child)
                    seen.add(str(child))


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
