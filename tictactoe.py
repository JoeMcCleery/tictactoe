"""
Tic Tac Toe Player
"""
import copy
import math

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
    diff = 0
    # Calculate difference in moves previously taken
    for row in board:
        for cell in row:
            if cell == X:
                diff -= 1
            elif cell == O:
                diff += 1
    # Player X has the next turn if they have less or equal moves taken to player O, else player O has next turn
    return X if diff >= 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    # Loop all cells
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            # If cell is empty add to possible actions
            if cell == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp_board = copy.deepcopy(board)
    if temp_board[action[0]][action[1]] == EMPTY:
        # Set cell value to player taking current move
        temp_board[action[0]][action[1]] = player(temp_board)
    else:
        raise Exception("Attempting illegal move")

    return temp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Test diagonals for winner
    if board[1][1] != EMPTY and (
            board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]):
        return board[1][1]

    # Test rows and columns for winner
    for i in range(3):
        if board[i][0] != EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        elif board[0][i] != EMPTY and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is over if there is a winner or no actions remaining
    return True if winner(board) or len(actions(board)) == 0 else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    return 1 if winning_player == X else (-1 if winning_player == O else 0)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    optimal_action = (0, 0)
    if current_player == X:
        best = -math.inf
        beta = 0
        for action in actions(board):
            v = min_value(result(board, action), 0, beta)
            if v < beta:
                beta = v
            if v > best:
                best = v
                optimal_action = action
    else:
        best = math.inf
        alpha = 0
        for action in actions(board):
            v = max_value(result(board, action), alpha, 0)
            if v > alpha:
                alpha = v
            if v < best:
                best = v
                optimal_action = action
    return optimal_action


def min_value(board, alpha, beta):
    """
    Returns the minimum utility for the current board
    """
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        if v < alpha:
            return v
    return v


def max_value(board, alpha, beta):
    """
    Returns the maximum utility for the current board
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        if v > beta:
            return v
    return v
