import pygame
import random

class Apple:
    def __init__(self, screen, background_color, x, y, width, height, color):
        self.screen = screen
        self.background_color = background_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def delete(self):
        pygame.draw.rect(self.screen, self.background_color, (self.x, self.y, self.width, self.height))

class Snake:
    def __init__(self, screen, background_color, x, y, width, height, color):
        self.screen = screen
        self.background_color = background_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.body = [[self.x, self.y]]
        self.direction = "right"
        self.score = 0
        self.game_over = False

    def draw(self):
        for i in range(len(self.body)):
            pygame.draw.rect(self.screen, self.color, (self.body[i][0], self.body[i][1], self.width, self.height))

    def move(self):
        if self.direction == "right":
            self.x += 10
        elif self.direction == "left":
            self.x -= 10
        elif self.direction == "up":
            self.y -= 10
        elif self.direction == "down":
            self.y += 10

        self.body.insert(0, [self.x, self.y])
        self.body.remove(self.body[len(self.body) - 1])

    def change_direction(self, direction):
        self.direction = direction

    def check_collision(self):
        if self.x < 0 or self.x > self.screen.get_width() - self.width:
            self.game_over = True
        if self.y < 0 or self.y > self.screen.get_height() - self.height:
            self.game_over = True

    def check_collision_with_food(self, food):
        if self.x == food.x and self.y == food.y:
            self.score += 1
            self.body.append([self.x, self.y])
            return True
        return False

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.body = [[self.x, self.y]]
        self.direction = "right"
        self.score = 0
        self.game_over = False

pygame.font.init()

font = pygame.font.SysFont('Arial', 18)
size = (400, 400)
background_color = (0, 0, 0)
rendered_game_over = False

screen = pygame.display.set_mode(size)
screen.fill(background_color)
pygame.display.set_caption("Snake")

snake = Snake(screen, background_color, size[0] / 2, size[1] / 2, 10, 10, (255, 255, 255))
apples = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if snake.game_over == False:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction("right")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("left")
                elif event.key == pygame.K_UP:
                    snake.change_direction("up")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("down")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.key == pygame.K_RETURN:
                snake.reset(size[0] / 2, size[1] / 2)
                apples = []
                rendered_game_over = False
                screen.fill(background_color)
            elif event.key == pygame.K_SPACE:
                snake.game_over = False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
 
    if snake.game_over == False:
        if len(apples) < 1:
            x = random.randint(0, size[0] - 10)
            y = random.randint(0, size[1] - 10)

            x = x - x % 10
            y = y - y % 10

            apples.append(Apple(screen, background_color, x, y, 10, 10, (255, 0, 0)))
    
        screen.fill(background_color)
    
        for apple in apples:
            apple.draw()
    
        snake.draw()
        snake.move()
        snake.check_collision()
    
        for apple in apples:
            if snake.check_collision_with_food(apple):
                apples.remove(apple)

        text = font.render("Pontuação: " + str(snake.score), True, (255, 255, 255))
        screen.blit(text, (10, 10))
    
    else:
        if rendered_game_over == False:
            rendered_game_over = True

            text = font.render("Ops... Game Over", True, (255, 255, 255))
            text2 = font.render("Aperte Enter para tentar novamente!", True, (255, 255, 255))
            
            screen.blit(text, (size[0] / 2 - text.get_width() / 2, size[1] / 2 - text.get_height() / 2 - 20))
            screen.blit(text2, (size[0] / 2 - text2.get_width() / 2, size[1] / 2 - text2.get_height() / 2))

    pygame.display.update()
    pygame.time.delay(85)