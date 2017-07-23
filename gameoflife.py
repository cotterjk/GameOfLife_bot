import random
import re
import sys
import twitter
from local_settings import *

def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api

def getBoardFromText(boardtext):
    board = [[0 for i in range(8)] for j in range(8)]
    boardtext = re.sub(r'\n','', boardtext) #take out new lines.
    boardtext = re.sub(r'\"|\(|\)', '', boardtext) #take out quotes.
    boardtext = boardtext.replace("🔵", "X")
    boardtext = boardtext.replace("⚪️", "_")
    boardtextlist = list(boardtext)
    # print(boardtextlist)
    for j in range(8):
        for i in range(8):
            if (boardtextlist[i+(j*8)] == 'X'):
                board[i][j] = 1
            elif (boardtextlist[i+(j*8)] == '_'):
                board[i][j] = 0
            else:
                board[i][j] = 5
    return board

def countNeighbors(x, y):
    count = 0
    if (board[x][(y-1)%8]==1):
        count +=1
    if (board[x][(y+1)%8]==1):
        count +=1
    if (board[(x-1)%8][y]==1):
        count +=1
    if (board[(x-1)%8][(y-1)%8]==1):
        count +=1
    if (board[(x-1)%8][(y+1)%8]==1):
        count +=1
    if (board[(x+1)%8][y]==1):
        count +=1
    if (board[(x+1)%8][(y-1)%8]==1):
        count +=1
    if (board[(x+1)%8][(y+1)%8]==1):
        count +=1
    return count

# Any live cell with fewer than two live neighbors dies, as if caused by under-population.
# Any live cell with two or three live neighbors lives on to the next generation.
# Any live cell with more than three live neighbors dies, as if by over-population.
# Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
def rules(x, y):
    if(board[x][y]==1):
        if (countNeighbors(x, y) < 2):
            return 0
        elif (1 < countNeighbors(x, y) < 4):
            return 1
        elif (countNeighbors(x, y) > 3):
            return 0
    elif(board[x][y]==0):
        if (countNeighbors(x, y) == 3):
            return 1
        else:
            return 0
    else:
        return 5


def getStringFromBoard(b):
    bs = ""
    for j in range(8):
        for i in range(8):
            if b[i][j] == 1:
                bs += '🔵'
            elif b[i][j] == 0:
                bs += '⚪️'
            else:
                bs += '🔴'
        bs += '\n'
    return bs

def getNextGenFromBoard():
    nextboard = [[0 for i in range(8)] for j in range(8)]
    for j in range(8):
        for i in range(8):
            nextboard[i][j] = rules(i, j)
    return nextboard

def generateRandomBoard():
    randboard = [[0 for i in range(8)] for j in range(8)]
    for j in range(8):
        for i in range(8):
            randboard[i][j] = random.randint(0, 1)
    return randboard

if __name__=='__main__':
    api = connect()

    boardtext = api.GetUserTimeline(screen_name='gameoflife_bot', count=1, max_id=None, include_rts=False, trim_user=True, exclude_replies=True)[0].text
    if '⚪️' not in boardtext:
        #Last board was a text message. Generate random board.
        nextboardstr = getStringFromBoard(generateRandomBoard())
        print(nextboardstr)
        status = api.PostUpdate(nextboardstr)
        sys.exit()
    board = [[0 for i in range(8)] for j in range(8)]
    board = getBoardFromText(boardtext)
    boardstr = ''
    boardstr = getStringFromBoard(board)

    nextboard = board
    nextboard = getNextGenFromBoard()
    nextboardstr = getStringFromBoard(nextboard)

    if '🔵' not in boardtext:
        nextboardstr = 'This population is extinct, so I\'ll generate a new board randomly.'
    if nextboardstr == boardstr:
        nextboardstr = 'Population is locked, so I\'ll generate a new board randomly.'

    print(nextboardstr)
    status = api.PostUpdate(nextboardstr)