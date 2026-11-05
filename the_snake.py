from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20
FPS = 5
INITIAL_LENGTH = 1
INITIAL_SNAKE_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

DIRECTION_MAP = {
    (UP, pygame.K_LEFT): LEFT,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_RIGHT): RIGHT,
    (LEFT, pygame.K_UP): UP,
    (LEFT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_UP): UP,
    (RIGHT, pygame.K_DOWN): DOWN,
    (UP, pygame.K_UP): UP,
    (DOWN, pygame.K_DOWN): DOWN,
    (LEFT, pygame.K_LEFT): LEFT,
    (RIGHT, pygame.K_RIGHT): RIGHT,
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(
        self,
        position=(0, 0),
        body_color=BOARD_BACKGROUND_COLOR,
    ):
        """Инициализировать позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Нарисовать объект на игровом поле."""


class Apple(GameObject):
    """Класс яблока, которое собирает змейка."""

    def __init__(self, occupied_positions=None):
        """Создать яблоко с учётом занятых клеток."""
        if occupied_positions is None:
            occupied_positions = []
        super().__init__(
            position=(0, 0),
            body_color=APPLE_COLOR,
        )
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Переместить яблоко в свободную случайную клетку."""
        if occupied_positions is None:
            occupied_positions = []
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if position not in occupied_positions:
                self.position = position
                break

    def draw(self):
        """Нарисовать яблоко."""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки и логика её движения."""

    def __init__(self):
        """Создать змейку в начальном положении."""
        super().__init__(
            position=INITIAL_SNAKE_POSITION,
            body_color=SNAKE_COLOR,
        )
        self.length = INITIAL_LENGTH
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применить следующее направление движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Переместить змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Нарисовать змейку и очистить последнюю клетку."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position,
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.get_head_position(),
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last is not None:
            last_rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                last_rect,
            )

    def reset(self):
        """Вернуть змейку в исходное состояние."""
        self.length = INITIAL_LENGTH
        self.positions = [INITIAL_SNAKE_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать события клавиатуры и закрытия окна."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            new_direction = DIRECTION_MAP.get(
                (game_object.direction, event.key)
            )
            if new_direction is not None:
                game_object.next_direction = new_direction


def main():
    """Запустить основной игровой цикл."""
    global screen

    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    pygame.display.set_caption('Змейка')

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(FPS)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
