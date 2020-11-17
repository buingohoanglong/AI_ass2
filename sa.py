import time
import random
import math
import decimal
import sys

class SA:
    def __init__(self, problem):
        self.problem = problem
        self.step = 0

    @staticmethod
    def exp_schedule(k=4, alpha=0.001, limit=20000):
        return lambda t: (k * math.exp(-alpha * t) if t < limit else 0)
    
    def random_start(self):
        while True:
            self.problem.random_init_state()
            result = self.start()
            if NQueenProblem.computeCost(result) == 0:
                return result
    
    def start(self):
        schedule = SA.exp_schedule()
        current_state = self.problem.initialState
        current_cost = NQueenProblem.computeCost(current_state)
        for t in range(sys.maxsize):
            if current_cost == 0:
                return current_state

            T = schedule(t)
            if T == 0:
                return current_state

            neighbour = NQueenProblem.random_next_state(current_state)
            if not neighbour:
                return current_state

            neighbour_cost = NQueenProblem.computeCost(neighbour)
            delta_E = neighbour_cost  - current_cost
            # prob = math.exp(-delta_E / T)
            prob = decimal.Decimal(decimal.Decimal(math.e) ** (decimal.Decimal(-delta_E) * decimal.Decimal(T)))
            if delta_E < 0 or random.uniform(0.0, 1.0) < prob:
                current_state = neighbour
                current_cost = neighbour_cost
                NQueenProblem.print(current_state)
                self.step += 1

class NQueenProblem:
    def __init__(self, dimension):
        self.initialState = [0] * dimension
        self.dimension = dimension

    def random_init_state(self):
        for i in range(self.dimension):
            self.initialState[i] = random.randint(0, self.dimension - 1)

    @staticmethod
    def computeCost(state):
        cost = 0
        for i in range(0, len(state)):
            for j in range(i+1, len(state)):
                if NQueenProblem.isThreatened(i, state[i], j, state[j]):
                    cost += 1
        return cost

    @staticmethod
    def isThreatened(r1, c1, r2, c2):
        return r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2)

    @staticmethod
    def print(state):
        print("Board: [", end=" ")
        for i in state:
            print(i, end=" ")
        print("], Cost: " + str(NQueenProblem.computeCost(state)))

    @staticmethod
    def neighbours(state):
        neighbours = []
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i] != j:
                    new_state = state.copy()
                    new_state[i] = j
                    neighbours.append(new_state)
        return neighbours

    @staticmethod
    def random_next_state(state):
        return random.choice(NQueenProblem.neighbours(state))


problem = NQueenProblem(20)
solver = SA(problem)
start = time.time()
goal = solver.random_start()
end = time.time()
print(solver.step)
print(end-start)