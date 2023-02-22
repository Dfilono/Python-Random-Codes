import random
import utils

BOARD_WIDTH = 3
BOARD_HEIGHT = 3

def human_player(board, player):
    x_coord = int(input("X?: "))
    y_coord = int(input("Y?: "))
    return (x_coord, y_coord)

def random_ai(board, player):
    return _random_move(board)

def finds_own_winning_move_ai(board, player):
    my_winning_move = _find_winning_move(board, player)
    if my_winning_move:
        return my_winning_move
    else:
        return _random_move(board);

def blocks_their_winning_moves_ai(board, player):
    their_winning_move = _find_winning_move(board, player)
    if their_winning_move:
        return their_winning_move
    else:
        return _random_move(board)

def finds_all_winning_moves(board, player):
    my_winning_move = _find_winning_move(board, player)
    if my_winning_move:
        return my_winning_move

    their_winning_move = _find_winning_move(board, utils.get_opponent(player))
    if their_winning_move:
        return their_winning_move

    return _random_move(board)

def _find_winning_move(board, player):
    all_line_coords = _get_line_coords()

    for line in all_line_coords:
        n_me = 0
        n_them = 0
        n_new = 0
        last_new_coord = None

        for (x, y) in line:
            value = board[x][y]
            if value == player:
                n_me += 1
            elif value is None:
                n_new += 1
                last_new_coord = (x, y)
            else:
                n_them += 1
        
        if n_me == 2 and n_new == 1:
            return last_new_coord

def _random_move(board):
    legal_moves = utils.get_all_legal_moves(board)
    return random.choice(legal_moves)

def _get_line_coords():
    cols = []
    rows = []
    for x in range(0, BOARD_WIDTH):
        col = []
        for y in range(0, BOARD_HEIGHT):
            col.append((x, y))
        cols.append(col)

    for y in range(0, BOARD_HEIGHT):
        row = []
        for x in range(0, BOARD_WIDTH):
            row.append((x, y))
        rows.append(row)

    diaganols = [
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    return cols + rows + diaganols