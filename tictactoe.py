"""
Tic Tac Toe Player
"""
import copy
from ctypes import util
import math
from operator import indexOf

from sqlalchemy import false

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    XCount = 0
    OCount = 0
    # Count number of X/O moves in each space
    for rowIdx, row in enumerate(board):
        for columnIdx, column in enumerate(row):
            if (board[rowIdx][columnIdx] == "X"):
                XCount += 1
            elif (board[rowIdx][columnIdx] == "O"):
                OCount += 1 
    # Get total    
    totalMoves = XCount + OCount
    # If total moves are greater than 8 then board is full
    if (totalMoves > 8):
        #print("\n No player selected \n")
        return None
    # If no moves made or both on the same number of moves
    if (totalMoves == 0 or XCount == OCount):
        #print("\n X selected \n")
        return "X"
    # If X has made more moves return O
    if (XCount > OCount):
        #print("\n O selected \n")
        return "O"
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleMoves = []
    for rowIdx, row in enumerate(board):
        for columnIdx, column in enumerate(row):
            #print("Checking: ", rowIdx , ", ", columnIdx, " = ", board[rowIdx][columnIdx])
            if (board[rowIdx][columnIdx] == EMPTY):
                #print("Added move")
                possibleMoves.append((rowIdx, columnIdx))
    #print("possible moves;", possibleMoves)    
    return possibleMoves

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardCopy = board.copy()
    row = action[0]
    column = action[1]
    #print("RESULT BOARD Before move: ", board)
    #print("Move valid? ", row, " - ", column, " = ", action, ", value on board: ", boardCopy[row][column])
    if (boardCopy[row][column] == EMPTY):
        boardCopy[row][column] = player(boardCopy)
        return boardCopy
    else:
        raise NameError(action, " is an Invalid Move")


    raise NotImplementedError

def counterCheck(value):
    if(value == "X"):
        return 1
    if(value == "O"):
        return -1
    return 0
def checkWinner(value):
    if (value == -3):
        return "O"
    if (value == 3):
        return "X"
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for rowIdx, row in enumerate(board):
        counter = 0 
        # X is +1, 0 is -1, -3 or 3 means all three values are the same 
        # check rows
        for columnIdx, column in enumerate(row):
            cell = board[rowIdx][columnIdx]
            if (cell == EMPTY):
                break
            counter += counterCheck(cell)
        # CheckWinnder will return none if no winner
        if(checkWinner(counter) != None):
            return checkWinner(counter)
    for column in range(0, 3):
        counter = 0
        for row in range(0,3):
            cell = board[row][column]
            if (cell == EMPTY):
                break
            counter += counterCheck(cell)
        if(checkWinner(counter) != None):
            return checkWinner(counter)
    counter = 0
    for x in range(0, 3):
        cell = board[x][x]
        if ( cell == EMPTY):
            break
        counter += counterCheck(cell)
    if(checkWinner(counter) != None):
        return checkWinner(counter)
    counter = 0
    for x in range(0, 3):
        cell = board[x][2-x]
        if ( cell == EMPTY):
            break
        counter += counterCheck(cell)
    if(checkWinner(counter) != None):
        return checkWinner(counter)
    
    return None
    raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If no moves left then game over
    if (len(actions(board)) ==0):
        return True
    # If a winner then game over
    if (winner(board) != None):
        return True
    # Otherwise game continues
    return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    outcome = winner(board)
    if (outcome == None):
        return 0
    if (outcome == "X"):
        return 1
    if (outcome == "O"):
        return -1
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    master = copy.deepcopy(board)
    frontier = []
    moves = actions(copy.deepcopy(master))
    for move in moves:
        b = result(copy.deepcopy(master), copy.deepcopy(move))
        frontier.append(b)

    for item in frontier:
        if (player(copy.deepcopy(item)) == "X"):
            outcome = maxMove(copy.deepcopy(item)) 
            frontier[frontier.index(item)] = outcome
        else:
            outcome = minMove(copy.deepcopy(item))
            frontier[frontier.index(item)] = outcome
    print("FRONTIER: ", frontier)
    if (player(copy.deepcopy(master)) == "X"):
        return moves[frontier.index(max(frontier))]
    else:
        return moves[frontier.index(min(frontier))]

def minMove(minBoard):
    minResults = []
    if (terminal(copy.deepcopy(minBoard)) == True):
        #print("Min terminal: ", utility(copy.deepcopy(minBoard)))
        return utility(copy.deepcopy(minBoard))
    minMoves = actions(copy.deepcopy(minBoard))
    minFrontier = []
    for minMove in minMoves:
        minFrontier.append(result(copy.deepcopy(minBoard), minMove))
    for minItem in minFrontier:
        minResults.append(maxMove(copy.deepcopy(minItem)))
        if(minResults[-1] == -1):
            return -1
    #print("Min Frontier: ", min(minResults))
    return min(minResults)
    return minFrontier[min(range(len(minFrontier)), key=minFrontier.__getitem__)]

def maxMove(maxBoard):
    maxResults = []
    if (terminal(copy.deepcopy(maxBoard)) == True):
        #print("Max terminal: ", utility(copy.deepcopy(maxBoard)))
        return utility(copy.deepcopy(maxBoard))
    maxMoves = actions(copy.deepcopy(maxBoard))
    maxFrontier = []
    for maxMove in maxMoves:
        maxFrontier.append(result(copy.deepcopy(maxBoard), maxMove))
    for maxItem in maxFrontier:
        maxResults.append(minMove(copy.deepcopy(maxItem)))
        if(maxResults[-1] == 1):
            return 1
    #print("Max Frontier: ", max(maxResults))
    return max(maxResults)
    #return maxFrontier[max(range(len(maxFrontier)), key=maxFrontier.__getitem__)]

#    boardCopy = board
#    if(terminal(boardCopy) == False):  
#        moves = actions(boardCopy) 
#        frontier = []
#        for moveIdx, move in enumerate(moves):
#            print("\n--- MAIN LOOP ---", moveIdx)
#            if (player(board) == "X"):
#                frontier.append(minimax(result(boardCopy, move)))
#            else:
#                frontier.append(minimax(result(boardCopy, move)))
#        # return the move that leads to the highest score 
#        if(player(board) == "X"):
#            return moves[max(range(len(frontier)), key=frontier.__getitem__)]
#        # return the move that leads to the lowest score (ie best of O) 
#        if(player(board) == "O"):
#            return moves[min(range(len(frontier)), key=frontier.__getitem__)]
#    return utility(boardCopy)

    raise NotImplementedError



#def maxMove(board):
#    boardCopy = board
#    print("\nMAX --- ")
#    moves = actions(boardCopy)
#    print("BOARD STATE: ", boardCopy)
#    print("COPY BOARD STATE:", board)
#    print("POSSIBLE MOVES: ", moves)
#    frontier = []
#    if (terminal(boardCopy)):
#        print("\n --- Number returned --- \n", "val: ", utility(board), ", Board: ", board, "\n")
#        return utility(boardCopy)
#    for moveIdx, move in enumerate(moves):
#        print("BOARD COPY STATE: ", boardCopy)
#        print("Checking move: ", move)
#        newBoard = result(boardCopy, move)
#        frontier.append(minMove(newBoard))
#        #if (terminal(newBoard)):
#        #    frontier.append(utility(newBoard))
#        #    print("\nTERMINAL: Frontier size: ", frontier, ", Index: ", moveIdx, ", Result: ", utility(newBoard))
#        #else:
#        #    frontier.append(minMove(newBoard))
#        #    print("\nAdding new move: Frontier size: ", frontier, ", Index: ", moveIdx, ", Result: ", utility(newBoard))
#    return max(range(len(frontier)), key=frontier.__getitem__)

#    minBoardCopy = minBoard
#    print("\nMIN --- ")
#    moves = actions(minBoardCopy)
#    print("minBOARD STATE: ", minBoard)
#    print("minBOARD COPY STATE: ", minBoardCopy)
#    print("minPOSSIBLE MOVES: ", moves)
#    frontier = []
#    if (terminal(minBoardCopy)):
#        print("\n --- minNumber returned --- \n", "val: ", utility(minBoardCopy), ", Board: ", minBoardCopy, "\n")
#        return utility(minBoardCopy)
#    for moveIdx, move in enumerate(moves):
#        print("minBOARD COPY STATE: ", minBoardCopy)
#        print("minChecking move: ", move)
#        minNewBoard = result(minBoardCopy, move)
#        frontier.append(maxMove(minNewBoard))
#        #if (terminal(newBoard)):
#        #    frontier.append(utility(newBoard))
#        #    print("\nTERMINAL: Frontier size: ", frontier, ", Index: ", moveIdx, ", Result: ", utility(newBoard))
#        #    #frontier[moveIdx] = utility(newBoard)
#        #else:
#        #    
#        #    print("\nAdding new move: Frontier size: ", frontier, ", Index: ", moveIdx, ", Result: ", utility(newBoard))
#    print("minFINISHED FOR LOOP: MIN VAL: ", min(range(len(frontier)), key=frontier.__getitem__), ", Frontier Length: ", len(frontier))
#    return min(range(len(frontier)), key=frontier.__getitem__)
            

