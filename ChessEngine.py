class GameState:
    def __init__(self):
        self.board = [
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (0, 4)
        self.blackKingLocation = (7, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()

    def make_move(self, move):
        self.board[move.endRow][move.endCol] = move.piece_captured
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.piece_moved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.piece_moved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.piece_moved[0] + 'Q'

        # enpassant
        if move.enPassantMove:
            self.board[move.startRow][move.endCol] = "--"

        if move.piece_moved[1] == 'p' and abs(move.endRow - move.startRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enPassantPossible = ()

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.piece_moved
            self.board[move.endRow][move.endCol] = move.piece_captured
            self.whiteToMove = not self.whiteToMove
            if move.piece_moved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.piece_moved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            self.checkMate = False
            self.staleMate = False
            if move.enPassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.piece_captured
                self.enPassantPossible = (move.endRow, move.endCol)
            if move.piece_moved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()

    def allValidMoves(self):
        temp_enpassant_possible = self.enPassantPossible
        moves = self.allPossibleMoves()

        for i in range(len(moves) - 1, -1, -1):
            # print(moves[i].moveID)
            self.make_move(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        self.enPassantPossible = temp_enpassant_possible
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        opp_moves = self.allPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for m in opp_moves:
            if m.endRow == r and m.endCol == c:
                return True
        return False

    def allPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                x = self.board[r][c][0]
                if (x == 'w' and self.whiteToMove) or (x == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r == 1 and self.board[r + 2][c] == "--" and self.board[r + 1][c] == "--":
                moves.append(movePieces(self.board, (r, c), (r + 2, c)))

            if r < 7 and self.board[r + 1][c] == "--":
                moves.append(movePieces(self.board, (r, c), (r + 1, c)))
            if r < 7 and c >= 1:
                if self.board[r + 1][c - 1][0] == "b":
                    moves.append(movePieces(self.board, (r, c), (r + 1, c - 1)))
                elif (r + 1, c - 1) == self.enPassantPossible:
                    moves.append(movePieces(self.board, (r, c), (r + 1, c - 1), isEnpassantMove=True))
            if r < 7 and c <= 6:
                if self.board[r + 1][c + 1][0] == "b":
                    moves.append(movePieces(self.board, (r, c), (r + 1, c + 1)))
                elif (r + 1, c + 1) == self.enPassantPossible:
                    moves.append(movePieces(self.board, (r, c), (r + 1, c + 1), isEnpassantMove=True))

            # if (r == 6)
        else:
            if r == 6 and self.board[r - 2][c] == "--" and self.board[r - 1][c] == "--":
                moves.append(movePieces(self.board, (r, c), (r - 2, c)))
            if r > 0 and self.board[r - 1][c] == "--":
                moves.append(movePieces(self.board, (r, c), (r - 1, c)))
            if r > 0 and c >= 1:
                if self.board[r - 1][c - 1][0] == "w":
                    moves.append(movePieces(self.board, (r, c), (r - 1, c - 1)))
                elif (r - 1, c - 1) == self.enPassantPossible:
                    moves.append(movePieces(self.board, (r, c), (r - 1, c - 1), isEnpassantMove=True))
            if r > 0 and c <= 6:
                if self.board[r - 1][c + 1][0] == "w":
                    moves.append(movePieces(self.board, (r, c), (r - 1, c + 1)))
                elif (r - 1, c + 1) == self.enPassantPossible:
                    moves.append(movePieces(self.board, (r, c), (r - 1, c + 1), isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        enemy_piece = "w"
        if self.whiteToMove:
            enemy_piece = "b"
        for d in directions:
            for i in range(1, 8):
                new_r = r + d[0] * i
                new_c = c + d[1] * i
                if 0 <= new_r <= 7 and 0 <= new_c <= 7:
                    if self.board[new_r][new_c] == "--":
                        moves.append(movePieces(self.board, (r, c), (new_r, new_c)))
                    elif self.board[new_r][new_c][0] == enemy_piece:
                        moves.append(movePieces(self.board, (r, c), (new_r, new_c)))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        directions = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        enemy_piece = 'w'
        if self.whiteToMove:
            enemy_piece = 'b'
        for d in directions:
            new_r = r + d[0]
            new_c = c + d[1]
            if 0 <= new_r <= 7 and 0 <= new_c <= 7 and (self.board[new_r][new_c] == "--" or enemy_piece ==
                                                        self.board[new_r][new_c][0]):
                moves.append(movePieces(self.board, (r, c), (new_r, new_c)))

    def getBishopMoves(self, r, c, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        enemy_piece = "w"
        if self.whiteToMove:
            enemy_piece = "b"
        for d in directions:
            for i in range(1, 8):
                new_r = r + d[0] * i
                new_c = c + d[1] * i
                if 0 <= new_r <= 7 and 0 <= new_c <= 7:
                    if self.board[new_r][new_c] == "--":
                        moves.append(movePieces(self.board, (r, c), (new_r, new_c)))
                    elif self.board[new_r][new_c][0] == enemy_piece:
                        moves.append(movePieces(self.board, (r, c), (new_r, new_c)))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        directions = [(1, 1), (1, 0), (1, -1), (0, -1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

        if self.whiteToMove:
            enemy_piece = 'b'
        else:
            enemy_piece = 'w'
        for d in directions:
            new_r = r + d[0]
            new_c = c + d[1]
            if 0 <= new_r <= 7 and 0 <= new_c <= 7 and (self.board[new_r][new_c] == "--" or enemy_piece ==
                                                        self.board[new_r][new_c][0]):
                moves.append(movePieces(self.board, (r, c), (new_r, new_c)))


class movePieces:
    def __init__(self, board, sq_start, sq_end, isEnpassantMove=False):
        """

        :type board: object
        """
        self.startRow = sq_start[0]
        self.startCol = sq_start[1]
        self.endRow = sq_end[0]
        self.endCol = sq_end[1]
        self.piece_moved = board[self.startRow][self.startCol]
        self.piece_captured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # pawn promo
        self.isPawnPromotion = False

        if (self.piece_moved == "wp" and self.endRow == 7) or (self.piece_moved == "bp" and self.endRow == 0):
            self.isPawnPromotion = True
        # enpassant
        self.enPassantMove = isEnpassantMove
        if self.enPassantMove:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'

        # print(self.moveID)

    def __eq__(self, other):
        if isinstance(other, movePieces):
            return self.moveID == other.moveID
