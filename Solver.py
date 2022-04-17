from MinPQ import MinPQ
from Board import Board

import functools
@functools.total_ordering
class Node(object):
    def __init__(self, board, moves, node):
        '''Construct a new node object.'''
        self.board = board
        self.moves = moves #g(n)
        self.heuristic = board.heuristic() #h(n) #bd.weighted_heuristic 
        self.total_cost = moves + board.heuristic() #f(n) = g(n) + h(n)
        self.previous = node    
    def __gt__(self, other):
        '''A node is 'greater' than another if the cost plus the
        number of moves is larger. Note that this code will fail
        if 'other' is None.'''
        return (self.total_cost) > (other.total_cost)
    def __eq__(self, other):
        '''Two nodes are equal if the sum of the cost and moves are
        the same. The board itself is ignored.'''
        if self is other: # if a node is compared to itself
            return True
        if other is None: # if a node is compared to None
            return False
        return (self.total_cost) == (other.total_cost)
  

class Solver(object):
    def __init__(self, initial):
        '''Initialize the object by finding the solution for the
        puzzle.'''
        self.__trace = [] 
        current_node = Node(initial, 0, None)
        PQ = MinPQ()
        PQ.insert(current_node)
        self.checked_board_positions = 0
        while not current_node.board.solved():
            self.checked_board_positions += 1
            if not PQ.isEmpty():
                current_node = PQ.delete()
            for neighbor in current_node.board.neighbors():
                if current_node.previous != None and neighbor == current_node.previous.board:
                    continue
                moves = current_node.moves + 1
                PQ.insert(Node(neighbor, moves, current_node))
        
        while current_node != None:
            self.__trace.append(current_node.board)
            current_node = current_node.previous

        self.__trace = self.__trace[::-1]

    def moves(self):
        return(len(self.__trace)-1)

    def solution(self):
        '''Returns a list of Board objects beginning with the initial Board
        and ending with the solved Board.'''
        return self.__trace.copy()