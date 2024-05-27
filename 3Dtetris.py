import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# ブロックの設定
shapes = [
    np.array([[[1, 1, 1, 1]]]),
    np.array([[[1, 1], [1, 1]]]),
    np.array([[[1, 1, 0], [0, 1, 1]]]),
    np.array([[[0, 1, 1], [1, 1, 0]]]),
    np.array([[[1, 0, 0], [1, 1, 1]]]),
    np.array([[[0, 0, 1], [1, 1, 1]]]),
    np.array([[[1, 1, 1], [0, 1, 0]]])
]
colors = ['cyan', 'magenta', 'green', 'yellow', 'orange', 'blue', 'red']

# グリッドの初期化
grid = np.zeros((10, 10, 20), dtype=int)

# ゲームの設定
score = 0
level = 1
lines_to_clear = 10
game_over = False
paused = False
speed = 1.0
high_score = 0

# パワーアップアイテムの設定
power_ups = ['slow_speed', 'clear_layer', 'extra_points']
active_power_up = None
power_up_duration = 0

# ブロックのランダムな選択と初期位置の設定
def new_block():
    global current_shape, current_color, current_pos
    idx = np.random.randint(len(shapes))
    current_shape = shapes[idx]
    current_color = idx + 1
    current_pos = [4, 4, 19]
    if not is_valid_position(current_pos):
        return False
    return True

# ブロックの回転
def rotate_block():
    global current_shape
    current_shape = np.rot90(current_shape, axes=(1, 2))

# ブロックの移動
def move_block(dx, dy, dz):
    global current_pos
    new_pos = [current_pos[0] + dx, current_pos[1] + dy, current_pos[2] + dz]
    if is_valid_position(new_pos):
        current_pos = new_pos

# 有効な位置かどうかの判定
def is_valid_position(pos):
    for z in range(current_shape.shape[0]):
        for y in range(current_shape.shape[1]):
            for x in range(current_shape.shape[2]):
                if current_shape[z, y, x] != 0:
                    if (
                        pos[0] + x < 0 or pos[0] + x >= grid.shape[0] or
                        pos[1] + y < 0 or pos[1] + y >= grid.shape[1] or
                        pos[2] - z < 0 or grid[pos[0] + x, pos[1] + y, pos[2] - z] != 0
                    ):
                        return False
    return True

# 行の消去処理
def remove_completed_lines():
    global grid, score, level, lines_to_clear, speed, active_power_up, power_up_duration
    completed_layers = 0
    for z in range(grid.shape[2]):
        if np.all(grid[:, :, z] != 0):
            completed_layers += 1
            grid[:, :, z:] = np.roll(grid[:, :, z:], -1, axis=2)
            grid[:, :, -1] = 0
    score += completed_layers ** 2
    lines_to_clear -= completed_layers
    if lines_to_clear <= 0:
        level += 1
        lines_to_clear = level * 10
        speed += 0.5
        if level % 3 == 0:
            active_power_up = np.random.choice(power_ups)
            power_up_duration = 5 * level

# パワーアップアイテムの適用
def apply_power_up():
    global grid, speed, score, active_power_up, power_up_duration
    if active_power_up == 'slow_speed':
        speed = max(1.0, speed - 1.0)
    elif active_power_up == 'clear_layer':
        grid[:, :, -1] = 0
    elif active_power_up == 'extra_points':
        score += 100
    active_power_up = None
    power_up_duration = 0

# キー入力の処理
def on_key_press(event):
    global paused
    if event.key == 'left':
        move_block(-1, 0, 0)
    elif event.key == 'right':
        move_block(1, 0, 0)
    elif event.key == 'down':
        move_block(0, 0, -1)
    elif event.key == 'up':
        move_block(0, 0, 1)
    elif event.key == 'a':
        move_block(0, -1, 0)
    elif event.key == 'd':
        move_block(0, 1, 0)
    elif event.key == 'r':
        rotate_block()
    elif event.key == 'p':
        paused = not paused
    elif event.key == 'enter' and game_over:
        restart_game()

# ゲームのリスタート
def restart_game():
    global grid, score, level, lines_to_clear, game_over, paused, speed, active_power_up, power_up_duration
    grid = np.zeros((10, 10, 20), dtype=int)
    score = 0
    level = 1
    lines_to_clear = 10
    game_over = False
    paused = False
    speed = 1.0
    active_power_up = None
    power_up_duration = 0
    new_block()

# アニメーションの更新
def update(frame):
    global game_over, score, speed, high_score, active_power_up, power_up_duration

    if not game_over and not paused:
        # ブロックの自動落下
        if frame % int(10 / speed) == 0:
            if is_valid_position([current_pos[0], current_pos[1], current_pos[2] - 1]):
                current_pos[2] -= 1
            else:
                for z in range(current_shape.shape[0]):
                    for y in range(current_shape.shape[1]):
                        for x in range(current_shape.shape[2]):
                            if current_shape[z, y, x] != 0:
                                grid[current_pos[0] + x, current_pos[1] + y, current_pos[2] - z] = current_color
                remove_completed_lines()
                if not new_block():
                    game_over = True
                    high_score = max(high_score, score)

        # パワーアップアイテムの適用
        if active_power_up is not None:
            power_up_duration -= 1
            if power_up_duration <= 0:
                apply_power_up()

    # グリッドの表示
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_zlim(0, 20)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xticks(range(11))
    ax.set_yticks(range(11))
    ax.set_zticks(range(21))

    for z in range(grid.shape[2]):
        for y in range(grid.shape[1]):
            for x in range(grid.shape[0]):
                if grid[x, y, z] != 0:
                    ax.scatter(x, y, z, c=colors[int(grid[x, y, z] - 1)], marker='s')

    for z in range(current_shape.shape[0]):
        for y in range(current_shape.shape[1]):
            for x in range(current_shape.shape[2]):
                if current_shape[z, y, x] != 0:
                    ax.scatter(current_pos[0] + x, current_pos[1] + y, current_pos[2] - z, c=colors[current_color - 1], marker='s')

    ax.set_title(f'Score: {score}  Level: {level}  High Score: {high_score}')

    if game_over:
        ax.text(5, 5, 10, 'Game Over', fontsize=20, color='red', ha='center')
        ax.text(5, 5, 9, 'Press Enter to Restart', fontsize=12, color='white', ha='center')
    elif paused:
        ax.text(5, 5, 10, 'Paused', fontsize=20, color='white', ha='center')

    if active_power_up is not None:
        ax.text(5, 5, 11, f'Power-Up: {active_power_up}', fontsize=12, color='green', ha='center')

    return ax

# メインループ
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

new_block()

fig.canvas.mpl_connect('key_press_event', on_key_press)

ani = animation.FuncAnimation(fig, update, frames=1000, repeat=False)

plt.show()
