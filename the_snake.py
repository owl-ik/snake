from random import randint
import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона
BORDER_COLOR = (93, 216, 228)  # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)  # Цвет яблока
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")  # Заголовок окна игрового поля
clock = pygame.time.Clock()  # Настройка времени


class GameObject:

    def __init__(self, position, body_color):

        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):

    def __init__(self):

        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):

        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):

        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self):

        super().__init__((320, 240), SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def update_direction(self):
        
        if self.next_direction:
            # Избегаем движения в противоположную сторону
            if (
                self.next_direction[0] * -1,
                self.next_direction[1] * -1,
            ) != self.direction:
                self.direction = self.next_direction

    def move(self):

        x, y = self.position
        dx, dy = self.direction
        self.position = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        if self.position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, self.position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self):

        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):

        return self.positions[0]

    def reset(self):

        self.length = 1
        self.position = (320, 240)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = RIGHT


def handle_keys(snake):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT

def main():
    
    pygame.init()
    
    # Создание игровых объектов
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            
        screen.fill(BOARD_BACKGROUND_COLOR)

        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, BORDER_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, BORDER_COLOR, (0, y), (SCREEN_WIDTH, y))

        snake.draw()
        apple.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()
