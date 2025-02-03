import pygame  # Импортируем библиотеку Pygame для создания игр
import random  # Импортируем модуль random для генерации случайных чисел

# Инициализация Pygame
pygame.init()

# Определяем размеры окна и сетки
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Определяем цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Циан
    (255, 165, 0),  # Оранжевый
    (0, 0, 255),  # Синий
    (255, 0, 0),  # Красный
    (128, 0, 128),  # Фиолетовый
    (0, 255, 0),  # Зеленый
    (255, 255, 0)  # Желтый
]

# Формы блоков Тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]  # J
]


class Tetris:
    def __init__(self):
        # Создаем сетку для игры (двумерный массив), заполненный нулями
        self.grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.position = [5, 0]  # Начальная позиция
        self.score = 0  # Инициализируем счет игрока
        self.paused = False  # Флаг паузы

    def new_piece(self):  # Метод для генерации нового блока Тетриса
        shape = random.choice(SHAPES)  # Выбираем случайную форму блока из списка SHAPES
        color = COLORS[SHAPES.index(shape)]  # Получаем цвет блока по индексу формы
        return {'shape': shape, 'color': color}  # Возвращаем словарь с формой и цветом блока

    def rotate_piece(self):
        self.current_piece['shape'] = [list(row) for row in zip(*self.current_piece['shape'][::-1])]  # Поворачиваем блок на 90 градусов по часовой стрелке

    def check_collision(self):  # Метод для проверки касаний с другими блоками или границами экрана
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    if (x + self.position[0] < 0 or
                            x + self.position[0] >= len(self.grid[0]) or
                            y + self.position[1] >= len(self.grid) or
                            self.grid[y + self.position[1]][x + self.position[0]]):
                        return True
        return False

    def merge_piece(self):  # Метод для слияния текущего блока с сеткой
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.position[1]][x + self.position[0]] = self.current_piece['color']

    def remove_lines(self):  # Метод для удаления заполненных линий из сетки
        lines_to_remove = []  # Список для хранения индексов заполненных линий
        for i, row in enumerate(self.grid):
            if all(row):
                lines_to_remove.append(i)
        for i in lines_to_remove:
            del self.grid[i]
            # Удаляем заполненные строки из сетки
            self.grid.insert(0, [0 for _ in range(len(self.grid[0]))])
        self.score += len(lines_to_remove)  # Увеличиваем счет на количество удаленных линий


def draw_grid(screen, grid):  # Функция для отрисовки сетки игры
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            color = grid[y][x]
            if color:
                # Рисуем прямоугольник
                pygame.draw.rect(screen, color,
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))


def draw_score(screen, score):  # Функция для отображения текущего счета игрока
    font = pygame.font.Font(None, 36)  # Создаем шрифт
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))  # Отображаем текст на экране


def draw_start_screen(screen):  # Функция для отрисовки стартового экрана
    font = pygame.font.Font(None, 48)
    text = font.render('Тетрис', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))

    font = pygame.font.Font(None, 36)
    text = font.render('Начать', True, WHITE)
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50)
    pygame.draw.rect(screen, (0, 128, 0), button_rect)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 15))

    return button_rect


def draw_pause_button(screen):  # Функция для отрисовки кнопки паузы
    font = pygame.font.Font(None, 36)
    text = font.render('Пауза', True, WHITE)
    button_rect = pygame.Rect(SCREEN_WIDTH - 100, 10, 80, 30)
    pygame.draw.rect(screen, (128, 0, 0), button_rect)
    screen.blit(text, (SCREEN_WIDTH - 90, 15))

    return button_rect


def main():  # Основная функция игры
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Создаем окно игры
    pygame.display.set_caption('Tetris')  # Устанавливаем заголовок окна

    clock = pygame.time.Clock()  # Создаем объект для управления частотой кадров
    tetris = Tetris()  # Инициализируем игру Тетрис

    running = True
    game_started = False
    while running:
        screen.fill(BLACK)  # Заполняем экран черным цветом

        if not game_started:
            start_button = draw_start_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
                    if start_button.collidepoint(event.pos):  # Если нажата кнопка "Начать"
                        game_started = True
        else:
            pause_button = draw_pause_button(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                    running = False
                if event.type == pygame.KEYDOWN:  # Если нажата клавиша
                    if event.key == pygame.K_LEFT:
                        tetris.position[0] -= 1
                        if tetris.check_collision():
                            tetris.position[0] += 1
                    elif event.key == pygame.K_RIGHT:
                        tetris.position[0] += 1
                        if tetris.check_collision():
                            tetris.position[0] -= 1
                    elif event.key == pygame.K_DOWN:
                        tetris.position[1] += 1
                        if tetris.check_collision():
                            tetris.position[1] -= 1
                    elif event.key == pygame.K_UP:
                        tetris.rotate_piece()
                        if tetris.check_collision():
                            tetris.rotate_piece()  # Возврат назад если коллизия
                if event.type == pygame.MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
                    if pause_button.collidepoint(event.pos):  # Если нажата кнопка "Пауза"
                        tetris.paused = not tetris.paused

            if not tetris.paused:
                # Обработка падения блока
                tetris.position[1] += 1
                if tetris.check_collision():
                    tetris.position[1] -= 1
                    tetris.merge_piece()
                    tetris.remove_lines()  # Удаляем заполненные линии из сетки
                    tetris.current_piece = tetris.next_piece  # Переключаем текущий блок на следующий
                    tetris.next_piece = tetris.new_piece()  # Генерируем новый следующий блок
                    tetris.position = [5, 0]
                    if tetris.check_collision():
                        print("Game Over")  # Выводим сообщение о конце игры
                        running = False  # Выход из основного цикла

            draw_grid(screen, tetris.grid)

            # Отрисовка текущего блока
            for y in range(len(tetris.current_piece['shape'])):
                for x in range(len(tetris.current_piece['shape'][y])):
                    if tetris.current_piece['shape'][y][x]:
                        pygame.draw.rect(screen,
                                         tetris.current_piece['color'],  # Рисуем блок текущего цвета
                                         ((x + tetris.position[0]) * BLOCK_SIZE,
                                          (y + tetris.position[1]) * BLOCK_SIZE,
                                          BLOCK_SIZE - 1,
                                          BLOCK_SIZE - 1))  # Параметры: координаты и размер блока

            draw_score(screen, tetris.score)  # Отрисовываем текущий счет игрока

        pygame.display.flip()  # Обновляем экран
        clock.tick(5)  # Ограничиваем частоту кадров до 5 FPS

    pygame.quit()


if __name__ == "__main__":
    main()