import sys
import copy


class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.domain = [[set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(9)] for _ in range(9)]

    def solve(self):
        self.preprocess()
        self.backtrack_search()
        return self.puzzle

    def preprocess(self):
        for i in range(0, 9):
            for j in range(0, 9):
                curr = self.puzzle[i][j]
                if curr != 0:
                    self.domain[i][j] = set([curr])
                    for k in range(0, 9):
                        if k != i:
                            self.domain[k][j].discard(curr)
                        if k != j:
                            self.domain[i][k].discard(curr)
                    translated_i = i // 3 * 3
                    translated_j = j // 3 * 3
                    for x in range(0, 3):
                        for y in range(0, 3):
                            if x + translated_i != i and y + translated_j != j:
                                self.domain[x + translated_i][y + translated_j].discard(curr)

    def pick_unassigned_var(self):
        # with MRV heuristic
        length = 10
        var = ()
        found = False
        for i in range(0, 9):
            for j in range(0, 9):
                if self.puzzle[i][j] == 0:
                    found = True
                    curr_length = len(self.domain[i][j])
                    if curr_length < length:
                        length = curr_length
                        var = (i, j)

        if not found:
            return (-1, -1)
        else:
            return var

    def is_complete(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.puzzle[i][j] == 0:
                    return False
        return True
    
    def discard(self, value, x, y):
        # Basically just one step forward-checking
        # Since puzzle[x][y] is now assigned, update the domain
        # Update domain for all tiles in same column, row, and sub-grid
        not_fail = True
        discarded = {}
        discarded[(x, y)] = self.domain[x][y]
        self.domain[x][y] = set([value])
        for k in range(0, 9):
            if k != x:
                if value in self.domain[k][y]:
                    discarded[(k, y)] = value
                    self.domain[k][y].discard(value)
                    if len(self.domain[k][y]) == 0:
                        not_fail = False
            if k != y:
                if value in self.domain[x][k]:
                    discarded[(x, k)] = value
                    self.domain[x][k].discard(value)
                    if len(self.domain[x][k]) == 0:
                        not_fail = False
        
        translated_x = x // 3 * 3
        translated_y = y // 3 * 3
        for i in range(0, 3):
            for j in range(0, 3):
                new_x = i + translated_x
                new_y = j + translated_y
                if new_x != x and new_y != y:
                    if value in self.domain[new_x][new_y]:
                        discarded[(new_x, new_y)] = value
                        self.domain[new_x][new_y].discard(value)
                        if len(self.domain[new_x][new_y]) == 0:
                            not_fail = False

        return (discarded, not_fail)

    def backtrack_search(self):
        x, y = self.pick_unassigned_var()
        if x == -1:
            return self.is_complete()
        for value in self.domain[x][y]:
            self.puzzle[x][y] = value
            discarded, not_fail = self.discard(value, x, y)
            if not_fail:
                result = self.backtrack_search()
                if result != False:
                    return result
            self.puzzle[x][y] = 0
            for i, j in discarded:
                if i == x and j == y:
                    self.domain[i][j] = discarded[(i, j)]
                else:
                    self.domain[i][j].add(discarded[(i, j)])
        
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("\nUsage: python Sudoku-Solver.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python Sudoku-Solver.py input.txt output.txt\n")
        raise IOError("Input file not found")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
