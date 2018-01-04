from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __str__(self):
        """
        String representation of WordLadder

        @param WordLadderPuzzle self:  this word ladder puzzle
        @rtype: str

        >>> w1 = WordLadderPuzzle("on", "no", {"on", "no", "oo"})
        >>> print(w1)
        on -> no
        """
        return "{} -> {}". format(self._from_word, self._to_word)

    def __eq__(self, other):
        """
        Check if self is the same as other

        @param WordLadderPuzzle self: this puzzle
        @param Any other: another object to compare self with
        @rtype: bool

        >>> w1 = WordLadderPuzzle("on", "no", {"on", "no", "oo"})
        >>> w2 = WordLadderPuzzle("on", "no", {"on", "no", "oo"})
        >>> w3 = WordLadderPuzzle("on", "ok", {"on", "no", "oo"})
        >>> w1 == w2
        True
        >>> w1 == w3
        False
        """
        return (type(self) == type(other) and self._chars == other._chars and
                self._from_word == other._from_word and
                self._to_word == other._to_word and self._word_set ==
                                                                other._word_set)

    def extensions(self):
        """
        Overrides Puzzle.extensions()

        Returns extensions of the present configuration. Legal extensions are
        WordLadderPuzzles that have a from_word that can be reached from this
        one by changing a single letter to one of those in self._chars.

        @param WordLadderPuzzle self: This word ladder puzzle
        @rtype: list[WordLadderPuzzle] | None

        >>> w1 = WordLadderPuzzle("on", "no", {"on", "no", "an","oo"})
        >>> l = w1.extensions()
        >>> word_set = {"on", "no", "an","oo"}
        >>> word_set2 = {"case", "same", "some", "rome", "rose", "rost", "cost"}
        >>> c1 = WordLadderPuzzle("an","no", word_set)
        >>> c2 = WordLadderPuzzle("oo","no", word_set)
        >>> l == [c1,c2]
        True
        >>> w2 = WordLadderPuzzle("same", "cost", word_set2)
        >>> l = w2.extensions()
        >>> l == [WordLadderPuzzle("some", "cost", word_set2)]
        True

        """
        l = []
        for i in range(len(self._from_word)):
            for c in self._chars:
                s = self._from_word[:i] + c + self._from_word[i+1:]
                if s in self._word_set and not s == self._from_word:
                    l.append(WordLadderPuzzle(s, self._to_word, self._word_set))

        return l

    def is_solved(self):
        """
        Overrides Puzzle.is_solved()

        @param WordLadderPuzzle self: This word ladder puzzle
        @rtype: bool

        >>> w1 = WordLadderPuzzle("on", "no", {"on", "no", "an","oo"})
        >>> w1.is_solved()
        False
        >>> w2 = WordLadderPuzzle("no", "no", {"on", "no", "an","oo"})
        >>> w2.is_solved()
        True
        """
        return self._from_word == self._to_word

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", encoding='utf-8') as words:
        # with open("words","r") as words:
        word_set = set(words.read().split())

    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
