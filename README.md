# Pygame Chess (เกมหมากรุกสากล ปะทะ AI)

## ชื่อทีมและสมาชิก

| ลำดับ | รหัสนักศึกษา | ชื่อ-นามสกุล |
|------|---------------|---------------|
| 1 | 68114540616 | ศิขรินทร์ ภูติโส |
| 2 | 68114540533 | นายฤทธิชัย โลมะกาล |

**ชื่อทีม:** chess เล่นดูครับสนุด

---

## รายละเอียดโปรเจกต์ (Description)

เป็นเกมหมากรุกสากลที่เขียนด้วย Pygame ผู้เล่นเล่นฝั่งขาว (White) ปะทะกับ AI ฝั่งดำ (Black)

**คุณสมบัติหลัก:**
- ระบบประมวลผลการเดินตามกฎหมากรุกสากล
- รองรับ Castling (เข้าป้อม)
- ระบบ Check และ Checkmate
- เสียงประกอบ (เดินหมาก, กินหมาก, รุก, รุกฆาต, เข้าป้อม)
- AI เบื้องต้นใช้ Minimax + Alpha-Beta Pruning

---

## วิธีการติดตั้ง (Installation)

### 1. Clone โปรเจกต์

```bash
git clone https://github.com/sikarin007/Chess-game.git
cd pygame_chess
```

### 2. สร้าง Virtual Environment (แนะนำ)

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 3. ติดตั้ง Library

**วิธีที่ 1: ใช้ requirements.txt**
```bash
pip install -r requirements.txt
```

**วิธีที่ 2: ใช้ pyproject.toml**
```bash
pip install .
```

---

## วิธีการใช้งาน (Usage)

รันเกมด้วยคำสั่ง:

```bash
python main.py
```

---

## การควบคุม (Controls)

- **เมาส์คลิกซ้าย** – คลิกที่หมากของตนเองเพื่อเลือก จากนั้นคลิกที่ช่องเป้าหมายเพื่อเดิน
- วงกลมสีเทาโปร่งใสจะแสดงช่องที่เดินได้
- กรอบสีแดงจะแสดงเมื่อ King โดนรุก (Check)
