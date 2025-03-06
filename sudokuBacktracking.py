import numpy as np
import time

puzzle = (np.loadtxt('puzzle.txt')).astype(int)

count = [0,0]

# Printing grid
def printPuzzle(puzzle):
    print ()
    for i in range(0,9):
        for j in range(0,9):
            print(puzzle[i][j], end = " ")
        print()
    print()
    
                       
# Conflicts - When the candidate number contradicts the uniqnuess of the row, column, or 3x3 partition grid which it is situated
def conflict(puzzle, row, column, candidate):
    
    # Checking row and column conflicts
    for i in range(0, 9):
        if (i != column):
            if (candidate == puzzle[row][i]):
                return True
        if (i != row):
            if (candidate == puzzle[i][column]):
                return True
            
    startRow = (row//3) *3
    startColumn = (column//3) * 3
   
    # Check conflicts in grid that we haven't checked (not in row or column)
    for i in range(startRow, startRow+3):
        for j in range(startColumn, startColumn+3):
            if (i != row or j != column):
                if (candidate == puzzle[i][j]):
                   return True
    return False;

'''
Backtracking method to solve the puzzle
Will try all the possibilities from 1 to 10 as long as there is no conflict 
Recursion will retry new values if we "backtrack" to previous cells
'''
def solve(puzzle, row, column, count):
    if (row == 9):
        return True
    if (column == 9):
        return solve(puzzle,row+1,0,count)
    
    if (puzzle[row][column] != 0):
        return solve(puzzle, row, column+1,count)
    
    for k in range(1,10):
        count[0] += 1
        if (not(conflict(puzzle, row, column, k))):
            puzzle[row][column] = k
            count[1] += 1
            if (solve(puzzle, row, column+1,count)):
                return True
            puzzle[row][column] = 0
    return False
        
# Print unsolved puzzle
printPuzzle(puzzle)

# Solving the puzzle and timing how long it takes
startTime = time.time()
solve(puzzle, 0, 0,count)
endTime = time.time()
runTime = endTime - startTime

# Printing puzzle with solution
print(f"{'Possibilities checked':<25}: {count[0]:} times")
print(f"{'Tries attempted':<25}: {count[1]} tries")
print(f"{'Time used':<25}: {runTime:.4f} seconds")
printPuzzle(puzzle)


