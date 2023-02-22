import copy

import game as ttt
import utils

def minimax_ai(board, player):
    best_move = None
    best_score = None
    
    for move in utils.get_all_legal_moves(board):
        _board = copy.deepcopy(board)
        ttt.make_move(player, _board, move)

        opp = utils.get_opponent(player)
        score = _minimax_score(_board, opp, player)
        
        if best_score is None or score > best_score:
            best_move = move
            best_score = score
        
    return best_move

def _minimax_score(board, player_to_move, player_to_optimize):
    winner = ttt.is_winner(board)

    if winner is not None:
        if winner == player_to_optimize:
            return 10
        else:
            return -10
    elif ttt.board_full(board):
        return 0

    legal_moves = utils.get_all_legal_moves(board)

    scores = []

    for move in legal_moves:
        _board = copy.deepcopy(board)
        ttt.make_move(player_to_move, _board, move)

        opp = utils.get_opponent(player_to_move)
        opp_best_response_score = _minimax_score(_board, opp, player_to_optimize)
        scores.append(opp_best_response_score)

    if player_to_move == player_to_optimize:
        return max(scores)
    else:
        return min(scores)