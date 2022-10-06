import pygame

BACKGROUND_COLOR = (150,255,150)

pygame.init()
screen = pygame.display.set_mode((1280  , 720))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

#collision function for rect and circle
def collision(rleft, rtop, rwidth, rheight, center_x, center_y, radius):
    rright, rbottom = rleft + rwidth, rtop + rheight

    cleft, ctop = center_x - radius, center_y - radius
    cright, cbottom = center_x + radius, center_y + radius

    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False
    
    for x in (rleft, rleft + rwidth):
        for y in (rtop, rtop + rheight):
            if (center_x - x)**2 + (center_y - y)**2 < radius**2:
                return True

    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True
    
    return False        

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
       
#player is a black bar
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.color = (0,0,0)
        self.speed = 10
    
    def draw(self):
        #bar
        pygame.draw.rect(screen, self.color, (self.x, self.y, 10, 100))

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
    if collision(player1.x, player1.y, 10, 100, ball.x, ball.y, ball.size):
        print("collision")
    pygame.display.update()
    clock.tick(60)
