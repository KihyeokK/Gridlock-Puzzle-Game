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

    board = Board(initial, goal)
    solver = Solver(board) #passing the initial board

    print(f"Minimum number of moves = {solver.moves()}")
    for i, board_position in enumerate(solver.solution()):
        print(f"\nMove # {i}")
        print(f"{board_position}")
    print(f"\n{solver.checked_board_positions} board positions checked.")

def main_test():
    heuristic = input("Choose heuristic. Type a single integer, 1 or 2:\n1.Manhattan Distance \n2.Weighted Manhattan Distance \n")
    if heuristic == "1":
        Board.m = True
        Board.wm = False
        heuristic_test()
    elif heuristic == "2":
        Board.m = False
        Board.wm = True
        heuristic_test()
    else:
        raise Exception("Please enter a single integer, 1 or 2.")

if __name__ == "__main__":
    main_test()
