from Board import Board
from Solver import Solver

#file_name = input("file name? ")



fp1 = open(f"puzzles/6x6-02.txt")
fp2 = open(f"puzzles/6x6-02solution.txt")
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

        self.start_frame()

        self.board = board

        self.board_size = PIXELS_PER_SQUARE * board.dimension()


    def start_frame(self):
        self.start_frame = tk.Frame(master=self)
        self.start_frame.grid(row=1)

        self.welcome = tk.Label(master=self.start_frame, text="Welcome to Gridlock puzzle game!")
        self.welcome.grid(row=1)

        self.choose_level_btn = tk.Button(master=self.start_frame, text="Choose Level", command=self.set_up_canvas)
        self.choose_level_btn.grid(row=2)
    

    def set_up_canvas(self):
        self.main_frame = tk.Frame(master=self)
        self.main_frame.grid(row=1)

        self.middle_frame = tk.Frame(master=self)
        self.middle_frame.grid(row=2)

        self.canvas = tk.Canvas(master=self.main_frame, width=self.board_size, height=self.board_size, bg="black")
        self.canvas.grid(row=2, column=2)

        self.left_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=self.board_size, bg="gray")
        self.left_canvas.grid(row=2, column=1)

        self.right_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=self.board_size, bg="gray")
        self.right_canvas.grid(row=2, column=3)

        self.top_canvas = tk.Canvas(master=self.main_frame, width=self.board_size, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.top_canvas.grid(row=1, column=2)

        self.bottom_canvas = tk.Canvas(master=self.main_frame, width=self.board_size, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.bottom_canvas.grid(row=3, column=2)    

        self.top_left_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.top_right_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.bottom_left_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.bottom_right_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=PIXELS_PER_SQUARE // 2, bg="gray")

        self.top_left_canvas.grid(row=1, column=1)
        self.top_right_canvas.grid(row=1, column=3)
        self.bottom_left_canvas.grid(row=3, column=1)
        self.bottom_right_canvas.grid(row=3, column=3)

        self.bottom_frame = tk.Frame(master=self)
        self.bottom_frame.grid(row=3)

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
        self.display_full_solution_btn.destroy()

        board = self.board
        solver = Solver(board)

        self.solution = solver.solution()
        self.step = 0
        self.max_step = len(self.solution) - 1

        self.move_count = tk.Label(master=self.middle_frame, text="Initial puzzle")
        self.move_count.pack()
        
        self.next_move_btn = tk.Button(master=self.bottom_frame, text="Next Move", command=lambda: [self.increment_step(), self.display_solution_move()]) #two commands
        self.next_move_btn.pack()        

    def display_solution_move(self):
        board = self.solution[self.step] #one board move configuration
        self.draw_solution_blocks(board)
    
    def draw_solution_blocks(self, board):
        '''Draw board configuration of each solution step'''
        #redraw canvas
        self.canvas.destroy()
        self.canvas = tk.Canvas(master=self.main_frame, width=self.board_size, height=self.board_size, bg="black")
        self.canvas.grid(row=2, column=2)
        self.draw_board_base()   

        self.next_move_btn.destroy()
        try:
            self.previous_move_btn.destroy()
        except Exception: #if button not created yet
            pass
        
        if self.step == 0:
            self.move_count["text"] = "Initial puzzle"
        elif self.step == self.max_step:
            self.move_count["text"] = "Puzzle is solved!"
        else:
            self.move_count["text"] = f"move #{self.step}"

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

        #handle buttons displaying
        if self.step == self.max_step:
            self.previous_move_btn = tk.Button(master=self.bottom_frame, text="Previous Move", command=lambda: [self.decrement_step(), self.display_solution_move()])
            self.previous_move_btn.pack()
        elif self.step == 0:
            self.next_move_btn = tk.Button(master=self.bottom_frame, text="Next Move", command=lambda: [self.increment_step(), self.display_solution_move()])
            self.next_move_btn.pack()
        else:
            self.previous_move_btn = tk.Button(master=self.bottom_frame, text="Previous Move", command=lambda: [self.decrement_step(), self.display_solution_move()])
            self.previous_move_btn.pack()

            self.next_move_btn = tk.Button(master=self.bottom_frame, text="Next Move", command=lambda: [self.increment_step(), self.display_solution_move()])
            self.next_move_btn.pack()

    def increment_step(self):
        self.step += 1
    
    def decrement_step(self):
        self.step -= 1






        



if __name__ == "__main__":
    app = Application(board)
    app.mainloop()



