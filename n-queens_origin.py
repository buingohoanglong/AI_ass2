# 1000 -> 14.88s
# 2000 -> 141.12s

import random
import time

class HState():

    def __init__(self, N):
        self.N = N

    def copy(self):
        state = HState(self.N)
        state.board = self.board.copy()
        state.neg_diag = self.neg_diag.copy()
        state.pos_diag = self.pos_diag.copy()
        state.cost = self.cost
        return state
            
    def random_init(self):
        self.board = list(range(self.N))
        random.shuffle(self.board)

        self.cost = 0

        self.neg_diag = [0] * (2*self.N - 1)
        self.pos_diag = [0] * (2*self.N - 1)

        for i in range(self.N):
            self.neg_diag[i + self.board[i]] += 1
            self.pos_diag[self.N - 1 - i + self.board[i]] += 1
        
        for i in range(2*self.N - 1):
            if self.neg_diag[i] > 1:
                self.cost += self.neg_diag[i] - 1
            if self.pos_diag[i] > 1:
                self.cost += self.pos_diag[i] - 1

    def printCost(self):
        print("Cost: " + str(self.cost))

    def printBoard(self, is_print):
        if self.cost == 0:
            print("Successful !")
        else:
            print("Failed !")
        
        if is_print and self.cost == 0:
            for i in range(self.N):
                for j in range(self.N):
                    if i == self.board[j]:
                        print("1", end=" ")
                    else:
                        print("0", end=" ")
                print("\n", end="")

    def is_attacked(self, r):
        return self.neg_diag[r + self.board[r]] > 1 or self.pos_diag[self.N - 1 - r + self.board[r]] > 1

    def remove_and_calculate_cost(self, r, c):
        cost = 0
        self.neg_diag[r + c] -= 1
        self.pos_diag[self.N - 1 - r + c] -= 1
        if self.neg_diag[r + c] >= 1:
            cost -= 1
        if self.pos_diag[self.N - 1 - r + c] >= 1:
            cost -= 1
        return cost

    def add_and_calculate_cost(self, r, c):
        cost = 0
        self.neg_diag[r + c] += 1
        self.pos_diag[self.N - 1 - r + c] += 1
        if self.neg_diag[r + c] > 1:
            cost += 1
        if self.pos_diag[self.N - 1 - r + c] > 1:
            cost += 1
        return cost

    def perform_swap(self, i, j):

        c_i, c_j = self.board[i], self.board[j]

        self.board[i], self.board[j] = self.board[j], self.board[i]

        cost = 0
        cost += self.remove_and_calculate_cost(i, c_i)
        cost += self.remove_and_calculate_cost(j, c_j)

        cost += self.add_and_calculate_cost(i, c_j)
        cost += self.add_and_calculate_cost(j, c_i)

        self.cost += cost

class Heuristic:
    def __init__(self, N):
        self.N = N

    def search(self):
        currentState = HState(self.N)
        currentState.random_init()
        while True:

            currentState.printCost()

            if currentState.cost == 0:
                return currentState
            
            nextState = currentState.copy()
            for i in range(self.N):
                for j in range(i+1, self.N):
                    if nextState.is_attacked(i) or nextState.is_attacked(j):
                        tempState = nextState.copy()
                        tempState.perform_swap(i, j)
                        if tempState.cost < nextState.cost:
                            nextState = tempState
                            
            if nextState.cost < currentState.cost:
                currentState = nextState
            else:
                return currentState

def main():
    start = time.time()
    h = Heuristic(2000)
    sol = h.search()
    sol.printBoard(False)
    print("Time elapsed: " + str(time.time() - start))

if __name__ == '__main__':
    main()