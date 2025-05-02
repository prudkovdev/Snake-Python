import pygame
import random

# константы
SCREEN_SIZE = 500
GRID_SIZE = 25
PIXEL_SIZE = SCREEN_SIZE / GRID_SIZE
FPS = 10

# инициализация pygame
pygame.init()
pygame.mixer.init()  # Инициализация звуковой подсистемы

class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = PIXEL_SIZE
        self.color = color

class Snake:
    def __init__(self):
        self.color = (0, 255, 0)
        self.eat_sound = pygame.mixer.Sound("eat.wav")
        self.pixels = []
        self.pixels.append(Pixel(PIXEL_SIZE * 5, PIXEL_SIZE * 5, self.color))
        self.pixels.append(Pixel(PIXEL_SIZE * 5, PIXEL_SIZE * 6, self.color))
        self.current_direction = "up"
        self.future_direction = "up"
        self.eating = False
    
    def draw(self, screen):
        for pixel in self.pixels:
            pygame.draw.rect(screen, self.color, pygame.Rect(pixel.x, pixel.y, pixel.size, pixel.size))

    def update(self):
        temp = self.pixels.copy()

        for i in range(len(self.pixels), 1, -1):
            if self.eating:
                self.pixels.append(Pixel(self.pixels[i-1].x, self.pixels[i-1].y, self.color))
                self.eating = False
            else:
                self.pixels[i-1].x = temp[i-2].x
                self.pixels[i-1].y = temp[i-2].y

        if self.current_direction == "up" and self.future_direction != "down":
            self.current_direction = self.future_direction
        elif self.current_direction == "down" and self.future_direction != "up":
            self.current_direction = self.future_direction
        elif self.current_direction == "left" and self.future_direction != "right":
            self.current_direction = self.future_direction
        elif self.current_direction == "right" and self.future_direction != "left":
            self.current_direction = self.future_direction

        match self.current_direction:
            case 'up':
                self.pixels[0].y -= PIXEL_SIZE
                if self.pixels[0].y == -PIXEL_SIZE:
                    self.pixels[0].y = PIXEL_SIZE * (GRID_SIZE - 1)
            case 'down':
                self.pixels[0].y += PIXEL_SIZE
                if self.pixels[0].y == SCREEN_SIZE:
                    self.pixels[0].y = 0
            case 'left':
                self.pixels[0].x -= PIXEL_SIZE
                if self.pixels[0].x == -PIXEL_SIZE:
                    self.pixels[0].x = PIXEL_SIZE * (GRID_SIZE - 1)
            case 'right':
                self.pixels[0].x += PIXEL_SIZE
                if self.pixels[0].x == SCREEN_SIZE:
                    self.pixels[0].x = 0

class Apple:
    def __init__(self):
        self.color = (255, 0, 0)
        self.pixel = Pixel(PIXEL_SIZE * random.randint(1, GRID_SIZE - 1), PIXEL_SIZE * random.randint(1, GRID_SIZE - 1), self.color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pixel.x, self.pixel.y, self.pixel.size, self.pixel.size))

    def update(self):
        self.pixel.x = PIXEL_SIZE * random.randint(1, GRID_SIZE - 1)
        self.pixel.y = PIXEL_SIZE * random.randint(1, GRID_SIZE - 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Snake")

        self.running = True
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.apple = Apple()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.snake.future_direction = "up"
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.snake.future_direction = "down"
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.snake.future_direction = "left"
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.snake.future_direction = "right"
    
    def draw(self):

        self.screen.fill((0,0,0))
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)

        pygame.display.flip()

    def update(self):
        self.snake.update()

        if self.apple.pixel.x == self.snake.pixels[0].x and self.apple.pixel.y == self.snake.pixels[0].y:
            self.apple.update()
            self.snake.eating = True
            self.snake.eat_sound.play()
    
    def run(self):
        self.draw()
        while self.running:
            self.handle_events()
            self.draw()
            self.update()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

