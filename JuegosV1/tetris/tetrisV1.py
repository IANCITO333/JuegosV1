import pygame
import random
import pickle
import os

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)]
                     for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.high_score = self.load_high_score()

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape)]
        return {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def draw_piece(self, piece):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece['color'],
                                     ((piece['x'] + x) * BLOCK_SIZE, (piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def move(self, dx, dy):
        new_x = self.current_piece['x'] + dx
        new_y = self.current_piece['y'] + dy
        if self.valid_move(self.current_piece['shape'], new_x, new_y):
            self.current_piece['x'] = new_x
            self.current_piece['y'] = new_y
            return True
        return False

    def rotate(self):
        new_shape = list(zip(*self.current_piece['shape'][::-1]))
        if self.valid_move(new_shape, self.current_piece['x'], self.current_piece['y']):
            self.current_piece['shape'] = new_shape

    def valid_move(self, shape, x, y):
        for y_offset, row in enumerate(shape):
            for x_offset, cell in enumerate(row):
                if cell:
                    if (x + x_offset < 0 or x + x_offset >= GRID_WIDTH or
                        y + y_offset >= GRID_HEIGHT or
                            (y + y_offset >= 0 and self.grid[y + y_offset][x + x_offset])):
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] +
                              y][self.current_piece['x'] + x] = self.current_piece['color']
        self.clear_lines()
        self.current_piece = self.new_piece()
        if not self.valid_move(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared ** 2 * 100

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = font.render(
            f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (BLOCK_SIZE * (GRID_WIDTH + 1), 20))
        self.screen.blit(high_score_text, (BLOCK_SIZE * (GRID_WIDTH + 1), 60))

    def load_high_score(self):
        if os.path.exists('high_score.pkl'):
            with open('high_score.pkl', 'rb') as f:
                return pickle.load(f)
        return 0

    def save_high_score(self):
        with open('high_score.pkl', 'wb') as f:
            pickle.dump(max(self.score, self.high_score), f)

    def run(self):
        fall_time = 0
        fall_speed = 0.5
        while not self.game_over:
            fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate()

            if fall_time / 1000 > fall_speed:
                if not self.move(0, 1):
                    self.lock_piece()
                fall_time = 0

            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_score()
            pygame.display.flip()

        self.save_high_score()
        pygame.quit()


if __name__ == "__main__":
    game = Tetris()
    game.run()
