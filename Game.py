import numpy as np
import copy
from termcolor import colored

#board dimensions
boardHeight = 6
boardWidth = 7

connect = 4     #winning line lenth

maxMoves = 6    #moves into the futures the ai should look

board = np.zeros((boardHeight,boardWidth))
lastPlacedRow = 0
lastPlacedCol = 0

def setupBoard():
    global board
    board = np.zeros((boardHeight,boardWidth))

def printBoard():
    for row in  board:
        for cell in row:
            if cell == 1:
                print (colored("#","red"),end='')
            elif cell == 2:
                print(colored("#","yellow"), end='')
            else:
                print(" ", end='')
            print("|", end='')
        print("")

    for x in range(boardWidth):
        print("--", end='')
    print("")
    for x in range(boardWidth):
        print (str(x)+"|",end='')
    print("")
    print("")


def checkRight(deapth, col, row, player,board):
    try:
        cell = board[row][col+1]
    except:
        return deapth

    if cell != player:
        return deapth
    deapth = deapth+1
    return checkRight(deapth,col+1,row,player,board)


def checkLeft(deapth, col, row, player,board):
    if col <= 0:
         return deapth
    try:
        cell = board[row][col-1]
    except:
        return deapth

    if cell != player:
        return deapth
    deapth = deapth+1
    return checkLeft(deapth,col-1,row,player,board)


def checkDown(deapth, col, row, player,board):
    try:
        cell = board[row+1][col]
    except:
        return deapth

    if cell != player:
        return deapth
    deapth = deapth+1
    return checkDown(deapth,col,row+1,player,board)

def checkUp(deapth, col, row, player,board):
    if row <= 0:
         return deapth

    try:
        cell = board[row-1][col]
    except:
        return deapth

    if cell != player:
        return deapth
    deapth = deapth+1
    return checkUp(deapth,col,row-1,player,board)


def checkDownRight(deapth, col, row, player,board):
    try:
        cell = board[row+1][col+1]
    except:
        return deapth

    if cell != player:
        return deapth
    deapth = deapth+1
    return checkDownRight(deapth,col+1,row+1,player,board)


def checkUpRight(deapth, col, row, player,board):
    if row <= 0:
         return deapth

    try:
        cell = board[row-1][col+1]
    except:
        return deapth

    if cell != player:
        return deapth
    deapth = deapth+1
    return checkUpRight(deapth,col+1,row-1,player,board)


def checkDownLeft(deapth, col, row, player,board):
    if col <= 0:
        return deapth
    try:
        cell = board[row+1][col-1]
    except:
        return deapth

    if cell != player:
        return deapth

    deapth = deapth+1
    return checkDownLeft(deapth,col-1,row+1,player,board)


def checkUpLeft(deapth, col, row, player,board):
    if col <= 0 or row <= 0:
         return deapth
    try:
        cell = board[row-1][col-1]
    except:
        return deapth

    if cell != player:
        return deapth
    deapth = deapth+1
    return checkUpLeft(deapth,col-1,row-1,player,board)


def checkWinner(row, col,player,board):
    return checkDown(0,col,row,player,board)+checkUp(0,col,row,player,board)+1 >= connect or\
           checkLeft(0, col, row, player,board) + checkRight(0, col, row, player,board)+1 >= connect or\
           checkDownLeft(0, col, row, player,board) + checkUpRight(0, col, row, player,board)+1 >= connect or\
           checkDownRight(0, col, row, player,board) + checkUpLeft(0, col, row, player,board)+1 >=connect


def placePlayer(col, player):
    global board
    global lastPlacedRow
    global lastPlacedCol
    if col < 0 or col > boardWidth or board[0][col] != 0:
        return False
    for row in range(len(board)):
        if board[row][col] != 0:
            board[row-1][col] = player
            lastPlacedRow = row-1
            lastPlacedCol = col
            break
        if row == len(board)-1:
            board[row][col] = player
            lastPlacedRow = row
            lastPlacedCol = col
            break
    return True

def placePlayerOnSubBoard(col, player,board):
    global lastPlacedRow
    global lastPlacedCol
    if col < 0 or col > boardWidth or board[0][col] != 0:
        return False
    for row in range(len(board)):
        if board[row][col] != 0:
            board[row-1][col] = player
            lastPlacedRow = row-1
            lastPlacedCol = col
            break
        if row == len(board)-1:
            board[row][col] = player
            lastPlacedRow = row
            lastPlacedCol = col
            break
    return True


def calulateComputer():
    moves = []
    values = 0
    score = -1000
    for col in range(boardWidth):
        values = values+1
        boardCopy = copy.deepcopy(board)
        if placePlayerOnSubBoard(col, 2, boardCopy):
            if checkWinner(lastPlacedRow, lastPlacedCol, 2, boardCopy):
                score = maxMoves
            else:
                score = getNextMove(boardCopy,1,1)
        moves.append(score)

    if values == 0:
        return -1
    return moves.index(max(moves))


def getNextMove(board,player,depth):
    if depth >= maxMoves:
        return 0
    moves = 0.00
    values = 0
    for col in range(boardWidth):
        boardCopy = copy.deepcopy(board)
        if placePlayerOnSubBoard(col,player,boardCopy):
            values = values+1

            if checkWinner(lastPlacedRow, lastPlacedCol,player,boardCopy):
                if player == 2:

                    moves = moves+(maxMoves/(depth))
                else:
                    moves= moves-(maxMoves/(depth))
            else:
                newPlayer = 2
                if player == 2:
                    newPlayer = 1

                moves = moves + getNextMove(boardCopy,newPlayer,depth+1)

    if values == 0:
        return 0
    return (moves/values)


def checkDraw(board):
    topRowsFilled = 0
    for cell in range(len(board[0])):
        if board[0][cell] != 0:
            topRowsFilled = topRowsFilled+1

    return topRowsFilled == boardWidth


def game():
    printBoard()
    while not placePlayer(int(input("Chose a colum: ")),1):
        print("Invalid Input")
    
    if checkWinner(lastPlacedRow, lastPlacedCol,1,board):
        print("One wins")
        return

    if(checkDraw(board)):
        print("Game Over")
        return

    printBoard()

    if(not placePlayer(calulateComputer(),2)):
        print("Game Over")
        return

    if checkWinner(lastPlacedRow, lastPlacedCol,2,board):
        printBoard()
        print("Two wins")
        return
    game()

setupBoard()
game()
