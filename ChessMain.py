import ChessEngine
import ChessAI
import pygame as p
p.init() #creation of instance
WIDTH = HEIGHT = 512 #pixel
DIMENSIONS = 8
SQ_SIZE = HEIGHT // DIMENSIONS #size of one box
MAX_FPS = 15 #rendering at 15 frames per second
IMAGES = {}


def load_images():
    pieces = ['wp', 'wQ', 'wK', 'wR', 'wB', 'wN', 'bp', 'bQ', 'bK', 'bR', 'bB', 'bN']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()#bringing time
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    valid_moves = gs.allValidMoves()

    move_made = False
    load_images()
    running = True
    sq_selected: tuple = ()
    move = []
    playerOne = True
    playerTwo = False
    while running:
        human_turn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col):
                        sq_selected = ()
                        move = []

                    else:
                        sq_selected = (row, col)
                        if len(move) == 0:
                            if gs.board[row][col] != "--":
                                move.append(sq_selected)
                        else:
                            move.append(sq_selected)
                    if len(move) == 2:
                        mv = ChessEngine.movePieces(gs.board, move[0], move[1])

                        # print(possible_moves)
                        if mv in valid_moves:
                            gs.make_move(mv)
                            move_made = True
                            sq_selected = ()
                            move = []
                            # print(gs.checkMate)
                        else:
                            move = [sq_selected]
        if not human_turn:
            ai_move = ChessAI.findBestMoveMinMax(gs, valid_moves)
            if ai_move is None:
                ai_move = ChessAI.findRandomMove(valid_moves)
            gs.make_move(ai_move)
            move_made = True
        if move_made:
            valid_moves = gs.allValidMoves()

            # print(possible_moves)
            move_made = False
        draw_game_state(screen, gs, valid_moves, sq_selected)
        if gs.checkMate:
            if gs.whiteToMove:
                putText(screen, "Black wins by CheckMate")
            else:
                putText(screen, "White wins by CheckMate")
        elif gs.staleMate:
            putText(screen, "Game is draw by stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()


def putText(screen, s):
    font = p.font.SysFont("Helvetica", 32, True)
    text = font.render(s, 0, p.Color("Green"))
    screen.blit(text, p.Rect(0, 0, WIDTH, HEIGHT, ).move(WIDTH / 2 - text.get_width() / 2,
                                                         HEIGHT / 2 - text.get_height() / 2))


def highlight(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.whiteToMove:
            ally = "w"
        else:
            ally = "b"
        if gs.board[r][c][0] == ally:
            # print("ewfewj")
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.startRow == r and move.startCol == c:
                    # print(move.endRow, move.endCol)
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_chess_board(screen)
    highlight(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)


def draw_chess_board(screen):
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            col = colours[(r + c) % 2]
            p.draw.rect(screen, col, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
