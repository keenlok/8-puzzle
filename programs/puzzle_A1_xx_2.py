import os
import sys


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # You may add more attributes as necessary
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.solvable = True

    def solve(self):
        #TODO: Write your code here
        if !checkSolvability(self.init_state):
            self.solvable = False
            return ["UNSOLVABLE"]
        
        
        
        # return: a list of actions like: ["UP", "DOWN"]
        pass

    # To check the solvability of a state
    def checkSolvability(state):
        inversion_count = 0
        for i in range(1, 9):
            for j in range(i+1, 9):
                if (state[(j-1)//3][(j-1)%3] > state[(i-1)//3][(i-1)%3]):
                    inversion_count++
        if inversion_count % 2 == 1:
            return False
        else:
            return True

    # Generate successors for a particular state
    def generateSuccessors(state, actions_taken):
        blank_tile = (0, 0)
        for i in range(1, 9):
            x = (i-1) // 3
            y = (i-1) % 3
            if state[x][y] == 0:
                blank_tile = (x,y)
                break
                
        children = []
        old_x = blank_tile[0]
        old_y = blank_tile[1]
        # move up --> move blank down --> increase blank y
        if (old_y + 1 < 3:
            tile_to_move = state[old_x][old_y+1]
            new_state = list(state)
            new_state[old_x][old_y] = tile_to_move
            new_state[old_x][old_y+1] = 0
            children += [(new_state, actions_taken + "UP")]
            
        # move down, move blank up, decrease blank y
        if (old_y - 1 >= 0:
            tile_to_move = state[old_x][old_y-1]
            new_state = list(state)
            new_state[old_x][old_y] = tile_to_move
            new_state[old_x][old_y-1] = 0
            children += [(new_state, actions_taken + "DOWN")]

        # move left, move blank right, increase blank x
        if (old_x + 1 < 3:
            tile_to_move = state[old_x+1][old_y]
            new_state = list(state)
            new_state[old_x][old_y] = tile_to_move
            new_state[old_x+1][old_y] = 0
            children += [(new_state, actions_taken + "LEFT")]
           
        # move right, move blank left, decrease blank x
        if (old_x - 1 >= 0:
            tile_to_move = state[old_x-1][old_y]
            new_state = list(state)
            new_state[old_x][old_y] = tile_to_move
            new_state[old_x-1][old_y] = 0
            children += [(new_state, actions_taken + "RIGHT")]
        
        return children
            
        
            






    # You may add more (helper) methods if necessary.
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # do NOT modify below
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    init_state = [[0 for i in range(3)] for j in range(3)]
    goal_state = [[0 for i in range(3)] for j in range(3)]
    lines = f.readlines()

    i,j = 0, 0
    for line in lines:
        for number in line:
            if '0'<= number <= '8':
                init_state[i][j] = int(number)
                j += 1
                if j == 3:
                    i += 1
                    j = 0

    for i in range(1, 9):
        goal_state[(i-1)//3][(i-1)%3] = i
    goal_state[2][2] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







