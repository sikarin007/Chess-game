"""
ไฟล์สร้างหมากแต่ละตัว - ใช้หลักการ Inheritance (การสืบทอด)
Class แม่: Piece
Class ลูก: Pawn, Rook, Knight, Bishop, Queen, King
"""

import pygame
from abc import ABC, abstractmethod
from config import square_size, row_count, column_count, PIECE_IMAGES

# สีหมาก
WHITE = "white"
BLACK = "black"


class Piece(ABC):
    """Class แม่ - เก็บข้อมูลพื้นฐานของหมากทุกตัว รับ row, col, color"""

    piece_type: str = ""  # แต่ละ Class ลูกกำหนดเอง: pawn, rook, knight, bishop, queen, king

    def __init__(self, row: int, col: int, color: str):
        self.row = row
        self.col = col
        self.color = color  # "white" หรือ "black"
        self.has_moved = False  # สำหรับกฎ Castling

    def calc_pos(self) -> tuple[int, int]:
        """คำนวณพิกัด x, y (topleft) จาก row, col สำหรับวาดรูป"""
        x = self.col * square_size
        y = self.row * square_size
        return (x, y)

    def draw(self, window: pygame.Surface):
        """วาดรูปหมากลงบนหน้าจอตามสีและประเภท ใช้ PIECE_IMAGES"""
        key = f"{self.color}_{self.piece_type}"
        if key in PIECE_IMAGES:
            img = PIECE_IMAGES[key]
            x, y = self.calc_pos()
            window.blit(img, (x, y))

    @abstractmethod
    def get_valid_moves(self, board: list) -> list[tuple[int, int]]:
        """คืนค่ารายการช่องที่เดินได้ [(row, col), ...] - แต่ละ Class ลูกต้อง implement เอง"""
        pass

    def _is_valid_square(self, row: int, col: int, board: list) -> bool:
        """เช็คว่าช่องอยู่บนกระดานหรือไม่"""
        return 0 <= row < row_count and 0 <= col < column_count

    def _is_empty_or_enemy(self, row: int, col: int, board: list) -> bool:
        """ช่องว่าง หรือ มีหมากฝั่งตรงข้าม (เดิน/กินได้)"""
        if not self._is_valid_square(row, col, board):
            return False
        piece = board[row][col]
        return not piece or piece.color != self.color


class Pawn(Piece):
    """เบี้ย - เดินหน้าหนึ่งช่อง (แรกเดินได้ 2) กินแนวทแยง"""
    piece_type = "pawn"

    def get_valid_moves(self, board: list) -> list[tuple[int, int]]:
        moves = []
        direction = 1 if self.color == BLACK else -1  # ดำลงล่าง(+1), ขาวขึ้นบน(-1)
        # แก้ไขจุดที่ผิด: ดำเริ่มแถว 1, ขาวเริ่มแถว 6
        start_row = 1 if self.color == BLACK else 6

        # เดินตรง 1 ช่อง
        nr, nc = self.row + direction, self.col
        if self._is_valid_square(nr, nc, board) and not board[nr][nc]:
            moves.append((nr, nc))
            # เดินครั้งแรก 2 ช่อง (ต้องเช็คด้วยว่าช่องแรกข้างหน้าต้องว่าง)
            if self.row == start_row:
                nr2 = self.row + 2 * direction
                if self._is_valid_square(nr2, nc, board) and not board[nr2][nc]:
                    moves.append((nr2, nc))

        # กินแนวทแยงซ้ายและขวา (ไม่สามารถเดินเฉียงได้ถ้าไม่มีศัตรู)
        for dc in (-1, 1):
            nr, nc = self.row + direction, self.col + dc
            if self._is_valid_square(nr, nc, board):
                target = board[nr][nc]
                if target and target.color != self.color:  # ถ้ามีคนยืนอยู่ และเป็นศัตรู
                    moves.append((nr, nc))
        return moves


class Rook(Piece):
    """เรือ - เดินแนวตรง (แนวนอน + แนวตั้ง)"""
    piece_type = "rook"

    def get_valid_moves(self, board: list) -> list[tuple[int, int]]:
        moves = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = self.row + dr, self.col + dc
            while self._is_valid_square(r, c, board):
                target = board[r][c]
                if not target:  # ถ้าช่องว่าง เดินไปได้แล้วเช็คช่องต่อไป
                    moves.append((r, c))
                elif target.color != self.color:  # ถ้าเจอศัตรู กินได้แต่ต้องหยุดทะลุ
                    moves.append((r, c))
                    break
                else:  # ถ้าเจอพวกเดียวกัน ห้ามเดินทับและหยุดเช็ค
                    break
                r, c = r + dr, c + dc
        return moves


class Knight(Piece):
    """ม้า - เดินรูปตัว L (2+1 หรือ 1+2)"""
    piece_type = "knight"

    def get_valid_moves(self, board: list) -> list[tuple[int, int]]:
        moves = []
        for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            r, c = self.row + dr, self.col + dc
            if self._is_empty_or_enemy(r, c, board):
                moves.append((r, c))
        return moves


class Bishop(Piece):
    """ตัวโคน - เดินเฉพาะแนวทแยง"""
    piece_type = "bishop"

    def get_valid_moves(self, board: list) -> list[tuple[int, int]]:
        moves = []
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = self.row + dr, self.col + dc
            while self._is_valid_square(r, c, board):
                target = board[r][c]
                if not target:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves


class Queen(Piece):
    """ราชินี - เดินได้ทุกทิศ (เอาท่าเรือ + โคนมารวมกัน)"""
    piece_type = "queen"

    def get_valid_moves(self, board: list) -> list[tuple[int, int]]:
        moves = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = self.row + dr, self.col + dc
            while self._is_valid_square(r, c, board):
                target = board[r][c]
                if not target:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves


class King(Piece):
    """ราชา - เดิน 1 ช่องทุกทิศ + Castling"""
    piece_type = "king"

    def get_valid_moves(self, board: list) -> list[tuple[int, int]]:
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = self.row + dr, self.col + dc
                if self._is_empty_or_enemy(r, c, board):
                    moves.append((r, c))

        # Castling
        if not self.has_moved:
            # Kingside (ขวา): col+1, col+2 ว่าง, col+3 เป็น Rook same color, has_moved=False
            if (self._is_valid_square(self.row, self.col + 1, board) and not board[self.row][self.col + 1]
                and self._is_valid_square(self.row, self.col + 2, board) and not board[self.row][self.col + 2]):
                rook = board[self.row][self.col + 3] if self.col + 3 < 8 else None
                if rook and rook.piece_type == "rook" and rook.color == self.color and not rook.has_moved:
                    moves.append((self.row, self.col + 2))

            # Queenside (ซ้าย): col-1, col-2, col-3 ว่าง, col-4 เป็น Rook same color, has_moved=False
            if (self._is_valid_square(self.row, self.col - 1, board) and not board[self.row][self.col - 1]
                and self._is_valid_square(self.row, self.col - 2, board) and not board[self.row][self.col - 2]
                and self._is_valid_square(self.row, self.col - 3, board) and not board[self.row][self.col - 3]):
                rook = board[self.row][self.col - 4] if self.col - 4 >= 0 else None
                if rook and rook.piece_type == "rook" and rook.color == self.color and not rook.has_moved:
                    moves.append((self.row, self.col - 2))

        return moves
