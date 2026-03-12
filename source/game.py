import pygame
from config import WIDTH, HEIGHT, FPS, BG_COLOR, load_piece_images
from source.board import Board


class Game:
    """หน้าต่างหลักของเกม จัดการ Game Loop และรับ Input จากเมาส์"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        load_piece_images()  # โหลดรูปหมาก 12 รูป เก็บใน config.PIECE_IMAGES
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = Board()
        self.game_over = False
        self.selected_piece = None

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_mouse_click(event.pos)

    def on_mouse_click(self, pos):
        """รับพิกัดเมาส์ (x, y) - เพิ่ม logic เลือกหมากในภายหลัง"""
        pass

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.board.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)  # 60 FPS
        pygame.quit()
