class Game():
    def __init__(self):
        self.chess_board = self.initialize_board()
        self.white_to_move = True
        self.move_log = []
        self.move_functions = {
            'p': self.get_valid_pawn_moves,
            'r': self.get_valid_rook_moves,
            'n': self.get_valid_knight_moves,
            'b': self.get_valid_bishop_moves,
            'q': self.get_valid_queen_moves,
            'k': self.get_valid_king_moves
            }
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False

        self.in_check = False
        self.pins = []
        self.checks = []

    def initialize_board(self):
        board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        return board
    

    def make_move(self, move):
        self.chess_board[move.start_row][move.start_col] = '--'
        self.chess_board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wk':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bk':
            self.black_king_location = (move.end_row, move.end_col)
    
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.chess_board[move.start_row][move.start_col] = move.piece_moved
            self.chess_board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wk':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bk':
                self.black_king_location = (move.start_row, move.start_col)

    def all_possible_moves(self):
        move = []
        for r in range(len(self.chess_board)):
            for c in range(len(self.chess_board[r])):
                player_turn = self.chess_board[r][c][0]
                if (player_turn == 'w' and self.white_to_move) or (player_turn == 'b' and not self.white_to_move):
                    piece = self.chess_board[r][c][1]
                    self.move_functions[piece](r, c, move)
        return move
    
    def valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.chess_board[check_row][check_col]
                valid_squares = []
                if piece_checking[1] == 'n':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'k':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_valid_king_moves(king_row, king_col, moves)
        else:
            moves = self.all_possible_moves()

        return moves


    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.chess_board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'k':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        type_of_piece = end_piece[1]
                        if (0 <= j <= 3 and type_of_piece == 'r') or \
                           (4 <= j <= 7 and type_of_piece == 'b') or \
                           (i == 1 and type_of_piece == 'p' and ((enemy_color == 'w' and j in (6, 7)) or (enemy_color == 'b' and j in (4, 5)))) or \
                           (type_of_piece == 'q') or (i == 1 and type_of_piece == 'k'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break

        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for d in knight_moves:
            end_row = start_row + d[0]
            end_col = start_col + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.chess_board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'n':
                    in_check = True
                    checks.append((end_row, end_col, d[0], d[1]))

        return in_check, pins, checks

    def in_check(self):
        if self.white_to_move:
            return self.is_under_check(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.is_under_check(self.black_king_location[0], self.black_king_location[1])
    

    def is_under_check(self, r, c):
        self.white_to_move = not self.white_to_move
        opponent_moves = self.all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False
    

    def get_valid_pawn_moves(self, r, c, move):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            if self.chess_board[r-1][c] == '--':
                if not piece_pinned or pin_direction == (-1, 0):
                    move.append(Move((r, c), (r-1, c), self.chess_board))
                    if r == 6 and self.chess_board[r-2][c] == '--':
                        move.append(Move((r, c), (r-2, c), self.chess_board))
            if c-1 >= 0:
                if self.chess_board[r-1][c-1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, -1):
                        move.append(Move((r, c), (r-1, c-1), self.chess_board))
            if c+1 <= 7:
                if self.chess_board[r-1][c+1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, 1):
                        move.append(Move((r, c), (r-1, c+1), self.chess_board))
        else:
            if self.chess_board[r+1][c] == '--':
                if not piece_pinned or pin_direction == (1, 0):
                    move.append(Move((r, c), (r+1, c), self.chess_board))
                    if r == 1 and self.chess_board[r+2][c] == '--':
                        move.append(Move((r, c), (r+2, c), self.chess_board))
            if c-1 >= 0:
                if self.chess_board[r+1][c-1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, -1):
                        move.append(Move((r, c), (r+1, c-1), self.chess_board))
            if c+1 <= 7:
                if self.chess_board[r+1][c+1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, 1):
                        move.append(Move((r, c), (r+1, c+1), self.chess_board))

    
    def get_valid_rook_moves(self, r, c, move):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.chess_board[r][c][1] != 'q':
                    self.pins.remove(self.pins[i])
                break
        
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.chess_board[end_row][end_col]
                        if end_piece == '--':
                            move.append(Move((r, c), (end_row, end_col), self.chess_board))
                        elif end_piece[0] == enemy_color:
                            move.append(Move((r, c), (end_row, end_col), self.chess_board))
                            break
                        move.append(Move((r, c), (end_row, end_col), self.chess_board))
                        break
                    else:
                        break
                else:
                    break

    def get_valid_knight_moves(self, r, c, move):
        possible_knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),(1, -2), (1, 2), (2, -1), (2, 1)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for m in possible_knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.chess_board[end_row][end_col]
                if end_piece == '--' or end_piece[0] == enemy_color:
                    move.append(Move((r, c), (end_row, end_col), self.chess_board)) 
    

    def get_valid_bishop_moves(self, r, c, move):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.chess_board[end_row][end_col]
                    if end_piece == '--':
                        move.append(Move((r, c), (end_row, end_col), self.chess_board))
                    elif end_piece[0] == enemy_color:
                        move.append(Move((r, c), (end_row, end_col), self.chess_board))
                        break
                    else:
                        break
                else:
                    break

        
    def get_valid_queen_moves(self, r, c, move):
        self.get_valid_rook_moves(r, c, move)
        self.get_valid_bishop_moves(r, c, move)

    
    def get_valid_king_moves(self, r, c, move):
        possible_king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for m in possible_king_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.chess_board[end_row][end_col]
                if end_piece == '--' or end_piece[0] == enemy_color:
                    move.append(Move((r, c), (end_row, end_col), self.chess_board))

    
class Move():
    
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}


    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = (self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
    
    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
