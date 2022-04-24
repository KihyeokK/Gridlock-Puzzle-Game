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

        self.board = board

        self.board_size = PIXELS_PER_SQUARE * board.dimension()

        self.top_frame = tk.Frame(master=self)
        self.top_frame.pack()

        self.canvas = tk.Canvas(master=self.top_frame, width=self.board_size, height=self.board_size, bg="black")
        self.canvas.pack()

        self.bottom_frame = tk.Frame(master=self)
        self.bottom_frame.pack()

        self.display_solved_btn = tk.Button(master=self.bottom_frame, text="Show Solved Board")
        self.display_solved_btn.pack()

        self.display_full_solution_btn = tk.Button(master=self.bottom_frame, text="Show Full Solution", command=self.display_full_solution)
        self.display_full_solution_btn.pack()

        self.draw_board_base()
        self.draw_initial_blocks()

    def draw_board_base(self):
        '''Draw the board base.'''
        board = self.board
        dim = board.dimension()
        for row in range(dim):
            for col in range(dim):
                x = col * PIXELS_PER_SQUARE
                y = row * PIXELS_PER_SQUARE
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE, y + PIXELS_PER_SQUARE, fill="gray")

    def draw_initial_blocks(self):
        '''Draw the initial board configuration.'''
        board = self.board
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
                
    def display_full_solution(self):
        board = self.board
        solver = Solver(board)

        self.solution = solver.solution()
        self.step = 0
        self.max_step = len(self.solution) - 1
        
        self.next_move_btn = tk.Button(master=self.bottom_frame, text="Next Move", command=lambda: [self.increment_step(), self.display_solution_move()]) #two commands
        self.next_move_btn.pack()
                
    def display_solution_move(self):
        board = self.solution[self.step] #one board move configuration
        self.draw_solution_blocks(board)
    
    def draw_solution_blocks(self, board):
        '''Draw board configuration of each solution step'''
        #redraw canvas
        self.canvas.destroy()
        self.canvas = tk.Canvas(master=self.top_frame, width=self.board_size, height=self.board_size, bg="blue")
        self.canvas.pack()
        self.draw_board_base()   

        self.next_move_btn.destroy()
        try:
            self.previous_move_btn.destroy()
        except Exception: #if button not created yet
            pass

        #may replace following lines with draw_initial_blocks() after modifying it.
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
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE * block_length, y + PIXELS_PER_SQUARE, fill="white" )
            elif direction == "vertical":
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE, y + PIXELS_PER_SQUARE * block_length, fill="white" )

        if self.step == self.max_step:
            self.previous_move_btn = tk.Button(master=self.bottom_frame, text="Previous Move", command=lambda: [self.decrement_step(), self.display_solution_move()])
            self.previous_move_btn.pack()
        elif self.step == 0:
            self.next_move_btn = tk.Button(master=self.bottom_frame, text="Next Move", command=lambda: [self.increment_step(), self.display_solution_move()]) #two commands
            self.next_move_btn.pack()
        else:
            self.previous_move_btn = tk.Button(master=self.bottom_frame, text="Previous Move", command=lambda: [self.decrement_step(), self.display_solution_move()])
            self.previous_move_btn.pack()

            self.next_move_btn = tk.Button(master=self.bottom_frame, text="Next Move", command=lambda: [self.increment_step(), self.display_solution_move()]) #two commands
            self.next_move_btn.pack()


    def increment_step(self):
        self.step += 1
    
    def decrement_step(self):
        self.step -= 1





        



if __name__ == "__main__":
    app = Application(board)
    app.mainloop()



