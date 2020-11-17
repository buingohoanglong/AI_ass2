import copy
import time
import random


# State used in BFS and DFS. Each state is a (N x N) matrix. 
# Value of cell (i,j) is 1 if there is a queen at (i,j), 0 otherwise
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
    return [[0 for i in range(N)] for j in range(N)]



# State used in Heuristic algorithm. Each state is an array of length N. 
# Each array's cell is a row. Value of row-th cell is the column where the queen is placed. 
# Initial state: array is a random permutation of [0...N] (every distinguished pair of queens are not on the same row or column) 
# Goal state: state with cost is 0
# cost (heuristic function) is total number of attacking pairs in all positive and negative diagonals
class HState():

    def __init__(self, N):
        self.N = N

    def copy(self):
        state = HState(self.N)
        state.board = [*self.board]
        state.neg_diag = [*self.neg_diag]
        state.pos_diag = [*self.pos_diag]
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

    def print_board_to_screen(self):
        self.printCost()
        if self.cost == 0:
            print("Successful !")
        else:
            print("Failed !")
        
        if self.cost == 0:
            for i in range(self.N):
                for j in range(self.N):
                    if i == self.board[j]:
                        print("1", end=" ")
                    else:
                        print("0", end=" ")
                print("\n", end="")

    def print_board_to_file(self):
        self.printCost()
        if self.cost == 0:
            print("Successful !")
        else:
            print("Failed !")

        with open('output.txt',"w+") as out:
            for i in range(0,self.N):
                for j in range(0,self.N):
                    if i == self.board[j]:
                        out.write("1")
                    else:
                        out.write("0")
                out.write("\n")

    # Check if the queen on row r is attacked
    def is_attacked(self, r):
        return self.neg_diag[r + self.board[r]] > 1 or self.pos_diag[self.N - 1 - r + self.board[r]] > 1

    # Calculate cost in the two diagonals contaning cell (row,col) when we remove a queen on that cell 
    def remove_and_calculate_cost(self, r, c):
        cost = 0
        self.neg_diag[r + c] -= 1
        self.pos_diag[self.N - 1 - r + c] -= 1
        if self.neg_diag[r + c] >= 1:
            cost -= 1
        if self.pos_diag[self.N - 1 - r + c] >= 1:
            cost -= 1
        return cost

    #Calculate cost in the two diagonals containing cell (row,col) when we remove a queen on that cell 
    def add_and_calculate_cost(self, r, c):
        cost = 0
        self.neg_diag[r + c] += 1
        self.pos_diag[self.N - 1 - r + c] += 1
        if self.neg_diag[r + c] > 1:
            cost += 1
        if self.pos_diag[self.N - 1 - r + c] > 1:
            cost += 1
        return cost

    # Swap columns of two queens on row i-th, j-th if we gain better cost
    def perform_swap(self, i, j): 
        c_i, c_j = self.board[i], self.board[j]

        cost = 0
        cost += self.remove_and_calculate_cost(i, c_i)# Remove a Queens in (i , c_i) cell and calculate cost
        cost += self.remove_and_calculate_cost(j, c_j)# Remove a Queens in (j , c_j) cell and calculate cost

        cost += self.add_and_calculate_cost(i, c_j)# Add a Queens in (i , c_j) cell and calculate cost
        cost += self.add_and_calculate_cost(j, c_i)# Add a Queens in (J , c_I) cell and calculate cost
        
        if cost < 0:    # cost < 0 mean we will get a better cost after swapping
            self.board[i], self.board[j] = self.board[j], self.board[i] # perform swap two queens' columns
            self.cost += cost # Update cost
        else: # Because we change the board's state to calculate cost, but it not better, now we roll back it to the previous state
            cost += self.remove_and_calculate_cost(i, c_j)
            cost += self.remove_and_calculate_cost(j, c_i)

            cost += self.add_and_calculate_cost(i, c_i)
            cost += self.add_and_calculate_cost(j, c_j)
            assert cost == 0

class Heuristic:
    def __init__(self, N):
        self.N = N

    def search(self):
        currentState = HState(self.N)
        currentState.random_init()
        while True:
            currentState.printCost()
            
            nextState = currentState.copy()
            for i in range(self.N):
                for j in range(i+1, self.N):
                    if nextState.is_attacked(i) or nextState.is_attacked(j):
                        nextState.perform_swap(i, j)
                        if nextState.cost == 0:
                            return nextState
                                         
            if nextState.cost < currentState.cost:
                currentState = nextState
            else:
                currentState = HState(self.N)
                currentState.random_init()



def main():
    N = int(input("Input N: "))
    algorithm = input("Input algorithm (DFS, BFS or Heuristic):  ")
    
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
        heuristic = Heuristic(N)
        start = time.time()
        result = heuristic.search()
        result.printCost()
        end = time.time()
        print("Time elapsed: " + str(end - start))

        ##########   WARNING     #########.
        # To print board to output file or to screen, uncomment below lines.
        # If you want to run a LARGE number of queens ( N > 100 ), PLEASE COMMENT print board functions below (both to file and to screen). 
        # Because it takes VERY LONG TIME to print this large board
        ##################################
        is_print = input("Print this board to output file(f) or screen(s)? (f/s):   ")
        if is_print == "f":
            result.print_board_to_file()
        else:
            result.print_board_to_screen()      

    

if __name__ == "__main__":
    main()


#Explain about Heuristic algorithm of my team:
# 1. Initially, we have a board NxN (every pairs are on different row and column).
# Example: We have a 4x4 board, like that:
#   0 0 1 0
#   0 1 0 0  
#   0 0 0 1
#   1 0 0 0
# 2. We repeatedly try to swap attacked queen with other queens to gain better cost until goal is reached (cost == 0):
# 2.1. Find a pair of queens on row i-th and j-th (with at leat one queen is being attacked).
# 2.2. Swap two queens
# 2.3. If we gain better cost -> update current best cost, otherwise swap two queen back
# 2.4. Go back to step 2.1

# Example:
#   0 1 0 0      0 0 0 1    1 0 0 0     0 0 1 0     0 0 1 0
#   0 0 1 0  ->  0 1 0 0 -> 0 1 0 0  -> 0 0 0 1  -> 1 0 0 0
#   0 0 0 1      0 0 1 0    0 0 0 1     0 1 0 0     0 0 0 1
#   1 0 0 0      1 0 0 0    0 0 1 0     1 0 0 0     0 1 0 0
# OK, we get the zero cost and we stop 

#Some benchmark of Heuristic algorithm on my laptop:
# 4         ---> 0.0002548694610595703
# 8         ---> 0.0004458427429199219
# 64        ---> 0.04718804359436035
# 1000      ---> 0.9645581245422363
# 10000     ---> 58.04304218292236
# 100000    ---> 115.90305185317993