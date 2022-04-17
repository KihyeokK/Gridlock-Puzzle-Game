from Board import Board
from Solver import Solver

fp1 = open("puzzles/6x6-02.txt")
fp2 = open("puzzles/6x6-02-solution.txt")
initial, goal = "", ""
for line in fp1.readlines():
    initial += line #constructing a string containing all the lines
for line in fp2.readlines():
    goal += line
board = Board(initial, goal)

'''print(board)
print(board.blocks)
print(board.occupied_tiles)
print(board.goal_blocks)

for i in board.neighbors():
    print(i)'''

solver = Solver(board) #passing the initial board


print(f"Minimum number of moves = {solver.moves()}")
for i, board_position in enumerate(solver.solution()):
    print(f"\nMove # {i}")
    print(board_position)
print(solver.checked_board_positions)



