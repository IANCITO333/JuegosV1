import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana de juego
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

# Colores
colors = [
    (0, 0, 0),       # Black
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 165, 0),   # Orange
    (128, 0, 128),   # Purple
    (0, 255, 255)    # Cyan
]

# Configuración de la cuadrícula
grid_size = 30
grid_width = screen_width // grid_size
grid_height = screen_height // grid_size

# Piezas de Tetris (formas y colores)
shapes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # J
    [[1, 1, 1], [0, 0, 1]]   # L
]


class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(grid_width)]
                     for _ in range(grid_height)]
        self.current_shape = random.choice(shapes)
        self.current_color = random.randint(1, len(colors) - 1)
        self.shape_x = grid_width // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0

    def rotate_shape(self):
        self.current_shape = [list(row)
                              for row in zip(*self.current_shape[::-1])]

    def move(self, dx, dy):
        self.shape_x += dx
        self.shape_y += dy

    def can_move(self, dx, dy):
        new_x = self.shape_x + dx
        new_y = self.shape_y + dy
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    if (x + new_x < 0 or x + new_x >= grid_width or
                        y + new_y >= grid_height or
                            self.grid[y + new_y][x + new_x]):
                        return False
        return True

    def place_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.shape_y + y][self.shape_x +
                                                x] = self.current_color
        self.clear_lines()
        self.current_shape = random.choice(shapes)
        self.current_color = random.randint(1, len(colors) - 1)
        self.shape_x = grid_width // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        while len(new_grid) < grid_height:
            new_grid.insert(0, [0 for _ in range(grid_width)])
        self.grid = new_grid

    def draw_grid(self):
        for y in range(grid_height):
            for x in range(grid_width):
                color = colors[self.grid[y][x]]
                pygame.draw.rect(screen, color, (x * grid_size,
                                 y * grid_size, grid_size, grid_size))

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    color = colors[self.current_color]
                    pygame.draw.rect(screen, color, ((
                        self.shape_x + x) * grid_size, (self.shape_y + y) * grid_size, grid_size, grid_size))

# Loop principal


def main():
    clock = pygame.time.Clock()
    game = Tetris()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.can_move(-1, 0):
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT and game.can_move(1, 0):
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN and game.can_move(0, 1):
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_shape()

        if not game.can_move(0, 1):
            game.place_shape()
        else:
            game.move(0, 1)

        screen.fill((0, 0, 0))
        game.draw_grid()
        game.draw_shape()
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
