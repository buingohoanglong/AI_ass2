import time
import random

class HC:
    def __init__(self, dimension):
        self.dimension = dimension
        self.initialState = State([0] * dimension)
        self.currentState = self.initialState
        self.step = 0

    def compute_cost(self, state):
        cost = 0
        for i in range(0, self.dimension):
            for j in range(i+1, self.dimension):
                if self.is_threatened(i, state.board[i], j, state.board[j]):
                    cost += 1
        return cost

    @staticmethod
    def is_threatened(r1, c1, r2, c2):
        return r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2)
    
    def reset(self):
        self.currentState = self.initialState     

    def next_state(self, state):
        nextState = state
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                if state.board[i] != j:
                    board = state.board.copy()
                    board[i] = j
                    neigbour = State(board)
                    if self.compute_cost(nextState) > self.compute_cost(neigbour):
                        nextState = neigbour
        return nextState

    def start(self):
        current_cost = self.compute_cost(self.currentState)
        while True:
            if current_cost == 0:
                return self.currentState

            nextState = self.next_state(self.currentState)
            next_cost = self.compute_cost(nextState)
            if next_cost < current_cost:
                self.step += 1
                self.print(nextState, next_cost)
                self.currentState = nextState
                current_cost = next_cost
            else:
                return self.currentState

    def random_start(self):
        while True:
            self.initialState.random_init()
            result = self.start()
            if self.compute_cost(result) == 0:
                return result
            else:
                self.reset()

    def print(self, state, cost = None):
        if not cost:
            cost = self.compute_cost(state)
        print("Board: [", end=" ")
        for i in state.board:
            print(i, end=" ")
        print("] , Cost: " + str(cost))


class State:
    def __init__(self, board):
        self.board = board  # board[x] = y if the queen on row x is on column y
        self.dimension = len(self.board)

    def random_init(self):
        self.board = [random.randint(0, self.dimension - 1) for i in range(0,self.dimension)]


solver = HC(20)
start = time.time()
goal = solver.random_start()
print(solver.step)
print(time.time() - start)