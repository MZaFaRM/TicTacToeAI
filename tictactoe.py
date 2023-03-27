"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Denotes the number of moves already played by either
    x_moves = 0
    o_moves = 0

    # Gets the number of moves already played
    for rows in board:
        for item in rows:
            if item == X:
                x_moves += 1
            elif item == O:
                o_moves += 1

    # If board has more X than O return O else return X; ie:
    return X if x_moves <= o_moves else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Represents actions available
    action_list = []

    # Loops through row and column to find 'EMPTY'
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if not column:
                # If found append location to list
                move = (i, j)
                action_list.append(move)

    return action_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Makes a deep copy of the 'board' to preserve 'board'
    sample = copy.deepcopy(board)

    # If a value exists at the given location raise Exception
    if sample[action[0]][action[1]]:
        raise Exception("Invalid Position")

    # 'board''s copy but with value assigned at that location
    sample[action[0]][action[1]] = player(sample)

    return sample


def check_winner(board, player):
    # List of all the win conditions
    wins = {
        "123": 0,
        "147": 0,
        "159": 0,
        "258": 0,
        "357": 0,
        "369": 0,
        "456": 0,
        "789": 0,
    }

    # Ctores the player's positions
    player_value = ""

    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == player:
                # Converts the position values like (2, 1) to 8
                value = (3 * i) + j + 1
                # And adds it to player's value
                player_value += str(value)

    for value in player_value:
        for key in wins:
            if value in key:
                # If player position is part of an item in win position increment by one
                wins[key] += 1

    for key in wins:
        if wins[key] == 3:
            # If for any win position value is 3 player won
            return player

    return None


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checks if either of the player won
    return check_winner(board, X) or check_winner(board, O)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Gets status from winner
    status = winner(board)

    if not status:
        # Checks if status was result of tie
        for row in board:
            for column in row:
                # If empty value exist return game not over
                if column == EMPTY:
                    return False

    # No empty rows; game over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Checks if either of the player won
    if check_winner(board, X):
        return 1
    elif check_winner(board, O):
        return -1
    else:
        return 0


def minimax_helper(board):
    _choices = actions(board)
    
    # If initial state selects the first choice
    if board == initial_state():
        return {"position" : random.choice(_choices)}
    
    _player = player(board)

    # If there are choices that can be made and the game hasn't ended
    if _choices and not terminal(board):
        
        results = []

        # Recursively plays out all the scenarios
        for choice in _choices:
            
            action = {}
            _board = result(board, choice)
            value = minimax_helper(_board)
            action["position"] = choice
            try:
                action["value"] = value["value"]
            except TypeError:
                action["value"] = value

            results.append(action)
        
        reference = None

        # Minimax filtering
        if _player == O:
            reference = math.inf
            for action in results:
                if action["value"] < reference:
                    reference = action["value"]
                    
        elif _player == X:
            reference = -math.inf
            for action in results:
                if action["value"] > reference:
                    reference = action["value"]

        # Return a random best choice from the list of choices for the given player
        results = [action for action in results if action["value"] == reference]
        results = random.choice(results)
        return results

    else:
        # Returns the value of the position
        return utility(board)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Returns the best position from helper function
    try:
        return minimax_helper(board)["position"]
    # Occurs when passed games that already ended
    except TypeError:
        raise Exception("Game already ended.")
