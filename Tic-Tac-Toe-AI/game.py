import random

import heuristic_ais as ai
import minimax_ai as mm

BOARD_WIDTH = 3
BOARD_HEIGHT = 3

def new_board():
    board = []
    for x in range(0, BOARD_WIDTH):
        column = []
        for y in range(0, BOARD_HEIGHT):
            column.append(None)
        board.append(column)

    return board

def is_winner(board):
    all_line_coords = get_lines()

    for line in all_line_coords:
        line_values = [board[x][y] for (x, y) in line]

        if len(set(line_values)) == 1 and line_values[0] is not None:
            return line_values[0]

    return None

def get_lines():
    cols = []
    rows = []

    for x in range(0, BOARD_WIDTH):
        col = []
        for y in range(0, BOARD_HEIGHT):
            col.append((x, y))
        cols.append(col)

    for y in range(0, BOARD_HEIGHT):
        row = []
        for x in range(0, BOARD_HEIGHT):
            row.append((x, y))
        rows.append(row)

    diaganols = [
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    return cols + rows + diaganols

def render(board):
    rows = []
    for y in range(0, BOARD_HEIGHT):
        row = []
        for x in range(0, BOARD_WIDTH):
            row.append(board[x][y])
        rows.append(row)

    row_num = 0
    print('  0 1 2 ')
    print('  ------')
    for row in rows:
        output_row = ''
        for i in row:
            if i is None:
                output_row += ' '
            else:
                output_row += i
        print ("%d|%s|" % (row_num, ' '.join(output_row)))
        row_num += 1
    print('  ------')

def make_move(player, board, move_coords):
    if board[move_coords[0]][move_coords[1]] is not None:
        raise Exception("Illegal move!")
    
    board[move_coords[0]][move_coords[1]] = player

def board_full(board):
    for col in board:
        for i in col:
            if i is None:
                return False
    return True

def get_move(board, current_player_id, alogrithm_name):
    if alogrithm_name == 'random_ai':
        return ai.random_ai(board, current_player_id)
    elif alogrithm_name == 'finds_own_winning_move_ai':
        return ai.finds_own_winning_move_ai(board, current_player_id)
    elif alogrithm_name == 'finds_all_winning_moves':
        return ai.finds_all_winning_moves(board, current_player_id)
    elif alogrithm_name == 'human_player':
        return ai.human_player(board, current_player_id)
    elif alogrithm_name == 'minimax_ai':
        return mm.minimax_ai(board, current_player_id)
    else:
        raise Exception("Unknown algorithm name: " + alogrithm_name)

def play(player1, player2):
    players = [
        ('X', player1),
        ('O', player2)
    ]

    turn_num = 0
    board = new_board()

    while True:
        current_player_id, current_player = players[turn_num % 2]
        render(board)

        move_coords = get_move(board, current_player_id, current_player)
        make_move(current_player_id, board, move_coords)

        winner = is_winner(board)
        if winner is not None:
            render(board)
            print("The WINNER is %s" % winner)
            break

        if board_full(board):
            render(board)
            print("It's a TIE!")
            break

        turn_num += 1