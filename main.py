import math
import os

board = [[' ' for row in range(3)] for col in range(3)] # Create an empty 3x3 board

def player_choice():
    """
    Ask the player for their choice and assign the corresponding symbols
    """
    
    global human, ai 
    first_player = 1 
    second_player = 2 

    while True: # Keep asking for a choice until a valid one is entered
        try:
            order = int(input('Do you want to play first? (1: Yes, 2: No):')) 

            if order in [first_player, second_player]:
                human = 'X' if order == first_player else 'O'
                ai = 'X' if order == second_player else 'O'
                break          

        except ValueError:
            print('Invalid input! Try again!')


def draw_board(board):
    """
    Prints the Tic-Tac-Toe board on the terminal
    """

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal depending on the OS

    cell_number = 1

    for row in range(3):
        for col in range(3):
    
            if board[row][col] == ' ':
                print_value = str(cell_number)
            else:
                print_value = board[row][col] # If the cell is not empty, set print_value to 'X' or 'O'

            if col == 0:
                print(" " + print_value, end="") # Print the cell's value preceded by a space
            elif col == 1:
                print(" | " + print_value, end="") # Print the cell's value preceded by a vertical bar
            else:
                print(" | " + print_value)

            cell_number += 1

        if row < 2:
            print("-----------")

    print("\n")



def player_move():
    """
    Ask the player for their move and update the board accordingly
    """

    # Define a dictionary that maps the positions (1-9) to their corresponding coordinates in the board
    moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
             4: [1, 0], 5: [1, 1], 6: [1, 2],
             7: [2, 0], 8: [2, 1], 9: [2, 2]}

    while True: # Keep asking for a move until a valid one is entered
        try:
            move = int(input('Choose a position (1-9):'))

            if move < 1 or move > 9:
                print('Invalid Move! Try again!')
                continue

            if not check_position(moves[move]): # Check if the chosen position is empty
                print('Invalid Move! Try again!')
                continue

            set_move(moves[move], human) # Set the human's move on the board
            draw_board(board)
            break

        except ValueError:
            print('Enter a number!')


def check_position(moves):
    """
    Check if the chosen position is empty
    """

    return True if board[moves[0]][moves[1]] == ' ' else False


def set_move(moves, player):
    """
    Set the player's move on the board
    """
    
    board[moves[0]][moves[1]] = player


def ai_move():
    """
    The AI's move is determined by the minimax algorithm
    """
    _, best_move = minimax(board, 3, True, -math.inf, math.inf)
    set_move(best_move, ai)
    draw_board(board)


def minimax(board, depth, maximizing_player, alpha, beta):
    """
    The minimax algorithm is used to determine the best move for the AI
    """

    if depth == 0 or terminal(board): # If the game is over or the maximum depth is reached, return the utility of the board
        return utility(ai if maximizing_player else human, board), None

    elif maximizing_player: # If it's the AI's turn, maximize the score
        return max_value(board, depth, alpha, beta)

    else: # If it's the human's turn, minimize the score
        return min_value(board, depth, alpha, beta)


def max_value(board, depth, alpha, beta):
    """
    Maximize the score
    """
    
    best_score = -math.inf
    best_move = None
    
    for i in range(3):
        for j in range(3):

            if board[i][j] == ' ':
                board[i][j] = ai
                score, _ = minimax(board, depth - 1, False, alpha, beta)
                board[i][j] = ' '

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

                alpha = max(alpha, best_score)

                if beta <= alpha: # Alpha pruning
                    break

    return best_score, best_move


def min_value(board, depth, alpha, beta):
    """
    Minimize the score
    """

    best_score = math.inf
    best_move = None

    for i in range(3):
        for j in range(3):

            if board[i][j] == ' ':
                board[i][j] = human
                score, _ = minimax(board, depth - 1, True, alpha, beta)
                board[i][j] = ' '

                if score < best_score:
                    best_score = score
                    best_move = (i, j)
                    
                beta = min(beta, best_score)

                if beta <= alpha: # Beta pruning
                    break

    return best_score, best_move


def utility(player, board):
    """
    Calculate the utility of the board for the AI
    """

    global human_score, ai_score
    human_score = 0
    ai_score = 0

    if check_win(board, human): # If the human wins, the AI gets a negative score
        human_score -= 100 - count_empty_cells(board)
        return human_score

    elif check_win(board, ai): # If the AI wins, the AI gets a positive score
        ai_score += 100 + count_empty_cells(board)
        return ai_score

    if player == human: 
        human_score -= evaluate_board(board, human)
        return human_score
    
    elif player == ai:
        ai_score += evaluate_board(board, ai)
        return ai_score


def evaluate_board(board, player):
    """
    Evaluate the board based on the player's moves
    """

    weights = [
        [3, 2, 3],
        [2, 8, 2],
        [3, 2, 3]
    ]

    score = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == player:
                score += weights[i][j] # If the cell contains the player's marker, add the corresponding weight to the score

    for i in range(3):
        if board[i].count(player) == 2 and board[i].count(' ') == 1: # If a row contains two of the player's markers and one empty cell
            score += 1
        if [row[i] for row in board].count(player) == 2 and [row[i] for row in board].count(' ') == 1: # If a column contains two of the player's markers and one empty cell
            score += 1
 
    # Check for diagonals
    if board[0][0] == board[1][1] == player and board[2][2] == ' ':
        score += 1
    if board[0][2] == board[1][1] == player and board[2][0] == ' ':
        score += 1
    if board[2][2] == board[1][1] == player and board[0][0] == ' ':
        score += 1
    if board[2][0] == board[1][1] == player and board[0][2] == ' ':
        score += 1

    return score


def check_win(board, player):
    """
    Check if the player has won the game
    """

    for i in range(3):
        if [player, player, player] in [[board[i][0], board[i][1], board[i][2]], [board[0][i], board[1][i], board[2][i]]]: return True # Check rows and columns

    if [player, player, player] in [[board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]: return True # Check diagonals

    return False


def count_empty_cells(board):
    """
    Count the number of empty cells on the board
    """

    score = 0
    for row in board:
        for item in row:
                if item == ' ':
                    score += 1
    return score


def print_result():

    if check_win(board, human):
        print('YOU BEAT THE AI! \n')
    
    elif check_win(board, ai):
        print('womp womp :( \n')
    
    else:
        print('Draw \n')


def terminal(board):
    """
    Check if the game is over
    """

    return True if check_win(board, human) or check_win(board, ai) or is_board_full(board) else False

def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True


def main():

    player_choice()
    draw_board(board)

    if human == 'X':
        while not terminal(board): # Keep playing until the game is over
            player_move()
            if not terminal(board):
                ai_move()
        print_result()

    else:
        while not terminal(board): # Keep playing until the game is over
            ai_move()
            if not terminal(board):
                player_move()
        print_result()


if __name__ == "__main__":
    main()