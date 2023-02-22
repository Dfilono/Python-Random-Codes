def get_opponent(player):
    if player == 'X':
        return 'O'
    elif player == 'O':
        return 'X'
    else:
        raise Exception("Unknown player: " + player)

def get_all_legal_moves(board):
    legal_moves = []
    for x, row in enumerate(board):
        for y, val in enumerate(row):
            if val is None:
                legal_moves.append((x, y))
    return legal_moves