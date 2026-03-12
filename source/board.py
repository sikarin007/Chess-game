"""
ไฟล์กระดาน - จัดการข้อมูลบนกระดาน 8x8 และการวาดตารางหมากรุก
"""

import pygame
from config import square_size, row_count, column_count, BOARD_LIGHT, BOARD_DARK
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

        # แถว 0: ขาว (เรือ, ม้า, โคน, ราชินี, ราชา, โคน, ม้า, เรือ)
        board[0] = [
            Rook(0, 0, WHITE), Knight(0, 1, WHITE), Bishop(0, 2, WHITE), Queen(0, 3, WHITE),
            King(0, 4, WHITE), Bishop(0, 5, WHITE), Knight(0, 6, WHITE), Rook(0, 7, WHITE),
        ]
        # แถว 1: เบี้ยขาว
        board[1] = [Pawn(1, c, WHITE) for c in range(column_count)]

        # แถว 6: เบี้ยดำ
        board[6] = [Pawn(6, c, BLACK) for c in range(column_count)]
        # แถว 7: ดำ (เรือ, ม้า, โคน, ราชินี, ราชา, โคน, ม้า, เรือ)
        board[7] = [
            Rook(7, 0, BLACK), Knight(7, 1, BLACK), Bishop(7, 2, BLACK), Queen(7, 3, BLACK),
            King(7, 4, BLACK), Bishop(7, 5, BLACK), Knight(7, 6, BLACK), Rook(7, 7, BLACK),
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

    def move(self, piece, row: int, col: int):
        """ย้ายตำแหน่งหมากใน Array 2 มิติเมื่อมีการเดินเกิดขึ้น"""
        old_row, old_col = piece.row, piece.col
        self.board[old_row][old_col] = 0
        self.board[row][col] = piece
        piece.row, piece.col = row, col

    def get_piece_at(self, row: int, col: int):
        """คืนค่าหมากที่ช่อง (row, col) หรือ 0 ถ้าช่องว่าง"""
        if 0 <= row < row_count and 0 <= col < column_count:
            return self.board[row][col]
        return None
