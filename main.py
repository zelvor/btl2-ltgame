import pygame, sys, random, math

WIDTH, HEIGHT = 1600, 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)

                
class Paddle:
	def __init__(self, screen, color, posX, posY, width, height):
		self.screen = screen
		self.color = color
		self.posX = posX
		self.posY = posY
		self.width = width
		self.height = height
		self.state = 'stopped'
		self.draw()

	def draw(self):
		pygame.draw.rect( self.screen, self.color, (self.posX, self.posY, self.width, self.height) )

	def move(self):
		if self.state == 'up' and self.posY > 14:
			self.posY -= 8
		elif self.state == 'down' and self.posY < 875:
			self.posY += 8
		elif self.state == 'left' and self.posX > 14:
			self.posX -= 8
		elif self.state == 'right'and self.posX < 1575:
			self.posX += 8

	def clamp(self):
		if self.posY <= 0:
			self.posY = 0

		if self.posY + self.height >= HEIGHT:
			self.posY = HEIGHT - self.height

	def restart_pos(self):
		self.posY = HEIGHT//2 - self.height//2
		self.state = 'stopped'
		self.draw()

class Ball:
	def __init__(self, screen, color, posX, posY, radius):
		self.screen = screen
		self.color = color
		self.posX = posX
		self.posY = posY
		self.dx = 0
		self.dy = 0
		self.radius = radius
		self.draw()

	def draw(self):
		pygame.draw.circle( self.screen, self.color, (self.posX, self.posY), self.radius)

	def start(self):
		# this will be random
		self.dx = random.randint(6,8) * random.choice([1,-1])
		self.dy = random.randint(2,3) * random.choice([1,-1])

	def move(self):
		self.posX += self.dx
		self.posY += self.dy
        
	def windy(self):
		self.dx *= 1.3
		self.dy *= random.choice([0.6, 0.8, 1.4 , 2, 2.5])
		self.dy += self.dy/abs(self.dy)*2
		print(self.dx)
		print(self.dy)
		# self.dy += random.randrange(3, 4) * random.choice([1,-1])
		# if(self.dy < 3 and self.dy > -3):
		# 	self.dy += random.randrange(3, 4) * random.choice([1,-1])
		# if(self.dx < 3 and self.dx > -3):
		# 	self.dx += random.randrange(6, 8) * random.choice([1,-1])

	def wall_collision(self):
		self.dy = -self.dy
                
	def paddle_collision(self):
		self.dx = -self.dx
		self.posX += self.dx

	def restart_pos(self):
		self.posX = WIDTH//2
		self.posY = HEIGHT//2
		self.dx = 0
		self.dy = 0
		self.draw()

class PlayerScore:
	def __init__(self, screen, points, posX, posY):
		self.screen = screen
		self.points = points
		self.posX = posX
		self.posY = posY
		self.font = pygame.font.SysFont("monospace", 80, bold=True)
		self.label = self.font.render(self.points, 0, WHITE)
		self.show()

	def show(self):
		self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

	def increase(self):
		points = int(self.points) + 1
		self.points = str(points)
		self.label = self.font.render(self.points, 0, WHITE)

	def restart(self):
		self.points = '0'
		self.label = self.font.render(self.points, 0, WHITE)

class CollisionManager:
        def ball_and_left_right(self, ball, score1, score2):
                if(ball.posX < 0 or ball.posX > 1600):
                        ball.dx = -ball.dx
                        if(ball.posY >= 300 and ball.posY <= 600 and ball.posX < 0):
                                score2.increase()
                                return 1
                        if(ball.posY >= 300 and ball.posY <= 600 and ball.posX > 1600):
                                score1.increase()
                                return 2
                return 0

        def between_ball_and_paddle(self, ball, paddle):
                ballX = ball.posX
                ballY = ball.posY
                paddleX = paddle.posX
                paddleY = paddle.posY
                # y is in collision area?
                if ballY + ball.radius > paddleY and ballY - ball.radius < paddleY + paddle.height:
                        # x is in collision area?
                        if ballX + ball.radius > paddleX and ballX - ball.radius <= paddleX + paddle.width:
                                return True

		# no collision
                return False

        def between_ball_and_up_down(self, ball):
                ballY = ball.posY

		# top collision
                if ballY - ball.radius <= 0:
                        return True

		# bottom collision
                if ballY + ball.radius >= HEIGHT:
                        return True

		# no collision
                return False

        def between_ball_and_goal1(self, ball):
                return ball.posX + ball.radius <= 0

        def between_ball_and_goal2(self, ball):
                return ball.posX - ball.radius >= WIDTH

# ---------------------------------------------

class MordenPong():
        def __init__(self):
                self.screen = pygame.display.set_mode((1600, 900))
                self.score1 = PlayerScore( self.screen, '0', WIDTH//4, 15 )
                self.score2 = PlayerScore( self.screen, '0', WIDTH - WIDTH//4, 15 )
                self.ball = Ball( self.screen, WHITE, WIDTH//2, HEIGHT//2, 15 )
                self.collision = CollisionManager()
                self.paddle1 = Paddle( self.screen, RED, 15, HEIGHT//2 - 60, 10, 120 )
                self.paddle3 = Paddle( self.screen, WHITE, 255, HEIGHT//2 - 60, 10, 120 )
                self.paddle2 = Paddle( self.screen, RED, WIDTH - 20 - 15, HEIGHT//2 - 60, 10, 120 )
                self.paddle4 = Paddle( self.screen, WHITE, WIDTH - 20 - 255, HEIGHT//2 - 60, 10, 120 )

        def draw_board(self):
                self.screen.fill( BLACK )
                pygame.draw.line( self.screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5 )
                pygame.draw.line( self.screen, BLUE, (1, 300), (1, 600), 10 )
                pygame.draw.line( self.screen, BLUE, (WIDTH-1, 300), (WIDTH-1, 600), 10 )

        def restart(self):
                self.draw_board()
                # self.score1.restart()
                # self.score2.restart()
                self.ball.restart_pos()
                self.paddle1.restart_pos()
                self.paddle2.restart_pos()
                self.paddle3.restart_pos()
                self.paddle4.restart_pos()
                
        def start(self):
                self.restart()

                # -------
                # OBJECTS
                # -------

                # ball = Ball( self.screen, WHITE, WIDTH//2, HEIGHT//2, 15 )
                # collision = CollisionManager()
                # score1 = PlayerScore( self.screen, '0', WIDTH//4, 15 )
                # score2 = PlayerScore( self.screen, '0', WIDTH - WIDTH//4, 15 )

                # ---------
                # VARIABLES
                # ---------
                cycle_time = 0
                count = 0
                playing = False
                clock = pygame.time.Clock()
                start_ticks=0
                # --------
                # MAINLOOP
                # --------
                global p1
                p1 = self.paddle1
                global p2
                p2 = self.paddle2

                while True:
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        sys.exit()

                                if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_p and not playing:
                                                self.ball.start()
                                                playing = True
                                                start_ticks = pygame.time.get_ticks() #starter tick

                                        if event.key == pygame.K_r and playing:
                                                self.restart()
                                                playing = False

                                
                                        #if press shift, p1 is self.paddle3
                                        if event.key == pygame.K_LSHIFT:
                                                if self.paddle1.color == RED:
                                                        p1 = self.paddle3
                                                        self.paddle1.color = WHITE
                                                        self.paddle3.color = RED
                                                elif self.paddle1.color == WHITE:
                                                        p1 = self.paddle1
                                                        self.paddle1.color = RED
                                                        self.paddle3.color = WHITE
                                        
                                        if event.key == pygame.K_RSHIFT:
                                                if self.paddle2.color == RED:
                                                        p2 = self.paddle4
                                                        self.paddle2.color = WHITE
                                                        self.paddle4.color = RED
                                                elif self.paddle2.color == WHITE:
                                                        p2 = self.paddle2
                                                        self.paddle2.color = RED
                                                        self.paddle4.color = WHITE

                                        

                                        if event.key == pygame.K_w:
                                                p1.state = 'up'

                                        if event.key == pygame.K_s:
                                                p1.state = 'down'
                                        
                                        if event.key == pygame.K_a:
                                                p1.state = 'left'

                                        if event.key == pygame.K_d:
                                                p1.state = 'right'

                                        if event.key == pygame.K_UP:
                                                p2.state = 'up'

                                        if event.key == pygame.K_DOWN:
                                                p2.state = 'down'

                                        if event.key == pygame.K_LEFT:
                                                p2.state = 'left'
                                        
                                        if event.key == pygame.K_RIGHT:
                                                p2.state = 'right'

                                if event.type == pygame.KEYUP:
                                        self.paddle1.state = 'stopped'
                                        self.paddle2.state = 'stopped'
                                        self.paddle3.state = 'stopped'
                                        self.paddle4.state = 'stopped'

                        if playing:
                                self.draw_board()

                                # self.ball
                                self.ball.move()
                                self.ball.draw()

                                # paddle 1
                                self.paddle1.move()
                                self.paddle1.clamp()
                                self.paddle1.draw()

                                # paddle 2
                                self.paddle2.move()
                                self.paddle2.clamp()
                                self.paddle2.draw()

                                # paddle 3
                                self.paddle3.move()
                                self.paddle3.clamp()
                                self.paddle3.draw()

                                # paddle 4
                                self.paddle4.move()
                                self.paddle4.clamp()
                                self.paddle4.draw()

                                # wall collision
                                if self.collision.between_ball_and_up_down(self.ball):
                                        self.ball.wall_collision()

                                if self.collision.ball_and_left_right(self.ball, self.score1, self.score2) != 0:
                                        self.start()
                                # self.paddle1 collision
                                if self.collision.between_ball_and_paddle(self.ball, self.paddle1):
                                       self.ball.paddle_collision()

                                # self.paddle2 collision
                                if self.collision.between_ball_and_paddle(self.ball, self.paddle2):
                                       self.ball.paddle_collision()

                                if self.collision.between_ball_and_paddle(self.ball, self.paddle3):
                                       self.ball.paddle_collision()

                                if self.collision.between_ball_and_paddle(self.ball, self.paddle4):
                                       self.ball.paddle_collision()

                                # # GOAL OF PLAYER 1 !
                                # if collision.between_ball_and_goal2(ball):
                                # 	self.draw_board()
                                # 	score1.increase()
                                # 	ball.restart_pos()
                                # 	self.paddle1.restart_pos()
                                # 	self.paddle2.restart_pos()
                                # 	self.paddle3.restart_pos()
                                # 	playing = False

                                # # GOAL OF PLAYER 2!
                                # if collision.between_ball_and_goal1(ball):
                                # 	self.draw_board()
                                # 	score2.increase()
                                # 	ball.restart_pos()
                                # 	self.paddle1.restart_pos()
                                # 	self.paddle2.restart_pos()
                                # 	self.paddle3.restart_pos()
                                # 	playing = False

                                cycle = (pygame.time.get_ticks() - start_ticks) % 5000
                                # sec = mil / 1000.0
                                # cycle_time += sec
                                # count = count + mil
                                if cycle < 10:
                                        # count = 0
                                        self.ball.windy()
                        self.time = 0
                        self.score1.show()
                        self.score2.show()

                        clock.tick(60)
                        pygame.display.update()

#------------------------------------------------------------------------#
def main():
    # Initialize the game
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.init()
    # Run the main loop
    game = MordenPong()
    game.start()
    # Exit the game if the main loop ends
    pygame.quit()

def main_menu():
    global dif
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption('Soccer Pong')
    screen.fill((0,0,0))
    #Title
    game_title = pygame.font.Font('fonts/Pixelboy.ttf', 160)
    game_title_text = game_title.render('Soccer Pong', True, (255, 255, 255))
    screen.blit(game_title_text, (425, 250))
    #start button with text
    start_button = pygame.Rect(670, 600, 200, 70)
    pygame.draw.rect(screen, (47, 143, 194), start_button)
    font = pygame.font.Font('fonts/Pixelboy.ttf', 80)
    text = font.render('Start', True, (255, 255, 255))
    screen.blit(text, (675, 615))
    #options button with text
    options_button = pygame.Rect(670, 700, 210, 70)
    pygame.draw.rect(screen, (47, 143, 194), options_button)
    font = pygame.font.Font('fonts/Pixelboy.ttf', 80)
    text = font.render(("vs Com" if dif == 1 else "vs P2"), True, (255, 255, 255))
    screen.blit(text, (675, 715))
    #quit button with text
    quit_button = pygame.Rect(670, 800, 200, 70)
    pygame.draw.rect(screen, (47, 143, 194), quit_button)
    font = pygame.font.Font('fonts/Pixelboy.ttf', 80)
    text = font.render('Quit', True, (255, 255, 255))
    screen.blit(text, (675, 815))
    pygame.display.flip()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main()
                if options_button.collidepoint(event.pos):
                    if dif == 1:
                        dif = 2
                    else:
                        dif = 1
                    pygame.draw.rect(screen, (47, 143, 194), options_button)
                    font = pygame.font.Font('fonts/Pixelboy.ttf', 80)
                    text = font.render(("vs Com" if dif == 1 else "vs P2"), True, (255, 255, 255))
                    screen.blit(text, (675, 715))
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    global dif
    dif = 1     #dif = 1 -> vs com
    main_menu()
