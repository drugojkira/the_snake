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

# тест не дает это использовть (снять коммент):
# eat_sound = pygame.mixer.Sound("eat_sound.wav")

# Настройка времени:
clock = pygame.time.Clock()

HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self, position=(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT),
                 body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, surface):
        """Рисует ячейку на заданной поверхности"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def draw(self):
        """Заготовка метода для отрисовки"""
        pass


class Apple(GameObject):
    """Яблоко и действия с ним"""

    def __init__(self, snake_positions=[], body_color=APPLE_COLOR):
        """Задаёт цвет яблока"""
        super().__init__(position=(0, 0), body_color=body_color)
        self.occupied_positions = snake_positions
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение"""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if position not in self.occupied_positions:
                self.position = position
                break

    def draw(self, surface):
        """Отрисовывает яблоко"""
        self.draw_cell(surface)


class Snake(GameObject):
    """Змейка и её поведение."""

    def __init__(self):
        """Инициализирует начальное состояние"""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.next_direction = None
        self.length = 1

    def update_direction(self, direction):
        """Обновляет направление движения"""
        if direction in [UP, DOWN, LEFT, RIGHT]:
            self.next_direction = direction

    def move(self):
        """Обновляет позицию змейки"""
        head_position = self.get_head_position()
        dx, dy = self.direction
        new_head_position = (
            (head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head_position)
        if new_head_position in self.positions[2:]:
            self.reset()
            return True
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_circle = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(head_circle, self.body_color,
                           (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 2)
        surface.blit(head_circle, self.positions[0])

    def get_head_position(self):
        """Возвращает позицию головы"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку"""
        if hasattr(self, 'length'):
            show_result(self.length - 1)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


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
            elif event.key == pygame.K_UP and snake.direction != DOWN:
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
        if snake.next_direction:
            snake.direction, snake.next_direction = snake.next_direction, None

        self_collision = snake.move()
        if self_collision:
            continue

        if snake.get_head_position() == apple.position:
            snake.length += 1
            record_length = max(record_length, snake.length)
            # eat_sound.play()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        info = ("SPACE - x10, BACKSPACE - x15, TAB - x20 для скорости."
                f"Record: {record_length}")
        pygame.display.set_caption(info)
        pygame.display.update()


def show_result(apples_eaten):
    """Выводит результат игры"""
    print(f"Вы съели {apples_eaten} яблок!")


if __name__ == "__main__":
    main()
