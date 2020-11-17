import time
import random
class HC:
    def __init__(self, dimension):
        self.dimension = dimension
        self.initialState = State([0] * dimension)
        self.currentState = self.initialState
        self.count = 0

    def reset(self):
        self.currentState = self.initialState
        # self.count = 0        

    def random_start(self):
        while True:
            for i in range(0,self.dimension):
                self.initialState.board[i] = random.randint(0, self.dimension - 1)
            result = self.start()
            if result.cost == 0:
                return result
            else:
                self.reset()

    def start(self):
        if self.currentState.cost == 0:
            return self.currentState

        nextState = self.currentState
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                if self.currentState.board[i] != j:
                    board = self.currentState.board.copy()
                    board[i] = j
                    neigbour = State(board)
                    if nextState.cost > neigbour.cost:
                        nextState = neigbour

        if nextState.cost < self.currentState.cost:
            self.count += 1
            nextState.print()
            self.currentState = nextState
            return self.start()
        else:
            return self.currentState

class State:
    def __init__(self, board):
        self.board = board  # board[x] = y if the queen on row x is on column y
        self.dimension = len(self.board)
        self.cost = self.computeCost()

    def computeCost(self):
        cost = 0
        for i in range(0, self.dimension):
            for j in range(i+1, self.dimension):
                if self.isThreatened(i, self.board[i], j, self.board[j]):
                    cost += 1
        return cost

    @staticmethod
    def isThreatened(r1, c1, r2, c2):
        return r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2)

    def print(self):
        print("Board: [", end=" ")
        for i in self.board:
            print(i, end=" ")
        print("] , Cost: " + str(self.cost))


solver = HC(20)
start = time.time()
goal = solver.random_start()
end = time.time()
print(solver.count)
print(end-start)