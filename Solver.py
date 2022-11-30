"""
Algorithm to solve a sudoku board
"""

class SudokuSolver:

    def __init__(self, board) -> None:
        self.board = board

    def solve(self) -> bool:
        """
        Solves sudoku board row by row using backtracking
        """
        #Find empty position
        found_position = self.find_empty()
        
        #If no position found meaning reached the end, so return true(GOAL)(BASE CASE)
        if found_position is None:
            return True
        
        row,col = found_position

        #Make the decision for the number (CHOICE)
        for i in range(1,10):
            if self.isValid(row, col,i): #(CONSTRAINT)
                #If valid placement then change the number and recurse
                self.board[row][col] = i
                flag = self.solve()
                #If flag is true meaning reached the end
                if flag == True:
                    return True
                self.board[row][col] = 0
        #When no choices available return false and undo the previous choice
        return False

    def find_empty(self) -> int:
        """
        Function to find empty position
        """
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return i,j
        return None

    def isValid(self, row: int, col: int, num: int) -> bool:
        """
        Checks if the placement in the board is valid, by checking the row, col, and 3x3 grid(CONSTRAINT)
        """
        #Finds the top left most cell in the current position's grid
        start_row = row - (row % 3)
        start_col = col - (col % 3)

        for i in range(len(self.board)):
            #Checks number against the row and column
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
            #Checks number against 3x3 grid 
            if self.board[start_row + i // 3][start_col + (i % 3)] == num:
                return False
        return True

    def print_board(self) -> None:
        """
        Prints Sudoku board 
        """
        for row in self.board:
            print(row)


"""
Tests
"""
# sudoku = SudokuSolver()
# sudoku.solve()
# sudoku.print_board()
