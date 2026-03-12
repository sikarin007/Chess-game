# chess game config
import pygame

WIDTH, HEIGHT = 800, 800  # ขนาดหน้าจอ 800x800
FPS = 60

# Square Size
# จำนวนแถว/คอลัมน์ (8x8)
row_count = 8
column_count = 8
square_size = WIDTH // column_count

# สีตารางหมากรุก (Light square / Dark square)
BOARD_LIGHT = (240, 217, 181)  # สีอ่อน (ครีม/เบจ)
BOARD_DARK = (181, 136, 99)   # สีเข้ม (น้ำตาล)

# สีพื้นหลัง
BG_COLOR = (0, 0, 0)

# สีหมาก (ตัวหมากขาว/ดำ และเส้นขอบ)
PIECE_WHITE = (255, 255, 255)
PIECE_WHITE_BORDER = (200, 200, 200)
PIECE_BLACK = (50, 50, 50)
PIECE_BLACK_BORDER = (100, 100, 100)

# โหลดรูปหมากรุก 12 รูป (ต้องเรียกหลัง pygame.init() แล้ว)
PIECE_IMAGES: dict = {}  # เก็บรูปหมาก - key เช่น "white_pawn", "black_king"


def load_piece_images() -> dict:
    """โหลดรูปจาก assets/game/white และ black แล้ว scale ให้ขนาดเท่ากับ square_size"""
    global PIECE_IMAGES
    pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    colors = ["white", "black"]
    size = (square_size, square_size)
    for color in colors:
        for piece in pieces:
            key = f"{color}_{piece}"
            path = f"assets/game/{color}/{color}_{piece}.png"
            img = pygame.image.load(path).convert_alpha()
            PIECE_IMAGES[key] = pygame.transform.scale(img, size)
    return PIECE_IMAGES
