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
        moves = self.all_possible_moves()
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check:
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        
        return moves
    

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
        if self.white_to_move:
            if self.chess_board[r-1][c] == '--':
                move.append(Move((r, c), (r-1, c), self.chess_board))
                if r == 6 and self.chess_board[r-2][c] == '--':
                    move.append(Move((r, c), (r-2, c), self.chess_board))
            if c-1 >= 0:
                if self.chess_board[r-1][c-1][0] == 'b':
                    move.append(Move((r, c), (r-1, c-1), self.chess_board))
            if c+1 <= 7:
                if self.chess_board[r-1][c+1][0] == 'b':
                    move.append(Move((r, c), (r-1, c+1), self.chess_board))
        else:
            if self.chess_board[r+1][c] == '--':
                move.append(Move((r, c), (r+1, c), self.chess_board))
                if r == 1 and self.chess_board[r+2][c] == '--':
                    move.append(Move((r, c), (r+2, c), self.chess_board))
            if c-1 >= 0:
                if self.chess_board[r+1][c-1][0] == 'w':
                    move.append(Move((r, c), (r+1, c-1), self.chess_board))
            if c+1 <= 7:
                if self.chess_board[r+1][c+1][0] == 'w':
                    move.append(Move((r, c), (r+1, c+1), self.chess_board))

    
    def get_valid_rook_moves(self, r, c, move):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
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
