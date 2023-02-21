import random

BOARD_WIDTH = 3
BOARD_HEIGHT = 3

def new_board():
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(None)
        board.append(column)

    return board

def is_winner(board):
    pass

def get_lines():
    cols = []
    rows = []

    for x in range(BOARD_WIDTH):
        col = []
        for y in range(BOARD_HEIGHT):
            col.append((x, y))
        cols.append(col)

    for y in range(BOARD_HEIGHT):
        row = []
        for x in range(BOARD_HEIGHT):
            row.append((x, y))
        rows.append(row)

    diaganols = [
        [(0, 0)], [(1, 1)], [(2, 2)],
        [(0, 2)], [(1, 1)], [(2, 0)]
    ]

    return cols + rows + diaganols

def render(board):
    rows = []
    for y in range(BOARD_HEIGHT):
        row = []
        for x in range(BOARD_WIDTH):
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

def play(player1, player2):
    players = [
        ('X', player1),
        ('O', player2)
    ]

    turn_num = 0
    board = new_board

    while True:
        current_player_id, current_player = players[turn_num % 2]
        render(board)

        move_coords = current_player(board, current_player_id)
        make_move(current_player_id, board, move_coords)

        winner = is_winner(board)
        if winner is None:
            render(board)
            print("The WINNER is %s" % winner)
            break

        if board_full(board):
            render(board)
            print("It's a TIE!")
            break

        turn_num += 1
