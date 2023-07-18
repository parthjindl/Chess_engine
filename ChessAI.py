import random

piece_score = {"K": 1000, "Q": 9, "B": 3.1, "N": 3, "R": 5, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validmoves):
    turn_mult = 1 if gs.whiteToMove else -1
    oppMinMaxScore = CHECKMATE
    max_score = CHECKMATE * turn_mult
    best_mv = None
    for mv in validmoves:
        gs.make_move(mv)
        if gs.checkMate:
            sc = CHECKMATE
        elif gs.staleMate:
            sc = 0
        else:
            sc = score_board(gs.board) * turn_mult
        if sc > max_score:
            max_score = sc
            best_mv = mv
        gs.undoMove()
    return best_mv


def findBestMoveMinMax(gs, valid_moves):
    global nextMove
    nextMove = None
    alpha = -CHECKMATE
    beta = CHECKMATE
    find_move_minmax(gs, valid_moves, DEPTH, gs.whiteToMove, alpha, beta)
    return nextMove


def find_move_minmax(gs, valid_moves, depth, whiteToMove, alpha, beta):
    global nextMove
    if depth == 0:
        return score_board(gs)
    if whiteToMove:
        max_score = -CHECKMATE
        for mv in valid_moves:
            gs.make_move(mv)
            next_moves = gs.allValidMoves()
            score = find_move_minmax(gs, next_moves, depth - 1, not whiteToMove, alpha, beta)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    nextMove = mv
            gs.undoMove()
            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Beta cutoff
        return max_score
    else:
        min_score = CHECKMATE
        for mv in valid_moves:
            gs.make_move(mv)
            next_moves = gs.allValidMoves()
            score = find_move_minmax(gs, next_moves, depth - 1, not whiteToMove, alpha, beta)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    nextMove = mv
            gs.undoMove()
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_score



def score_board(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for sq in row:
            if sq[0] == 'w':
                score += piece_score[sq[1]]
            elif sq[0] == 'b':
                score -= piece_score[sq[1]]
    return score

