# หน้าที่ของไฟล์นี้คือ จับค่าการคลิกเมาส์ (Mouse Click) เพื่อหาว่าผู้เล่นคลิกที่ช่อง (Row, Col) ไหนบนกระดาน

from config import square_size


def get_row_col_from_mouse(pos: tuple[int, int]) -> tuple[int, int]:
    """รับพิกัด pos (x, y) จากเมาส์ คืนค่า row และ col ของช่องที่คลิก"""
    x, y = pos
    col = x // square_size
    row = y // square_size
    return (row, col)