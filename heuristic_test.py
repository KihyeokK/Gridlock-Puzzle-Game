from Board import Board
from Solver import Solver

def heuristic_test():
    file_name = input("name of the board file to check: ")
    sol_file_name = file_name[:-4] + "-sol.txt"
    size = file_name[5:8]

    file = open(f"puzzles/puzzle{size}/{file_name}")
    sol_file = open(f"puzzles/puzzle{size}-sol/{sol_file_name}")
    initial, goal = "", ""
    for line in file.readlines():
        initial += line #constructing a string containing all the lines
    for line in sol_file.readlines():
        goal += line

    choose_heuristic = input("Choose heuristic. m for Manhattan distance and wm for weighted Manhattan distance. ")

    if choose_heuristic == "m":
        Board.m = True
        Board.wm = False
    elif choose_heuristic == "wm":
        Board.m = False
        Board.wm = True
    else: 
        Board.m = True #default
        Board.wm = False

    board = Board(initial, goal)    
    solver = Solver(board) #passing the initial board

    print(f"Minimum number of moves = {solver.moves()}")
    for i, board_position in enumerate(solver.solution()):
        print(f"\nMove # {i}")
        print(f"{board_position}")
    print(f"\n{solver.checked_board_positions} board positions checked.")

if __name__ == "__main__":
    heuristic_test()
