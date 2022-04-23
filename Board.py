    #possible tiles: head, mid, tail
    #possible length
    #possible directions: horizontal, vertical
import copy 

class Board(object):
    def __init__(self, current, solved = None):
        if type(current) == str:
            start, goal = current.split(), solved.split()
            dim = int(start[0]) #dimension
            start = start[1:]
            
            blocks, occupied_tiles = self.get_start_blocks(start, dim)
            goal_blocks = self.get_goal_blocks(goal)

            board = self.create_1D_board(blocks, dim)

        elif type(current) == dict: #for neighbors
            dim = current.pop("dim")
            goal_blocks = current.pop("goalBlocks")
            blocks = current
            occupied_tiles = []
            for value in blocks.values():
                for tile in value[0]:
                    occupied_tiles.append(tile)


            board = self.create_1D_board(blocks, dim)

        self.goal_blocks = goal_blocks
        self.__dim = dim
        self.__board = board
        self.blocks = blocks #make private
        self.occupied_tiles = occupied_tiles

    def neighbors(self):
        '''Return a list of all the neighbor boards the current board can accesss'''
        neighbors = []
        dim = self.__dim
        goal_blocks = self.goal_blocks
        blocks = self.blocks
        occupied_tiles = self.occupied_tiles
        for block in blocks:
            max_dxs = [0, 0] #max_dx for head and tail
            max_dys = [0, 0] #max_dy for head and tail
            #if main block
            if blocks[block][1] == "horizontal":
                head_tile = blocks[block][0][0]
                tail_tile = blocks[block][0][-1]
                while head_tile % dim != 0: #while not first column
                    head_tile -= 1
                    if head_tile in occupied_tiles:
                        break
                    else:
                        max_dxs[0] += 1
                while tail_tile % dim != dim - 1: #while not last column
                    tail_tile += 1
                    if tail_tile in occupied_tiles:
                        break
                    else:
                        max_dxs[1] += 1

            elif blocks[block][1] == "vertical":
                head_tile = blocks[block][0][0]
                tail_tile = blocks[block][0][-1]
                while dim <= head_tile: #while not first row
                    head_tile -= dim
                    if head_tile in occupied_tiles:
                        break
                    else:
                        max_dys[0] += 1
                while tail_tile < dim**2 - dim: #while not last row
                    tail_tile += dim
                    if tail_tile in occupied_tiles:
                        break
                    else:
                        max_dys[1] += 1

            #if any movement is possible for this block            
            if max_dxs[0] != 0: 
                for i in range(max_dxs[0]): #from 0 to dim-1
                    temp = copy.deepcopy(blocks) #prevent blocks being changed as temp changes
                    temp["dim"] = dim #making accessible in Board
                    temp["goalBlocks"] = goal_blocks
                    for j in range(len(temp[block][0])):
                        temp[block][0][j] -= i+1 
                    neighbors.append(Board(temp))
            if max_dxs[1] != 0:
                for i in range(max_dxs[1]):
                    temp = copy.deepcopy(blocks) #prevent runtime error
                    temp["dim"] = dim
                    temp["goalBlocks"] = goal_blocks
                    for j in range(len(temp[block][0])):
                        temp[block][0][j] += i+1
                    neighbors.append(Board(temp))
            if max_dys[0] != 0:
                for i in range(max_dys[0]): #can be reduced to one max_dys calc
                    temp = copy.deepcopy(blocks)
                    temp["dim"] = dim
                    temp["goalBlocks"] = goal_blocks
                    for j in range(len(temp[block][0])):
                        temp[block][0][j] -= (i+1)*dim
                    neighbors.append(Board(temp))
            if max_dys[1] != 0:
                for i in range(max_dys[1]):
                    temp = copy.deepcopy(blocks)
                    temp["dim"] = dim
                    temp["goalBlocks"] = goal_blocks
                    for j in range(len(temp[block][0])):
                        temp[block][0][j] += (i+1)*dim
                    neighbors.append(Board(temp))
        return neighbors


    def get_start_blocks(self, start, dimension):
        '''
        Return a dictionary containing starting blocks as keys
        and a list containing indices and directions of the starting blocks as values, 
        as well as a list of occupied tiles indices at the start.
        '''
        dim = dimension
        blocks = {}
        occupied_tiles = []
        for i, tile in enumerate(start):
            if tile != "0":
                if tile in blocks and start[i-1] == start[i]:
                    blocks[tile][0].append(i)
                    blocks[tile][1] = "horizontal"
                    occupied_tiles.append(i)
                elif tile in blocks and start[i] == start[i-dim]:
                    blocks[tile][0].append(i)
                    blocks[tile][1] = "vertical"
                    occupied_tiles.append(i)
                elif not tile in blocks: 
                    blocks[tile] = [[i], None]
                    occupied_tiles.append(i)
                elif tile in blocks:
                    blocks[tile][0].append(i)
                    occupied_tiles.append(i)

        return (blocks, occupied_tiles)

    def get_goal_blocks(self, goal):
        '''
        Return a dictionary containing goal blocks as keys
        and a list of indices and directions of the goal blocks as values.
        '''
        goal_blocks = {}
        for i, tile in enumerate(goal):
            if tile != "0":
                if tile in goal_blocks:
                    goal_blocks[tile].append(i)
                elif not tile in goal_blocks: 
                    goal_blocks[tile] = [i]
        
        return goal_blocks

    def create_1D_board(self, blocks, dimension):
        '''Return a 1D array representation of the starting board.'''
        dim = dimension
        board = [0 for i in range((dim)**2)]
        for block in blocks:
            for i in blocks[block][0]:
                board[i] = block
        
        return board

    def heuristic(self):
        '''Compute manhattan distance using only head tiles of respective blocks.
        horizontal blocks will have dy=0 and vertical blocks will have dx=0.'''
        count = 0
        blocks = self.blocks
        goal_blocks = self.goal_blocks
        for tile in blocks:
            dx_or_dy = abs(blocks[tile][0][0] - goal_blocks[tile][0]) #only head tile needed
            count += dx_or_dy
        
        return count 

    def weighted_heuristic(self):
        count = self.heuristic()

        return count * 0.2
            

    def solved(self):
        '''Return True if the board is solved.'''
        return self.heuristic() == 0

    def dimension(self):
        '''Return the dimension of the board.'''
        return self.__dim

    def starting_blocks(self):
        '''Retrun starting blocks configuration'''
        return self.blocks


            
    #def create_2D_board():

    def __repr__(self):
        dim = self.__dim
        result = str(dim)
        for k, tile in enumerate(self.__board):
            if k % dim == 0:
                result += '\n'
            try:
                result += '{:2d} '.format(tile)
            except:
                result += '{:>2s} '.format(tile)
        return result




            

        

            



        
