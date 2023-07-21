from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
class PongBall(Widget):
    velocity_x=NumericProperty(0)
    velocity_y=NumericProperty(0)
    velocity= ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos=Vector(*self.velocity)+self.pos

class PongGame(Widget):
    def update(self, dt):
        pass

class PongApp(App):
    def build(self):
        game=PongGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__=='__main__':
    PongApp().run()
