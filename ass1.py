import copy
import numpy as np
import time
import random


# State used in BFS and DFS. Each state is a (N x N) matrix. Value of cell (i,j) is 1 if there is a queen at (i,j), 0 otherwise
# Initial state: every cell is 0 ([[0...0],....[0...0]])
# Goal state: N queens are placed on board without being attacked
class State:
    def __init__(self, board):
        self.board = board
        self.queen_count = 0
        self.N = len(board)

    # check whether all queens are placed correctly on board
    def is_goal(self):
        return self.queen_count == self.N


    # check the queen is non-attacked when placed at (row, col) cell 
    def is_safe(self , row , col):
        N = self.N
        # check row-attack and column-attack
        for i in range(0,N):
            if (self.board[row][i] == 1 or self.board[i][col] == 1):
                return False
        # check diagonal-attack
        for i in range(0,N):
            for j in range(0,N):
                if( (i+j) == row + col or (i-j) == row - col):
                    if self.board[i][j] == 1:
                        return False
        return True


class BFS:
    def __init__(self , N):     
        self.N = N
        self.initialState = State(board = create_board(self.N))

    def algorithm(self):
        queue = []
        queue.append(self.initialState)

        while True:
            if len(queue) == 0:
                return None
            state_explored = queue.pop(0)
            for col in range(0,self.N):
                for row in range(0,self.N):
                    # if cell (row, col) is safe, place the queen on it
                    if state_explored.is_safe(row, col):
                        child = copy.deepcopy(state_explored)    # create new child
                        child.board[row][col] = 1 # place the new queen on the child
                        child.queen_count += 1

                        # if goal is reached, print board on screen
                        if child.is_goal():
                            return child
                        else:   # put child on queue for later process
                            queue.append(child)
                            break

class DFS:
    def __init__(self , N):
        self.N = N
        self.initalState = State(board = create_board(self.N))

    def algorithm(self):
        stack = []
        stack.insert(0, self.initalState)

        while True:
            if len(stack) == 0:
                return None
            state_explored = stack.pop(0)
            for col in range(0,self.N):
                for row in range(0,self.N):
                    # if cell (row, col) is safe, place the queen on it
                    if state_explored.is_safe(row, col):
                        child = copy.deepcopy(state_explored)    # create new child
                        child.board[row][col] = 1 # place the new queen on the child
                        child.queen_count += 1

                        # if goal is reached, print board on screen
                        if child.is_goal():
                            return child
                        else:   # put child on queue for later process
                            stack.insert(0, child)
                            break


def solution(board, N):
    for i in range(0,N):
        for j in range(0,N):
            print(str(board[i][j]),end=" ")
        print()

def create_board(N):
    return np.zeros((N, N), dtype=np.int64)


class HC:
    def __init__(self, N):
        self.N = N
        self.initialState = HCState([0] * N)

    # Random restart hill climbing
    def random_start(self):
        initialState = self.initialState
        while True:
            result = self.start(initialState=initialState)
            if result.cost == 0:
                return result
            else:
                board = [random.randint(0, self.N - 1) for i in range(0,self.N)]
                initialState = HCState(board)

    # Steepest-Ascent Hill Climbing
    def start(self, initialState = None):
        currentState = self.initialState if (not initialState) else initialState
        # loop until goal is reach or no better choice is found
        while True:
            if currentState.cost == 0:
                return currentState

            nextState = currentState   # nextState is best choice
            for i in range(0, self.N):
                for j in range(0, self.N):
                    if currentState.board[i] != j:
                        board = currentState.board.copy()
                        board[i] = j
                        neigbour = HCState(board)   # create new state
                        # update best choice
                        if nextState.cost > neigbour.cost:
                            nextState = neigbour

            # climb up
            if nextState.cost < currentState.cost:
                nextState.print()
                currentState = nextState
            else:   # return local maximum
                return currentState

# State used in Hill Climbing. Each state is an array of length N. 
# Each array's cell is a row. Value of row-th cell is the column where the queen is placed. 
# Initial state: every cell is 0 (N queens are placed on first row)
# Goal state: state with cost is 0
# cost (heuristic function) is number of attacking pairs
class HCState:
    def __init__(self, board):
        self.board = board  # board[x] = y if the queen on row x is on column y
        self.N = len(self.board)
        self.cost = self.computeCost()

    # heuristic function
    def computeCost(self):
        cost = 0
        for i in range(0, self.N):
            for j in range(i+1, self.N):
                if self.isThreatened(i, self.board[i], j, self.board[j]):
                    cost += 1
        return cost

    # check row-attack, column-attack, diagonal-attack
    @staticmethod
    def isThreatened(r1, c1, r2, c2):
        return r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2)

    def print(self):
        print("Board: [", end=" ")
        for i in self.board:
            print(i, end=" ")
        print("] , Cost: " + str(self.cost))


def main():
    N = int(input("Input N: "))
    algorithm = input("Input algorithm: ")

    if algorithm == "DFS":
        dfs = DFS(N)
        start = time.time()
        result = dfs.algorithm()
        end = time.time()
        if result:
            solution(result.board, N)
        print("Time elapsed: " + str(end - start))
    elif algorithm == "BFS":
        bfs = BFS(N)
        start = time.time()
        result = bfs.algorithm()
        end = time.time()
        if result:
            solution(result.board, N)
        print("Time elapsed: " + str(end - start))
    else:
        hc = HC(N)
        start = time.time()
        result = hc.random_start()
        end = time.time()
        print("Time elapsed: " + str(end - start))
    

if __name__ == "__main__":
    main()