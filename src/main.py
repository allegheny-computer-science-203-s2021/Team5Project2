# Main file for TicTacToe
# Team5Project2 - TicTacToe
# Authors: Tommy Antle, Andre Hance, Bailey Matrascia, Alex Le Floch

# This will hold the GUI, User input, and other main features.

# Just for looks
print("Starting...")

# GUI will be built using PySimpleGUI
import PySimpleGUI as sg

from random import choice

# Setting Theme
sg.theme('BrightColors')

# piece image variables, to be assigned to buttons
xPiece = './images/xPiece.png'
oPiece = './images/oPiece.png'
emptyPiece = './images/emptyPiece.png'

# Creating the layout for the window
layout1 = [[sg.Text("Tic-Tac-Toe Main Menu")],
        [sg.Button("2 Player")],
        [sg.Button("VS Computer (easy)")],
        [sg.Button("VS Computer (hard)")]]

layout2 = [[sg.Text("Tic-Tac-Toe", key = 'title')],
        [sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '7'),
        sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '8'),
        sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '9')],
        [sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '4'),
        sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '5'),
        sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '6')],
        [sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '1'),
        sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '2'),
        sg.Button(image_filename = emptyPiece, image_size = (100, 100), key = '3')],
        [sg.Button("CLEAR"), sg.Button("Main Menu")],
        [sg.Text(text='GAME OVER',font=("Times New Roman",12), visible=False, key='0')]]

layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-')],
        [sg.Button("EXIT")]]
# Creating the window
window = sg.Window("TicTacToe", layout)

# Creating the game mode state
gameMode = "menu"

# counter variable to determine which player is taking their turn.
turnCounter = 0

#A dictionary to contain the board state for the program to assess
theBoard = {'7': ' ' , '8': ' ' , '9': ' ' ,
            '4': ' ' , '5': ' ' , '6': ' ' ,
            '1': ' ' , '2': ' ' , '3': ' ' }

# Prints current board start to terminal(Mainly for testing puporses.)
def printBoard(theBoard):
    print(theBoard['7'] + '|' + theBoard['8'] + '|' + theBoard['9'])
    print("-----")
    print(theBoard['4'] + '|' + theBoard['5'] + '|' + theBoard['6'])
    print("-----")
    print(theBoard['1'] + '|' + theBoard['2'] + '|' + theBoard['3'])
    print("\n\n")


def playerAction(event):
    """Function containing possible player actions, also calls for computer action"""
    global turnCounter
    if event in ['1','2','3','4','5','6','7','8','9']:
        if (turnCounter % 2 == 0):
            window.FindElement(event).Update(image_filename = xPiece, image_size = (100, 100), disabled = True)
            theBoard[event] = 'X'
            turnCounter += 1
            printBoard(theBoard)

        else:
            window.FindElement(event).Update(image_filename = oPiece, image_size = (100, 100), disabled = True)
            theBoard[event] = 'O'
            turnCounter = turnCounter + 1
            printBoard(theBoard)
        computerAction()

def computerAction():
    """Wrapper for both types of VS AI action"""
    if gameMode == 'VS Computer (easy)':
        randomAI()
    if gameMode == 'VS Computer (hard)':
        miniMaxAI()

# Random opponent turn AI
def randomAI():
    """The 'easy' game mode, computer selects random blank space to fill"""
    global turnCounter
    # searches theBoard for empty spaces, puts them into the 'available' list
    available = [k for (k,v) in theBoard.items() if v == ' ']
    if len(available) > 0:
        randstr = choice(available) # random choice from the list of options
        window.FindElement(randstr).Update(image_filename = oPiece, image_size = (100, 100), disabled = True)
        theBoard[randstr] = 'O'
        turnCounter += 1

# Hard opponent turn
def minimaxAI():
    """The 'hard' game mode, will utilize 'minimax()' function to determine best move"""
    bestScore = -100
    bestMove = 0

    for key in theBoard.keys():
        if (theBoard[key] == ' '):  # Checks to see if board spot is empty
            theBoard[key] = 'O'    # Inputs a possible turn
            currentScore = minimax(theBoard, False)    # To then be tested here
            theBoard[key] = ' '    # Resets board spot back to empty
            if (currentScore > bestScore):
                bestScore = currentScore  # Updates new best score
                bestMove = key     # Updates new best move

    window.FindElement(bestMove).Update(image_filename = oPiece, image_size = (100, 100), disabled = True)

# Minimax algorithm
def minimax(board, isMaximizing):
    """The minimax algorithm used with the above minimaxAI function"""
    if checkWhoWon('O'):
        return 10

    elif checkWhoWon('X'):
        return -10

    elif checkIfDraw():
        return 0

    if isMaximizing():
        bestScore = -100
        for key in theBoard.keys():
            if(theBoard[key] == ' '):
                theBoard[key] = 'O'
                currentScore = minimax(theBoard, False)
                theBoard[key] = ' '
                if (currentScore > bestScore):
                    bestScore = currentScore

        return bestScore

    else:
        bestScore = 100
        for key in theBoard.keys():
            if (theBoard[key] == ' '):
                theBoard[key] = 'X'   # Tests for the potential player move
                currentScore = minimax(theBoard, True) # Now that it is minimizing sets true,
                theBoard[key] = ' '
                if (currentScore < bestScore):
                    bestScore = currentScore


def checkWhoWon(y):
    """Checks to see if the given player, x or o has won"""
    if theBoard['7'] == theBoard['8'] == theBoard['9'] == y:
        return True
    elif theBoard['4'] == theBoard['5'] == theBoard['6'] == y:
        return True
    elif theBoard['1'] == theBoard['2'] == theBoard['3'] == y:
        return True
    elif theBoard['1'] == theBoard['4'] == theBoard['7'] == y:
        return True
    elif theBoard['2'] == theBoard['5'] == theBoard['8'] == y:
        return True
    elif theBoard['3'] == theBoard['6'] == theBoard['9'] == y:
        return True
    elif theBoard['7'] == theBoard['5'] == theBoard['3'] == y:
        return True
    elif theBoard['1'] == theBoard['5'] == theBoard['9'] == y:
        return True
    else:
        return False

def checkIfDraw():
    """A method that checks if the move results in a draw"""
    for key in theBoard.keys():
        if theBoard[key] == ' ':
            return False
    return True


# Create an event loop while the window is open
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the Exit button
    if event == "EXIT" or event == sg.WIN_CLOSED:
        break

    if gameMode == 'menu' and event in ['2 Player','VS Computer (easy)', 'VS Computer (hard)']:
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=True)
        gameMode = event

    # Buttons are clicked
    playerAction(event)

    # Check if a player has won,for every move after 5 moves (minimum to win).
    if turnCounter >= 5:
            if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ': # across the top
                window.FindElement('title').Update("Game Over")
            elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ': # across the middle
                window.FindElement('title').Update("Game Over")
            elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ': # across the bottom
                window.FindElement('title').Update("Game Over")
            elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ': # down the left side
                window.FindElement('title').Update("Game Over")
            elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ': # down the middle
                window.FindElement('title').Update("Game Over")
            elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ': # down the right side
                window.FindElement('title').Update("Game Over")
            elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ': # diagonal
                window.FindElement('title').Update("Game Over")
            elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ': # diagonal
                window.FindElement('title').Update("Game Over")
            # If neither X nor O wins and the board is full, we'll declare the result as 'tie'.
            elif turnCounter == 9:
                window.FindElement('title').Update("Tie Game!")
                window.FindElement('0').Update(visible=True)


    # "CLEAR" is clicked, the entire game is reset
    if event == "CLEAR":
        for i in range(1,10):
            s = str(i)
            window.FindElement(s).Update(image_filename = emptyPiece, image_size = (100, 100), disabled=False)
        theBoard = {'7': ' ' , '8': ' ' , '9': ' ' ,
                    '4': ' ' , '5': ' ' , '6': ' ' ,
                    '1': ' ' , '2': ' ' , '3': ' ' }
        turnCounter = 0

    if event == "Main Menu":
        window[f'-COL2-'].update(visible=False)
        window[f'-COL1-'].update(visible=True)


window.close()
