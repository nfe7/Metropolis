import numpy as np
import random
import time
           
# print puzzle
def printPuzzle(puzzle):
    print ()
    for i in range(0,9):
        for j in range(0,9):
            print(puzzle[i][j], end = " ")
        print()
    print()    

# Conflicts - When the candidate number contradicts the uniqnuess of the row, column, or 3x3 partition grid which it is situated
# "Energy"
def conflict(puzzle, row, column, candidate): 
    conflicts = 0
    # Checking row and column conflicts
    for i in range(0, 9):
        if (i != column):
            if (candidate == puzzle[row][i]):
                conflicts += 5 if clues[row][i] or clues[row][column] else 1
        if (i != row):
            if (candidate == puzzle[i][column]):
                conflicts += 5 if clues[i][column]or clues[row][column] else 1
            
    startRow = (row//3) *3
    startColumn = (column//3) * 3
   
    # Check conflicts in grid that we haven't checked (not in row or column)
    for i in range(startRow, startRow+3):
        for j in range(startColumn, startColumn+3):
            if (i != row and j != column):
                if (candidate == puzzle[i][j]):
                   conflicts += 5 if clues[i][j] or clues[row][column] else 1
    return conflicts

# Calculated the energy of the puzzle
# Ground state is when energy = 0 (when there are no conflicts in the puzzle = solved!)
def e(puzzle):
    energy  = 0
    for i in range(9):
        for j in range(9):
            energy += conflict(puzzle, i, j, puzzle[i][j])
    return energy/2


def metropolis(puzzle, clues):
    t = float(input("Enter the temperature (suggested 0.36 < t < 0.44): "))
    startTime = time.time()
    fill(puzzle)
           
    energy = e(puzzle)
    print("\nChosen temperature: ",t)
    print("\nInitial energy after random fill: ",energy)

    n = 0
    delta = 0

    # When we reach the ground state (energy = 0) and the puzzle is solved with no conflicts
    while energy > 0:
        accept = 0
        deltaE = 0
        proba = 0
        n+=1
               
        # Pick random cell to work on   
        U1 = random.randint(0,8)
        U2 = random.randint(0,8)

        # Not allowed to edit clue cells       
        if not clues[U1][U2]:
                   
            U = random.randint(1,9)
                   
            if U != puzzle[U1][U2]: 
                deltaE = conflict(puzzle, U1, U2, U) - conflict(puzzle, U1, U2, puzzle[U1][U2])
                proba = prob(deltaE, t)

                V = random.random()
                if (V < proba):
                    accept = 1
        
                if accept:
                    puzzle[U1][U2] = U
                    energy += deltaE
                    
        if n%5000 == 0: 
            print("Try#: ",n,"\tenergy: ",energy)
            if n == 5000000:
                return False

    endTime = time.time()
    timeElapsed = endTime - startTime
    print("\nAttempt#: ",n,"\tenergy: ",energy)
    print("Time:\t ",timeElapsed)     
    return True

# Filling the puzzle with random values to start our algorithm
def fill(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                 puzzle[i][j] = random.randint(1,9)
    return


'''
Our acceptance probability
If the change in energy is less (less conflicts), then we accept it
If change in energy is more (more conflicts), we accept with probability e^(-delta/t) so 
that we prevent the algorithm from stopping in a local minimum
'''
def prob(deltaE, t):-
    if deltaE <= 0:
        return 1
    if deltaE > 0:
        return  np.exp(-deltaE/t)
    return 0
   
#----------------------------------------------------------------------------------------
# Main

# Load puzzle and remember the clue cells
puzzle = np.loadtxt("puzzle.txt").astype(int)
clues = np.zeros(puzzle.shape).astype(int)

for i in range(9):
    for j in range(9):
        clues[i][j] = True if puzzle[i][j] != 0 else False

print("\nUnsolved Sudoku Puzzle: ")
printPuzzle(puzzle)
if metropolis(puzzle, clues):
    print("\nSolved Sudoku Puzzle: ")
    printPuzzle(puzzle)
else:
    print("Please try again or it could be unsolvable.")


