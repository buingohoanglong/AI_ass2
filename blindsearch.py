import time

class State:
    def __init__(self, board):
        self.board = board
        self.dimension = len(board)

    def is_goal(self):
        for i in range(0, self.dimension):
            for j in range(i+1, self.dimension):
                if self.isThreatened(i, self.board[i], j, self.board[j]):
                    return False
        return True

    @staticmethod
    def isThreatened(r1, c1, r2, c2):
        return r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2)

    def print(self):
        print("Board: [", end=" ")
        for i in self.board:
            print(i, end=" ")
        print("]")


class BFS:
    def __init__(self, dimension):
        self.dimension = dimension

    def start(self):
        queue = []
        current_state = State([0] * self.dimension)
        queue.append(current_state)

        while True:
            if len(queue) == 0:
                return False
                exit()

            state_explored = queue.pop(0)
            for i in range(0, self.dimension):
                for j in range(0, self.dimension):
                    if state_explored.board[i] != j:
                        board = state_explored.board.copy()
                        board[i] = j
                        new_state = State(board)
                        new_state.print()
                        if new_state.is_goal():
                            return new_state
                        queue.append(new_state)

class DFS:
    def __init__(self, dimension):
        self.dimension = dimension

    def start(self):
        stack = []
        current_state = State([0] * self.dimension)
        stack.insert(0, current_state)

        while True:
            if len(stack) == 0:
                return False
                exit()

            state_explored = stack[0]
            del stack[0]
            for i in range(0, self.dimension):
                for j in range(0, self.dimension):
                    if state_explored.board[i] != j:
                        board = state_explored.board.copy()
                        board[i] = j
                        new_state = State(board)
                        if new_state.is_goal():
                            return new_state
                        stack.insert(0, new_state)

        
solver = BFS(4)
start = time.time()
goal = solver.start()
end = time.time()
goal.print()
print(end - start)
