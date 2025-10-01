import pygame
import random
import sys
from typing import List, Tuple, Optional

# Инициализация pygame
pygame.init()

# Константы
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

# Размеры экрана
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + GRID_X_OFFSET * 2 + 200
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + GRID_Y_OFFSET * 2

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Цвета для фигур тетриса
COLORS = [
    (255, 0, 0),    # Красный - I
    (0, 255, 0),    # Зеленый - O
    (0, 0, 255),    # Синий - T
    (255, 255, 0),  # Желтый - S
    (255, 0, 255),  # Пурпурный - Z
    (0, 255, 255),  # Голубой - J
    (255, 165, 0),  # Оранжевый - L
]

# Фигуры тетриса (тетромино)
TETROMINOS = [
    # I-фигура
    [
        ['.....',
         '..#..',
         '..#..',
         '..#..',
         '..#..'],
        ['.....',
         '.....',
         '####.',
         '.....',
         '.....']
    ],
    # O-фигура
    [
        ['.....',
         '.....',
         '.##..',
         '.##..',
         '.....']
    ],
    # T-фигура
    [
        ['.....',
         '.....',
         '.#...',
         '###..',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '##...',
         '.#...']
    ],
    # S-фигура
    [
        ['.....',
         '.....',
         '.##..',
         '##...',
         '.....'],
        ['.....',
         '.#...',
         '.##..',
         '..#..',
         '.....']
    ],
    # Z-фигура
    [
        ['.....',
         '.....',
         '##...',
         '.##..',
         '.....'],
        ['.....',
         '..#..',
         '.##..',
         '.#...',
         '.....']
    ],
    # J-фигура
    [
        ['.....',
         '.#...',
         '.#...',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '#....',
         '###..',
         '.....'],
        ['.....',
         '.##..',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '..#..',
         '.....']
    ],
    # L-фигура
    [
        ['.....',
         '..#..',
         '..#..',
         '.##..',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '#....',
         '.....'],
        ['.....',
         '##...',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '..#..',
         '###..',
         '.....']
    ]
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Цветной Тетрис")
        self.clock = pygame.time.Clock()
        
        # Игровое поле
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Текущая фигура
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        
        # Позиция текущей фигуры
        self.piece_x = GRID_WIDTH // 2 - 2
        self.piece_y = 0
        
        # Состояние игры
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # миллисекунды
        
        # Шрифты
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def get_new_piece(self) -> Tuple[List[List[str]], int]:
        """Получить новую случайную фигуру"""
        piece_type = random.randint(0, len(TETROMINOS) - 1)
        rotation = random.randint(0, len(TETROMINOS[piece_type]) - 1)
        return TETROMINOS[piece_type][rotation], piece_type
    
    def draw_grid(self):
        """Отрисовка игрового поля"""
        # Фон поля
        pygame.draw.rect(self.screen, DARK_GRAY, 
                        (GRID_X_OFFSET, GRID_Y_OFFSET, 
                         GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        
        # Сетка
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY,
                           (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET),
                           (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET + GRID_HEIGHT * CELL_SIZE))
        
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY,
                           (GRID_X_OFFSET, GRID_Y_OFFSET + y * CELL_SIZE),
                           (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE, GRID_Y_OFFSET + y * CELL_SIZE))
        
        # Заполненные клетки
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != 0:
                    color = COLORS[self.grid[y][x] - 1]
                    pygame.draw.rect(self.screen, color,
                                   (GRID_X_OFFSET + x * CELL_SIZE + 1,
                                    GRID_Y_OFFSET + y * CELL_SIZE + 1,
                                    CELL_SIZE - 2, CELL_SIZE - 2))
    
    def draw_piece(self, piece: List[List[str]], piece_type: int, x: int, y: int, alpha: int = 255):
        """Отрисовка фигуры"""
        color = list(COLORS[piece_type])
        if alpha < 255:
            color.append(alpha)
        
        for row_idx, row in enumerate(piece):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    rect_x = GRID_X_OFFSET + (x + col_idx) * CELL_SIZE + 1
                    rect_y = GRID_Y_OFFSET + (y + row_idx) * CELL_SIZE + 1
                    
                    if alpha < 255:
                        # Создаем поверхность с прозрачностью для призрака
                        ghost_surface = pygame.Surface((CELL_SIZE - 2, CELL_SIZE - 2))
                        ghost_surface.set_alpha(alpha)
                        ghost_surface.fill(color[:3])
                        self.screen.blit(ghost_surface, (rect_x, rect_y))
                    else:
                        pygame.draw.rect(self.screen, color[:3],
                                       (rect_x, rect_y, CELL_SIZE - 2, CELL_SIZE - 2))
    
    def draw_next_piece(self):
        """Отрисовка следующей фигуры"""
        next_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        next_y = GRID_Y_OFFSET + 50
        
        # Заголовок
        text = self.font.render("Следующая:", True, WHITE)
        self.screen.blit(text, (next_x, next_y - 30))
        
        # Фигура
        piece, piece_type = self.next_piece
        for row_idx, row in enumerate(piece):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    rect_x = next_x + col_idx * 20
                    rect_y = next_y + row_idx * 20
                    pygame.draw.rect(self.screen, COLORS[piece_type],
                                   (rect_x, rect_y, 18, 18))
    
    def draw_info(self):
        """Отрисовка информации об игре"""
        info_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        info_y = GRID_Y_OFFSET + 200
        
        # Счет
        score_text = self.font.render(f"Счет: {self.score}", True, WHITE)
        self.screen.blit(score_text, (info_x, info_y))
        
        # Уровень
        level_text = self.font.render(f"Уровень: {self.level}", True, WHITE)
        self.screen.blit(level_text, (info_x, info_y + 40))
        
        # Линии
        lines_text = self.font.render(f"Линии: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (info_x, info_y + 80))
        
        # Управление
        controls_y = info_y + 150
        controls = [
            "Управление:",
            "← → - движение",
            "↓ - ускорение",
            "↑ - поворот",
            "Пробел - сброс"
        ]
        
        for i, control in enumerate(controls):
            color = WHITE if i == 0 else LIGHT_GRAY
            font = self.font if i == 0 else self.small_font
            text = font.render(control, True, color)
            self.screen.blit(text, (info_x, controls_y + i * 25))
    
    def is_valid_position(self, piece: List[List[str]], x: int, y: int) -> bool:
        """Проверка валидности позиции фигуры"""
        for row_idx, row in enumerate(piece):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    new_x = x + col_idx
                    new_y = y + row_idx
                    
                    # Проверка границ
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    
                    # Проверка столкновения с другими фигурами
                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return False
        
        return True
    
    def place_piece(self):
        """Размещение фигуры на поле"""
        piece, piece_type = self.current_piece
        for row_idx, row in enumerate(piece):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    x = self.piece_x + col_idx
                    y = self.piece_y + row_idx
                    if y >= 0:
                        self.grid[y][x] = piece_type + 1
    
    def clear_lines(self) -> int:
        """Очистка заполненных линий"""
        lines_to_clear = []
        
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] != 0 for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)
        
        # Удаляем заполненные линии
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # Обновляем счет
        lines_cleared = len(lines_to_clear)
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.score += lines_cleared * 100 * self.level
            
            # Увеличиваем уровень каждые 10 линий
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        return lines_cleared
    
    def get_ghost_y(self) -> int:
        """Получить Y-координату призрака фигуры"""
        ghost_y = self.piece_y
        piece, _ = self.current_piece
        
        while self.is_valid_position(piece, self.piece_x, ghost_y + 1):
            ghost_y += 1
        
        return ghost_y
    
    def rotate_piece(self):
        """Поворот фигуры"""
        piece_type = self.current_piece[1]
        current_rotation = None
        
        # Находим текущую ротацию
        for i, rotation in enumerate(TETROMINOS[piece_type]):
            if rotation == self.current_piece[0]:
                current_rotation = i
                break
        
        if current_rotation is not None:
            # Следующая ротация
            next_rotation = (current_rotation + 1) % len(TETROMINOS[piece_type])
            new_piece = TETROMINOS[piece_type][next_rotation]
            
            if self.is_valid_position(new_piece, self.piece_x, self.piece_y):
                self.current_piece = (new_piece, piece_type)
    
    def handle_input(self):
        """Обработка ввода"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.is_valid_position(self.current_piece[0], self.piece_x - 1, self.piece_y):
            self.piece_x -= 1
        
        if keys[pygame.K_RIGHT] and self.is_valid_position(self.current_piece[0], self.piece_x + 1, self.piece_y):
            self.piece_x += 1
        
        if keys[pygame.K_DOWN] and self.is_valid_position(self.current_piece[0], self.piece_x, self.piece_y + 1):
            self.piece_y += 1
            self.score += 1  # Бонус за ускорение
    
    def update(self, dt: int):
        """Обновление игры"""
        self.fall_time += dt
        
        if self.fall_time >= self.fall_speed:
            if self.is_valid_position(self.current_piece[0], self.piece_x, self.piece_y + 1):
                self.piece_y += 1
            else:
                # Фигура достигла дна или столкнулась
                self.place_piece()
                self.clear_lines()
                
                # Новая фигура
                self.current_piece = self.next_piece
                self.next_piece = self.get_new_piece()
                self.piece_x = GRID_WIDTH // 2 - 2
                self.piece_y = 0
                
                # Проверка на конец игры
                if not self.is_valid_position(self.current_piece[0], self.piece_x, self.piece_y):
                    return False  # Игра окончена
            
            self.fall_time = 0
        
        return True  # Игра продолжается
    
    def draw(self):
        """Отрисовка игры"""
        self.screen.fill(BLACK)
        
        # Игровое поле
        self.draw_grid()
        
        # Призрак фигуры
        ghost_y = self.get_ghost_y()
        self.draw_piece(self.current_piece[0], self.current_piece[1], 
                       self.piece_x, ghost_y, alpha=100)
        
        # Текущая фигура
        self.draw_piece(self.current_piece[0], self.current_piece[1], 
                       self.piece_x, self.piece_y)
        
        # Следующая фигура
        self.draw_next_piece()
        
        # Информация
        self.draw_info()
        
        pygame.display.flip()
    
    def run(self):
        """Основной игровой цикл"""
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        # Сброс игры
                        self.__init__()
            
            # Обработка непрерывного ввода
            self.handle_input()
            
            # Обновление игры
            if not self.update(dt):
                # Игра окончена
                self.screen.fill(BLACK)
                game_over_text = self.font.render("ИГРА ОКОНЧЕНА!", True, WHITE)
                score_text = self.font.render(f"Финальный счет: {self.score}", True, WHITE)
                
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
                
                self.screen.blit(game_over_text, text_rect)
                self.screen.blit(score_text, score_rect)
                
                pygame.display.flip()
                
                # Ждем нажатия клавиши для перезапуска
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.__init__()
                                waiting = False
            
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
