import pygame as p
from engine import Game, Move

# Board dimensions
HEIGHT = WIDTH = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 45

IMAGES = {}


def load_images():
    piece_map = {
        "wp": "white-pawn.png",
        "wr": "white-rook.png",
        "wn": "white-knight.png",
        "wb": "white-bishop.png",
        "wq": "white-queen.png",
        "wk": "white-king.png",
        "bp": "black-pawn.png",
        "br": "black-rook.png",
        "bn": "black-knight.png",
        "bb": "black-bishop.png",
        "bq": "black-queen.png",
        "bk": "black-king.png",
    }

    for piece, filename in piece_map.items():
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"images/{filename}"),
            (SQ_SIZE, SQ_SIZE)
        )


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()

    gs = Game()
    valid_moves = gs.all_valid_moves()
    user_move = False

    load_images()

    running = True
    selected_square = ()
    player_clicks = [] 
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                    if len(player_clicks) == 2:
                        move = Move(player_clicks[0], player_clicks[1], gs.chess_board)
                        print(move.get_chess_notation())
                        if move in valid_moves:
                            gs.make_move(move)
                            user_move = True
                        selected_square = ()
                        player_clicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    user_move = True

        if user_move:
            valid_moves = gs.all_valid_moves()
            user_move = False
                    
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

    p.quit()


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.chess_board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("pink")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(
                screen,
                color,
                p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(
                    IMAGES[piece],
                    p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )


if __name__ == "__main__":
    main()
