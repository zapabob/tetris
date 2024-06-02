import pygame
import random
import os
import sys

# ゲームの設定
pygame.init()
screen = pygame.display.set_mode((300, 600))
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 50)
grid = [[0] * 10 for _ in range(20)]
score = 0
frame = 0

# ブロックの設定
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]]
]
colors = [(0, 255, 255), (255, 0, 255), (0, 255, 0), (255, 255, 0), (255, 165, 0), (0, 0, 255), (255, 0, 0)]
current_shape = None
current_color = None
current_pos = (3, 0)

def new_block():
    global current_shape, current_color, current_pos
    idx = random.randint(0, len(shapes) - 1)
    current_shape = shapes[idx]
    current_color = colors[idx]
    current_pos = (3, 0)

# 初期ブロックの生成
new_block()

# ブロックの移動と回転の処理
def move_block(dx, dy):
    global current_pos
    new_pos = (current_pos[0] + dx, current_pos[1] + dy)
    if is_valid_position(new_pos):
        current_pos = new_pos

def rotate_block():
    global current_shape
    new_shape = list(zip(*reversed(current_shape)))
    if is_valid_position(current_pos, new_shape):
        current_shape = new_shape

def is_valid_position(pos, shape=None):
    if shape is None:
        shape = current_shape
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and (x + pos[0] < 0 or x + pos[0] >= 10 or y + pos[1] >= 20 or grid[y + pos[1]][x + pos[0]]):
                return False
    return True

# 行の消去処理
def remove_completed_lines():
    global grid, score
    completed_lines = 0
    for y in range(19, -1, -1):
        if all(grid[y]):
            completed_lines += 1
            for y2 in range(y, 0, -1):
                grid[y2] = grid[y2 - 1]
            grid[0] = [0] * 10
    if completed_lines > 0:
        score += completed_lines ** 2
        os.system('echo -n "\a"')

# ゲームオーバー処理
def game_over():
    os.system('echo -n "\a"')
    os.system('echo -n "\a"')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(150, 300))
        screen.blit(text, text_rect)
        pygame.display.update()
        clock.tick(10)

# ゲームループ
while True:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_block(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_block(1, 0)
            elif event.key == pygame.K_DOWN:
                move_block(0, 1)
            elif event.key == pygame.K_UP:
                rotate_block()

    # ブロックの自動落下
    if frame % 30 == 0:
        if not is_valid_position((current_pos[0], current_pos[1] + 1)):
            for y, row in enumerate(current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[y + current_pos[1]][x + current_pos[0]] = current_color
            remove_completed_lines()
            new_block()
            if not is_valid_position(current_pos):
                game_over()
                grid = [[0] * 10 for _ in range(20)]
                score = 0
                frame = 0
        else:
            current_pos = (current_pos[0], current_pos[1] + 1)

    # ゲーム画面の更新
    screen.fill((0, 0, 0))
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * 30, y * 30, 30, 30))
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_color, ((x + current_pos[0]) * 30, (y + current_pos[1]) * 30, 30, 30))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 300, 600), 2)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (310, 10))
    pygame.display.update()

    frame += 1
    clock.tick(10)
