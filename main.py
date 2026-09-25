import streamlit as st
import pygame
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# -----------------------------
# ゲーム設定
# -----------------------------
screen_width = 640
screen_height = 640
square_num = 8
square_size = screen_width // square_num
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

vec_table = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1),  (0, 1),  (1, 1),
]

# -----------------------------
# pygame初期化
# -----------------------------
pygame.init()
pygame.font.init()

# Streamlit用に、見えないキャンバスへ描く
screen = pygame.Surface((screen_width, screen_height))

font = pygame.font.SysFont(None, 100, bold=False, italic=False)

black_win_surface = font.render("Black win!!", False, BLACK, RED)
white_win_surface = font.render("White win!!", False, WHITE, RED)
draw_surface = font.render("Draw...", False, BLUE, RED)
reset_surface = font.render("click to reset!", False, BLACK, RED)
skip_surface = font.render("skip", False, WHITE, RED)

clock = pygame.time.Clock()

# -----------------------------
# 初期盤面を返す関数
# -----------------------------
def make_initial_board():
    return [
        [0, 0, 0, 0, 0, 0, 0, 0],   # 1
        [0, 0, 0, 0, 0, 0, 0, 0],   # 2
        [0, 0, 0, 0, 0, 0, 0, 0],   # 3
        [0, 0, 0, -1, 1, 0, 0, 0],  # 4
        [0, 0, 0, 1, -1, 0, 0, 0],  # 5
        [0, 0, 0, 0, 0, 0, 0, 0],   # 6
        [0, 0, 0, 0, 0, 0, 0, 0],   # 7
        [0, 0, 0, 0, 0, 0, 0, 0],   # 8
    ]

# -----------------------------
# 描画関数
# -----------------------------
def draw_grid():
    for i in range(square_num):
        pygame.draw.line(screen, BLACK, (0, i * square_size), (screen_width, i * square_size), 3)
        pygame.draw.line(screen, BLACK, (i * square_size, 0), (i * square_size, screen_height), 3)

def draw_board(board):
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if col == 1:
                pygame.draw.circle(screen, BLACK, (col_index * square_size + 40, row_index * square_size + 40), 35)
            elif col == -1:
                pygame.draw.circle(screen, WHITE, (col_index * square_size + 40, row_index * square_size + 40), 35)

def get_validation_positions(board, player):
    valid_position_list = []
    for row in range(square_num):
        for col in range(square_num):
            if board[row][col] == 0:
                for vx, vy in vec_table:
                    x = vx + col
                    y = vy + row
                    if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
                        while True:
                            x += vx
                            y += vy
                            if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
                                continue
                            elif 0 <= x < square_num and 0 <= y < square_num and board[y][x] == player:
                                valid_position_list.append((col, row))
                                break
                            else:
                                break
    return valid_position_list

def flip_pieces(board, col, row, player):
    for vx, vy in vec_table:
        flip_list = []
        x = vx + col
        y = vy + row
        while 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
            flip_list.append((x, y))
            x += vx
            y += vy
            if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == player:
                for flip_x, flip_y in flip_list:
                    board[flip_y][flip_x] = player

def reset_game():
    st.session_state.board = make_initial_board()
    st.session_state.player = 1
    st.session_state.game_over = False
    st.session_state.pass_num = 0
    st.session_state.click_count = 0

def render_game_image():
    # 背景
    screen.fill(GREEN)

    # 盤面描画
    draw_grid()
    draw_board(st.session_state.board)

    # 置ける場所を表示
    valid_position_list = get_validation_positions(st.session_state.board, st.session_state.player)
    for x, y in valid_position_list:
        pygame.draw.circle(screen, YELLOW, (x * square_size + 40, y * square_size + 40), 35, 3)

    # 石の数を数える
    black_num = sum(row.count(1) for row in st.session_state.board)
    white_num = sum(row.count(-1) for row in st.session_state.board)
    total = black_num + white_num

    # ゲーム終了判定
    if total == 64:
        st.session_state.game_over = True
    else:
        if len(valid_position_list) < 1:
            if st.session_state.pass_num == 2:
                st.session_state.game_over = True
            else:
                st.session_state.player *= -1
                st.session_state.pass_num += 1

    # 勝敗表示
    if st.session_state.game_over:
        if black_num > white_num:
            screen.blit(black_win_surface, (230, 200))
        elif white_num > black_num:
            screen.blit(white_win_surface, (230, 200))
        else:
            screen.blit(draw_surface, (230, 200))
        screen.blit(reset_surface, (180, 400))
    elif len(valid_position_list) < 1:
        screen.blit(skip_surface, (230, 200))

    # pygame画面をStreamlit表示用画像へ変換
    frame = pygame.surfarray.array3d(screen)
    frame = np.transpose(frame, (1, 0, 2))
    return Image.fromarray(frame), valid_position_list

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Streamlit版 オセロ")

if "board" not in st.session_state:
    reset_game()

col1, col2 = st.columns([2, 1])

with col2:
    st.write("### 操作")
    if st.button("リセット"):
        reset_game()
        st.rerun()

    st.write(f"現在の番: {'黒' if st.session_state.player == 1 else '白'}")
    black_num = sum(row.count(1) for row in st.session_state.board)
    white_num = sum(row.count(-1) for row in st.session_state.board)
    st.write(f"黒: {black_num}")
    st.write(f"白: {white_num}")

# 画像を作る
game_image, valid_position_list = render_game_image()

with col1:
    # 画像を表示して、その上でクリック位置を取る
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=1,
        stroke_color="#000000",
        background_image=game_image,
        update_streamlit=True,
        height=screen_height,
        width=screen_width,
        drawing_mode="point",
        key="canvas",
    )

# クリック座標を取得して石を置く
if canvas_result.json_data is not None and not st.session_state.game_over:
    objects = canvas_result.json_data["objects"]
    if len(objects) > st.session_state.click_count:
        last = objects[-1]
        click_x = int(last["left"])
        click_y = int(last["top"])

        x = click_x // square_size
        y = click_y // square_size

        if 0 <= x < square_num and 0 <= y < square_num:
            if st.session_state.board[y][x] == 0 and (x, y) in valid_position_list:
                flip_pieces(st.session_state.board, x, y, st.session_state.player)
                st.session_state.board[y][x] = st.session_state.player
                st.session_state.player *= -1
                st.session_state.pass_num = 0

        st.session_state.click_count = len(objects)
        st.rerun()