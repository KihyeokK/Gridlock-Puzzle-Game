from Board import Board
from Solver import Solver
import tkinter as tk
import os
import tkinter.dnd
import tkinter.messagebox

PIXELS_PER_SQUARE = 100
LEVEL_FONT_SIZE = 20
MODE_FONT_SIZE = 30
BLOCK_GAP = 5
ADJUSTMENT_TOLERANCE = 40

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

        self.bottom_frame = tk.Frame(master=self)
        self.bottom_frame.grid(row=4)

        #main canvas with board
        self.canvas = tk.Canvas(master=self.main_frame, width=self.board_size, height=self.board_size, bg="black")

        self.left_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=self.board_size, bg="gray")
        self.right_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=self.board_size, bg="gray")
        self.top_canvas = tk.Canvas(master=self.main_frame, width=self.board_size, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.bottom_canvas = tk.Canvas(master=self.main_frame, width=self.board_size, height=PIXELS_PER_SQUARE // 2, bg="gray")  
        self.top_left_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.top_right_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.bottom_left_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=PIXELS_PER_SQUARE // 2, bg="gray")
        self.bottom_right_canvas = tk.Canvas(master=self.main_frame, width=PIXELS_PER_SQUARE // 2, height=PIXELS_PER_SQUARE // 2, bg="gray")

        self.canvas.grid(row=2, column=2)

        self.left_canvas.grid(row=2, column=1)
        self.right_canvas.grid(row=2, column=3)
        self.top_canvas.grid(row=1, column=2)
        self.bottom_canvas.grid(row=3, column=2)
        self.top_left_canvas.grid(row=1, column=1)
        self.top_right_canvas.grid(row=1, column=3)
        self.bottom_left_canvas.grid(row=3, column=1)
        self.bottom_right_canvas.grid(row=3, column=3)

        #self.main_frame.columnconfigure(1, pad=10)
        #self.main_frame.rowconfigure(1, pad=10)
        #self.main_frame.columnconfigure(0, pad=10)
        #self.main_frame.rowconfigure(0, pad=10)
        #self.main_frame.columnconfigure(2, pad=10)
        #self.main_frame.rowconfigure(2, pad=10)

        if puzzle[-3:] == "4x4":
            self.mode_lbl = tk.Label(master=self.top_frame, text="EASY MODE:", font=("Arial", LEVEL_FONT_SIZE))
        elif puzzle[-3:] == "5x5":
            self.mode_lbl = tk.Label(master=self.top_frame, text="INTERMEDIATE MODE:", font=("Arial", LEVEL_FONT_SIZE))
        elif puzzle[-3:] == "6x6":
            self.mode_lbl = tk.Label(master=self.top_frame, text="HARD MODE:", font=("Arial", LEVEL_FONT_SIZE))
        self.mode_lbl.grid(row=1, column=1)
        
        self.level_lbl = tk.Label(master=self.top_frame, text=f"LEVEL {level}", font=("Arial", LEVEL_FONT_SIZE))
        self.level_lbl.grid(row=1, column=2)

        self.choose_again_btn = tk.Button(master=self.middle_frame, text="Choose different mode or level", command=self.choose_again)
        self.choose_again_btn.grid(row=2)

        #self.display_solved_btn = tk.Button(master=self.bottom_frame, text="Show Solved Board")
        #self.display_solved_btn.grid(row=1)

        self.display_full_solution_btn = tk.Button(master=self.bottom_frame, text="Show Full Solution", command=self.display_full_solution)
        self.display_full_solution_btn.grid(row=2)

        self.player_move = 0
        self.player_move_lbl = tk.Label(self.middle_frame, text=f"Moves: {self.player_move}")
        self.player_move_lbl.grid(row=1)

        self.sources = [] #used to keep track of all the sources

        self.draw_board_base()
        self.draw_exit()
        self.draw_blocks(self.board)


    def draw_board_base(self):
        '''Draw the board base.'''
        board = self.board
        dim = board.dimension()
        for row in range(dim):
            for col in range(dim):
                x = col * PIXELS_PER_SQUARE
                y = row * PIXELS_PER_SQUARE
                self.canvas.create_rectangle(x + BLOCK_GAP, y + BLOCK_GAP, x + PIXELS_PER_SQUARE, y + PIXELS_PER_SQUARE, fill="gray")
        
    def draw_exit(self):
        '''Draw exit based on main block's position'''
        board = self.board
        dim = board.dimension()
        blocks = board.starting_blocks()
        for block in blocks:
            if block == "M":
                direction = blocks[block][1]
                start_tile = blocks[block][0][0]
                break
        if direction == "horizontal":
            row = start_tile // dim
            x = 0
            y = row * PIXELS_PER_SQUARE
            self.right_canvas.create_rectangle(x, y, x + PIXELS_PER_SQUARE // 2 + BLOCK_GAP, y + PIXELS_PER_SQUARE + BLOCK_GAP, fill="white")
        elif direction == "vertical":
            col = start_tile // dim
            x = col * PIXELS_PER_SQUARE
            y = 0
            self.bottom_canvas.create_rectangle(x, y, x + PIXELS_PER_SQUARE + BLOCK_GAP, y + PIXELS_PER_SQUARE // 2 + BLOCK_GAP, fill="white")
            

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
            hx1, hy1, hx2, hy2 = x + BLOCK_GAP, y + BLOCK_GAP, x + PIXELS_PER_SQUARE * block_length, y + PIXELS_PER_SQUARE
            vx1, vy1, vx2, vy2 = x + BLOCK_GAP, y + BLOCK_GAP, x + PIXELS_PER_SQUARE, y + PIXELS_PER_SQUARE * block_length
            if block == "M":
                id = self.canvas.create_rectangle(hx1, hy1, hx2, hy2, fill="red", tags="main")
                source = Source(id, self.canvas, board.occupied_tiles, block_length, dim)
                source.attach()
                self.sources.append(source) #used to keep track of all the block sources in a board. Needed to update occupied tiles lists.
            elif direction == "horizontal":
                id = self.canvas.create_rectangle(hx1, hy1, hx2, hy2, fill=block_color, tags="horizontal")
                source = Source(id, self.canvas, board.occupied_tiles, block_length, dim)
                source.attach()
                self.sources.append(source)
            elif direction == "vertical":
                id = self.canvas.create_rectangle(vx1, vy1, vx2, vy2, fill=block_color, tags="vertical")
                source = Source(id, self.canvas, board.occupied_tiles, block_length, dim)
                source.attach()
                self.sources.append(source)
                
    def display_full_solution(self):
        '''Handle display_full_solution_btn click.'''
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
        '''Display board from a solution step, different labels and associated buttons.'''
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

    def display_win_message(self):
        self.choose_again()
        message = f"Successfully escaped from the gridlock!\nRecord: {self.player_move - 1} moves" #escaping does not count as a move, so decrease by 1.
        tkinter.messagebox.showinfo('Success!', message)

    def is_illegal_move(self, source, direction):
        if direction == "rightward":
            current_tile = source.moved_occupied_tiles[-1]
            check_tile = source.initial_occupied_tiles[-1]
            while current_tile != check_tile:
                if current_tile in source.full_occupied_tiles:
                    return True
                print("current and check tiles", current_tile, check_tile)
                current_tile -= 1
            return False
        elif direction == "leftward":
            current_tile = source.moved_occupied_tiles[0]
            check_tile = source.initial_occupied_tiles[0]
            while current_tile != check_tile:
                if current_tile in source.full_occupied_tiles:
                    return True
                print("current and check tiles", current_tile, check_tile)
                current_tile += 1
            return False

    #source is an instance of Source class, containing a canvas item's info
    def dnd_motion(self, source, event):
        full_occupied_tiles = source.full_occupied_tiles
        print("dnd_motion", full_occupied_tiles)
        initial_occupied_tiles = source.initial_occupied_tiles    

        #remove initially occupied tiles from full occupied tiles list
        for tile in initial_occupied_tiles:
            try:
                full_occupied_tiles.remove(tile)
            except Exception:
                pass

        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(source.dndid)
        x1, y1, x2, y2 = x1+1, y1+1, x2-1, y2-1 #bbox makes 1 pixel difference


        moved_head_tile_x = (x1-BLOCK_GAP) // PIXELS_PER_SQUARE
        moved_head_tile_y = (y1-BLOCK_GAP) // PIXELS_PER_SQUARE

        #if moved block is out of canvas
        if x1 < 0: 
            moved_head_tile_x = 0
        if y1 < 0:
            moved_head_tile_y = 0

        #convert to tile_index for 1D representation of the board
        tile_index = moved_head_tile_y * source.dim + moved_head_tile_x

        #get all of occupied tiles for one moved block 
        block_tag = source.block_tag #block_tag is a list of all the tags of a canvas object
        if block_tag[0] == "horizontal" or block_tag[0] == "main":
            source.moved_occupied_tiles = [(tile_index + i) for i in range(source.block_length)] 
        elif block_tag[0] == "vertical":
            source.moved_occupied_tiles = [(tile_index + i*source.dim) for i in range(source.block_length)] 

        print("dnd_motion: initial occupied tiles: ", initial_occupied_tiles)
        print("moved occupied tiles:", source.moved_occupied_tiles)

        self.left_should_move_back = False #for leftward movement
        self.right_should_move_back = False #for rightward movement
        self.up_should_move_back = False
        self.down_should_move_back = False
        if block_tag[0] == "horizontal" or block_tag[0] == "main":
            for tile in source.moved_occupied_tiles:
                if tile in full_occupied_tiles:
                    self.left_should_move_back = True
                    break 
            for tile in source.moved_occupied_tiles:
                if tile in full_occupied_tiles: #To check tail tile as well
                    self.right_should_move_back = True
                    break
                if tile+1 in full_occupied_tiles:
                    self.right_should_move_back = True
                    break
            self.canvas.move(source.dndid, x-x1, 0)
            #tile_x_position = ((tile+1) % source.dim) * PIXELS_PER_SQUARE
            #print("tile x:", tile_x_position)
            #self.canvas.move(source.dndid, (x//PIXELS_PER_SQUARE +1)*PIXELS_PER_SQUARE-x1//PIXELS_PER_SQUARE*PIXELS_PER_SQUARE, 0)
        elif block_tag[0] == "vertical":
            for tile in source.moved_occupied_tiles:
                if tile in full_occupied_tiles:
                    self.up_should_move_back = True
                    break
            for tile in source.moved_occupied_tiles:
                if tile in full_occupied_tiles: #To check tail tile as well
                    self.right_should_move_back = True
                    break
                if tile+source.dim in full_occupied_tiles:
                    self.up_should_move_back = True
                    break  
            self.canvas.move(source.dndid, 0, y-y1)

    def update_horizontal_source(self, source, x1, y1, x2, y2):
        print("SOURCES", self.sources)
        #update source object for following movements
        for tile in source.initial_occupied_tiles:
            for src in self.sources:
                print(f"inside update: initial occupied tiles: {tile}")
                try:
                    src.full_occupied_tiles.remove(tile)
                except Exception:
                    pass
        print(f"out of loop inside update: initial occupied tiles: {source.initial_occupied_tiles}")
        source.initial_occupied_tiles = []
        for tile in [int(((y1-BLOCK_GAP) // PIXELS_PER_SQUARE * source.dim + (x1-BLOCK_GAP) // PIXELS_PER_SQUARE + i)) for i in range(source.block_length)]:
            for src in self.sources:    
                print("UPDATE IN EVERY SOURCES: full occupied tiles change : ", tile)
                print("ORIGINAL SRC full occupied tiles", src.full_occupied_tiles)
                if tile not in src.full_occupied_tiles:
                    src.full_occupied_tiles.append(tile)
                src.full_occupied_tiles = sorted(src.full_occupied_tiles)
                print("ALL SOURCES full occupied tiles updating", src.full_occupied_tiles)
            source.initial_occupied_tiles.append(tile)
            print("update: tile added to initial occupied list: ", tile)
        print("update full occupied tiles: ", source.full_occupied_tiles)
        source.initial_occupied_tile_head_i = source.full_occupied_tiles.index(source.initial_occupied_tiles[0])
        source.initial_occupied_tile_tail_i = source.full_occupied_tiles.index(source.initial_occupied_tiles[-1])

        source.block_coords = (x1, y1, x2, y2)
        print("update full occupied tiles: ", source.full_occupied_tiles)
        print("important block coords: ", source.block_coords)

    def update_vertical_source(self, source, x1, y1, x2, y2):
        #update source object for following movements
        for tile in source.initial_occupied_tiles:
            for src in self.sources:
                print(f"inside update: initial occupied tiles: {tile}")
                try:
                    src.full_occupied_tiles.remove(tile)
                except Exception:
                    pass
        print(f"out of loop inside update: initial occupied tiles: {source.initial_occupied_tiles}")
        source.initial_occupied_tiles = []
        for tile in [int(((y1-BLOCK_GAP) // PIXELS_PER_SQUARE * source.dim + (x1-BLOCK_GAP) // PIXELS_PER_SQUARE + i*source.dim)) for i in range(source.block_length)]:
            for src in self.sources:    
                print("UPDATE IN EVERY SOURCES: full occupied tiles change : ", tile)
                print("ORIGINAL SRC full occupied tiles", src.full_occupied_tiles)
                if tile not in src.full_occupied_tiles:
                    src.full_occupied_tiles.append(tile)
                src.full_occupied_tiles = sorted(src.full_occupied_tiles)
                print("ALL SOURCES full occupied tiles updating", src.full_occupied_tiles)
            source.initial_occupied_tiles.append(tile)
            print("update: tile added to initial occupied list: ", tile)
        print("update full occupied tiles: ", source.full_occupied_tiles)
        source.initial_occupied_tile_head_i = source.full_occupied_tiles.index(source.initial_occupied_tiles[0])
        source.initial_occupied_tile_tail_i = source.full_occupied_tiles.index(source.initial_occupied_tiles[-1])

        source.block_coords = (x1, y1, x2, y2)
        print("update full occupied tiles: ", source.full_occupied_tiles)
        print("important block coords: ", source.block_coords)

    def dnd_accept(self, source, event):
        return self

    def dnd_enter(self, source, event):
        self.dnd_motion(source, event)

    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = source.where(self.canvas, event)
    
    def dnd_leave(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(source.dndid)
        x1, y1, x2, y2 = x1+1, y1+1, x2-1, y2-1
        print("x:", x)
        print("coordinates of the block in movement",x1,y1,x2,y2)
        block_tag = source.block_tag
        self.canvas.delete(source.dndid)

        #handle block positioning when the moved position is out of the board size.
        if x1 < 0:
            block_length = x2-x1 #block length in terms of canvas coordinates
            x1, x2 = BLOCK_GAP, block_length + BLOCK_GAP
            source.moved_occupied_tiles = [(y1 // PIXELS_PER_SQUARE * source.dim + i) for i in range(source.block_length)]
            print("moved block out of canvas, so had to change value", source.moved_occupied_tiles)        
        elif y1 < 0:
            block_length = y2-y1
            y1, y2 = BLOCK_GAP, block_length + BLOCK_GAP
            source.moved_occupied_tiles = [(x1 // PIXELS_PER_SQUARE + i*source.dim) for i in range(source.block_length)]
            print("moved block out of canvas, so had to change value", source.moved_occupied_tiles)
        elif x2 > self.board_size:
            block_length = x2-x1
            x1, x2 = self.board_size - block_length, self.board_size
            source.moved_occupied_tiles = [(y1 // PIXELS_PER_SQUARE * source.dim + source.dim - 1 - i) for i in range(source.block_length)][::-1]
            print("moved block out of canvas, so had to change value", source.moved_occupied_tiles)
        elif y2 > self.board_size:
            block_length = y2-y1
            y1, y2 = self.board_size - block_length, self.board_size
            source.moved_occupied_tiles = [(x1 // PIXELS_PER_SQUARE + (source.dim - 1)*source.dim - i*source.dim) for i in range(source.block_length)][::-1]
            print("moved block out of canvas, so had to change value", source.moved_occupied_tiles)

        #for rectangle drawing
        ix1, iy1, ix2, iy2 = source.block_coords #initial coords
        print("x1, x2: ", x1, x2)
        print("ix1: ", ix1, iy1, ix2, iy2)
        if block_tag[0] == "horizontal" or block_tag[0] == "main":
            if block_tag[0] == "main":
                fill_color = "red"
            else:
                fill_color = "silver"
            print("moved:", source.moved_occupied_tiles)
            print("initial occupied tiles", source.initial_occupied_tiles)
            print("moved tale tile", source.moved_occupied_tiles[-1])
            print("horizontal left and right full occupied tiles", source.full_occupied_tiles)
            #if any of the tiles occupied by the moved block overlaps with any other block, don't allow any movement, since it is an illegal move.
            # 
            if any([(source.moved_occupied_tiles[-1-i] in source.full_occupied_tiles) for i in range(source.block_length)]) and ix1-abs(x1) > 0: #if movement is leftward
                for i in range(source.block_length):
                    tile = source.moved_occupied_tiles[-1-i] #[-1-i] is important. This will prevent moving block from overlapping with another block when more than two blocks are overlapping along the way.
                    if tile in source.full_occupied_tiles:
                        overlapping_tile = tile
                        break
                #reinsert initially occupied tiles for overlapping handling
                for tile in source.initial_occupied_tiles:
                    for src in self.sources:
                        if tile not in src.full_occupied_tiles:
                            src.full_occupied_tiles.append(tile)
                        src.full_occupied_tiles = sorted(src.full_occupied_tiles)
                        print("tile added", src.full_occupied_tiles)
                source.full_occupied_tiles = sorted(source.full_occupied_tiles) #should be sorted to get correct overlapping tile
                print('leftward movement')
                print("full occupied list:", source.full_occupied_tiles)
                print("overlapping tile:", overlapping_tile)
                overlap_x1 = (overlapping_tile) % source.dim * PIXELS_PER_SQUARE
                overlap_x2 = (overlapping_tile) % source.dim * PIXELS_PER_SQUARE + PIXELS_PER_SQUARE
                adjusted_x1 = (overlapping_tile+1) % source.dim * PIXELS_PER_SQUARE + BLOCK_GAP
                adjusted_x2 = (overlapping_tile+1) % source.dim * PIXELS_PER_SQUARE + source.block_length * PIXELS_PER_SQUARE
                print("adj:", adjusted_x1)
                if self.is_illegal_move(source, "leftward") and abs(overlap_x2 - x1) > ADJUSTMENT_TOLERANCE:
                    self.moved_block_id = self.canvas.create_rectangle(ix1, iy1, ix2, iy2,  fill=fill_color, tags=f"{block_tag[0]}")
                    self.player_move -= 1 #so that it doesn't change. (Since it's an illegal move)
                else:
                    print("adjusted movement") 
                    self.moved_block_id = self.canvas.create_rectangle(adjusted_x1, y1, adjusted_x2, y2,  fill=fill_color, tags=f"{block_tag[0]}")

                    #update source object for following movements
                    self.update_horizontal_source(source, adjusted_x1, y1, adjusted_x2, y2)

            elif any([((source.moved_occupied_tiles[0+i] + 1) in source.full_occupied_tiles) for i in range(source.block_length)]) and ix1-abs(x1) < 0: #for rightward movement
                for i in range(source.block_length):
                    tile = source.moved_occupied_tiles[0+i] + 1 #[0+i] + 1 is important. This will prevent moving block from overlapping with another block when more than two blocks are overlapping along the way.
                    if tile in source.full_occupied_tiles:
                        overlapping_tile = tile
                        break
                for tile in source.initial_occupied_tiles:
                    for src in self.sources:
                        if tile not in src.full_occupied_tiles:
                            src.full_occupied_tiles.append(tile)
                        print("tile is being added to full occupied tiles IN EVERY SOURCES for overlapping tile calc", tile)
                        src.full_occupied_tiles = sorted(src.full_occupied_tiles)
                        print("tile added//", src.full_occupied_tiles)
                source.full_occupied_tiles = sorted(source.full_occupied_tiles) #sort
                print("tile added full occupied tiles list", source.full_occupied_tiles)
                print('occupied rightward movement')
                print("overlapping tile: ", overlapping_tile)
                overlap_x1 = (overlapping_tile) % source.dim * PIXELS_PER_SQUARE #overlapping tile's coordinates
                overlap_x2 = (overlapping_tile) % source.dim * PIXELS_PER_SQUARE + PIXELS_PER_SQUARE
                adjusted_x1 = (overlapping_tile - source.block_length) % source.dim * PIXELS_PER_SQUARE + BLOCK_GAP
                adjusted_x2 = (overlapping_tile - source.block_length) % source.dim * PIXELS_PER_SQUARE + source.block_length * PIXELS_PER_SQUARE
                if self.is_illegal_move(source, "rightward") and abs(overlap_x1 - x2) > ADJUSTMENT_TOLERANCE:
                    ix1, iy1, ix2, iy2 = source.block_coords #initial coords
                    self.moved_block_id = self.canvas.create_rectangle(ix1, iy1, ix2, iy2,  fill=fill_color, tags=f"{block_tag[0]}")
                    self.player_move -= 1 #so that move count doesn't change. Illegal move attempt won't count as a move.
                    #no need for occupied tiles update
                else:
                    print("adjusted movement")
                    print("adjusted x1, x2", adjusted_x1, adjusted_x2)
                    self.moved_block_id = self.canvas.create_rectangle(adjusted_x1, y1, adjusted_x2, y2,  fill=fill_color, tags=f"{block_tag[0]}")          
            
                    #update source object for following movements
                    self.update_horizontal_source(source, adjusted_x1, y1, adjusted_x2, y2)
            
            elif ix1-abs(x1) > 0: #for leftward normal movement
                print("normal leftward movement")  
                if x1 == BLOCK_GAP: #if out of range while doing normal leftward movement
                    self.moved_block_id = self.canvas.create_rectangle(x1, y1, x2, y2,  fill=fill_color, tags=f"{block_tag[0]}")
                    self.update_horizontal_source(source, x1, y1, x2, y2)
                elif self.is_illegal_move(source, "leftward"):
                    ix1, iy1, ix2, iy2 = source.block_coords #initial coords
                    self.moved_block_id = self.canvas.create_rectangle(ix1, iy1, ix2, iy2,  fill=fill_color, tags=f"{block_tag[0]}")
                else: 
                    print("snap left")
                    snap_x1 = (x1-BLOCK_GAP) // PIXELS_PER_SQUARE * PIXELS_PER_SQUARE + BLOCK_GAP
                    snap_x2 = x2 // PIXELS_PER_SQUARE * PIXELS_PER_SQUARE
                    print("snapx1, snapx2 ", snap_x1, snap_x2) 
                    self.moved_block_id = self.canvas.create_rectangle(snap_x1, y1, snap_x2, y2,  fill=fill_color, tags=f"{block_tag[0]}")
                    #update source object for following movements
                    self.update_horizontal_source(source, snap_x1, y1, snap_x2, y2)
                
            elif ix1-abs(x1) < 0: #for rightward normal movement:
                print("normal rightward movement")
                if x2 == self.board_size:
                    print("normal out of canvas move ")
                    self.moved_block_id = self.canvas.create_rectangle(x1, y1, x2, y2,  fill=fill_color, tags=f"{block_tag[0]}")
                    self.update_horizontal_source(source, x1, y1, x2, y2)
                elif self.is_illegal_move(source, "rightward"):
                    ix1, iy1, ix2, iy2 = source.block_coords #initial coords
                    self.moved_block_id = self.canvas.create_rectangle(ix1, iy1, ix2, iy2,  fill=fill_color, tags=f"{block_tag[0]}") 
                else: 
                    print("snap right")
                    snap_x1 = ((x1-BLOCK_GAP) // PIXELS_PER_SQUARE + 1) * PIXELS_PER_SQUARE + BLOCK_GAP
                    snap_x2 = (x2 // PIXELS_PER_SQUARE + 1) * PIXELS_PER_SQUARE 
                    print("snapx1, snapx2 ", snap_x1, snap_x2)
                    self.moved_block_id = self.canvas.create_rectangle(snap_x1, y1, snap_x2, y2,  fill=fill_color, tags=f"{block_tag[0]}")
                    #update source object for following movements
                    self.update_horizontal_source(source, snap_x1, y1, snap_x2, y2)

            else:
                print("out of canvas movement")
                self.moved_block_id = self.canvas.create_rectangle(x1, y1, x2, y2,  fill=fill_color, tags=f"{block_tag[0]}")
                #update source object for following movements
                self.update_horizontal_source(source, x1, y1, x2, y2)

        elif block_tag[0] == "vertical":
            if any([(source.moved_occupied_tiles[-1-i] in source.full_occupied_tiles) for i in range(source.block_length)]) and iy1-abs(y1) > 0: #if movement is upward
                for i in range(source.block_length):
                    tile = source.moved_occupied_tiles[-1-i] #[-1-i] is important. This will prevent moving block from overlapping with another block when more than two blocks are overlapping along the way.
                    if tile in source.full_occupied_tiles:
                        overlapping_tile = tile
                        break
                print("overlapping tile:", overlapping_tile)
                #reinsert initially occupied tiles for overlapping handling
                for tile in source.initial_occupied_tiles:
                    for src in self.sources:
                        if tile not in src.full_occupied_tiles:
                            src.full_occupied_tiles.append(tile)
                        src.full_occupied_tiles = sorted(src.full_occupied_tiles)
                        print("tile added", src.full_occupied_tiles)
                print("full occupied list:", source.full_occupied_tiles)
                overlap_y1 = (overlapping_tile) // source.dim * PIXELS_PER_SQUARE
                overlap_y2 = (overlapping_tile) // source.dim * PIXELS_PER_SQUARE + PIXELS_PER_SQUARE
                adjusted_y1 = (overlapping_tile + source.dim) // source.dim * PIXELS_PER_SQUARE + BLOCK_GAP
                adjusted_y2 = (overlapping_tile + source.dim) // source.dim * PIXELS_PER_SQUARE + source.block_length * PIXELS_PER_SQUARE 
                print("adjusted y1:", adjusted_y1)
                if self.up_should_move_back and abs(overlap_y2 - y1) > ADJUSTMENT_TOLERANCE:
                    self.moved_block_id = self.canvas.create_rectangle(ix1, iy1, ix2, iy2,  fill="silver", tags=f"{block_tag[0]}")
                    self.player_move -= 1 #so that it doesn't change. (Since it's an illegal move)
                else:
                    print("adjusted movement")
                    self.moved_block_id = self.canvas.create_rectangle(x1, adjusted_y1, x2, adjusted_y2,  fill="silver", tags=f"{block_tag[0]}")
                    #update source object for following movements
                    self.update_vertical_source(source, x1, adjusted_y1, x2, adjusted_y2)

            elif any([((source.moved_occupied_tiles[0+i] + source.dim) in source.full_occupied_tiles) for i in range(source.block_length)]) and iy1-abs(y1) < 0: #if movement is downward
                for i in range(source.block_length):
                    tile = source.moved_occupied_tiles[0+i] + source.dim
                    if tile in source.full_occupied_tiles:
                        overlapping_tile = tile
                        break
                print("overlapping tile:", overlapping_tile)
                #reinsert initially occupied tiles for overlapping handling
                for tile in source.initial_occupied_tiles:
                    for src in self.sources:
                        if tile not in src.full_occupied_tiles:
                            src.full_occupied_tiles.append(tile)
                        src.full_occupied_tiles = sorted(src.full_occupied_tiles)
                        print("tile added", src.full_occupied_tiles)
                print("full occupied list:", source.full_occupied_tiles)
                overlap_y1 = (overlapping_tile) // source.dim * PIXELS_PER_SQUARE
                overlap_y2 = (overlapping_tile) // source.dim * PIXELS_PER_SQUARE + PIXELS_PER_SQUARE
                adjusted_y1 = (overlapping_tile - source.dim * source.block_length) // source.dim * PIXELS_PER_SQUARE + BLOCK_GAP
                adjusted_y2 = (overlapping_tile - source.dim * source.block_length) // source.dim * PIXELS_PER_SQUARE + source.block_length * PIXELS_PER_SQUARE 
                print("adjusted y1 and y2:", adjusted_y1, adjusted_y2)
                if self.down_should_move_back and abs(overlap_y1 - y2) > ADJUSTMENT_TOLERANCE:
                    print("asdfklsajfjfldaf")
                    self.moved_block_id = self.canvas.create_rectangle(ix1, iy1, ix2, iy2, fill="silver", tags=f"{block_tag[0]}")
                    self.player_move -= 1 #so that it doesn't change. (Since it's an illegal move)
                else:
                    print("adjusted movement")
                    self.moved_block_id = self.canvas.create_rectangle(x1, adjusted_y1, x2, adjusted_y2, fill="silver", tags=f"{block_tag[0]}")
                    #update source object for following movements
                    self.update_vertical_source(source, x1, adjusted_y1, x2, adjusted_y2)

            elif iy1-abs(y1) > 0: #for upward normal movement
                print("normal upward movement")  
                if y1 == BLOCK_GAP: #if out of range while doing normal upward movement
                    self.moved_block_id = self.canvas.create_rectangle(x1, y1, x2, y2,  fill="silver", tags=f"{block_tag[0]}")
                    self.update_vertical_source(source, x1, y1, x2, y2)
                else: 
                    print("snap up")
                    snap_y1 = (y1-BLOCK_GAP) // PIXELS_PER_SQUARE * PIXELS_PER_SQUARE + BLOCK_GAP
                    snap_y2 = y2 // PIXELS_PER_SQUARE * PIXELS_PER_SQUARE
                    print("snapy1, snapy2 ", snap_y1, snap_y2) 
                    self.moved_block_id = self.canvas.create_rectangle(x1, snap_y1, x2, snap_y2,  fill="silver", tags=f"{block_tag[0]}")
                    #update source object for following movements
                    self.update_vertical_source(source, x1, snap_y1, x2, snap_y2)
                
            elif iy1-abs(y1) < 0: #for downward normal movement:
                print("normal downward movement")
                if y2 == self.board_size:
                    print("normal out of canvas move ")
                    self.moved_block_id = self.canvas.create_rectangle(x1, y1, x2, y2,  fill="silver", tags=f"{block_tag[0]}")
                    self.update_vertical_source(source, x1, y1, x2, y2)
                else: 
                    print("snap down")
                    snap_y1 = ((y1-BLOCK_GAP) // PIXELS_PER_SQUARE + 1) * PIXELS_PER_SQUARE + BLOCK_GAP
                    snap_y2 = (y2 // PIXELS_PER_SQUARE + 1) * PIXELS_PER_SQUARE 
                    print("snapy1, snapy2 ", snap_y1, snap_y2)
                    self.moved_block_id = self.canvas.create_rectangle(x1, snap_y1, x2, snap_y2,  fill="silver", tags=f"{block_tag[0]}")
                    #update source object for following movements
                    self.update_vertical_source(source, x1, snap_y1, x2, snap_y2)  
            else:
                print("out of canvas movement")
                self.moved_block_id = self.canvas.create_rectangle(x1, y1, x2, y2,  fill="silver", tags=f"{block_tag[0]}")
                #update source object for following movements
                self.update_vertical_source(source, x1, y1, x2, y2)

        source.dndid = self.moved_block_id #updating the source object
        source.attach()   

        self.player_move += 1
        self.player_move_lbl.destroy()
        self.player_move_lbl = tk.Label(self.middle_frame, text=f"Moves: {self.player_move}")
        self.player_move_lbl.grid(row=1)

        if block_tag[0] == "main" and x2 == self.board_size and not self.is_illegal_move(source, "rightward"):
            self.display_win_message()

class Source:
    def __init__(self, id, canvas, occupied_tiles, block_length, dimension):
        self.canvas = canvas
        self.dndid = id
        self.full_occupied_tiles = occupied_tiles #every occupied tiles
        self.block_length = block_length #block length in terms of number of occupied tiles for one block
        self.dim = dimension
        self.block_tag = self.canvas.gettags(self.dndid) #block_tag is a list of all the tags of a canvas object
        print("occupied:", self.full_occupied_tiles)
        print(self.block_tag[0])

        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)

        initial_x_tile_position = x1 // PIXELS_PER_SQUARE
        initial_y_tile_position = y1 // PIXELS_PER_SQUARE

        #convert to tile_index for 1D representation of the board
        tile_index = int(initial_y_tile_position * self.dim + initial_x_tile_position)

        #get all of initially occupied tiles for one block
        if self.block_tag[0] == "horizontal" or self.block_tag[0] == "main":
            self.initial_occupied_tiles = [(tile_index + i) for i in range(self.block_length)]
        elif self.block_tag[0] == "vertical":
            self.initial_occupied_tiles = [(tile_index + i*self.dim) for i in range(self.block_length)]
        print("source: initial occupied tiles", self.initial_occupied_tiles) 
        self.moved_occupied_tiles = [] 
        self.block_coords = (x1+1, y1+1, x2-1, y2-1) #bbox makes -1 pixel difference #needs to be updated when new position 
        print("self.block_coords: ", self.block_coords)

    def attach(self):
        self.canvas.tag_bind(self.dndid, '<ButtonPress-1>', self.press)

    def press(self, event):
        if tkinter.dnd.dnd_start(self, event):
            x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
            self.x_off = event.x - x1 #x position of pointer - x position of block
            self.y_off = event.y - y1
    
    def dnd_end(self, target, event):
        pass
    
    def where(self, canvas, event):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        return x - self.x_off, y - self.y_off

    
    









        



if __name__ == "__main__":
    app = Application()
    app.mainloop()



