#draw.py
import pygame

# 보드 색상
BOARD_COLOR = (255, 176, 68)
LINE_COLOR = (0, 0, 0)

# 돌 색상
BLACK_STONE_COLOR = (0, 0, 0)
WHITE_STONE_COLOR = (255, 255, 255)

# 보드 크기 및 돌 반지름
BOARD_SIZE = 15
BOARD_WIDTH = 600
LINE_WIDTH = 2
CELL_SIZE = BOARD_WIDTH // BOARD_SIZE
STONE_RADIUS = CELL_SIZE // 2 - 5

# 게임 보드 초기화
def init_board(board_size):
    global BOARD_SIZE, BOARD_WIDTH, CELL_SIZE
    BOARD_SIZE = board_size
    BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
    pygame.display.set_caption("오목")
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
    screen.fill(BOARD_COLOR)
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (BOARD_WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_WIDTH), LINE_WIDTH)
    pygame.display.update()

# 마우스 클릭 위치를 보드의 행과 열로 변환
def get_clicked_position(x, y):
    col = (x - CELL_SIZE) // CELL_SIZE  # 격자 시작 위치에서의 행과 열로 변환
    row = (y - CELL_SIZE) // CELL_SIZE
    remainder_x = (x - CELL_SIZE) % CELL_SIZE  # 격자 내에서의 남은 x 좌표 계산
    remainder_y = (y - CELL_SIZE) % CELL_SIZE  # 격자 내에서의 남은 y 좌표 계산
    if remainder_x >= CELL_SIZE // 2:
        col += 1
    if remainder_y >= CELL_SIZE // 2:
        row += 1
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return row, col
    return None, None

# 보드에 돌 그리기
def draw_stone(row, col, player):
    screen = pygame.display.get_surface()
    x = (col + 1) * CELL_SIZE  # 격자 교차점 위치에 돌을 그리기 위해 +1 조정
    y = (row + 1) * CELL_SIZE
    color = BLACK_STONE_COLOR if player == 1 else WHITE_STONE_COLOR
    pygame.draw.circle(screen, color, (x, y), STONE_RADIUS)
    pygame.display.update()