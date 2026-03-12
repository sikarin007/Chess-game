import random
import pygame
from config import (
    WIDTH, HEIGHT, FPS, BG_COLOR, load_piece_images, row_count, column_count,
    CHECKMATE_SOUND,
)
from source.board import Board
from source.systems.control import get_row_col_from_mouse
from source.systems.ai import ChessAI


class Game:
    """หน้าต่างหลักของเกม จัดการ Game Loop และรับ Input"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        load_piece_images()
        pygame.display.set_caption("Chess Game VS AI")
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = Board()
        self.game_over = False
        self.game_over_message = ""

        # --- สถานะของเกม ---
        self.turn = "white"  # ให้ผู้เล่น (ขาว) เริ่มก่อน
        self.selected_piece = None
        self.valid_moves = []

        # --- สร้าง AI ---
        self.ai = ChessAI(self.board)
        self.ai_timer_start = 0
        self.ai_delay = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.game_over and self.turn == "white":
                    self.on_mouse_click(event.pos)

    def on_mouse_click(self, pos):
        """จัดการเมื่อผู้เล่นคลิกเมาส์ (เลือกหมาก / เดินหมาก)"""
        row, col = get_row_col_from_mouse(pos)
        if not (0 <= row < row_count and 0 <= col < column_count):
            return

        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.board.move(self.selected_piece, row, col)
                self.turn = "black"
                self.ai_timer_start = pygame.time.get_ticks()
                self.ai_delay = random.randint(1000, 3000)
                self.selected_piece = None
                self.valid_moves = []
                if self.board.is_checkmate(self.turn):
                    self.game_over = True
                    self.game_over_message = "Checkmate!"
                    if CHECKMATE_SOUND:
                        CHECKMATE_SOUND.play()
                elif self.board.is_stalemate(self.turn):
                    self.game_over = True
                    self.game_over_message = "Stalemate!"
            else:
                self.select_new_piece(row, col)
        else:
            self.select_new_piece(row, col)

    def select_new_piece(self, row, col):
        """ฟังก์ชันช่วยสำหรับเลือกหมากตัวใหม่"""
        piece = self.board.get_piece_at(row, col)
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.board.get_legal_moves(piece)
        else:
            self.selected_piece = None
            self.valid_moves = []

    def update(self):
        if self.turn == "black" and not self.game_over:
            if pygame.time.get_ticks() - self.ai_timer_start >= self.ai_delay:
                self.ai_move()

    def ai_move(self):
        """สั่งให้ AI คำนวณตาเดินและขยับหมาก"""
        best_move = self.ai.get_best_move()
        if best_move:
            piece, row, col = best_move
            self.board.move(piece, row, col)
            self.turn = "white"
            if self.board.is_checkmate(self.turn):
                self.game_over = True
                self.game_over_message = "Checkmate!"
                if CHECKMATE_SOUND:
                    CHECKMATE_SOUND.play()
            elif self.board.is_stalemate(self.turn):
                self.game_over = True
                self.game_over_message = "Stalemate!"
        else:
            self.game_over = True
            self.game_over_message = "Checkmate!"
            if CHECKMATE_SOUND:
                CHECKMATE_SOUND.play()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.board.draw(self.screen)
        self.board.draw_valid_moves(self.screen, self.valid_moves)
        if self.game_over and self.game_over_message:
            font = pygame.font.Font(None, 72)
            text = font.render(self.game_over_message, True, (255, 255, 255))
            rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text, rect)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
