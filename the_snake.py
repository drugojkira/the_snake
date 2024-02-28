from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()

HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self, position=None, body_color=None):
        if position is None:
            position = (HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT)
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position=None):
        """Рисует ячейку на заданной поверхности"""
        if position is None:
            position = self.position
        cell_rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, cell_rect)
        pygame.draw.rect(screen, BORDER_COLOR, cell_rect, 1)

    def draw(self):
        """Заготовка метода для отрисовки"""
        pass


class Apple(GameObject):
    """Яблоко и действия с ним"""

    def __init__(self, occupied_positions=[], body_color=APPLE_COLOR):
        """Задаёт цвет яблока"""
        super().__init__(position=(0, 0), body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайное положение"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Змейка и её поведение."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует начальное состояние"""
        super().__init__(body_color=body_color)
        self.reset()

    def update_direction(self, direction):
        """Обновляет направление движения"""
        if direction in [UP, DOWN, LEFT, RIGHT]:
            self.direction = direction

    def move(self):
        """Обновляет позицию змейки"""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_head_x, new_head_y)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()
        return new_head_position

    def draw(self, surface):
        """Отрисовывает змейку на экране"""
        if len(self.positions) > 0:
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            self.draw_cell(head_rect)
    
        if len(self.positions) > 1:
            for position in self.positions[1:-1]:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                self.draw_cell(rect)

            tail_rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
            if pygame.time.get_ticks() % 2 == 0:
                self.draw_cell(tail_rect)

    def get_head_position(self):
        """Возвращает позицию головы"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        show_result(self.length - 1)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def get_speed(current_speed):
    """Возвращает соответствующую скорость."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        return 10
    elif keys[pygame.K_BACKSPACE]:
        return 15
    elif keys[pygame.K_TAB]:
        return 20
    else:
        return current_speed


def main():
    """Основной цикл игры"""
    snake = Snake()
    apple = Apple(snake.positions)
    record_length = 1
    speed = SPEED

    while True:
        clock.tick(speed)
        speed = get_speed(speed)

        handle_keys(snake)
        new_head_position = snake.move()
        if new_head_position in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            record_length = max(record_length, snake.length)
            apple.randomize_position(snake.positions)
            show_result(record_length)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw()

        info = ("SPACE - x10, BACKSPACE - x15, TAB - x20 для скорости."
                f"Record: {record_length}")
        pygame.display.set_caption(info)
        pygame.display.update()  # Обновление экрана


def show_result(apples_eaten):
    """Выводит результат игры"""
    print(f"Вы съели {apples_eaten} яблок!")


if __name__ == "__main__":
    main()
