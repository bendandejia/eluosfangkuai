# 文件路径: PROJECTS/eluosfangk/tetris.py
import pygame
import random

# 游戏设置
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE
FALL_TIME = 500  # 方块下落的时间间隔（毫秒）

# 定义方块形状和颜色
SHAPES = [
    ([[1, 1, 1, 1]], (0, 255, 255)),  # I
    ([[1, 1], [1, 1]], (255, 255, 0)),  # O
    ([[0, 1, 0], [1, 1, 1]], (128, 0, 128)),  # T
    ([[1, 1, 0], [0, 1, 1]], (0, 255, 0)),  # S
    ([[0, 1, 1], [1, 1, 0]], (255, 0, 0)),  # Z
    ([[1, 0, 0], [1, 1, 1]], (255, 165, 0)),  # L
    ([[0, 0, 1], [1, 1, 1]], (0, 0, 255)),  # J
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = [[(0, 0, 0)] * COLS for _ in range(ROWS)]  # 修改为存储颜色
        self.current_shape, self.current_color = self.new_shape()
        self.current_pos = [0, COLS // 2 - 1]  # 初始位置
        self.fall_time = 0  # 下落计时器
        self.score = 0  # 初始化得分
        self.high_score = 0  # 初始化历史最高分

    def new_shape(self):
        return random.choice(SHAPES)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 设置帧率为60

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(-1)
                if event.key == pygame.K_RIGHT:
                    self.move(1)
                if event.key == pygame.K_DOWN:
                    self.drop()
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:  # 使用空格键旋转
                    self.rotate()

    def move(self, direction):
        self.current_pos[1] += direction
        if self.check_collision():
            self.current_pos[1] -= direction

    def drop(self):
        self.current_pos[0] += 1
        if self.check_collision():
            self.current_pos[0] -= 1
            self.merge_shape()
            self.clear_lines()
            self.current_shape, self.current_color = self.new_shape()  # 生成新方块
            self.current_pos = [0, COLS // 2 - 1]
            if self.check_collision():
                self.high_score = max(self.high_score, self.score)  # 更新历史最高分
                self.running = False  # 游戏结束

    def rotate(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        if self.check_collision():
            self.current_shape = [list(row) for row in zip(*self.current_shape)][::-1]  # 旋转失败，恢复

    def check_collision(self):
        for y, row in enumerate(self.current_shape):
            for x, block in enumerate(row):
                if block:
                    grid_x = self.current_pos[1] + x
                    grid_y = self.current_pos[0] + y
                    if grid_x < 0 or grid_x >= COLS or grid_y >= ROWS or (grid_y >= 0 and self.grid[grid_y][grid_x] != (0, 0, 0)):
                        return True
        return False

    def merge_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, block in enumerate(row):
                if block:
                    self.grid[self.current_pos[0] + y][self.current_pos[1] + x] = self.current_color  # 存储颜色

    def clear_lines(self):
        lines_cleared = 0
        self.grid = [row for row in self.grid if any(cell == (0, 0, 0) for cell in row)]
        lines_cleared = ROWS - len(self.grid)  # 计算消除的行数
        while len(self.grid) < ROWS:
            self.grid.insert(0, [(0, 0, 0)] * COLS)
        self.score += lines_cleared * 100  # 每消除一行得100分

    def update(self):
        self.fall_time += self.clock.get_time()  # 增加下落计时器
        if self.fall_time >= FALL_TIME:  # 检查是否达到下落时间
            self.drop()  # 让方块下落
            self.fall_time = 0  # 重置计时器

    def draw(self):
        self.screen.fill((0, 0, 0))  # 清屏
        self.draw_grid()
        self.draw_shape(self.current_shape, self.current_pos, self.current_color)
        self.draw_score()  # 绘制得分
        if not self.running:  # 如果游戏结束，显示结束提示
            self.draw_game_over()
        pygame.display.flip()

    def draw_shape(self, shape, pos, color):
        for y, row in enumerate(shape):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(self.screen, color, 
                                     (pos[1] * BLOCK_SIZE + x * BLOCK_SIZE, 
                                      pos[0] * BLOCK_SIZE + y * BLOCK_SIZE, 
                                      BLOCK_SIZE, BLOCK_SIZE))

    def draw_grid(self):
        for y in range(ROWS):
            for x in range(COLS):
                if self.grid[y][x] != (0, 0, 0):  # 只绘制非黑色的方块
                    pygame.draw.rect(self.screen, self.grid[y][x], 
                                     (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # 在屏幕上绘制得分

    def draw_game_over(self):
        font = pygame.font.Font(None, 48)
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        high_score_text = font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        current_score_text = font.render(f'Your Score: {self.score}', True, (255, 255, 255))
        
        self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        self.screen.blit(high_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
        self.screen.blit(current_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()