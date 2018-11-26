#!/usr/bin/env python3
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.
# Aravind Parappil
# Indiana University Bloomington

import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row]  ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board])

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board])

# Returns column index of leftmost empty column on board
def find_leftmost_empty_col(board):
    for c in range(0,N):
        if(count_on_col(board,c)==0 and not None):
            return c

# Checks if list contains numbers greater than 0
def are_elements_gt_zero(list_to_check):
    flag = 1
    for element in list_to_check:
        if(element <= 0):
            flag = 0
            break
    if(flag):
        return True
    else:
        return False
        

# For CURRENT board state, gets the x & y coords of each queen
# and stores them in separate arrays. These are checked to
# see if any queens can diagonally attack another queen
def is_diagonal_attack_possible(board):
    x_array = []
    y_array = []
    for r in range(0,N):
        for c in range(0,N):
            if (board[r][c]==1):
                x_array.append(r)
                y_array.append(c)
    if(len(x_array) > 1):
        for i in range(0,len(x_array)):
            for j in range(0, len(x_array)):
                if(i!=j):
                    
                    # Below logic (line 62) for checking diagonal queen attacks
                    # referred from
                    # https://stackoverflow.com/questions/3209165/need-help-with-n-queens-program-checking-diagonals
                    
                    if(abs(y_array[i] - y_array[j]) == abs(x_array[i] - x_array[j])):
                        return True
    return False
    
# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "R" if col==1 and puzzle_type=='nrook' else "Q" if col==1 else "X" if col=='X'  else "_" for col in row]) for row in board ])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):   
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]


# Successors prevented when totally N pieces have already been placed
# and also when there's already a piece at the location currently being checked
# Note: Requires empty list to be returned to avoid 'NoneType' error
#       for whenever count_pieces(board) is N-1
def successors2(board):
    if count_pieces(board) < N :
        return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) if board[r][c]!=1]
    else:
        return []

# Successors prevented when totally N pieces have already been placed
# and also when there's already a piece at the location currently being checked
# Also, only adds piece to the leftmost column which is currently empty
# Note: Requires empty list to be returned to avoid 'NoneType' error
#       for whenever count_pieces(board) is N-1

def successors3(board):

    # Get the index of leftmost column having no piece at all
    empty_col_index = find_leftmost_empty_col(board)

    # Allow move only if total pieces currently on board is < N
    if(count_pieces(board) < N):

        # Avoids adding a piece if there's already a '1' at that
        # location (i.e., a move adding no piece at all)
        # Also avoids adding a piece to an unavailable position
        
        new_successors = [ add_piece(board, r, empty_col_index) for r in range(0,N)\
                           if board[r][empty_col_index] != 1 and (r,empty_col_index) not in tuples_cancelled                           
                           ]
        
        # This list is for nrook scenarios
        trimmed_list = [] 

        # Taking only states which have 1 element per row and column
        # and where total number of pieces is not zero
        for i in new_successors:
            if count_pieces(i) and \
               all([ count_on_row(i, r) <= 1 for r in range(0, N) ] ) and \
               all([ count_on_col(i, c) <= 1 for c in range(0, N) ] ):
             
                trimmed_list.append(i)
                
        if(puzzle_type == 'nrook'):
            return trimmed_list
        
        else:
            
            # This list is for nqueen scenarios
            diagonal_trimmed =[] 

            # Keeps only those states that do not have
            # a diagonal queen attack and returns the list
            # Note: Checking the same here instead of in is_goal() 
            #       as it takes up too much time because of the
            #       for loop in solve()
            
            for i in trimmed_list:
                if not is_diagonal_attack_possible(i):
                    diagonal_trimmed.append(i)
           
            return diagonal_trimmed
    else:
        return []
   
# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] ) 
        
# Solve n-rooks & nqueens!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):           
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

try:
    
    # Getting the cmd-line args
    puzzle_type = sys.argv[1]
    N = int(sys.argv[2])
    num_cancelled = int(sys.argv[3])
except Exception as e:
    print("Oh dang! Your cmd line args messed up :(", e)
    
cancelled_coords = []
tuples_cancelled =[]

try:
    # Add cmd-line args for unavailable positions to a list, if any
    if(num_cancelled):
        for coord in range(4, len(sys.argv)):
            cancelled_coords.append(int(sys.argv[coord]))

        # Segregating coords into x & y and then forming a list of tuples (x, y)
        # Must decrement each arg by 1 to conform to list indices
        
        if(are_elements_gt_zero(cancelled_coords)):
            x_cancelled = [cancelled_coords[i]-1 for i in range(0,len(cancelled_coords)) if i%2 == 0]
            y_cancelled = [cancelled_coords[i]-1 for i in range(0,len(cancelled_coords)) if i%2 != 0]
            tuples_cancelled = list(zip(x_cancelled,y_cancelled))
        else:
            print("Oops!! Board indices start at 1! Change your arguments :) ")
            exit(0)
        
    # The board is stored as a list-of-lists. Each inner list is a row of the board.
    # A zero in a given square indicates no piece, and a 1 indicates a piece.
    initial_board = [[0]*N]*N
    
    print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
    solution = solve(initial_board)

    # Assigning a marker to unavailable positions
    # in the board, so that it can be checked at printable_board()
    # NB: Done only if a solution exists
    
    if(solution):
        for i in range(0, num_cancelled):
            solution[x_cancelled[i]][y_cancelled[i]] = 'X'
        
    print (printable_board(solution) if solution else "Sorry, no solution found. :(")

except Exception as e:
    print("Oops! Exception Caught!",e)
