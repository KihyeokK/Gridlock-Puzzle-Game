from Board import Board
from Solver import Solver

#file_name = input("file name? ")



fp1 = open(f"puzzles/5x5.txt")
fp2 = open(f"puzzles/5x5solution.txt")
initial, goal = "", ""
for line in fp1.readlines():
    initial += line #constructing a string containing all the lines
for line in fp2.readlines():
    goal += line
board = Board(initial, goal)

solver = Solver(board) #passing the initial board


print(f"Minimum number of moves = {solver.moves()}")
for i, board_position in enumerate(solver.solution()):
    print(f"\nMove # {i}")
    print(board_position)
print(solver.checked_board_positions)

#---------------------------------

import tkinter as tk

PIXELS_PER_SQUARE = 100

class Application(tk.Tk):

    def __init__(self, board):
        super().__init__()


        BOARD_SIZE = PIXELS_PER_SQUARE * board.dimension()
        self.canvas = tk.Canvas(master=self, width=BOARD_SIZE, height=BOARD_SIZE, bg="black")
        self.canvas.pack()

        self.draw_board_base(board)
        self.draw_initial_blocks(board)

    def draw_board_base(self, board):
        '''Draw the board base.'''
        dim = board.dimension()
        for row in range(dim):
            for col in range(dim):
                x = col * PIXELS_PER_SQUARE
                y = row * PIXELS_PER_SQUARE
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE, y + PIXELS_PER_SQUARE, fill="gray")

    def draw_initial_blocks(self, board):
        '''Draw the initial board configuration.'''
        dim = board.dimension()
        blocks = board.starting_blocks()
        for block in blocks:
            direction = blocks[block][1]
            block_length = len(blocks[block][0])
            start_tile = blocks[block][0][0]
            row = start_tile // dim
            col = start_tile % dim
            x = col * PIXELS_PER_SQUARE
            y = row * PIXELS_PER_SQUARE
            if block == "M":
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE * block_length, y + PIXELS_PER_SQUARE, fill="red" )
            elif direction == "horizontal":
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE * block_length, y + PIXELS_PER_SQUARE, fill="yellow" )
            elif direction == "vertical":
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE, y + PIXELS_PER_SQUARE * block_length, fill="yellow" )
                

        



if __name__ == "__main__":
    app = Application(board)
    app.mainloop()



