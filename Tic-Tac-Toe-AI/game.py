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

        
