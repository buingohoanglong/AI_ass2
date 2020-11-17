import heapq
import time

class State:
    def __init__(self, board):
        self.board = board  # board[x] = y if the queen on row x is on column y
        self.N = len(self.board)
        self.h = self.heuristic()
        self.g = 0

    # heuristic function
    def heuristic(self):
        left_diag = [0] * (2*self.N - 1)
        right_diag = [0] * (2*self.N - 1)

        for i in range(self.N):
            left_diag[i + self.board[i]] += 1
            right_diag[self.N - 1 - i + self.board[i]] += 1

        result = 0
        for i in range(2*self.N - 1):
            if left_diag[i] > 1:
                result += left_diag[i] - 1
            if right_diag[i] > 1:
                result += right_diag[i] - 1

        return result

    def print(self):
        print("Board: [", end=" ")
        for i in self.board:
            print(i, end=" ")
        print("] , Cost: " + str(self.g + self.h))

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h



class AStar:
    def __init__(self, N):
        self.N = N
        self.initialState = State(list(range(0,self.N)))


    def start(self, initialState = None):
        currentState = self.initialState if (not initialState) else initialState
        prio_queue = []
        heapq.heappush(prio_queue, (currentState.g + currentState.h, currentState))
        
        while True:
            if len(prio_queue) == 0:
                return currentState

            state_explored = heapq.heappop(prio_queue)[1]
            state_explored.print()
            if state_explored.h == 0:
                return state_explored

            for i in range(0, self.N):
                for j in range(i + 1, self.N):
                    board = state_explored.board.copy()
                    board[i], board[j] = board[j], board[i]
                    neigbour = State(board)
                    if neigbour.h == 0:
                        return neigbour
                    neigbour.g = state_explored.g + 1
                    heapq.heappush(prio_queue, (neigbour.g + neigbour.h, neigbour))

N = int(input("Number of queen: "))
solver = AStar(N)
start = time.time()
result = solver.start()
end = time.time()
print("Time elapsed: " + str(end - start))