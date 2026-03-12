"""
ไฟล์กระดาน - จัดการข้อมูลบนกระดาน 8x8 และการวาดตารางหมากรุก
"""

import pygame
from config import square_size, row_count, column_count, BOARD_LIGHT, BOARD_DARK
from config import MOVE_SOUND, CAPTURE_SOUND, CASTLE_SOUND
from source.entities.piece import (
    WHITE, BLACK,
    Rook, Knight, Bishop, Queen, King, Pawn,
)


class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self) -> list:
        """สร้าง Array 2 มิติ 8x8 วางหมากรุกตำแหน่งเริ่มต้นมาตรฐาน ช่องว่างใส่ 0"""
        board = [[0 for _ in range(column_count)] for _ in range(row_count)]

        # แถว 0: ดำ (เรือ, ม้า, โคน, ราชินี, ราชา, โคน, ม้า, เรือ) - ดำอยู่ด้านบน
        board[0] = [
            Rook(0, 0, BLACK), Knight(0, 1, BLACK), Bishop(0, 2, BLACK), Queen(0, 3, BLACK),
            King(0, 4, BLACK), Bishop(0, 5, BLACK), Knight(0, 6, BLACK), Rook(0, 7, BLACK),
        ]
        # แถว 1: เบี้ยดำ (ดำเริ่มแถว 1 เดินลง)
        board[1] = [Pawn(1, c, BLACK) for c in range(column_count)]

        # แถว 6: เบี้ยขาว (ขาวเริ่มแถว 6 เดินขึ้น)
        board[6] = [Pawn(6, c, WHITE) for c in range(column_count)]
        # แถว 7: ขาว (เรือ, ม้า, โคน, ราชินี, ราชา, โคน, ม้า, เรือ) - ขาวอยู่ด้านล่าง
        board[7] = [
            Rook(7, 0, WHITE), Knight(7, 1, WHITE), Bishop(7, 2, WHITE), Queen(7, 3, WHITE),
            King(7, 4, WHITE), Bishop(7, 5, WHITE), Knight(7, 6, WHITE), Rook(7, 7, WHITE),
        ]
        # แถว 2-5: ช่องว่าง (0)
        return board

    def draw_squares(self, window: pygame.Surface):
        """วาดตารางสลับสีลงบนหน้าจอ"""
        for row in range(row_count):
            for col in range(column_count):
                color = BOARD_LIGHT if (row + col) % 2 == 0 else BOARD_DARK
                rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
                pygame.draw.rect(window, color, rect)

    def draw(self, window: pygame.Surface):
        """วาดตารางแล้ววาดหมากทับ เรียก draw_squares ก่อน จากนั้นวนลูปวาด piece แต่ละตัว"""
        self.draw_squares(window)
        for row in self.board:
            for piece in row:
                if piece:
                    piece.draw(window)

    def draw_valid_moves(self, window: pygame.Surface, moves: list):
        """วาดวงกลมสีเทาโปร่งแสงที่กึ่งกลางช่องที่เดินได้"""
        radius = 15
        for row, col in moves:
            cx = col * square_size + square_size // 2
            cy = row * square_size + square_size // 2
            surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (128, 128, 128, 100), (radius, radius), radius)
            window.blit(surf, (cx - radius, cy - radius))

    def move(self, piece, row: int, col: int):
        """ย้ายตำแหน่งหมากใน Array 2 มิติเมื่อมีการเดินเกิดขึ้น"""
        old_row, old_col = piece.row, piece.col
        is_capture = bool(self.board[row][col])
        is_castle = False

        if piece.piece_type == "king" and abs(col - piece.col) == 2:
            is_castle = True
            if col > piece.col:  # Kingside (ขวา)
                rook = self.board[row][7]
                self.board[row][7] = 0
                self.board[row][col - 1] = rook
                rook.row, rook.col = row, col - 1
                rook.has_moved = True
            else:  # Queenside (ซ้าย)
                rook = self.board[row][0]
                self.board[row][0] = 0
                self.board[row][col + 1] = rook
                rook.row, rook.col = row, col + 1
                rook.has_moved = True

        self.board[old_row][old_col] = 0
        self.board[row][col] = piece
        piece.row, piece.col = row, col
        piece.has_moved = True

        if is_castle and CASTLE_SOUND:
            CASTLE_SOUND.play()
        elif is_capture and CAPTURE_SOUND:
            CAPTURE_SOUND.play()
        elif MOVE_SOUND:
            MOVE_SOUND.play()

    def get_piece_at(self, row: int, col: int):
        """คืนค่าหมากที่ช่อง (row, col) หรือ 0 ถ้าช่องว่าง"""
        if 0 <= row < row_count and 0 <= col < column_count:
            return self.board[row][col]
        return None

    def get_piece_positions(self, color: str) -> list[tuple[int, int]]:
        """ดึงตำแหน่ง (row, col) ของหมากทั้งหมดของสีที่ระบุ"""
        positions = []
        for row in range(row_count):
            for col in range(column_count):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    positions.append((row, col))
        return positions

    def _find_king(self, color: str) -> tuple[int, int] | None:
        """หาตำแหน่ง King ของสีที่ระบุ"""
        for row in range(row_count):
            for col in range(column_count):
                piece = self.board[row][col]
                if piece and piece.piece_type == "king" and piece.color == color:
                    return (row, col)
        return None

    def is_in_check(self, color: str) -> bool:
        """เช็คว่า King ของสีที่ระบุกำลังถูกโจมตี (รุก) อยู่หรือไม่"""
        king_pos = self._find_king(color)
        if king_pos is None:
            return False
        king_row, king_col = king_pos
        opponent_color = BLACK if color == WHITE else WHITE

        for row in range(row_count):
            for col in range(column_count):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    if (king_row, king_col) in piece.get_valid_moves(self.board):
                        return True
        return False

    def get_legal_moves(self, piece) -> list[tuple[int, int]]:
        """กรองตาเดินที่ทำให้ King โดนรุก ออก คืนเฉพาะตาที่ปลอดภัย"""
        valid_moves = piece.get_valid_moves(self.board)
        legal_moves = []
        old_row, old_col = piece.row, piece.col

        for row, col in valid_moves:
            captured = self.board[row][col]
            rook_saved = None
            rook_old_col = None
            if piece.piece_type == "king" and abs(col - old_col) == 2:
                if col > old_col:  # Kingside
                    rook_saved = self.board[row][7]
                    rook_old_col = 7
                    self.board[row][7] = 0
                    self.board[row][5] = rook_saved
                    if rook_saved:
                        rook_saved.col = 5
                else:  # Queenside
                    rook_saved = self.board[row][0]
                    rook_old_col = 0
                    self.board[row][0] = 0
                    self.board[row][3] = rook_saved
                    if rook_saved:
                        rook_saved.col = 3
            self.board[old_row][old_col] = 0
            self.board[row][col] = piece
            piece.row, piece.col = row, col

            if not self.is_in_check(piece.color):
                legal_moves.append((row, col))

            self.board[old_row][old_col] = piece
            self.board[row][col] = captured
            piece.row, piece.col = old_row, old_col
            if rook_saved is not None:
                self.board[row][rook_old_col] = rook_saved
                self.board[row][5 if rook_old_col == 7 else 3] = 0
                rook_saved.row, rook_saved.col = row, rook_old_col

        return legal_moves

    def _has_any_legal_move(self, color: str) -> bool:
        """เช็คว่าหมากของสีนี้มีตาเดินที่ถูกกฎอย่างน้อย 1 ตาหรือไม่"""
        for row, col in self.get_piece_positions(color):
            piece = self.board[row][col]
            if self.get_legal_moves(piece):
                return True
        return False

    def is_checkmate(self, color: str) -> bool:
        """รุกฆาต: ไม่มี legal moves เหลือ + กำลังโดนรุกอยู่"""
        return not self._has_any_legal_move(color) and self.is_in_check(color)

    def is_stalemate(self, color: str) -> bool:
        """เสมอ: ไม่มี legal moves เหลือ + ไม่โดนรุก"""
        return not self._has_any_legal_move(color) and not self.is_in_check(color)
