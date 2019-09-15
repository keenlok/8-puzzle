import os
import sys
import copy
import 

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # You may add more attributes as necessary
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.solvable = True

    def solve(self):
        #TODO: Write your code here
        if not self.checkSolvability(self.init_state):
            self.solvable = False
            return ["UNSOLVABLE"]
        
        # initialise frontier list
        frontier = []
        # initialise explored list
        explored = []
        # add init state
        # each node consists of the states and the actions it has taken
        init_node = (self.init_state, [])
        frontier.append(init_node)
        # while frontier not empty
        count = 10
        while frontier:
            # pop frontier list
            curr_node = frontier.pop(0)
            
            # add node to explored set
            print(curr_node)
            explored.append(curr_node[0])
            
            # check if goal node
            if self.checkGoalNode(curr_node[0], self.goal_state):
                return curr_node[1] # return the actions taken to get to this state
            
            # generate children
            children = self.generateSuccessors(curr_node[0], curr_node[1])
            # for each child
            for child in children:
                # check if each child is in explored set or in frontier
                if child in frontier:
                    continue
                if child[0] in explored:
                    continue
                # add child to frontier if not explored
                frontier.append(child)
            
            #count -= 1
            #if count <= 0:
            #    break
        
        # return: a list of actions like: ["UP", "DOWN"]
        pass

    # To check the solvability of a state
    def checkSolvability(self, state):
        inversion_count = 0
        for i in range(1, 10):
            for j in range(i+1, 10):
                if (state[(j-1)//3][(j-1)%3] > state[(i-1)//3][(i-1)%3]):
                    inversion_count += 1
        if inversion_count % 2 == 1:
            return False
        else:
            return True

    def checkNumEmptyTiles(self, state):
        empty_count = 0
        for i in range(1, 10):
            if state[(i-1)//3][(i-1)%3] == 0:
                    empty_count += 1
        if empty_count == 1:
            return True
        if empty_count > 1:
            return False
        return False

    # check goal node
    def checkGoalNode(self, state, goal):
        if state == goal:
            return True
        else:
            return False

    # Generate successors for a particular state
    def generateSuccessors(self, state, actions_taken):
        blank_tile = (0, 0)
        #print ((9-1) // 3), ((9-1) % 3)
        for i in range(1, 10):
            #print "curr iteration: ", i
            x = (i-1) // 3
            y = (i-1) % 3
            #print "What is x and y: ", x, y
            if state[x][y] == 0:
                blank_tile = (x,y)
                break
                
        children = []
        old_x = blank_tile[0]
        old_y = blank_tile[1]
        print "Location of Blank (", old_x, ", ", old_y, ")"
        
        print actions_taken
        # move LEFT --> move blank right --> increase blank y
        if (old_y + 1) < 3:
            tile_to_move = state[old_x][old_y+1]
            print "Tile to move", tile_to_move, old_x, old_y+1
            print "Old state: ", state
            new_state = copy.deepcopy(state)
            new_state[old_x][old_y] = tile_to_move
            new_state[old_x][old_y+1] = 0
            new_actions = list(actions_taken)
            new_actions.append("LEFT")
            print "Actions Taken: ", new_actions
            print "New state: ", new_state
            print
            if not self.checkNumEmptyTiles(state):
                raise ValueError("Wrong Number of empty tiles")
            children.append((new_state, new_actions))
            
        # move RIGHT, move blank left, decrease blank y
        if (old_y - 1) >= 0:
            tile_to_move = state[old_x][old_y-1]
            print "Tile to move", tile_to_move, old_x, old_y-1
            print "Old state: ", state
            new_state = copy.deepcopy(state)
            new_state[old_x][old_y] = tile_to_move
            new_state[old_x][old_y-1] = 0
            new_actions = list(actions_taken)
            new_actions.append("RIGHT")
            print "Actions Taken: ", new_actions
            print "New State: ", new_state
            print
            if not self.checkNumEmptyTiles(state):
                raise ValueError("Wrong Number of empty tiles")
            children.append((new_state, new_actions))
            
        # move UP, move blank right, increase blank x
        if (old_x + 1) < 3:
            tile_to_move = state[old_x+1][old_y]
            print "Tile to move", tile_to_move, old_x+1, old_y
            print "Old State: ", state
            new_state = copy.deepcopy(state)
            new_state[old_x][old_y] = tile_to_move
            new_state[old_x+1][old_y] = 0
            new_actions = list(actions_taken)
            new_actions.append("UP")
            print "Actions Taken: ", new_actions
            print "New State: ", new_state
            print
            if not self.checkNumEmptyTiles(state):
                raise ValueError("Wrong Number of empty tiles")
            children.append((new_state, new_actions))
            
        # move DOWN, move blank left, decrease blank x
        if (old_x - 1) >= 0:
            tile_to_move = state[old_x-1][old_y]
            print "Tile to move", tile_to_move, old_x-1, old_y
            print "Old State: ", state
            new_state = copy.deepcopy(state)
            new_state[old_x][old_y] = tile_to_move
            new_state[old_x-1][old_y] = 0
            new_actions = list(actions_taken)
            new_actions.append("DOWN")
            print new_actions
            print "New State: ", new_state
            print
            if not self.checkNumEmptyTiles(state):
                raise ValueError("Wrong Number of empty tiles")
            children.append((new_state, new_actions))
        return children


    # You may add more (helper) methods if necessary.
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # do NOT modify below
    if len(sys.argv) != 3:
        print(sys.argv)
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







