"""
ระบบบอทหมากรุก - ใช้ Minimax + Alpha-Beta Pruning
"""

from config import row_count, column_count
from source.entities.piece import WHITE, BLACK

# คะแนนหมากแต่ละตัว
PIECE_VALUES = {
    "pawn": 10,
    "knight": 30,
    "bishop": 30,
    "rook": 50,
    "queen": 90,
    "king": 0,  # ไม่นับใน evaluation
}


class ChessAI:
    """บอทหมากรุก รับ board เข้ามา"""

    def __init__(self, board):
        self.board = board
        self.max_depth = 2

    def evaluate_board(self) -> float:
        """ประเมินกระดาน - ขาวบวก ดำลบ"""
        score = 0
        for row in range(row_count):
            for col in range(column_count):
                piece = self.board.board[row][col]
                if piece:
                    value = PIECE_VALUES.get(piece.piece_type, 0)
                    if piece.color == WHITE:
                        score += value
                    else:
                        score -= value
        return score

    def _simulate_move(self, piece, row: int, col: int) -> tuple:
        """จำลองการเดิน คืนค่า (captured_piece) สำหรับ undo"""
        old_row, old_col = piece.row, piece.col
        captured = self.board.board[row][col]
        self.board.board[old_row][old_col] = 0
        self.board.board[row][col] = piece
        piece.row, piece.col = row, col
        return (old_row, old_col, captured)

    def _undo_move(self, piece, old_row: int, old_col: int, captured):
        """ย้อนการเดิน"""
        row, col = piece.row, piece.col
        self.board.board[old_row][old_col] = piece
        self.board.board[row][col] = captured
        piece.row, piece.col = old_row, old_col

    def minimax(self, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        """จำลองการเดินล่วงหน้า หาคะแนนที่ดีที่สุด"""
        # Terminal: ถึง depth หรือจบเกม
        if depth == 0:
            return self.evaluate_board()

        color = WHITE if is_maximizing else BLACK
        if self.board.is_checkmate(color):
            return -10000 if is_maximizing else 10000
        if self.board.is_stalemate(color):
            return 0

        if is_maximizing:
            max_eval = float("-inf")
            for row, col in self.board.get_piece_positions(WHITE):
                piece = self.board.board[row][col]
                for move_row, move_col in self.board.get_legal_moves(piece):
                    old_row, old_col, captured = self._simulate_move(piece, move_row, move_col)
                    eval_score = self.minimax(depth - 1, False, alpha, beta)
                    self._undo_move(piece, old_row, old_col, captured)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float("inf")
            for row, col in self.board.get_piece_positions(BLACK):
                piece = self.board.board[row][col]
                for move_row, move_col in self.board.get_legal_moves(piece):
                    old_row, old_col, captured = self._simulate_move(piece, move_row, move_col)
                    eval_score = self.minimax(depth - 1, True, alpha, beta)
                    self._undo_move(piece, old_row, old_col, captured)
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval

    def get_best_move(self) -> tuple | None:
        """คืนค่า (piece, row, col) ที่ดีที่สุด หรือ None ถ้าไม่มีตาเดิน"""
        best_move = None
        best_score = float("inf")

        for row, col in self.board.get_piece_positions(BLACK):
            piece = self.board.board[row][col]
            for move_row, move_col in self.board.get_legal_moves(piece):
                old_row, old_col, captured = self._simulate_move(piece, move_row, move_col)
                score = self.minimax(self.max_depth - 1, True, float("-inf"), float("inf"))
                self._undo_move(piece, old_row, old_col, captured)
                if score < best_score:
                    best_score = score
                    best_move = (piece, move_row, move_col)

        return best_move
