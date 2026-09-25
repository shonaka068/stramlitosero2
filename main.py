# import streamlit as st
# import pygame
# import numpy as np
# from PIL import Image

# # -----------------------------
# # ゲーム設定
# # -----------------------------
# screen_width = 640
# screen_height = 640
# square_num = 8
# square_size = screen_width // square_num
# FPS = 60

# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 128, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)

# vec_table = [
#     (-1, -1), (0, -1), (1, -1),
#     (-1, 0),           (1, 0),
#     (-1, 1),  (0, 1),  (1, 1),
# ]

# # -----------------------------
# # pygame初期化
# # -----------------------------
# pygame.init()
# pygame.font.init()

# # 見えないキャンバスに描く
# screen = pygame.Surface((screen_width, screen_height))
# font = pygame.font.SysFont(None, 100, bold=False, italic=False)

# black_win_surface = font.render("Black win!!", False, BLACK, RED)
# white_win_surface = font.render("White win!!", False, WHITE, RED)
# draw_surface = font.render("Draw...", False, BLUE, RED)
# reset_surface = font.render("click reset!", False, BLACK, RED)
# skip_surface = font.render("skip", False, WHITE, RED)

# # -----------------------------
# # 初期盤面
# # -----------------------------
# def make_initial_board():
#     return [
#         [0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0],
#         [0,0,0,-1,1,0,0,0],
#         [0,0,0,1,-1,0,0,0],
#         [0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0],
#     ]

# # -----------------------------
# # 描画関数
# # -----------------------------
# def draw_grid():
#     for i in range(square_num):
#         pygame.draw.line(screen, BLACK, (0, i * square_size), (screen_width, i * square_size), 3)
#         pygame.draw.line(screen, BLACK, (i * square_size, 0), (i * square_size, screen_height), 3)

# def draw_board(board):
#     for row_index, row in enumerate(board):
#         for col_index, col in enumerate(row):
#             if col == 1:
#                 pygame.draw.circle(screen, BLACK, (col_index * square_size + 40, row_index * square_size + 40), 35)
#             elif col == -1:
#                 pygame.draw.circle(screen, WHITE, (col_index * square_size + 40, row_index * square_size + 40), 35)

# def get_validation_positions(board, player):
#     valid_position_list = []
#     for row in range(square_num):
#         for col in range(square_num):
#             if board[row][col] == 0:
#                 for vx, vy in vec_table:
#                     x = vx + col
#                     y = vy + row
#                     if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
#                         while True:
#                             x += vx
#                             y += vy
#                             if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
#                                 continue
#                             elif 0 <= x < square_num and 0 <= y < square_num and board[y][x] == player:
#                                 valid_position_list.append((col, row))
#                                 break
#                             else:
#                                 break
#     return valid_position_list

# def flip_pieces(board, col, row, player):
#     for vx, vy in vec_table:
#         flip_list = []
#         x = vx + col
#         y = vy + row
#         while 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
#             flip_list.append((x, y))
#             x += vx
#             y += vy
#             if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == player:
#                 for flip_x, flip_y in flip_list:
#                     board[flip_y][flip_x] = player

# def reset_game():
#     st.session_state.board = make_initial_board()
#     st.session_state.player = 1
#     st.session_state.game_over = False
#     st.session_state.pass_num = 0

# def render_image(board, player, game_over, pass_num):
#     # 背景
#     screen.fill(GREEN)

#     # 盤面描画
#     draw_grid()
#     draw_board(board)

#     # 置ける場所表示
#     valid_position_list = get_validation_positions(board, player)
#     for x, y in valid_position_list:
#         pygame.draw.circle(screen, YELLOW, (x * square_size + 40, y * square_size + 40), 35, 3)

#     # 数を数える
#     black_num = sum(row.count(1) for row in board)
#     white_num = sum(row.count(-1) for row in board)
#     total = black_num + white_num

#     # ゲーム終了判定
#     if total == 64:
#         game_over = True

#     # パス判定
#     if not game_over and len(valid_position_list) < 1:
#         if pass_num >= 1:
#             game_over = True
#         else:
#             pass_num += 1

#     # 勝敗表示
#     if game_over:
#         if black_num > white_num:
#             screen.blit(black_win_surface, (230, 200))
#         elif white_num > black_num:
#             screen.blit(white_win_surface, (230, 200))
#         else:
#             screen.blit(draw_surface, (230, 200))
#         screen.blit(reset_surface, (200, 400))
#     elif len(valid_position_list) < 1:
#         screen.blit(skip_surface, (230, 200))

#     frame = pygame.surfarray.array3d(screen)
#     frame = np.transpose(frame, (1, 0, 2))
#     return Image.fromarray(frame), valid_position_list, game_over, pass_num

# # -----------------------------
# # Streamlit画面
# # -----------------------------
# st.title("Streamlit版 オセロ（追加ライブラリなし）")

# if "board" not in st.session_state:
#     reset_game()

# col1, col2 = st.columns([2, 1])

# with col2:
#     st.write("### 操作")
#     st.write("1. 列と行を選ぶ")
#     st.write("2. ボタンを押す")
#     if st.button("リセット"):
#         reset_game()
#         st.rerun()

#     st.write(f"現在の番: {'黒' if st.session_state.player == 1 else '白'}")
#     black_num = sum(row.count(1) for row in st.session_state.board)
#     white_num = sum(row.count(-1) for row in st.session_state.board)
#     st.write(f"黒: {black_num}")
#     st.write(f"白: {white_num}")

#     # 置く場所を入力する
#     col_input = st.number_input("列（1〜8）", min_value=1, max_value=8, value=1, step=1)
#     row_input = st.number_input("行（1〜8）", min_value=1, max_value=8, value=1, step=1)

#     # 石を置く
#     if st.button("この場所に置く"):
#         x = int(col_input) - 1
#         y = int(row_input) - 1
#         valid_position_list = get_validation_positions(st.session_state.board, st.session_state.player)

#         if st.session_state.game_over:
#             st.warning("ゲーム終了中です。リセットしてください。")
#         elif st.session_state.board[y][x] == 0 and (x, y) in valid_position_list:
#             flip_pieces(st.session_state.board, x, y, st.session_state.player)
#             st.session_state.board[y][x] = st.session_state.player
#             st.session_state.player *= -1
#             st.session_state.pass_num = 0
#             st.rerun()
#         else:
#             st.warning("そこには置けません。")

# # 画像を表示
# game_image, valid_position_list, game_over_now, pass_num_now = render_image(
#     st.session_state.board,
#     st.session_state.player,
#     st.session_state.game_over,
#     st.session_state.pass_num
# )

# st.session_state.game_over = game_over_now
# st.session_state.pass_num = pass_num_now

# with col1:
#     st.image(game_image, caption="オセロ盤面")


import streamlit as st

# -----------------------------
# 初期盤面を作る
# -----------------------------
def make_initial_board():
    return [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0],
        [0, 0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

# -----------------------------
# 8方向
# -----------------------------
vec_table = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1),  (0, 1),  (1, 1),
]

# -----------------------------
# 置ける場所を調べる
# -----------------------------
def get_validation_positions(board, player):
    valid_position_list = []
    for row in range(8):
        for col in range(8):
            if board[row][col] != 0:
                continue
            for vx, vy in vec_table:
                x = col + vx
                y = row + vy
                if 0 <= x < 8 and 0 <= y < 8 and board[y][x] == -player:
                    while True:
                        x += vx
                        y += vy
                        if 0 <= x < 8 and 0 <= y < 8 and board[y][x] == -player:
                            continue
                        elif 0 <= x < 8 and 0 <= y < 8 and board[y][x] == player:
                            valid_position_list.append((col, row))
                            break
                        else:
                            break
    return valid_position_list

# -----------------------------
# 石をひっくり返す
# -----------------------------
def flip_pieces(board, col, row, player):
    for vx, vy in vec_table:
        flip_list = []
        x = col + vx
        y = row + vy
        while 0 <= x < 8 and 0 <= y < 8 and board[y][x] == -player:
            flip_list.append((x, y))
            x += vx
            y += vy
        if 0 <= x < 8 and 0 <= y < 8 and board[y][x] == player:
            for fx, fy in flip_list:
                board[fy][fx] = player

# -----------------------------
# 盤面を文字で表示する
# -----------------------------
def show_board(board, valid_positions):
    header = "   1 2 3 4 5 6 7 8"
    st.text(header)
    for r in range(8):
        line = f"{r+1} "
        for c in range(8):
            if board[r][c] == 1:
                cell = "●"
            elif board[r][c] == -1:
                cell = "○"
            elif (c, r) in valid_positions:
                cell = "・"
            else:
                cell = "□"
            line += f" {cell}"
        st.text(line)

# -----------------------------
# 状態を初期化
# -----------------------------
if "board" not in st.session_state:
    st.session_state.board = make_initial_board()
    st.session_state.player = 1
    st.session_state.game_over = False
    st.session_state.pass_num = 0

# -----------------------------
# タイトル
# -----------------------------
st.title("オセロ")
st.write("● = 黒, ○ = 白, ・ = 置ける場所")

# -----------------------------
# 現在の状態
# -----------------------------
board = st.session_state.board
player = st.session_state.player

valid_positions = get_validation_positions(board, player)

# 石の数
black_num = sum(row.count(1) for row in board)
white_num = sum(row.count(-1) for row in board)

# -----------------------------
# ゲーム終了判定
# -----------------------------
if black_num + white_num == 64:
    st.session_state.game_over = True

if not st.session_state.game_over and len(valid_positions) == 0:
    if st.session_state.pass_num >= 1:
        st.session_state.game_over = True
    else:
        st.session_state.pass_num += 1
        st.session_state.player *= -1
        st.rerun()

# -----------------------------
# 盤面表示
# -----------------------------
valid_positions = get_validation_positions(st.session_state.board, st.session_state.player)
show_board(st.session_state.board, valid_positions)

st.write(f"黒の数: {black_num}")
st.write(f"白の数: {white_num}")
st.write(f"現在の番: {'黒' if st.session_state.player == 1 else '白'}")

# -----------------------------
# 操作
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    row_input = st.number_input("行（1〜8）", min_value=1, max_value=8, value=1, step=1)

with col2:
    col_input = st.number_input("列（1〜8）", min_value=1, max_value=8, value=1, step=1)

with col3:
    place = st.button("石を置く")

if st.button("リセット"):
    st.session_state.board = make_initial_board()
    st.session_state.player = 1
    st.session_state.game_over = False
    st.session_state.pass_num = 0
    st.rerun()

# -----------------------------
# 石を置く処理
# -----------------------------
if place:
    if st.session_state.game_over:
        st.warning("ゲーム終了です。リセットしてください。")
    else:
        x = int(col_input) - 1
        y = int(row_input) - 1

        if (x, y) in valid_positions:
            flip_pieces(st.session_state.board, x, y, st.session_state.player)
            st.session_state.board[y][x] = st.session_state.player
            st.session_state.player *= -1
            st.session_state.pass_num = 0
            st.rerun()
        else:
            st.warning("そこには置けません。")