from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock

# PongPaddle is a subclass of the Widget class from the Kivy framework
class PongPaddle(Widget):
    # keeps the score of each player and automatically updates the ui when its value is changed
    score = NumericProperty(0)

    # defining method bounce_ball with a single parameter constructor method checks if the ball collides with the
    # paddle widget. If the ball collides with the paddle, the method calculates the balls new velocity based on its
    # current velocity and position relative to the paddle.
    # offset value is calculated based on the relative position of the ball and the paddle
    # used to add a vertical component to the ball's velocity which makes it bounce at an angle
    # bounced variable is created as a new Vector instance where the x component is negated and y is unchanged.
    # This reverses the horizontal direction of the ball
    # the new velocity is calculated by multiplying bounced by 1.1 to increase the speed
    # and adding the offset value to its y component
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y-self.center_y)/(self.height/2)
            bounced = Vector(-1*vx, vy)
            vel = bounced*1.1
            ball.velocity = vel.x, vel.y + offset

# PongBall is a subclass of the Widget class from the Kivy framework
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # defining the method move
    # this method updates the position of the ball based on the current velocity of the ball
    def move(self):
        self.pos = Vector(*self.velocity)+self.pos

# PongGame is a subclass of the Widget class from the Kivy framework
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

    # method update takes single argument
    # the move method is called on the ball attribute to update its position depending on the current velocity
    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if(self.ball.y<self.y) or (self.ball.top> self.top):
            self.ball.velocity_y *= -1

        # checks if the ball has gone out of bounds or past the paddles
        # if it has, the score of the opposing player gets incremented
        # and the serve_ball method is called to reset the ball to the initial position and velocity
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    # on_touch_move takes one argument for touch
    # the method handles touch events and moves the paddle based on the user input(touch)
    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width-self.width/3:
            self.player2.center_y = touch.y

# class PongApp is a subclass of App from the Kivy framework
class PongApp(App):
    # the build method builds the user interface of the app
    # an instance of the PongGame class is created and assigned to the variable game
    # the serve_ball() method is called on this instance to set the initial position and the velocity of the ball
    # schedule_interval method of the Clock class in the Kivy framework is called to schedule the
    # update method of the game instance
    # the second argument 1.0/6.0 specifies that the update method should be called 60 times per second
    # the game instance is returned and is used as the root widget of the app
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)

        return game

# a Python idiom used to check if the script is being run as the main program
# if the script is run as the main program, an instance of the PongApp class is created and its run method is called
# this starts the Kivy application and displays the user interface
if __name__=='__main__':
    PongApp().run()
