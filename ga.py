import time
import random
import math
import decimal
import sys
import numpy as np

class GA:
    def __init__(self, dimension, n):
        self.dimension = dimension
        self.n = n
        self.goal_cost = (self.dimension * (self.dimension - 1)) // 2

    def random_init_population(self):
        population = []
        for i in range(self.n):
            state = State(self.dimension)
            state.random_init_state()
            population.append(state)
        return population

    def calculate_chance(self, population):
        costs = [state.computeCost() for state in population]
        total_cost = sum(costs)
        for i in range(len(population)):
            population[i].chance = costs[i] / total_cost
            
    def random_select(self, population):
        p = np.random.random_sample()
        # print(p)
        index = 0
        prob = 0
        for state in population:
            prob += state.chance
            if p < prob:
                break
            index += 1
        return population[index]

    def reproduce(self,x,y):
        c = np.random.randint(0, self.dimension - 1)
        child = State(self.dimension)
        child.board = x.board[0:c] + y.board[c:self.dimension]
        return child

    def mutate(self, state):
        position = np.random.randint(0, self.dimension - 1)
        value = np.random.randint(1, self.dimension - 1)
        state.board[position] = value

    def best_state(self, population):
        chances = [state.chance for state in population]
        index = chances.index(max(chances))
        return population[index]
    
    def start(self, loop = 0):
        population = self.random_init_population()
        for state in population:
            if state.computeCost() == self.goal_cost:
                return state
        count = 0
        while True:
            self.calculate_chance(population)
            if loop != 0 and count == loop:
                return self.best_state(population)

            new_population = []
            for i in range(self.n):
                x = self.random_select(population)
                y = self.random_select(population)
                child = self.reproduce(x,y)
                if child.computeCost() == self.goal_cost:
                    return child
                mutate_prob = 0.99
                if np.random.random_sample() < mutate_prob:
                    self.mutate(child)
                new_population.append(child)
            population = new_population

            for state in population:
                state.print()

            count += 1


class State:
    def __init__(self, dimension):
        self.board = [0] * dimension
        self.dimension = dimension
        self.chance = 0

    def random_init_state(self):
        for i in range(self.dimension):
            self.board[i] = np.random.randint(0, self.dimension - 1)

    def computeCost(self):
        cost = 0
        for i in range(0, self.dimension):
            for j in range(i+1, self.dimension):
                if not State.isThreatened(i, self.board[i], j, self.board[j]):
                    cost += 1
        return cost

    @staticmethod
    def isThreatened(r1, c1, r2, c2):
        return r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2)

    def print(self):
        print("Board: [", end=" ")
        for i in self.board:
            print(i, end=" ")
        print("], Cost: " + str(self.computeCost()))

start = time.time()
solver = GA(dimension=4, n=10)
goal = solver.start(loop=50)
end = time.time()
goal.print()
print(start - end)
# population = solver.random_init_population()
# for state in population:
#     state.print()
# solver.reproduce(population[0], population[1]).print()