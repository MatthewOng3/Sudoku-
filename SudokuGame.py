"""
Playable sudoku game with an inbuilt backtracking sudoku solver algorithm
"""

import pygame
from Solver import *
from sys import exit
pygame.font.init() 
import time

#Constants
GRID_X = 9
GRID_Y = 9
CUBE_THICKNESS = 1
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
GRAY = (128,128,128)
RED = (255,0,0)

WIDTH,HEIGHT = 540,600  #define dimensions of the game window
CLOCK = pygame.time.Clock() #For fps

class MainGrid(SudokuSolver):
    """
    Handles the main grid of the GUI and the self solving algorithm
    """

    board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    def __init__(self, rows: int, cols: int, width: int, height: int, win) -> None:
        self.rows = rows
        self.cols = cols
        self.width = width #540
        self.height = height #540
        self.win = win
        self.selected = None
        self.board = MainGrid.board
        self.cubes = [[InnerCube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)] #Store cube objects in a list
        SudokuSolver.__init__(self,self.board)

    def build_grid(self) -> None:
        """
        Draw grid lines
        """
        gap = self.height // 3 #Find first starting point
        thickness = 5
        for i in range(1, self.rows // 3 + 1):
            pygame.draw.line(self.win, BLACK, (0, gap * i), (self.width, gap * i), thickness) #Horizontal lines
            if i == self.rows // 3:
                continue
            else:
                pygame.draw.line(self.win, BLACK, (gap * i, 0), (gap * i, self.height), thickness) #Vertical lines

        #Draw the inner cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].generate_cube(self.win)

    def solve(self) -> None:
        """
        Solve sudoku board using backtracking
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
                self.selected = (row,col)
                self.cubes[row][col].set_val(i)
                self.cubes[row][col].update_changes(self.win, True)
                self.board[row][col] = i
                pygame.display.update() #update the display with a delay
                pygame.time.delay(5)
                flag = self.solve()
                #If flag is true meaning reached the end
                if flag == True:
                    return True
                self.board[row][col] = 0
                self.cubes[row][col].set_val(0)
                self.cubes[row][col].update_changes(self.win, False)
                pygame.display.update()
                pygame.time.delay(5)
        #When no choices available return false and undo the previous choice
        return False    

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

    def select(self, row: int, col: int) -> None:
        """
        Select cubes
        """
        previous_cube = self.selected

        #Reset the old position 
        if previous_cube is not None:
            old_row, old_col = previous_cube
            self.cubes[old_row][old_col].set_selected_state(False)

        #Newly selected cell
        self.selected = (row,col)
        self.cubes[row][col].set_selected_state(True)
    
    def temp_display(self, value: int) -> None:
        """
        Display temp value on cube
        """
        row,col = self.selected
        self.cubes[row][col].set_temp(value)

    def clicked_index(self, pos: tuple) -> tuple:
        """
        Returns clicked position in terms of index in the array 
        """
        #If clicked position is within bounds
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / GRID_X
            return (int(pos[1] // gap), int(pos[0] // gap)) #Return index in array representation
        return None

    def place(self, i: int, j:int, value: int) -> None:
        """
        Place pressed key number in cube
        """
        self.cubes[i][j].set_val(value)
    
    def isValidSudoku(self) -> bool:
        """
        Checks if board is a valid sudoku solution
        """
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.cubes[i][j].get_val() != "0":
                    if self.isValidCheck(i,j, self.cubes[i][j].get_val()) == False:
                        return False
        return True

    def isValidCheck(self, row: int, col: int, num: int) -> bool:
        """
        Valid placement check for verifier above
        """
        #Finds the top left most cell in the current position's grid
        start_row = row - (row % 3)
        start_col = col - (col % 3)
        num_position = (row,col)
        for i in range(len(self.board)):
            #Checks number against the row and column
            if (self.cubes[row][i].get_val() == num or self.cubes[row][i].get_val() == num) and ((row,i) != num_position and (i,col) != num_position):
                return False
            #Checks number against 3x3 grid 
            if self.cubes[start_row + i // 3][start_col + (i % 3)].get_val() == num and (start_row + i // 3, start_col + (i % 3)) !=   num_position:
                return False
        return True

    def rebuild_window(self, time, outcome) -> None:   
        """
        Redraw everything on the game window
        """
        self.win.fill(WHITE)
        #Display time
        font = pygame.font.SysFont("comicsans", 25)
        text = font.render("Time: " + reformat_time(time), 1, BLACK)
        self.win.blit(text, (540 - 160, 560))

        #Display success or failure
        if outcome == "success":
            text = font.render("Success!", 1, GREEN)
            self.win.blit(text, (20, 560))
        elif outcome == "failure":
            text = font.render("FAILURE!", 1, RED)
            self.win.blit(text, (20, 560))

        #Rebuild grid
        self.build_grid()

    def clear(self) -> None:
        """
        Clear current cell
        """
        row, col = self.selected
        self.cubes[row][col].set_val(0)

    def is_finished(self):
        """
        Checks if all numbers on the board are filled
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class InnerCube:
    """
    Class object for each inner cubes, so each cell in each 3x3 grid
    """
    
    def __init__(self, value: int, row: int, col: int, width: int, height: int) -> None:
        """
        Initialise relevant instance attributes
        """
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.gap = self.width / GRID_X
        self.temp = 0
        self.x_coord = self.col * self.gap #Finds the starting top left x coordinate of the rect
        self.y_coord = self.row * self.gap #Finds the starting top left y coordinate of the rect
        self.selected = False

    def generate_cube(self, win) -> None:
        """
        Draws each inner square(cell) represented by pygame rect
        """
        font = pygame.font.SysFont("Arial", 40)
        
        #Draws the lines of the inner cube
        if self.selected:
            pygame.draw.rect(win, RED, (self.x_coord,self.y_coord,self.gap,self.gap), 3) 
        else:
            pygame.draw.rect(win, BLACK, (self.x_coord,self.y_coord,self.gap,self.gap), CUBE_THICKNESS) 

        #Draw values
        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, GRAY)
            win.blit(text, (self.x_coord + 5, self.y_coord + 5))
        elif self.value != 0:
            number = font.render(str(self.value), 1, BLACK)
            win.blit(number, (self.x_coord + (self.gap / 2 - number.get_width() / 2), self.y_coord + (self.gap / 2 - number.get_height() / 2)))
    
    def update_changes(self, win, green=True) -> None:
        """
        Updating each time a number is chosen to visualise the backtracking algorithm better
        """
        font = pygame.font.SysFont("Arial", 40)
        pygame.draw.rect(win, WHITE, (self.x_coord, self.y_coord, self.gap, self.gap), 0) #Fill the rect object with white color

        value = font.render(str(self.value), 1, BLACK)
        win.blit(value, (self.x_coord + (self.gap / 2 - value.get_width() / 2), self.y_coord + (self.gap / 2 - value.get_height() / 2)))
        if green:
            pygame.draw.rect(win, GREEN, (self.x_coord, self.y_coord, self.gap, self.gap), 3)
        else:
            pygame.draw.rect(win, RED, (self.x_coord, self.y_coord, self.gap, self.gap), 3)

    def get_coords(self) -> tuple[int]:
        """
        Retreives corresponding coordinates on the sudoku board
        """
        return (self.x_coord, self.y_coord)

    def already_placed(self) -> bool:
        """
        Boolean helper method to see if a value has already been placed
        """
        if self.value == 0:
            return False
        return True

    def set_selected_state(self, state: bool) -> None:
        """
        Set selected boolean flag state
        """
        self.selected = state

    def set_val(self, value) -> None:
        """
        Set permanent value for this cube object
        """
        self.value = value

    def get_val(self) -> int:
        """
        Returns set value for the current cube
        """
        return self.value

    def set_temp(self, value) -> None:
        """
        Sets temp value for this cube object
        """
        self.temp = value

    def get_temp(self) -> int:
        """
        Return temp value
        """
        return self.temp

def reformat_time(ms: int) -> int:
    """
    Reformat input time to minutes and seconds
    Input: Milliseconds
    """
    secs = ms % 60
    minutes = ms // 60
    hour = minutes // 60
    return " {}:{}".format(str(minutes), str(secs))

def main():
    """
    Main game function
    """
    win = pygame.display.set_mode((WIDTH,HEIGHT)) #make a new window with the dimensions
    pygame.display.set_caption("Sudoku") #Set window name at the top
    win.fill(WHITE) #Fill the background with white colour
    key = None
    board = MainGrid(GRID_X, GRID_Y, WIDTH, HEIGHT - 60, win) #initalise main grid class
    board.build_grid() 
    start_time = time.time()
    outcome = "nothing"
    #Game loop
    while True:
        play_time = round(time.time() - start_time)
        #Get events from event queue
        for event in pygame.event.get():
            #Quits the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #Checks if user is clicking the box
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() #Gets mouse position
                clicked_index = board.clicked_index(pos) #Gets clicked index position in array form
                current_row, current_col = clicked_index
                board.select(current_row, current_col) #Mark the cube object as selected
            #Key events
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                
                #Algorithamically solve sudoku board
                if event.key == pygame.K_SPACE:
                    board.solve()
                    outcome = "success"

                #Place a number in the cell 
                if event.key== pygame.K_RETURN and board.cubes[current_row][current_col].get_temp() != 0:
                    board.place(current_row,current_col,board.cubes[current_row][current_col].get_temp())

                    #Checks if board is finished
                    if board.is_finished():
                        #Call verifier to check if sudoku board is correctly solved
                        if board.isValidSudoku():
                            outcome = "success"
                        else:
                            outcome = "failure"

                #Deleting a number
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

            #Displaying the temp number(potential number in cell)
            if board.selected and key != None:
                board.temp_display(key)
                key = None

        board.rebuild_window(play_time, outcome)
        pygame.display.update()
        CLOCK.tick(60)

if __name__ == "__main__":
    main()