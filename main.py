import pygame

BACKGROUND_COLOR = (150,255,150)

pygame.init()
screen = pygame.display.set_mode((1280  , 720))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

#collision function for circles
def collision(self, other):
    return (self.x - other.x)**2 + (self.y - other.y)**2 < (self.size + other.size)**2
        

class SoccerGround:
    def __init__(self):
        self.image = pygame.image.load("images/soccer_ground.png")
        self.image = pygame.transform.scale(self.image, (1280, 720))
        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)

    def draw(self):
        screen.blit(self.image, self.rect)
    
    #draw 4 lines of the soccer ground
    def draw_lines(self):
        pygame.draw.line(screen, (0,0,0), (60, 35), (1220, 35), 10)
        pygame.draw.line(screen, (0,0,0), (60, 685), (1220, 685), 10)
        pygame.draw.line(screen, (0,0,0), (60, 35), (60, 685), 10)
        pygame.draw.line(screen, (0,0,0), (1220, 35), (1220, 685), 10)
       

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.color = (255, 0, 0)
        self.speed = 10

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        if self.x > 1220:
            self.x = 1220
        if self.x < 60:
            self.x = 60
        if self.y > 685:
            self.y = 685
        if self.y < 35:
            self.y = 35
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.x -= self.speed
        if key[pygame.K_d]:
            self.x += self.speed
        if key[pygame.K_w]:
            self.y -= self.speed
        if key[pygame.K_s]:
            self.y += self.speed
        
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.color = (0,0,0)
        self.speed = 10
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)


soccer_ground = SoccerGround()
player1 = Player(400, 300)

ball = Ball(640, 360)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill(BACKGROUND_COLOR)
    soccer_ground.draw()
    soccer_ground.draw_lines()
    player1.draw()
    player1.move()
    ball.draw()
    if collision(player1, ball):
        print("collision")
    pygame.display.update()
    clock.tick(60)
