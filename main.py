from Board import Board
from Solver import Solver

#file_name = input("file name? ")



fp1 = open(f"puzzles/puzzle6x6/board6x6-3.txt")
fp2 = open(f"puzzles/puzzle6x6-sol/board6x6-3-sol.txt")
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
import os

PIXELS_PER_SQUARE = 100
LEVEL_FONT_SIZE = 20
MODE_FONT_SIZE = 30

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        width_position = self.winfo_screenwidth()//2 - self.winfo_reqwidth()
        height_position = self.winfo_screenheight()//2 - self.winfo_reqheight()
        self.geometry(f"+{width_position}+{height_position}")
        self.title('Gridlock Puzzle Game')
        self.display_start_frame()

    def display_start_frame(self):
        self.start_frame = tk.Frame(master=self)
        self.start_frame.grid(row=1)

        self.welcome_lbl = tk.Label(master=self.start_frame, text="Welcome to Gridlock Puzzle Game!",width=30, height=5)
        self.welcome_lbl.config(font=("Arial", 40))
        self.welcome_lbl.grid(row=1, column=1)

        self.choose_level_btn = tk.Button(master=self.start_frame, text="Choose Level", command=self.display_choose_level_frame)
        self.choose_level_btn.config(font=("Arial", LEVEL_FONT_SIZE), padx=5, pady=10)
        self.choose_level_btn.grid(row=2, column=1)

    def display_choose_level_frame(self):
        try:
            self.start_frame.destroy()
        except Exception:
            pass

        self.choose_level_frame = tk.Frame(master=self)
        self.choose_level_frame.grid(row=1)

        self.easy = tk.Label(master=self.choose_level_frame, text="Easy Mode: 4x4 puzzles", width=30, height=2)
        self.intermediate = tk.Label(master=self.choose_level_frame, text="Intermediate Mode: 5x5 puzzles", width=30, height=2)
        self.hard = tk.Label(master=self.choose_level_frame, text="Hard Mode: 6x6 puzzles", width=30, height=2)

        self.easy.config(font=("Arial", MODE_FONT_SIZE))
        self.intermediate.config(font=("Arial", MODE_FONT_SIZE))
        self.hard.config(font=("Arial", MODE_FONT_SIZE))

        self.easy.grid(row=1, column=1)
        self.intermediate.grid(row=3, column=1)
        self.hard.grid(row=5, column=1)

        self.display_levels()

    def display_levels(self):
        '''Display level buttons.'''
        self.level_frame1 = tk.Frame(master=self.choose_level_frame)
        self.level_frame2 = tk.Frame(master=self.choose_level_frame)
        self.level_frame3 = tk.Frame(master=self.choose_level_frame)

        self.level_frame1.grid(row=2, column=1)
        self.level_frame2.grid(row=4, column=1)
        self.level_frame3.grid(row=6, column=1)

        easy, intermediate, hard = self.get_puzzle_names()

        for i in range(len(easy)):
            self.level_btn = tk.Button(master=self.level_frame1, text=f"Level {i+1}", command=lambda level=i+1: self.display_canvas("4x4", level))
            self.level_btn.config(font=("Arial", LEVEL_FONT_SIZE), padx=3, pady=5)
            self.level_btn.grid(row=1, column=i+1)

        for i in range(len(intermediate)):
            self.level_btn = tk.Button(master=self.level_frame2, text=f"Level {i+1}", command=lambda level=i+1: self.display_canvas("5x5", level))
            self.level_btn.config(font=("Arial", LEVEL_FONT_SIZE), padx=3, pady=5)
            self.level_btn.grid(row=1, column=i+1)

        for i in range(len(hard)):
            self.level_btn = tk.Button(master=self.level_frame3, text=f"Level {i+1}", command=lambda level=i+1: self.display_canvas("6x6", level))
            self.level_btn.config(font=("Arial", LEVEL_FONT_SIZE), padx=3, pady=5)
            self.level_btn.grid(row=1, column=i+1)  

    @staticmethod
    def get_puzzle_names():
        puzzles = []
        puzzles.append(os.listdir("puzzles/puzzle4x4"))
        puzzles.append(os.listdir("puzzles/puzzle5x5"))
        puzzles.append(os.listdir("puzzles/puzzle6x6"))

        return puzzles        

    def get_board(self, puzzle, level):
        '''Read puzzle files and return board instance.'''
        fp1 = open(f"puzzles/puzzle{puzzle}/board{puzzle}-{level}.txt")
        fp2 = open(f"puzzles/puzzle{puzzle}-sol/board{puzzle}-{level}-sol.txt")
        initial, goal = "", ""
        for line in fp1.readlines():
            initial += line #constructing a string containing all the lines
        for line in fp2.readlines():
            goal += line
        board = Board(initial, goal)

        return board
        


    def display_canvas(self, puzzle, level):
        self.choose_level_frame.destroy()

        self.board = self.get_board(puzzle, level)

        self.board_size = PIXELS_PER_SQUARE * self.board.dimension()

        self.top_frame = tk.Frame(master=self)
        self.top_frame.grid(row=1)

        self.main_frame = tk.Frame(master=self)
        self.main_frame.grid(row=2)

        self.middle_frame = tk.Frame(master=self)
        self.middle_frame.grid(row=3)

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
        self.bottom_frame.grid(row=4)

        if puzzle[-3:] == "4x4":
            self.mode_lbl = tk.Label(master=self.top_frame, text="EASY MODE:")
        elif puzzle[-3:] == "5x5":
            self.mode_lbl = tk.Label(master=self.top_frame, text="INTERMEDIATE MODE:")
        elif puzzle[-3:] == "6x6":
            self.mode_lbl = tk.Label(master=self.top_frame, text="HARD MODE:")
        self.mode_lbl.grid(row=1, column=1)
        self.mode_lbl.config(font=("Arial", LEVEL_FONT_SIZE))
        
        self.level_lbl = tk.Label(master=self.top_frame, text=f"LEVEL {level}")
        self.level_lbl.config(font=("Arial", LEVEL_FONT_SIZE))
        self.level_lbl.grid(row=1, column=2)

        self.choose_again_btn = tk.Button(master=self.middle_frame, text="Choose different mode or level", command=self.choose_again)
        self.choose_again_btn.grid(row=2)

        #self.display_solved_btn = tk.Button(master=self.bottom_frame, text="Show Solved Board")
        #self.display_solved_btn.grid(row=1)

        self.display_full_solution_btn = tk.Button(master=self.bottom_frame, text="Show Full Solution", command=self.display_full_solution)
        self.display_full_solution_btn.grid(row=2)

        self.draw_board_base()
        self.draw_blocks(self.board)



    def draw_board_base(self):
        '''Draw the board base.'''
        board = self.board
        dim = board.dimension()
        for row in range(dim):
            for col in range(dim):
                x = col * PIXELS_PER_SQUARE
                y = row * PIXELS_PER_SQUARE
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE, y + PIXELS_PER_SQUARE, fill="gray")

    def draw_blocks(self, board, block_color="yellow"):
        '''Draw the board configuration.'''
        board = board
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
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE * block_length, y + PIXELS_PER_SQUARE, fill=block_color )
            elif direction == "vertical":
                self.canvas.create_rectangle(x + 5, y + 5, x + PIXELS_PER_SQUARE, y + PIXELS_PER_SQUARE * block_length, fill=block_color )
                
    def display_full_solution(self):
        self.display_full_solution_btn.destroy()

        board = self.board
        solver = Solver(board)

        self.solution = solver.solution()
        self.step = 0
        self.max_step = len(self.solution) - 1

        self.move_count_lbl = tk.Label(master=self.middle_frame, text="")
        self.move_count_lbl.grid(row=1)

        self.display_solution_move()   
    
    def display_solution_move(self):
        '''Display board of each solution step, different lables and associated buttons.'''
        board = self.solution[self.step] #one board move configuration

        #redraw canvas
        self.canvas.destroy()
        self.canvas = tk.Canvas(master=self.main_frame, width=self.board_size, height=self.board_size, bg="black")
        self.canvas.grid(row=2, column=2)
        self.draw_board_base()   

        try:
            self.next_move_btn.destroy()
            self.previous_move_btn.destroy()
        except Exception: #if button not created yet
            pass
            
        #top label
        if self.step == 0:
            self.move_count_lbl["text"] = "Initial puzzle"
        elif self.step == self.max_step:
            self.move_count_lbl["text"] = "Puzzle is solved!"
        else:
            self.move_count_lbl["text"] = f"move #{self.step}"

        #replaced
        self.draw_blocks(board, "white")

        #handle buttons displaying
        if self.step == self.max_step:
            self.previous_move_btn = tk.Button(master=self.bottom_frame, text="Previous Move", command=lambda: [self.decrease_step(), self.display_solution_move()])
            self.previous_move_btn.grid(row=2, column=1)
        elif self.step == 0:
            self.next_move_btn = tk.Button(master=self.bottom_frame, text="Next Move", command=lambda: [self.increase_step(), self.display_solution_move()])
            self.next_move_btn.grid(row=2, column=2)
        else:
            self.previous_move_btn = tk.Button(master=self.bottom_frame, text="Previous Move", command=lambda: [self.decrease_step(), self.display_solution_move()])
            self.previous_move_btn.grid(row=2, column=1)

            self.next_move_btn = tk.Button(master=self.bottom_frame, text="Next Move", command=lambda: [self.increase_step(), self.display_solution_move()])
            self.next_move_btn.grid(row=2, column=2)

    def choose_again(self):
        self.top_frame.destroy()
        self.main_frame.destroy()
        self.middle_frame.destroy()
        self.bottom_frame.destroy()

        self.display_choose_level_frame()

    def increase_step(self):
        self.step += 1
    
    def decrease_step(self):
        self.step -= 1






        



if __name__ == "__main__":
    app = Application()
    app.mainloop()



