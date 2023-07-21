from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock

class PongPaddle(Widget):
    # keeps the score of each player
    score = NumericProperty(0)

    # defining method bounce_ball with a single parameter constructor
    # method checks if the ball collides with the paddle widget
    # if the ball collides, method calculates the ball's new velocity based on its current velocity and position relative to the paddle
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y-self.center_y)/(self.height/2)
            bounced = Vector(-1*vx, vy)
            vel = bounced*1.1
            ball.velocity = vel.x, vel.y + offset
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity)+self.pos
class PongGame(Widget):
    # initializing the observable properties to none
    # ObjectProperty class automatically observes changes and notifies and responds the program accordingly
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    # serve_ball method sets the initial position of the ball to the center
    # the default value of the optional argument vel is given as 4.0
    # the balls velocity is set to the value of the vel argument
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if(self.ball.y<self.y) or (self.ball.top> self.top):
            self.ball.velocity_y *= -1

        #
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width-self.width/3:
            self.player2.center_y = touch.y
class PongApp(App):
    def build(self):
        game = PongGame()
        # calling method serve_ball()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)

        return game

if __name__=='__main__':
    PongApp().run()
