import os
import sys
import copy
from heapq import heappop, heappush

# Gets the estimated path cost of n, f(n), where f(n) = g(n) + h(n)
def getEstimatedCost(node):
  return node[0]

# Finds the 2d indices of blank tile in the form of tuple
def getIndexOfBlankTile(state):
  for i in range(0, len(state)):
    for j in range(0, len(state[i])):
      if state[i][j] == 0:
        return (i, j)
  raise ValueError("No blank tile found!")

class Puzzle(object):
  def __init__(self, init_state, goal_state):
    # You may add more attributes as necessary
    self.init_state = init_state
    self.goal_state = goal_state
    self.actions = list()
    self.solvable = True
    self.numOfNodes = 0
    self.maxFrontier = 0


  # Computes the sum of manhattan distances of all tiles
  def computeHeuristic(self, curr_state, goal_state):
    total = 0
    for i in range(0, len(curr_state)):
      for j in range(0, len(curr_state[i])):
        for goalRowIndex in range(0, len(goal_state)):
          if curr_state[i][j] in goal_state[goalRowIndex]:
            goalColIndex = goal_state[goalRowIndex].index(curr_state[i][j])
            total += (abs(i - goalRowIndex) + abs(j - goalColIndex))
    #print total
    return total

  def solve(self):
    # TODO: Write your code here
    # return: a list of actions like: ["UP", "DOWN"]
    if not self.isSolvable(self.init_state):
        self.solvable = False
        return ["UNSOLVABLE"]

    frontier = []
    explored = []
    # A node consists of state, actions, heuristics, g and f.
    init_h = self.computeHeuristic(self.init_state, self.goal_state)
    init_g = 0
    init_f = init_h + init_g
    init_node = (init_f, self.init_state, [], init_h, init_g)
    #frontier.append(init_node)
    heappush(frontier,init_node)

    # Graph Search
    numOfGenerated = 0
    numOfExplored = 0
    maxNumInFrontier = 0
    iterationNum = 0
    while frontier:
      #frontier.sort(key=getEstimatedCost)
      #curr_node = frontier.pop(0)
      curr_node = heappop(frontier)
      iterationNum += 1
      maxNumInFrontier = max(maxNumInFrontier, len(frontier))

      # add node to explored set
      #print(curr_node)
      print "Number of nodes in frontier: ", len(frontier)
      print "Number of nodes in explored: ", len(explored)
      print
      print "Current Node: "
      print "             Cost: ", curr_node[0]
      print "             State: "
      self.print_state(curr_node[1])
      print " Number of actions: ", len(curr_node[2])
      print "         Heuristic: ", (self.computeHeuristic(curr_node[1], self.goal_state))
      print
      explored.append(curr_node[1])

      # goal test
      if self.checkGoalNode(curr_node[1], self.goal_state):
        print "goal found"

        self.print_state(curr_node[1])
        print(curr_node[2])
        print "Number of nodes generated: ", numOfGenerated
        print "Number of nodes in explored", numOfExplored
        print "Number of nodes in frontier", len(frontier)
        print "Maximum number of nodes in frontier: ", maxNumInFrontier
        print "Iteration number is ", iterationNum
        return curr_node[2] # return the actions taken to get to this state

      # expands node
      children = self.generateSuccessors(curr_node)
      numOfGenerated += len(children)
      numOfExplored += 1
      # for each child
      for child in children:
        # check if each child is in explored set or in frontier
        if self.checkIfContainNode(frontier, child):
          continue
        if child[1] in explored:
          continue
        # add child to frontier if not explored
        #frontier.append(child)
        heappush(frontier, child)

      frontier_size = len(frontier)
      if frontier_size > self.maxFrontier:
        self.maxFrontier = frontier_size

      print "Max frontier: ", self.maxFrontier
      print


  # You may add more (helper) methods if necessary.
  # Note that our evaluation scripts only call the solve method.
  # Any other methods that you write should be used within the solve() method.
  def checkIfContainNode(self, list, node):
        for child in list:
            if child[1] == node[1]:
                #print child
                #print node
                if (child[0] > node[0]):
                    child = node #updates costs and actions taken
                return True
        return False
  
  def isSolvable(self, state):
    inversion_count = 0
    for i in range(0, 9):
      tile_i = state[i//3][i%3]
      if tile_i == 0:
        continue
      for j in range(i+1, 9):
        tile_j = state[j//3][j%3]
        if tile_j == 0:
          continue
        if (tile_j < tile_i):
          inversion_count += 1
    return inversion_count % 2 == 0

  def emptyTilesCount(self, state):
    empty_count = 0
    for i in range(0, 9):
      if state[i//3][i%3] == 0:
        empty_count += 1
    #print "empty_count is " + str(empty_count)
    return empty_count == 1

  def checkGoalNode(self, state, goal):
    return state == goal

  def print_state(self, state):
    for i in range(len(state)):
      print state[i]
    print

  # Generate successors for a particular state
  def generateSuccessors(self, curr_node):
    state = curr_node[1]
    actions_taken = curr_node[2]
    h = curr_node[3]
    g = curr_node[4]
    f = curr_node[0]
    blank_tile = getIndexOfBlankTile(state)
    children = []
    old_x = blank_tile[0]
    old_y = blank_tile[1]
    #print "Location of Blank (", old_x, ", ", old_y, ")"

    #print actions_taken
    # move LEFT --> move blank right --> increase blank y
    if (old_y + 1) < 3:
      tile_to_move = state[old_x][old_y+1]
      #print "Tile to move", tile_to_move, old_x, old_y+1
      #print "Old state: "
      #self.print_state(state)

      new_state = copy.deepcopy(state)
      new_state[old_x][old_y] = tile_to_move
      new_state[old_x][old_y+1] = 0
      new_actions = list(actions_taken)
      new_actions.append("LEFT")
      new_h = self.computeHeuristic(new_state, self.goal_state)
      new_g = g + 1 # only one tile is moved
      new_f = new_h + new_g
      #print "Actions Taken: ", new_actions
      #print "New state: "
      #self.print_state(new_state)

      if not self.emptyTilesCount(state):
        raise ValueError("Wrong Number of empty tiles")
      children.append((new_f, new_state, new_actions, new_h, new_g))

    # move RIGHT, move blank left, decrease blank y
    if (old_y - 1) >= 0:
      tile_to_move = state[old_x][old_y-1]
      #print "Tile to move", tile_to_move, old_x, old_y-1
      #print "Old state: "
      #self.print_state(state)

      new_state = copy.deepcopy(state)
      new_state[old_x][old_y] = tile_to_move
      new_state[old_x][old_y-1] = 0
      new_actions = list(actions_taken)
      new_actions.append("RIGHT")
      new_h = self.computeHeuristic(new_state, self.goal_state)
      new_g = g + 1 # only one tile is moved
      new_f = new_h + new_g
      #print "Actions Taken: ", new_actions
      #print "New State: "
      #self.print_state(new_state)

      if not self.emptyTilesCount(state):
        raise ValueError("Wrong Number of empty tiles")
      children.append((new_f, new_state, new_actions, new_h, new_g))

    # move UP, move blank right, increase blank x
    if (old_x + 1) < 3:
      tile_to_move = state[old_x+1][old_y]
      #print "Tile to move", tile_to_move, old_x+1, old_y
      #print "Old State: "
      #self.print_state(state)

      new_state = copy.deepcopy(state)
      new_state[old_x][old_y] = tile_to_move
      new_state[old_x+1][old_y] = 0
      new_actions = list(actions_taken)
      new_actions.append("UP")
      new_h = self.computeHeuristic(new_state, self.goal_state)
      new_g = g + 1 # only one tile is moved
      new_f = new_h + new_g
      #print "Actions Taken: ", new_actions
      #print "New State: "
      #self.print_state(new_state)

      if not self.emptyTilesCount(state):
        raise ValueError("Wrong Number of empty tiles")
      children.append((new_f, new_state, new_actions, new_h, new_g))

    # move DOWN, move blank left, decrease blank x
    if (old_x - 1) >= 0:
      tile_to_move = state[old_x-1][old_y]
      #print "Tile to move", tile_to_move, old_x-1, old_y
      #print "Old State: "
      #self.print_state(state)

      new_state = copy.deepcopy(state)
      new_state[old_x][old_y] = tile_to_move
      new_state[old_x-1][old_y] = 0
      new_actions = list(actions_taken)
      new_actions.append("DOWN")
      new_h = self.computeHeuristic(new_state, self.goal_state)
      new_g = g + 1 # only one tile is moved
      new_f = new_h + new_g
      #print new_actions
      #print "New State: "
      #self.print_state(new_state)

      if not self.emptyTilesCount(state):
        raise ValueError("Wrong Number of empty tiles")
      children.append((new_f, new_state, new_actions, new_h, new_g))
    return children

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
